import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time
import pypinyin
import sys
import re

# Usage: python scrape_category.py <category_id> <output_name>
# e.g. python scrape_category.py 0003 rihan
# e.g. python scrape_category.py 0004 oumei

CATEGORY = sys.argv[1] if len(sys.argv) > 1 else "0003"
OUT_NAME = sys.argv[2] if len(sys.argv) > 2 else "rihan"

BASE_DOMAIN = "http://www.cecet.cn"
LIST_URL = f"http://www.cecet.cn/stardata/{CATEGORY}/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

PROGRESS_FILE = f"data/{OUT_NAME}_progress.json"
LINKS_FILE = f"data/{OUT_NAME}_links.json"
OUTPUT_FILE = f"data/{OUT_NAME}_star_20260426.json"

def get_person_id(name):
    try:
        pys = pypinyin.lazy_pinyin(name)
        pid = "_".join(pys)
        if pid and not pid.replace("_", "").isdigit():
            return pid
    except:
        pass
    # Fallback: use name as-is, replace spaces
    return re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '_', name)

def guess_gender(name):
    female_chars = set("姐婷娜娟妍妃妙姝婉萱颖璐瑶琳芳薇静蕾倩淑媛樱嫣珏怡芬娇璐霞")
    male_chars = set("刚强伟勇军磊涛峰鹏辉浩杰志明龙虎威震坤锋毅宏博毅雄")
    f_count = sum(1 for c in name if c in female_chars)
    m_count = sum(1 for c in name if c in male_chars)
    if f_count > m_count:
        return 2
    elif m_count > f_count:
        return 1
    return 1

def scrape_list_page(page_url):
    """Scrape one list page to get detail links and names"""
    try:
        resp = requests.get(page_url, headers=HEADERS, timeout=30)
        resp.encoding = "gb18030"
    except Exception as e:
        print(f"  ERROR fetching {page_url}: {e}")
        return [], []

    soup = BeautifulSoup(resp.text, "html.parser")
    main_div = soup.select_one("div.main.cbody.margintop")
    if not main_div:
        return [], []

    table = main_div.find("table")
    if not table:
        return [], []

    stars = []
    page_links = []
    for a_tag in table.find_all("a", href=True):
        name = a_tag.get_text(strip=True)
        href = a_tag["href"]
        if not name or not href:
            continue
        if name in ("下一页", "末页", "上一页", "首页"):
            continue

        # Pagination link: list_XXXX_N.shtml
        if "list_" in href and href.endswith(".shtml"):
            page_links.append(urljoin(page_url, href))
            continue

        # Star detail link
        detail_url = urljoin(page_url, href)
        stars.append({"name": name, "detail_url": detail_url})

    return stars, page_links

def scrape_detail_page(detail_url):
    """Scrape detail page for image URL"""
    try:
        resp = requests.get(detail_url, headers=HEADERS, timeout=30)
        resp.encoding = "gb18030"
        soup = BeautifulSoup(resp.text, "html.parser")

        fontzoom = soup.select_one("#fontzoom")
        if not fontzoom:
            return None

        img = fontzoom.find("img")
        if not img:
            return None

        src = img.get("src", "") or img.get("data-src", "") or img.get("data-original", "")
        if not src:
            return None

        if src.startswith("//"):
            src = "http:" + src
        elif src.startswith("/"):
            src = BASE_DOMAIN + src
        elif not src.startswith("http"):
            src = urljoin(detail_url, src)

        return src
    except:
        return None

def collect_all_list_links():
    """Step 1: Collect all star links from all list pages"""
    all_stars = []
    visited_pages = set()
    pages_to_visit = [LIST_URL]
    visited_pages.add(LIST_URL)

    while pages_to_visit:
        page_url = pages_to_visit.pop(0)
        stars, page_links = scrape_list_page(page_url)

        for pl in page_links:
            if pl not in visited_pages:
                visited_pages.add(pl)
                pages_to_visit.append(pl)

        all_stars.extend(stars)
        print(f"Page {page_url}: {len(stars)} stars, total: {len(all_stars)}, remaining pages: {len(pages_to_visit)}")
        time.sleep(0.1)

    # Deduplicate
    seen = set()
    unique = []
    for s in all_stars:
        if s["name"] not in seen:
            seen.add(s["name"])
            unique.append(s)

    print(f"\nTotal unique stars collected: {len(unique)}")
    with open(LINKS_FILE, "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)
    print(f"Saved to {LINKS_FILE}")
    return unique

def scrape_all_details(stars):
    """Step 2: Scrape detail pages for images"""
    results = []
    total = len(stars)
    # Load progress if exists
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            results = json.load(f)
        done_names = {r["name"] for r in results}
        print(f"Resuming from {len(results)} already processed")
    except:
        done_names = set()

    for i, star in enumerate(stars):
        if star["name"] in done_names:
            continue

        name = star["name"]
        detail_url = star["detail_url"]
        img_url = scrape_detail_page(detail_url)

        if img_url:
            results.append({
                "name": name,
                "person_id": get_person_id(name),
                "gender": guess_gender(name),
                "url": img_url,
                "remark": ""
            })

        # Save progress every 50 stars
        if (i + 1) % 50 == 0:
            with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent="\t")
            print(f"  Progress saved: {len(results)}/{total}")

        if (i + 1) % 100 == 0:
            print(f"  [{i+1}/{total}] processed, {len(results)} with images")

        time.sleep(0.15)

    return results

def main():
    mode = sys.argv[3] if len(sys.argv) > 3 else "all"

    print(f"=== Scraping category {CATEGORY} ({OUT_NAME}) ===")

    if mode in ("all", "list"):
        stars = collect_all_list_links()
    else:
        with open(LINKS_FILE, "r", encoding="utf-8") as f:
            stars = json.load(f)
        print(f"Loaded {len(stars)} stars from {LINKS_FILE}")

    if mode in ("all", "detail"):
        if mode == "detail":
            with open(LINKS_FILE, "r", encoding="utf-8") as f:
                stars = json.load(f)
            print(f"Loaded {len(stars)} stars from {LINKS_FILE}")

        results = scrape_all_details(stars)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent="\t")
        print(f"\nDone! Saved {len(results)} stars to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
