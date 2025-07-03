import requests
from bs4 import BeautifulSoup
import re
import time

_cache = {}
_cache_timeout = 300

def cached_get(url):
    now = time.time()
    if url in _cache:
        data, timestamp = _cache[url]
        if now - timestamp < _cache_timeout:
            return data
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        _cache[url] = (response.text, now)
        return response.text
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch URL: {url} | {e}")
        return ""

def parse_bge_list(soup):
    results = []
    for div in soup.select("div.bge"):
        try:
            link_tag = div.select_one(".bgei a")
            title_tag = div.select_one("h3")
            img_tag = div.select_one("img")
            tpe_tag = div.select_one(".tpe1_inf")
            desc_tag = div.select_one("p")
            chapter_links = div.select("div.new1 a")

            if not all([link_tag, title_tag, img_tag]):
                continue

            type_genre = tpe_tag.get_text(strip=True).split(maxsplit=1) if tpe_tag else ["", ""]

            results.append({
                "title": title_tag.get_text(strip=True),
                "type": type_genre[0],
                "genre": type_genre[1] if len(type_genre) > 1 else "",
                "thumbnail": re.sub(r'\?resize=.*$', '', img_tag["src"]),
                "description": desc_tag.get_text(strip=True) if desc_tag else "",
                "link": link_tag["href"],
                "chapter_awal": {
                    "title": chapter_links[0].get_text(strip=True).replace("Awal: ", "") if len(chapter_links) > 0 else "",
                    "url": chapter_links[0]["href"] if len(chapter_links) > 0 else ""
                },
                "chapter_terbaru": {
                    "title": chapter_links[1].get_text(strip=True).replace("Terbaru: ", "") if len(chapter_links) > 1 else "",
                    "url": chapter_links[1]["href"] if len(chapter_links) > 1 else ""
                }
            })
        except Exception as e:
            print(f"[ERROR] Failed to parse div.bge: {e}")
            continue
    return results

def scrape_paginated_bge(url, page):
    html = cached_get(url)
    if not html:
        return {"page": page, "has_next_page": False, "results": []}
    soup = BeautifulSoup(html, "html.parser")
    return {
        "page": page,
        "has_next_page": soup.select_one("a.next.page-numbers") is not None,
        "results": parse_bge_list(soup)
    }

def scrape_paginated_bge_with_page(tipe="manga", page=1):
    return scrape_paginated_bge(f"https://api.komiku.org/manga/page/{page}/?orderby&tipe={tipe}", page)

def scrape_hot_bge_with_page(tipe="manga", page=1):
    return scrape_paginated_bge(f"https://api.komiku.org/other/hot/page/{page}/?orderby=meta_value_num&tipe={tipe}", page)

def scrape_rekomendasi_bge_with_page(page=1):
    return scrape_paginated_bge(f"https://api.komiku.org/manga/page/{page}/?orderby=rand&genre&genre2&statusmanga&tipe", page)

def scrape_genre_page(genre="action", page=1):
    return scrape_paginated_bge(f"https://api.komiku.org/genre/{genre}/page/{page}/", page)
