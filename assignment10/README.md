# Assignment 10: Web Scraping - Durham County Library

## Overview

This assignment involves ethical web scraping of the Durham County Library book search to extract book information.

## Tasks Completed

### Task 1: Review robots.txt to Ensure Policy Compliance ✓

- **File**: [get_books.py](get_books.py#L11-L13)
- Verified compliance with Durham County Library's robots.txt policy
- Public content is allowed (not under /staff/ directory)
- Using standard User-Agent header for ethical scraping
- robots.txt link: https://durhamcountylibrary.org/robots.txt

### Task 2: Understanding HTML and the DOM for the Durham Library Site ✓

- **File**: [get_books.py](get_books.py#L15-L22)
- Located search result `<li>` elements with class: `cp-search-result-item` and `row`
- Found title element: `<h3>` tag within `cp-deprecated-bib-brief` div
- Found author elements: `<a>` tags with class `author-link`
- Found format/year element: `<span>` with class `display-info`

### Task 3: Main Implementation ✓

- **File**: [get_books.py](get_books.py#L43-L116)
- Implemented `scrape_books()` function that:
  1. Loads the Durham County Library search page
  2. Finds all search result `<li>` elements
  3. For each result:
     - Extracts the book title from `<h3>` tag
     - Extracts author(s) from `<a>` tags with class `author-link`
     - Joins multiple authors with semicolon separator
     - Extracts format and year from `<span>` with class `display-info`
     - Creates a dictionary with Title, Author, and Format-Year keys
  4. Appends each result to results list
  5. Creates DataFrame from results list
  6. Prints DataFrame to console
  7. Saves results to `books.csv`

### For Further Thought: Pagination ✓

- **File**: [get_books.py](get_books.py#L133-L175)
- Implemented pagination logic to detect additional pages
- Script respects robots.txt by using delays between requests
- Currently scrapes only first page to be respectful
- Code includes commented section for enabling full pagination with `time.sleep()` delays

## Files Generated

- **get_books.py** - Main web scraping script
- **books.csv** - Output CSV file with extracted book data

## Sample Output

```
Title,Author,Format-Year
Learning Spanish-beginner I,"Iris Acevedo A.; Spanishonline, Costarica","eBook, 2025 — Spanish"
Real-World Spanish: The Conversation Learning System,Camila Vega Rivera,"eAudiobook, 2025"
100 Facts About Learning Spanish,Science-Based Language Learning Lab,"eAudiobook, 2024"
A Beginner's Guide to Learning Spanish,"Miller, Jackson","eAudiobook, 2024"
100 Facts About Learning Spanish,Science-Based Language Learning Lab,"eBook, 2024"
```

## Running the Script

```bash
python get_books.py
```

## Ethical Considerations

This scraper follows web scraping best practices:

- ✓ Verifies robots.txt compliance
- ✓ Uses appropriate User-Agent header
- ✓ Includes delays between page requests (configurable)
- ✓ Only targets public data (not /staff/ paths)
- ✓ Respectfully handles pagination to avoid server overload
