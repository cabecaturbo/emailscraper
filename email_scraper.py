import re
import requests

def scrape_emails(url):
    """Scrape email addresses from a given website URL."""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"Fetching {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = set(re.findall(email_pattern, response.text))
        
        return emails
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return set()
    except Exception as e:
        print(f"An error occurred: {e}")
        return set()

def main():
    """Main function to run the email scraper."""
    print("=" * 50)
    print("Email Scraper")
    print("=" * 50)
    
    url = input("\nEnter website URL: ").strip()
    
    if not url:
        print("No URL provided. Exiting.")
        return
    
    emails = scrape_emails(url)
    
    print("\n" + "=" * 50)
    if emails:
        print(f"Found {len(emails)} email(s):\n")
        for email in sorted(emails):
            print(f"  â€¢ {email}")
    else:
        print("No emails found on this page.")
    print("=" * 50)

if __name__ == "__main__":
    main()
