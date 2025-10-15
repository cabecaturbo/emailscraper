# Email Scraper Tool - Multi-Website Web App

A beautiful web app to extract email addresses from **multiple websites at once**! No command-line needed!

## âœ¨ Features

âœ“ **Scrape Multiple Websites** - Enter as many URLs as you want, one per line  
âœ“ **Parallel Processing** - All websites are scraped simultaneously for speed  
âœ“ **Beautiful Web Interface** - Modern, gradient design that's easy to use  
âœ“ **Results Summary** - See total unique emails across all sites  
âœ“ **Per-Website Breakdown** - View emails found on each individual site  
âœ“ **Copy to Clipboard** - One-click copy for individual or all emails  
âœ“ **Error Handling** - Clear error messages if any website fails  
âœ“ **Real-time Results** - See results as they're scraped  
âœ“ **Responsive Design** - Works on desktop and mobile  

## Quick Start

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. Download or clone this folder
2. Open a terminal/command prompt in this folder
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Running the App

1. Run the web app:
   ```
   python app.py
   ```

2. Open your browser and go to:
   ```
   http://localhost:5000
   ```

3. Enter multiple website URLs (one per line) and click "Scrape All Websites"!

## How to Use

1. Start the app with `python app.py`
2. Open `http://localhost:5000` in your browser
3. Enter website URLs in the text box, **one URL per line**:
   ```
   example.com
   https://another-site.org
   third-website.com
   ```
4. Click "Scrape All Websites"
5. View results:
   - **Summary** showing total unique emails and websites scraped
   - **Per-website breakdown** showing which emails came from which site
   - **All unique emails** combined from all websites
6. Copy individual emails or click "Copy All Unique Emails"!

## Example

Enter these URLs:
```
github.com
stackoverflow.com
reddit.com
```

The app will:
- Scrape all three sites simultaneously
- Show you how many emails were found on each site
- Display all unique emails (removing duplicates)
- Let you copy all emails with one click

## What Makes This Special?

- **Parallel Processing**: Scrapes multiple websites at the same time (up to 5 simultaneously)
- **Duplicate Removal**: Automatically removes duplicate emails across all sites
- **Error Resilience**: If one website fails, others continue working
- **Beautiful Results**: Color-coded results with clear organization

## Sharing with Others

To share this tool:
1. Zip this entire folder
2. Share the zip file
3. Recipients just need to:
   - Unzip the folder
   - Run `pip install -r requirements.txt`
   - Run `python app.py`
   - Open their browser to `http://localhost:5000`

## Limitations

This tool:
- Only scrapes the specific pages you provide (doesn't follow links)
- Doesn't handle JavaScript-generated content
- Won't bypass anti-scraping measures
- Runs locally on your computer
- Processes up to 5 websites simultaneously (configurable in code)

## Important Note

**Always ensure you have permission to scrape websites.** Respect each website's `robots.txt` file and terms of service. This tool is intended for legitimate purposes only (like gathering public contact information).

## Troubleshooting

**"No module named 'flask'" error:**
- Run `pip install -r requirements.txt`

**Port 5000 already in use:**
- Close any other apps using port 5000, or edit `app.py` and change `port=5000` to another port like `port=8080`

**Some websites show errors:**
- Normal! Some websites block automated requests or may be temporarily down
- The tool will still show results from websites that succeeded

**"No emails found" but you know there are emails:**
- Some websites load content with JavaScript (this tool only reads static HTML)
- The emails might be displayed as images or obfuscated

**App runs slow with many URLs:**
- The tool processes up to 5 URLs simultaneously
- Each site has a 10-second timeout
- Large numbers of URLs will take proportionally longer

## Advanced Usage

Want to scrape more websites simultaneously? Edit `app.py` and change:
```python
with ThreadPoolExecutor(max_workers=5) as executor:
```
to a higher number like `max_workers=10`

## License

Free to use and share!
