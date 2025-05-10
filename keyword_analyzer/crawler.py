import requests
import re
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from tqdm import tqdm
from config import USER_AGENT, MAX_CRAWL_PAGES

class WebsiteCrawler:
    def __init__(self):
        self.visited = set()
        self.context = {}
        self.full_corpus = []
        self.seen_hashes = set()
        self.domain = ""
        self.headers = {'User-Agent': USER_AGENT}
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'}

    def _is_image_url(self, url):
        path = urlparse(url).path.lower()
        return any(path.endswith(ext) for ext in self.image_extensions)

    def crawl(self, start_url):
        self.domain = urlparse(start_url).netloc
        to_visit = [start_url]
        self.visited = set()
        
        with tqdm(total=MAX_CRAWL_PAGES, desc="Crawling website") as pbar:
            while to_visit and len(self.visited) < MAX_CRAWL_PAGES:
                url = to_visit.pop(0)
                if url in self.visited or self._is_image_url(url):
                    continue

                try:
                    resp = requests.get(url, headers=self.headers, timeout=10)
                    if resp.status_code == 200 and 'text/html' in resp.headers.get('Content-Type', ''):
                        soup = BeautifulSoup(resp.content, 'html.parser')
                        
                        # Clean page content
                        for tag in ["script", "style", "nav", "footer", "header"]:
                            for element in soup.find_all(tag):
                                element.decompose()
                        
                        text = soup.get_text(separator='\n')
                        cleaned = re.sub(r'\s+', ' ', text).strip()
                        
                        if len(cleaned) > 500:
                            content_hash = hash(cleaned)
                            if content_hash not in self.seen_hashes:
                                self.context[url] = cleaned
                                self.full_corpus.append(cleaned)
                                self.seen_hashes.add(content_hash)

                        # Find new links
                        for link in soup.find_all('a', href=True):
                            href = urljoin(url, link['href'])
                            parsed = urlparse(href)
                            if parsed.netloc == self.domain and href not in self.visited:
                                to_visit.append(href)
                                
                    self.visited.add(url)
                    pbar.update(1)
                    time.sleep(0.5)
                    
                except Exception as e:
                    continue
                    
        return self