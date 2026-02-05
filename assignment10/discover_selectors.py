"""
Discovery script to find the CSS selectors for book search results
"""
import requests
from bs4 import BeautifulSoup
import time

# URL from Task 2
url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

print("Fetching page...")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    print("Page loaded. Parsing HTML...")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all li elements
    all_lis = soup.find_all('li')
    print(f"\nTotal <li> elements found: {len(all_lis)}")
    
    # Look for search result li elements
    # Typically they have classes like 'bibSearchResult' or similar
    print("\n--- Analyzing first 5 <li> elements ---")
    for i, li in enumerate(all_lis[:5]):
        print(f"\n<li {i+1}> classes: {li.get('class', [])}")
        print(f"ID: {li.get('id', 'No ID')}")
        
        # Look for title
        title_elem = li.find(['h2', 'h3', 'a', 'span'], class_=True)
        if title_elem:
            print(f"  Title element: <{title_elem.name}> class={title_elem.get('class', [])}, text: {title_elem.get_text()[:50]}...")
        
        # Look for author links
        author_links = li.find_all('a', class_=True)
        if author_links:
            print(f"  Found {len(author_links)} links:")
            for link in author_links[:3]:
                print(f"    <a> class={link.get('class', [])}, text: {link.get_text()[:40]}...")
        
        # Look for format/year info
        divs = li.find_all('div', class_=True)
        if divs:
            print(f"  Found {len(divs)} divs:")
            for div in divs[:3]:
                print(f"    <div> class={div.get('class', [])}")
                spans = div.find_all('span', class_=True)
                if spans:
                    for span in spans:
                        text = span.get_text()[:40]
                        if text:
                            print(f"      <span> class={span.get('class', [])}, text: {text}...")

except requests.RequestException as e:
    print(f"Error fetching page: {e}")

print("\n--- Instructions ---")
print("Use the information above to identify:")
print("1. The class value of the <li> search result elements")
print("2. The tag and class for the title element")
print("3. The class for author link elements")
print("4. The class for the format/year container div and its span child")
