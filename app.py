from flask import Flask, render_template, request, jsonify
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import webbrowser
import threading
import time
import urllib.parse
from urllib.robotparser import RobotFileParser
import socket
from bs4 import BeautifulSoup
import html
import random

app = Flask(__name__)

# Enhanced email regex patterns for better accuracy
EMAIL_PATTERNS = [
    # Standard email pattern (enhanced)
    r'\b[A-Za-z0-9](?:[A-Za-z0-9._%+-]*(?!\w))?@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    # Pattern for emails in quotes or encoded
    r'["\']([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})["\']',
    # Pattern for mailto links
    r'mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
    # Pattern for obfuscated emails (basic protection)
    r'([A-Za-z0-9._%+-]+)\s*\[at\]\s*([A-Za-z0-9.-]+)\s*\[dot\]\s*([A-Za-z0-9.-]+)',
    r'([A-Za-z0-9._%+-]+)\s*@\s*([A-Za-z0-9.-]+)\s*\.\s*([A-Za-z0-9.-]+)',
]

# Common false positive patterns to filter out
FALSE_POSITIVE_PATTERNS = [
    r'example\.com',
    r'test@test\.com',
    r'no-reply@',
    r'noreply@',
    r'admin@localhost',
    r'root@localhost',
]

# Enhanced user agents to avoid blocking
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
]

def normalize_url(url):
    """Normalize and validate URL"""
    if not url:
        return None
    
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        parsed = urllib.parse.urlparse(url)
        if not parsed.netloc:
            return None
        return parsed.geturl()
    except Exception:
        return None

def check_robots_txt(url):
    """Check if URL is allowed by robots.txt"""
    try:
        parsed = urllib.parse.urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        
        return rp.can_fetch('*', url)
    except Exception:
        return True  # If we can't check robots.txt, assume it's allowed

def is_valid_email(email):
    """Validate if email is legitimate and not a false positive"""
    if not email or len(email) < 5:
        return False
    
    email = email.lower().strip()
    
    # Check against false positive patterns
    for pattern in FALSE_POSITIVE_PATTERNS:
        if re.search(pattern, email, re.IGNORECASE):
            return False
    
    # Additional validation
    parts = email.split('@')
    if len(parts) != 2:
        return False
    
    local, domain = parts
    
    # Local part validation
    if len(local) == 0 or len(local) > 64:
        return False
    
    # Domain validation
    if len(domain) == 0 or len(domain) > 253:
        return False
    
    # Check for suspicious patterns
    suspicious_patterns = ['.png', '.jpg', '.gif', '.css', '.js', 'localhost']
    if any(pattern in domain for pattern in suspicious_patterns):
        return False
    
    return True

def extract_emails_from_text(text):
    """Extract emails using multiple patterns and validation"""
    emails = set()
    text = html.unescape(text)  # Decode HTML entities
    
    for pattern in EMAIL_PATTERNS:
        if '[at]' in pattern and '[dot]' in pattern:
            # Handle obfuscated emails
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                email = f"{match.group(1)}@{match.group(2)}.{match.group(3)}"
                if is_valid_email(email):
                    emails.add(email.lower())
        else:
            # Standard email patterns
            found_emails = re.findall(pattern, text, re.IGNORECASE)
            for email in found_emails:
                if isinstance(email, tuple):
                    email = email[0]  # Extract from groups
                if is_valid_email(email):
                    emails.add(email.lower())
    
    return list(emails)

