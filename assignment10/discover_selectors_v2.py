"""
Enhanced discovery script to find search result elements
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

# Look for common search result patterns
print("Looking for search result containers...\n")

# Check for ul with specific classes
uls = soup.find_all('ul', class_=True)
print(f"Found {len(uls)} <ul> elements with classes")
for i, ul in enumerate(uls):
    print(f"  {i+1}. class={ul.get('class', [])}, children: {len(ul.find_all(recursive=False))}")

# Look for divs that might contain results
print("\nLooking for divs that might be search results...")
divs_with_classes = soup.find_all('div', class_=True)
print(f"Found {len(divs_with_classes)} divs with classes")

# Look for elements with 'result', 'item', 'book' in their class
interesting_divs = []
for div in divs_with_classes:
    classes = ' '.join(div.get('class', []))
    if any(word in classes.lower() for word in ['result', 'item', 'book', 'search', 'entry']):
        interesting_divs.append(div)

print(f"\nDivs with 'result/item/book/search/entry' in class: {len(interesting_divs)}")
for i, div in enumerate(interesting_divs[:5]):
    print(f"  {i+1}. class={div.get('class', [])}")

# Look for list items in result-like divs
print("\nLooking for structure with specific search terms...")
print("\nSearching for 'learning' or 'spanish' in page (first book should be about that)...")
text_items = soup.find_all(string=True)
for item in text_items:
    if 'learning' in item.lower() or 'spanish' in item.lower():
        parent = item.parent
        print(f"Found text: '{item.strip()[:50]}' in <{parent.name}> class={parent.get('class', [])}")
        # Walk up the tree
        ancestor = parent.parent
        for level in range(4):
            if ancestor:
                print(f"  Level {level+1} parent: <{ancestor.name}> class={ancestor.get('class', [])}")
                ancestor = ancestor.parent
        break

# Save the full HTML to inspect manually
with open('/tmp/page_source.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
print("\nFull HTML saved to /tmp/page_source.html")
