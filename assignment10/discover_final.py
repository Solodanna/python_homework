"""
Final discovery script to identify search result selectors
"""
import requests
from bs4 import BeautifulSoup

url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

print("Fetching page...")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the results ul
results_ul = soup.find('ul', class_='results')
if results_ul:
    print(f"Found <ul class='results'> with {len(results_ul.find_all('li', recursive=False))} direct children\n")
    
    # Get the first result li
    result_lis = results_ul.find_all('li', recursive=False)
    if result_lis:
        first_li = result_lis[0]
        print(f"FIRST RESULT LI:")
        print(f"  Classes: {first_li.get('class', [])}")
        print(f"  ID: {first_li.get('id', 'No ID')}\n")
        
        # Find title
        print("TITLE ELEMENT:")
        title_elem = first_li.find('h2', class_=True) or first_li.find('a', class_=True)
        if not title_elem:
            title_elem = first_li.find(['h2', 'h3', 'a'])
        if title_elem:
            print(f"  Tag: <{title_elem.name}>")
            print(f"  Classes: {title_elem.get('class', [])}")
            print(f"  Text: {title_elem.get_text()[:60]}\n")
        
        # Find authors
        print("AUTHOR ELEMENTS:")
        author_links = first_li.find_all('a', class_=True)
        for i, link in enumerate(author_links[:5]):
            classes = link.get('class', [])
            text = link.get_text().strip()
            # Skip if it looks like a button or control
            if 'btn' not in ' '.join(classes) and text and len(text) > 2:
                print(f"  Link {i+1}: classes={classes}, text='{text[:50]}'")
        
        print("\nALL DIVS IN FIRST RESULT:")
        all_divs = first_li.find_all('div', class_=True)
        for i, div in enumerate(all_divs):
            classes = div.get('class', [])
            print(f"  Div {i+1}: {classes}")
            
            # Check for spans in each div
            spans = div.find_all('span', class_=True, recursive=False)
            for span in spans[:2]:
                span_classes = span.get('class', [])
                span_text = span.get_text().strip()[:50]
                if span_text:
                    print(f"    Span: classes={span_classes}, text='{span_text}'")
        
        print("\n" + "="*70)
        print("SUMMARY FOR get_books.py:")
        print("="*70)
        print(f"\n1. Search result li selector: ul.results > li (or li with class={first_li.get('class', [])})")
        print(f"\n2. Title element: Look for <h2> or first link containing book title")
        print(f"\n3. Author links: Find all <a> tags and filter by class/content")
        print(f"\n4. Format/Year: Look in divs for specific class patterns")
        
else:
    print("Could not find <ul class='results'>")