def scrape_emails(url):
    """Scrape email addresses from a given website URL with enhanced robustness."""
    start_time = time.time()
    
    try:
        # Normalize URL
        normalized_url = normalize_url(url)
        if not normalized_url:
            return {
                'success': False,
                'emails': [],
                'count': 0,
                'url': url,
                'error': 'Invalid URL format'
            }
        
        # Check robots.txt (disabled for better compatibility - can be re-enabled if needed)
        # if not check_robots_txt(normalized_url):
        #     return {
        #         'success': False,
        #         'emails': [],
        #         'count': 0,
        #         'url': normalized_url,
        #         'error': 'Blocked by robots.txt'
        #     }
        
        # Enhanced headers with random user agent
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Make request with enhanced settings
        session = requests.Session()
        session.headers.update(headers)
        
        response = session.get(
            normalized_url, 
            timeout=15,  # Increased timeout
            allow_redirects=True,
            verify=True
        )
        response.raise_for_status()
        
        # Parse content type
        content_type = response.headers.get('content-type', '').lower()
        if 'text/html' not in content_type:
            return {
                'success': False,
                'emails': [],
                'count': 0,
                'url': normalized_url,
                'error': f'Not HTML content (type: {content_type})'
            }
        
        # Use BeautifulSoup for better HTML parsing
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "noscript"]):
            script.extract()
        
        # Get text content
        text_content = soup.get_text()
        
        # Also check plain text content from response
        plain_text = response.text
        
        # Extract emails from both sources
        emails_from_text = extract_emails_from_text(text_content)
        emails_from_html = extract_emails_from_text(plain_text)
        
        # Combine and deduplicate
        all_emails = set(emails_from_text + emails_from_html)
        
        # Final validation
        valid_emails = []
        for email in all_emails:
            if is_valid_email(email):
                valid_emails.append(email)
        
        processing_time = round(time.time() - start_time, 2)
        
        return {
            'success': True,
            'emails': sorted(valid_emails),
            'count': len(valid_emails),
            'url': normalized_url,
            'processing_time': processing_time,
            'status_code': response.status_code
        }
        
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'emails': [],
            'count': 0,
            'url': url,
            'error': 'Request timeout (15s exceeded)'
        }
    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'emails': [],
            'count': 0,
            'url': url,
            'error': 'Connection error - unable to reach website'
        }
    except requests.exceptions.HTTPError as e:
        return {
            'success': False,
            'emails': [],
            'count': 0,
            'url': url,
            'error': f'HTTP Error {e.response.status_code}: {e.response.reason}'
        }
    except socket.gaierror:
        return {
            'success': False,
            'emails': [],
            'count': 0,
            'url': url,
            'error': 'DNS resolution failed - invalid domain'
        }
    except Exception as e:
        return {
            'success': False,
            'emails': [],
            'count': 0,
            'url': url,
            'error': f'Unexpected error: {str(e)}'
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    urls_input = data.get('urls', '').strip()
    
    if not urls_input:
        return jsonify({
            'success': False,
            'error': 'Please provide at least one URL'
        })
    
    # Split by newlines and filter out empty lines
    raw_urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
    
    if not raw_urls:
        return jsonify({
            'success': False,
            'error': 'Please provide at least one URL'
        })
    
    # Normalize and validate URLs
    urls = []
    invalid_urls = []
    
    for url in raw_urls:
        normalized = normalize_url(url)
        if normalized:
            urls.append(normalized)
        else:
            invalid_urls.append(url)
    
    if not urls:
        return jsonify({
            'success': False,
            'error': f'No valid URLs provided. Invalid URLs: {", ".join(invalid_urls)}'
        })
    
    # Limit concurrent requests for better reliability
    max_workers = min(5, len(urls))
    
    # Scrape all URLs in parallel
    results = []
    all_emails = set()
    successful_scrapes = 0
    failed_scrapes = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(scrape_emails, url): url for url in urls}
        
        for future in as_completed(future_to_url):
            result = future.result()
            results.append(result)
            
            if result['success'] and result['emails']:
                all_emails.update(result['emails'])
                successful_scrapes += 1
            else:
                failed_scrapes += 1
    
    # Add results for invalid URLs
    for invalid_url in invalid_urls:
        results.append({
            'success': False,
            'emails': [],
            'count': 0,
            'url': invalid_url,
            'error': 'Invalid URL format'
        })
        failed_scrapes += 1
    
    return jsonify({
        'success': True,
        'results': results,
        'total_emails': len(all_emails),
        'total_urls': len(raw_urls),
        'successful_scrapes': successful_scrapes,
        'failed_scrapes': failed_scrapes,
        'all_emails': sorted(list(all_emails))
    })

def open_browser():
    """Open the browser after a short delay"""
    import time
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print('='*60)
    print('Email Scraper Web App Starting...')
    print('='*60)
    print('\nYour browser will open automatically.')
    print('If it doesn\'t open, go to: http://localhost:5000')
    print('\nPress Ctrl+C to stop the server when done.')
    print('='*60)
    
    # Open browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start Flask app
    app.run(debug=False, host='0.0.0.0', port=5000)
