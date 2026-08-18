import requests
from bs4 import BeautifulSoup

def calculate_onpage_keyword_density(url, target_phrase):
    """Task 3: Analyzes top competitor source text to extract on-page keyword density."""
    print(f"📉 Task [Page Crawler]: Crawling top placement website: {url}")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    phrase_lower = target_phrase.lower().strip()
    
    try:
        response = requests.get(url, headers=headers, timeout=7)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Kill script and style code text blocks to prevent measurement distortion
            for script in soup(["script", "style"]):
                script.extract()
                
            raw_text = soup.get_text().lower()
            words_list = raw_text.split()
            total_word_count = len(words_list)
            
            if total_word_count == 0: return "0.0% (Empty plain-text structure)"
            
            phrase_occurrences = raw_text.count(phrase_lower)
            # Density balance weight calculation map
            density_percentage = (phrase_occurrences * len(phrase_lower.split()) / total_word_count) * 100
            
            return f"{density_percentage:.2f}% (Total Content Words: {total_word_count} | Phrase Count: {phrase_occurrences})"
    except Exception: pass
    
    return "Could not reach site (Protected by CDN/Cloudflare sandbox boundary)"
