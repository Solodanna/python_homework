"""
Get detailed structure of search results to find title, authors, and format/year
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
result_lis = results_ul.find_all('li', recursive=False)

print(f"Found {len(result_lis)} search results\n")
print("="*80)

for idx, li in enumerate(result_lis[:3]):  # Check first 3 results
    print(f"\nRESULT #{idx+1}")
    print(f"LI class: {li.get('class', [])}")
    
    # Find all links and categorize them
    all_links = li.find_all('a')
    print(f"\nLinks in this result:")
    for link in all_links:
        href = link.get('href', '')
        classes = link.get('class', [])
        text = link.get_text().strip()[:60]
        print(f"  - class={classes}, href contains: {'/'.join(href.split('/')[-2:]) if href else 'no href'}")
        print(f"    text: '{text}'")
    
    # Look for manifestation link (usually the actual book title)
    manif_link = li.find('a', class_='manifestation-item-link')
    if manif_link:
        print(f"\n[TITLE] manifestation-item-link: '{manif_link.get_text().strip()[:80]}'")
    
    # Look for author links
    author_links = li.find_all('a', class_='author-link')
    if author_links:
        print(f"\n[AUTHORS] Found {len(author_links)} author-link elements:")
        for alink in author_links:
            print(f"  - '{alink.get_text().strip()}'")
    
    # Look for format/year span
    format_span = li.find('span', class_='display-info')
    if format_span:
        print(f"\n[FORMAT/YEAR] display-info span: '{format_span.get_text().strip()}'")
    
    # Look at the deprecated bib section which often has summary
    deprecated = li.find('div', class_='cp-deprecated-bib-brief')
    if deprecated:
        print(f"\ncp-deprecated-bib-brief div content:")
        print(f"  {deprecated.get_text().strip()[:120]}")
    
    print("\n" + "-"*80)
