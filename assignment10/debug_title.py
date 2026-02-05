"""
Debug script to see exact HTML structure for titles
"""
import requests
from bs4 import BeautifulSoup

url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.content, 'html.parser')

results_ul = soup.find('ul', class_='results')
result_lis = results_ul.find_all('li', class_='cp-search-result-item')

# Check first result's title area
first_li = result_lis[0]

# Find the title link (it has href but no class)
title_link = first_li.find('a', href=True)
print(f"First <a> with href: '{title_link.get_text().strip()}'")
print(f"  href: {title_link.get('href')}")

# Get all meaningful text from the bib section
bib_div = first_li.find('div', class_='cp-deprecated-bib-brief')
print(f"\nBib div full text:\n'{bib_div.get_text()}'")

# Get just the direct text (not nested)
print(f"\nBib div direct children:")
for child in bib_div.children:
    if isinstance(child, str):
        text = child.strip()
        if text:
            print(f"  Text node: '{text}'")
    else:
        print(f"  Element: <{child.name}> = '{child.get_text().strip()[:50]}'")
