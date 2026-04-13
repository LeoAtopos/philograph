"""
Fetch Wikipedia portrait URLs for philosophers missing real images.
Uses the Wikipedia API to find portrait images.
Output: a JSON mapping philosopher id -> image URL.
"""

import json
import urllib.request
import urllib.parse
import time
import os
import ssl

# Western philosophers with placeholder images
WESTERN = [
    ("heraclitus", "Heraclitus"),
    ("parmenides", "Parmenides"),
    ("plotinus", "Plotinus"),
    ("ockham", "William of Ockham"),
    ("hobbes", "Thomas Hobbes"),
    ("pascal", "Blaise Pascal"),
    ("berkeley", "George Berkeley"),
    ("montesquieu", "Montesquieu"),
    ("schopenhauer", "Arthur Schopenhauer"),
    ("kierkegaard", "Søren Kierkegaard"),
    ("peirce", "Charles Sanders Peirce"),
    ("james", "William James"),
    ("dewey", "John Dewey"),
    ("husserl", "Edmund Husserl"),
    ("arendt", "Hannah Arendt"),
    ("merleau-ponty", "Maurice Merleau-Ponty"),
    ("quine", "W.V.O. Quine"),
    ("davidson", "Donald Davidson"),
    ("kuhn", "Thomas Kuhn"),
    ("foucault", "Michel Foucault"),
    ("habermas", "Jürgen Habermas"),
    ("derrida", "Jacques Derrida"),
    ("searle", "John Searle"),
    ("nozick", "Robert Nozick"),
    ("singer", "Peter Singer"),
]

# Chinese philosophers with empty portrait
CHINESE = [
    ("sunzi", "Sun Tzu"),
    ("gongsunlong", "Gongsun Long"),
    ("liezi", "Liezi"),
    ("shen_buhai", "Shen Buhai"),
    ("zouyan", "Zou Yan"),
    ("yangxiong", "Yang Xiong"),
    ("wangbi", "Wang Bi"),
    ("guoxiang", "Guo Xiang"),
    ("jikang", "Ji Kang"),
    ("zhiyi", "Zhiyi"),
    ("xuanzang", "Xuanzang"),
    ("huineng", "Huineng"),
    ("fazang", "Fazang"),
    ("liuzongyuan", "Liu Zongyuan"),
    ("zhou_dunyi", "Zhou Dunyi"),
    ("zhangzai", "Zhang Zai"),
    ("chenghao", "Cheng Hao"),
    ("lu_jiuyuan", "Lu Jiuyuan"),
    ("li_zhi", "Li Zhi"),
    ("daizhen", "Dai Zhen"),
    ("gongzizhen", "Gong Zizhen"),
    ("weiyuan", "Wei Yuan"),
    ("kangyouwei", "Kang Youwei"),
    ("liangqichao", "Liang Qichao"),
    ("zhangtaiyan", "Zhang Taiyan"),
    ("xiongshili", "Xiong Shili"),
    ("liangshuming", "Liang Shuming"),
    ("tangjunyi", "Tang Junyi"),
    ("laosiguang", "Lao Siguang"),
    ("qianmu", "Qian Mu"),
]

ALL = WESTERN + CHINESE

