"""
Assignment 10 - Task 6: OWASP Top 10 Web Scraping
Extract the top 10 security vulnerabilities from OWASP and save to CSV
"""

import csv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# TASK 6: Use Selenium to scrape OWASP Top 10 vulnerabilities

def scrape_owasp_top_10():
    """
    Scrape the OWASP Top 10 vulnerabilities from the official page
    Returns a list of dictionaries with 'title' and 'link' keys
    """
    
    # Set up Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Initialize the WebDriver
    print("Initializing Selenium WebDriver...")
    driver = webdriver.Chrome(options=chrome_options)
    
    vulnerabilities = []
    
    try:
        # Navigate to the OWASP Top 10 page
        url = "https://owasp.org/Top10/2025/"
        print(f"Loading page: {url}")
        driver.get(url)
        
        # Wait for the page to load
        print("Waiting for page to load...")
        time.sleep(3)
        
        # TASK 6: Find each of the top 10 vulnerabilities using XPath
        # XPath to find vulnerability items (typically in list items or divs)
        
        # Try multiple XPath strategies to find the top 10 items
        vulnerabilities = extract_vulnerabilities_method1(driver)
        
        if not vulnerabilities:
            print("Method 1 failed, trying alternative XPath...")
            vulnerabilities = extract_vulnerabilities_method2(driver)
        
        if not vulnerabilities:
            print("Method 2 failed, trying alternative XPath...")
            vulnerabilities = extract_vulnerabilities_method3(driver)
        
        print(f"\nFound {len(vulnerabilities)} vulnerabilities")
        
    except Exception as e:
        print(f"ERROR: {e}")
    
    finally:
        driver.quit()
    
    return vulnerabilities


def extract_vulnerabilities_method1(driver):
    """
    Method 1: Look for vulnerability links in main content area
    XPath: Find all links that appear to be vulnerability items
    """
    vulnerabilities = []
    
    try:
        # Wait for content to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@href]"))
        )
        
        # XPath to find all vulnerability pages - look for links to /A[1-9][0-9]* patterns
        # These match links like /A01_2025, /A02_2025, etc.
        xpath_vuln = "//a[contains(@href, '/A') and contains(@href, '2025')]"
        
        vulnerability_links = driver.find_elements(By.XPATH, xpath_vuln)
        
        print(f"Method 1 found {len(vulnerability_links)} items")
        
        # Keep track of seen titles to avoid duplicates
        seen_titles = set()
        
        for link in vulnerability_links:
            try:
                title = link.text.strip()
                href = link.get_attribute('href')
                
                # Only add if we have both title and href, and it's a new one
                if title and href and title not in seen_titles and len(vulnerabilities) < 10:
                    # Check it's a proper vulnerability entry (starts with A and a digit)
                    if title.startswith('A') and any(c.isdigit() for c in title[:2]):
                        vulnerabilities.append({
                            'title': title,
                            'link': href
                        })
                        seen_titles.add(title)
                        print(f"  - {title}")
            except Exception as e:
                continue
        
    except Exception as e:
        print(f"Method 1 XPath error: {e}")
    
    return vulnerabilities


def extract_vulnerabilities_method2(driver):
    """
    Method 2: Look for numbered vulnerabilities in order
    XPath: Find elements containing "A1", "A2", etc.
    """
    vulnerabilities = []
    
    try:
        # XPath to find items with vulnerability numbering
        xpath_vuln = "//a[contains(text(), 'A1') or contains(text(), 'A2') or contains(text(), 'A3') or contains(text(), 'A4') or contains(text(), 'A5')]"
        
        vulnerability_links = driver.find_elements(By.XPATH, xpath_vuln)
        
        print(f"Method 2 found {len(vulnerability_links)} items")
        
        for link in vulnerability_links[:10]:
            try:
                title = link.text.strip()
                href = link.get_attribute('href')
                
                if title and href and 'A' in title:
                    vulnerabilities.append({
                        'title': title,
                        'link': href
                    })
                    print(f"  - {title}")
            except Exception as e:
                continue
        
    except Exception as e:
        print(f"Method 2 XPath error: {e}")
    
    return vulnerabilities


def extract_vulnerabilities_method3(driver):
    """
    Method 3: Look for main vulnerability navigation/links
    XPath: Find all links in main content area with descriptive text
    """
    vulnerabilities = []
    
    try:
        # XPath to find main article links or navigation items
        # This looks for links that are likely to be vulnerability pages
        xpath_vuln = "//nav//a | //main//a | //article//a"
        
        all_links = driver.find_elements(By.XPATH, xpath_vuln)
        
        print(f"Method 3 found {len(all_links)} total links, filtering...")
        
        # Filter for likely vulnerability entries
        for link in all_links:
            try:
                title = link.text.strip()
                href = link.get_attribute('href')
                
                # Look for links that contain vulnerability indicators
                if title and href and len(title) > 5 and len(vulnerabilities) < 10:
                    # Skip navigation and common links
                    skip_keywords = ['github', 'slack', 'home', 'about', 'donate', 'members', 'chapters']
                    if not any(keyword in title.lower() or keyword in href.lower() for keyword in skip_keywords):
                        # Check if it looks like a vulnerability (has a number or security term)
                        if any(c.isdigit() for c in title) or any(term in title.lower() for term in ['injection', 'auth', 'broken', 'sensitive', 'xxe', 'access', 'csrf', 'vulnerable']):
                            vulnerabilities.append({
                                'title': title,
                                'link': href
                            })
                            print(f"  - {title}")
                        
            except Exception as e:
                continue
        
    except Exception as e:
        print(f"Method 3 XPath error: {e}")
    
    return vulnerabilities


def save_to_csv(vulnerabilities, filename='assignment10/owasp_top_10.csv'):
    """
    Save vulnerabilities to CSV file
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for vuln in vulnerabilities:
                writer.writerow(vuln)
        
        print(f"Saved {len(vulnerabilities)} vulnerabilities to {filename}")
        return True
    except Exception as e:
        print(f"ERROR saving CSV: {e}")
        return False


def save_to_json(vulnerabilities, filename='assignment10/owasp_top_10.json'):
    """
    Save vulnerabilities to JSON file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(vulnerabilities, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(vulnerabilities)} vulnerabilities to {filename}")
        return True
    except Exception as e:
        print(f"ERROR saving JSON: {e}")
        return False


# Main execution
if __name__ == "__main__":
    print("="*80)
    print("TASK 6: OWASP Top 10 Web Scraping with Selenium")
    print("="*80)
    print()
    
    # TASK 6: Scrape the page using Selenium
    vulnerabilities = scrape_owasp_top_10()
    
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    
    # TASK 6: Print the list to verify data
    if vulnerabilities:
        print(f"\nExtracted {len(vulnerabilities)} vulnerabilities:\n")
        for i, vuln in enumerate(vulnerabilities, 1):
            print(f"{i}. {vuln['title']}")
            print(f"   Link: {vuln['link']}\n")
        
        # TASK 6: Save to CSV file
        print("="*80)
        save_to_csv(vulnerabilities)
        save_to_json(vulnerabilities)
    else:
        print("WARNING: No vulnerabilities were extracted!")
        print("This may indicate a change in the website structure.")
        print("Check the page manually and update the XPath selectors.")
