import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import json

def fetch_all_urls(base_url, headers):
    req = Request(base_url, headers=headers)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    
    urls = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/'):
            url = urljoin(base_url, href)
            urls.add(url)
        elif href.startswith(base_url):
            urls.add(href)
    
    return list(urls)

def scrape_page_data(url, headers):
    req = Request(url, headers=headers)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    
    page_data = {
        "url": url,
        "title": soup.title.string if soup.title else "No title",
        "description": "",
        "content": ""
    }
    
    description_tag = soup.find('meta', attrs={"name": "description"})
    if description_tag:
        page_data["description"] = description_tag.get('content', "No description found")
    
    content_paragraphs = soup.find_all('p')
    page_data["content"] = " ".join([p.get_text() for p in content_paragraphs])
    
    return page_data

def main(base_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        urls = fetch_all_urls(base_url, headers)
        all_data = []
        for url in urls:
            page_data = scrape_page_data(url, headers)
            all_data.append(page_data)
        
        print(json.dumps(all_data, indent=4))
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    company_base_url = "https://lokker.com/"
    main(company_base_url)