def fetch_portrait(title, is_chinese=False):
    """Fetch portrait image URL from Wikipedia."""
    # For Chinese philosophers, try Chinese Wikipedia first
    if is_chinese:
        # Map to Chinese Wikipedia titles
        cn_title_map = {
            "Sun Tzu": "孙子",
            "Gongsun Long": "公孙龙",
            "Liezi": "列子",
            "Shen Buhai": "申不害",
            "Zou Yan": "邹衍",
            "Yang Xiong": "扬雄",
            "Wang Bi": "王弼",
            "Guo Xiang": "郭象",
            "Ji Kang": "嵇康",
            "Zhiyi": "智顗",
            "Xuanzang": "玄奘",
            "Huineng": "惠能",
            "Fazang": "法藏",
            "Liu Zongyuan": "柳宗元",
            "Zhou Dunyi": "周敦颐",
            "Zhang Zai": "张载",
            "Cheng Hao": "程颢",
            "Lu Jiuyuan": "陆九渊",
            "Li Zhi": "李贽",
            "Dai Zhen": "戴震",
            "Gong Zizhen": "龚自珍",
            "Wei Yuan": "魏源",
            "Kang Youwei": "康有为",
            "Liang Qichao": "梁启超",
            "Zhang Taiyan": "章太炎",
            "Xiong Shili": "熊十力",
            "Liang Shuming": "梁漱溟",
            "Tang Junyi": "唐君毅",
            "Lao Siguang": "劳思光",
            "Qian Mu": "钱穆",
        }
        cn_title = cn_title_map.get(title, title)
        
        # Try Chinese Wikipedia
        url = f"https://zh.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(cn_title)}&prop=pageimages&format=json&piprop=original&pithumbsize=120"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'PhilographBot/1.0 (philosophy visualization project)'})
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                data = json.loads(resp.read().decode())
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if 'original' in page_data:
                    return page_data['original']['source']
                if 'thumbnail' in page_data:
                    return page_data['thumbnail']['source']
        except Exception as e:
            print(f"  CN wiki error for {title}: {e}")
    
    # Fallback to English Wikipedia
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=pageimages&format=json&piprop=original&pithumbsize=120"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PhilographBot/1.0 (philosophy visualization project)'})
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            if 'original' in page_data:
                return page_data['original']['source']
            if 'thumbnail' in page_data:
                return page_data['thumbnail']['source']
    except Exception as e:
        print(f"  EN wiki error for {title}: {e}")
    
    return None

def download_image(url, filepath):
    """Download image from URL to filepath."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PhilographBot/1.0 (philosophy visualization project)'})
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            with open(filepath, 'wb') as f:
                f.write(resp.read())
        return True
    except Exception as e:
        print(f"  Download error: {e}")
        return False

def main():
    portraits_dir = os.path.join(os.path.dirname(__file__), 'portraits')
    os.makedirs(portraits_dir, exist_ok=True)
    
    results = {}
    
    print("=" * 60)
    print("Fetching Wikipedia portraits for missing philosophers")
    print("=" * 60)
    
    # Western philosophers
    print("\n--- Western Philosophers (25) ---")
    for phil_id, name in WESTERN:
        safe_name = name.encode('ascii', 'replace').decode('ascii')
        print(f"  Looking up {safe_name}...", end=" ", flush=True)
        img_url = fetch_portrait(name, is_chinese=False)
        if img_url:
            results[phil_id] = img_url
            # Download to local file
            ext = os.path.splitext(img_url)[1].split('?')[0] or '.jpg'
            if ext not in ('.jpg', '.jpeg', '.png', '.gif', '.webp'):
                ext = '.jpg'
            local_path = os.path.join(portraits_dir, f"{phil_id}{ext}")
            if download_image(img_url, local_path):
                results[phil_id] = f"data/portraits/{phil_id}{ext}"
                print(f"OK -> {phil_id}{ext}")
            else:
                print(f"DOWNLOAD FAILED: {img_url[:80]}...")
        else:
            print("NOT FOUND")
        time.sleep(0.3)
    
    # Chinese philosophers
    print("\n--- Chinese Philosophers (30) ---")
    for phil_id, name in CHINESE:
        safe_name = name.encode('ascii', 'replace').decode('ascii')
        print(f"  Looking up {safe_name}...", end=" ", flush=True)
        img_url = fetch_portrait(name, is_chinese=True)
        if img_url:
            results[phil_id] = img_url
            # Download to local file
            ext = os.path.splitext(img_url)[1].split('?')[0] or '.jpg'
            if ext not in ('.jpg', '.jpeg', '.png', '.gif', '.webp'):
                ext = '.jpg'
            local_path = os.path.join(portraits_dir, f"{phil_id}{ext}")
            if download_image(img_url, local_path):
                results[phil_id] = f"data/portraits/{phil_id}{ext}"
                print(f"OK -> {phil_id}{ext}")
            else:
                print(f"DOWNLOAD FAILED: {img_url[:80]}...")
        else:
            print("NOT FOUND")
        time.sleep(0.3)
    
    # Summary
    found = len(results)
    total = len(ALL)
    print(f"\n{'=' * 60}")
    print(f"Results: {found}/{total} portraits found")
    print(f"{'=' * 60}")
    
    # Save results as JSON for review
    output_path = os.path.join(os.path.dirname(__file__), 'wiki_portraits_result.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Saved to {output_path}")

if __name__ == '__main__':
    main()
