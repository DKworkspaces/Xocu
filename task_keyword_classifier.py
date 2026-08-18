import requests
import json

def harvest_and_classify_keywords(seed_word):
    """Task 1: Collects secondary vectors from multi-engine prompts and classifies Intent."""
    print(f"📡 Task [Classifier]: Expanding seed phrase clusters for '{seed_word}'...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    raw_discovered = set()
    
    # Target Google + Bing autocomplete indices to cross-reference trends
    for url_template in [
        f"http://google.com{seed_word.replace(' ', '+')}",
        f"https://bing.com{seed_word.replace(' ', '+')}"
    ]:
        try:
            res = requests.get(url_template, headers=headers, timeout=5)
            if res.status_code == 200:
                for suggestion in json.loads(res.text)[1]:
                    raw_discovered.add(suggestion.strip().lower())
        except Exception: pass

    classified_matrix = []
    
    # Evaluates user intent parameters based on structural semantics
    for kw in raw_discovered:
        kw_lower = kw.lower()
        if any(word in kw_lower for word in ['best', 'top', 'vs', 'review', 'alternative']):
            intent = "Commercial Investigation"
        elif any(word in kw_lower for word in ['buy', 'price', 'software', 'tool', 'service', 'hire']):
            intent = "Transactional (High Value)"
        elif any(word in kw_lower for word in ['how', 'why', 'what', 'guide', 'tutorial', 'tips', 'learn']):
            intent = "Informational (Content Drop)"
        else:
            intent = "Navigational / Brand Search"
            
        # Determine long-tail classification metric
        length = len(kw.split())
        kw_type = "Long-Tail Niche" if length >= 3 else "Short-Tail Broad Seed"
        
        classified_matrix.append({
            "keyword": kw,
            "intent": intent,
            "type": kw_type
        })
        
    return classified_matrix
