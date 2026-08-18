import requests
from bs4 import BeautifulSoup

def track_rankings_and_difficulty(target_phrase):
    """Task 2: Checks live multi-engine positions and runs an open-source Difficulty model."""
    print(f"🕵️ Task [SERP]: Tracking engine placements and analyzing difficulty metrics...")
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    cleaned_phrase = target_phrase.lower().strip()
    
    serp_records = []
    exact_title_or_snippet_matches = 0
    total_scanned_nodes = 0

    # 1. Evaluate Google Placements
    try:
        res = requests.get(f"https://google.com{cleaned_phrase.replace(' ', '+')}", headers=headers, timeout=8)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for rank, element in enumerate(soup.find_all('div', class_='g'), 1):
                anchor = element.find('a')
                snippet_node = element.find('div', class_='VwiC3b') # Google standard description layer
                if anchor and anchor.find('h3'):
                    title = anchor.find('h3').text
                    url = anchor['href']
                    snippet = snippet_node.text if snippet_node else ""
                    
                    total_scanned_nodes += 1
                    if cleaned_phrase in title.lower() or cleaned_phrase in snippet.lower():
                        exact_title_or_snippet_matches += 1
                        
                    serp_records.append({"engine": "Google", "rank": rank, "title": title, "url": url})
                if rank >= 5: break # Focus on Top 5 priority battlefield nodes
    except Exception as e: print(f"⚠️ Google monitor alert: {e}")

    # 2. Evaluate Bing Placements
    try:
        res = requests.get(f"https://bing.com{cleaned_phrase.replace(' ', '+')}", headers=headers, timeout=8)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for rank, item in enumerate(soup.find_all('li', class_='b_algo'), 1):
                title_node = item.find('h2')
                caption_node = item.find('p')
                if title_node and title_node.find('a'):
                    title = title_node.find('a').text
                    url = title_node.find('a')['href']
                    snippet = caption_node.text if caption_node else ""
                    
                    total_scanned_nodes += 1
                    if cleaned_phrase in title.lower() or cleaned_phrase in snippet.lower():
                        exact_title_or_snippet_matches += 1
                        
                    serp_records.append({"engine": "Bing", "rank": rank, "title": title, "url": url})
                if rank >= 5: break
    except Exception as e: print(f"⚠️ Bing monitor alert: {e}")

    # 3. Open-Source Keyword Difficulty Matrix Formula Strategy
    # If 100% of top competitors optimize their titles/snippets for this exact term, difficulty is Max (100%)
    if total_scanned_nodes > 0:
        difficulty_score = int((exact_title_or_snippet_matches / total_scanned_nodes) * 100)
    else:
        difficulty_score = 15 # Fallback baseline difficulty metric
        
    if difficulty_score < 30: difficulty_tier = "Easy (Green Arbitrage)"
    elif difficulty_score < 65: difficulty_tier = "Moderate (Requires Structural Content Density)"
    else: difficulty_tier = "Hard (High Authority Competitors Entrenched)"

    return serp_records, f"{difficulty_score}% - {difficulty_tier}"
