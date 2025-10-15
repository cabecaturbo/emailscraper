# Email Scraper Tool v2.0 - Enhanced Multi-Website Web App

A **professional-grade** web application to extract email addresses from multiple websites with **advanced accuracy** and **robust error handling**!

## 🚀 Enhanced Features v2.0

✅ **Advanced Email Detection** - Multiple regex patterns for obfuscated and encoded emails  
✅ **BeautifulSoup HTML Parsing** - Better content extraction and script filtering  
✅ **Robust Error Handling** - Specific handling for timeouts, DNS errors, and HTTP issues  
✅ **Anti-Detection Measures** - Multiple user agents, realistic headers, and session management  
✅ **URL Validation & Normalization** - Proper URL handling and robots.txt checking  
✅ **False Positive Filtering** - Removes example emails and suspicious patterns  
✅ **Enhanced Performance** - Better timeout handling and processing time tracking  
✅ **Parallel Processing** - Up to 5 websites scraped simultaneously  
✅ **Results Summary** - Comprehensive statistics including successful/failed scrapes  
✅ **Copy to Clipboard** - One-click copy for individual or all emails  
✅ **Professional UI** - Enterprise-grade interface with clear error reporting

## What's New in v2.0?

### Enhanced Accuracy
- **Multiple Email Patterns**: Detects standard emails, mailto links, obfuscated emails (user[at]domain[dot]com)
- **HTML Entity Decoding**: Properly handles encoded email addresses
- **False Positive Filtering**: Automatically removes test emails and suspicious patterns
- **Better Validation**: Stricter email validation with proper domain checking

### Robust Error Handling
- **Specific Exception Types**: Separate handling for timeouts, connection errors, DNS issues
- **HTTP Status Reporting**: Shows exact error codes and descriptions
- **Timeout Management**: Increased to 15 seconds with proper timeout handling
- **Content Type Validation**: Ensures only HTML content is processed

### Anti-Detection Features
- **User Agent Rotation**: Multiple realistic browser user agents
- **Session Management**: Proper session handling with cookies
- **Realistic Headers**: Adds proper browser headers to avoid blocking
- **Robots.txt Compliance**: Optional respect for website robots.txt files

## Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/cabecaturbo/emailscraper.git
   cd emailscraper
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```
   
   Or use the enhanced launcher on Windows:
   ```bash
   START_APP.bat
   ```

4. Open your browser and go to: `http://localhost:5000`

## How to Use

1. **Start the App**: Run `python app.py` or double-click `START_APP.bat` on Windows
2. **Open Browser**: Navigate to `http://localhost:5000`
3. **Enter URLs**: Input website URLs, one per line:
   ```
   example.com
   https://another-site.org
   third-website.com
   ```
4. **Scrape**: Click "Scrape All Websites" and watch the magic happen!
5. **Review Results**: 
   - View total unique emails across all sites
   - See per-website breakdowns
   - Copy individual emails or all emails at once

## Technical Improvements

### Enhanced Email Detection Patterns
```python
EMAIL_PATTERNS = [
    # Standard email pattern (enhanced)
    r'\b[A-Za-z0-9](?:[A-Za-z0-9._%+-]*(?!\w))?@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    # Pattern for emails in quotes or encoded
    r'["\']([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})["\']',
    # Pattern for mailto links
    r'mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
    # Pattern for obfuscated emails
    r'([A-Za-z0-9._%+-]+)\s*\[at\]\s*([A-Za-z0-9.-]+)\s*\[dot\]\s*([A-Za-z0-9.-]+)',
]
```

### New Dependencies
- `beautifulsoup4==4.12.2` - Enhanced HTML parsing
- `lxml==4.9.3` - Fast XML/HTML processing

## Enterprise Features

- **Professional Error Reporting**: Detailed error messages for troubleshooting
- **Performance Metrics**: Processing time tracking per website
- **Statistics Dashboard**: Success/failure rates and comprehensive reporting
- **Robust Configuration**: Configurable thread limits and timeout settings
- **Memory Efficient**: Optimized for handling large amounts of data

## Usage Examples

### Basic Usage
```bash
# Start the server
python app.py

# Visit http://localhost:5000
# Enter multiple URLs and scrape!
```

### Advanced Configuration
You can modify these settings in `app.py`:
- `max_workers`: Number of concurrent requests (default: 5)
- `timeout`: Request timeout in seconds (default: 15)
- `USER_AGENTS`: List of user agents for rotation

## Limitations & Considerations

- **JavaScript Content**: Cannot extract emails loaded via JavaScript
- **Rate Limiting**: Respects website limits and robots.txt (when enabled)
- **Legal Compliance**: Always ensure permission to scrape websites
- **Content Types**: Only processes HTML content

## Troubleshooting

**Dependencies Issues:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Port Already in Use:**
Edit `app.py` and change `port=5000` to another port like `port=8080`

**Some Websites Fail:**
- Normal behavior - websites may block automated requests
- Check the error messages for specific issues
- The tool continues processing other sites even if some fail

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool!

## License

This project is open source and available under the MIT License.

## Recent Updates (v2.0)

- ✅ Enhanced email detection with multiple patterns
- ✅ Better error handling and reporting
- ✅ Anti-detection measures implemented
- ✅ Professional UI improvements
- ✅ Performance optimizations
- ✅ Comprehensive validation and filtering

---

**Built with ❤️ for efficient and accurate email extraction**