import requests
from bs4 import BeautifulSoup
import re
import time

# --------------------
# Simple cache system
# --------------------
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

# --------------------
# Parse list of manga
# --------------------
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

# --------------------
# Paginated scraping with HTMX has_next_page detection
# --------------------
def scrape_paginated_bge(url, page):
    html = cached_get(url)
    if not html:
        return {"page": page, "has_next_page": False, "results": []}
    soup = BeautifulSoup(html, "html.parser")

    # detect HTMX lazy loading next page
    hx_next = soup.select_one("span[hx-get]")
    has_next = False
    if hx_next:
        next_url = hx_next.get("hx-get", "")
        if next_url:
            has_next = True

    return {
        "page": page,
        "has_next_page": has_next,
        "results": parse_bge_list(soup)
    }

# --------------------
# Genre list scraping
# --------------------
def scrape_genre_all():
    html = cached_get("https://api.komiku.org/")
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for option in soup.select('select[name="genre"] option'):
        slug = option["value"]
        title = option.get_text(strip=True)
        if slug and title != "Genre 1":
            results.append({
                "title": title,
                "slug": slug
            })
    return results

# --------------------
# Specific page endpoints
# --------------------
def scrape_paginated_bge_with_page(tipe="manga", page=1):
    url = f"https://api.komiku.org/manga/page/{page}/?orderby&tipe={tipe}"
    return scrape_paginated_bge(url, page)

def scrape_hot_bge_with_page(tipe="manga", page=1):
    url = f"https://api.komiku.org/other/hot/page/{page}/?orderby=meta_value_num&tipe={tipe}"
    return scrape_paginated_bge(url, page)

def scrape_rekomendasi_bge_with_page(page=1):
    url = f"https://api.komiku.org/manga/page/{page}/?orderby=rand&genre&genre2&statusmanga&tipe"
    return scrape_paginated_bge(url, page)

def scrape_genre_page(genre="action", page=1):
    url = f"https://api.komiku.org/genre/{genre}/page/{page}/"
    return scrape_paginated_bge(url, page)
