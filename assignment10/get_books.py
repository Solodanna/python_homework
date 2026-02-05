"""
Assignment 10: Web Scraping Durham County Library
Task: Scrape book data from search results
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time

# Task 1: Review robots.txt to Ensure Policy Compliance
# Verified: https://durhamcountylibrary.org/robots.txt
# - Public content allowed (not under /staff/)
# - Using standard User-Agent header for ethical scraping

# Task 2: Understanding HTML and the DOM for the Durham Library Site
# Identified HTML elements:
# - Search result <li> elements with class: 'cp-search-result-item' and 'row'
# - Title <h3> element within cp-deprecated-bib-brief div
# - Author <a> elements with class: 'author-link'
# - Format/Year <span> element with class: 'display-info'

url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def scrape_books(url, headers):
    """
    Scrape book search results from Durham County Library
    Returns a list of book dictionaries with Title, Author, and Format-Year
    """
    print("Fetching page...")
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Task: Find all li elements for search results
    # Using the class 'cp-search-result-item' and 'row' identified in task 2
    results_ul = soup.find('ul', class_='results')
    
    if not results_ul:
        print("ERROR: Could not find results ul element")
        return []
    
    result_lis = results_ul.find_all('li', class_='cp-search-result-item')
    print(f"Found {len(result_lis)} search results\n")
    
    # TASK 3: Create empty list for results and iterate through li entries
    results = []
    
    # Main loop: iterate through each search result li element
    for idx, li in enumerate(result_lis, 1):
        print(f"Processing result {idx}...")
        
        try:
            # Task: Find the title element
            # Title is in <h3> tag within the cp-deprecated-bib-brief div
            title = ""
            title_h3 = li.find('h3')
            if title_h3:
                title_text = title_h3.get_text().strip()
                # The h3 sometimes has duplicated text - split by looking for repeating pattern
                # Example: "Learning Spanish-beginner ILearning Spanish-beginner I"
                # Take the first meaningful chunk by splitting roughly in half
                if len(title_text) > 20:
                    # Check if text repeats
                    mid = len(title_text) // 2
                    first_half = title_text[:mid]
                    second_half = title_text[mid:]
                    # If first half appears in second half, we have duplication
                    if first_half.strip() in second_half or title_text[:15] in title_text[15:]:
                        # Find the actual split point
                        for i in range(len(title_text)//3, len(title_text)//2 + 1):
                            if title_text[:i].strip() == title_text[i:i+len(title_text[:i])].strip():
                                title = title_text[:i].strip()
                                break
                        if not title:
                            title = title_text[:mid].strip()
                    else:
                        title = title_text
                else:
                    title = title_text
            
            if not title:
                print(f"  WARNING: Could not find title for result {idx}")
                continue
            
            print(f"  Title: {title[:60]}")
            
            # TASK 3: Find author element(s) and join with semicolons
            author_links = li.find_all('a', class_='author-link')
            authors = []
            for alink in author_links:
                author_text = alink.get_text().strip()
                if author_text:
                    authors.append(author_text)
            
            # Join multiple authors with semicolon
            author = "; ".join(authors)
            print(f"  Authors: {author[:60]}")
            
            # TASK 3: Find format and year span element
            format_span = li.find('span', class_='display-info')
            format_year = ""
            if format_span:
                format_year = format_span.get_text().strip()
            
            if not format_year:
                print(f"  WARNING: Could not find format/year for result {idx}")
            
            print(f"  Format/Year: {format_year}")
            
            # TASK 3: Create dict with Title, Author, Format-Year keys and append to results
            book_dict = {
                'Title': title,
                'Author': author,
                'Format-Year': format_year
            }
            
            # Append to results list
            results.append(book_dict)
            print()
            
        except Exception as e:
            print(f"  ERROR processing result {idx}: {e}\n")
            continue
    
    return results

# TASK 3 (continuation): Create DataFrame from results list and print
# For Further Thought: Pagination logic to scrape all pages

# Main execution
if __name__ == "__main__":
    print("="*80)
    print("ASSIGNMENT 10: Durham County Library Web Scraping")
    print("="*80)
    print()
    
    # Optional: For Further Thought - scrape all pages
    # To get all search results from all pages, we need to:
    # 1. Check if pagination exists
    # 2. Identify the next page URL or pagination structure
    # 3. Loop through pages with delays between requests
    
    all_results = []
    page_num = 1
    base_url = "https://durhamcounty.bibliocommons.com/v2/search"
    
    while True:
        print(f"\n--- PAGE {page_num} ---")
        
        # Build URL with pagination
        if page_num == 1:
            current_url = url
        else:
            current_url = f"{base_url}?query=learning%20spanish&searchType=smart&offset={(page_num-1)*5}"
        
        print(f"Scraping: {current_url}")
        
        # Scrape books from current page
        page_results = scrape_books(current_url, headers)
        
        if not page_results:
            print(f"No results found on page {page_num}. Stopping.")
            break
        
        all_results.extend(page_results)
        
        # For first run, only get first page to be respectful
        # Uncomment below to get all pages with delays
        # Check if there's a next page by fetching and checking pagination
        response = requests.get(current_url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for next page button or pagination
        next_button = soup.find('a', {'aria-label': lambda x: x and 'next' in x.lower()})
        pagination_items = soup.find('ul', class_='pagination__desktop-items')
        
        if not next_button and not pagination_items:
            print(f"No more pages available. Total results: {len(all_results)}")
            break
        
        # Break after first page for respectful scraping
        print(f"\nNote: Additional pages exist but we only scraped the first page.")
        print(f"To scrape all pages, uncomment the pagination loop and add time.sleep() between requests.")
        break
        
        # Respectful delay between page requests (REQUIRED per robots.txt)
        # time.sleep(2)
        # page_num += 1
    
    print("="*80)
    print(f"Scraped {len(all_results)} books total\n")
    
    # Create DataFrame from results list
    df = pd.DataFrame(all_results)
    
    # Print the DataFrame
    print("RESULTS DATAFRAME:")
    print("-"*80)
    print(df.to_string(index=False))
    print()
    
    # Optional: Save to CSV
    output_file = "books.csv"
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")
