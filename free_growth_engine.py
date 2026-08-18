import os
import requests
import json
from datetime import datetime

def fetch_free_keywords(topic):
    """Scrapes Google Autocomplete for real, high-volume keywords for free."""
    print(f"🔍 Scraping Google trends for: '{topic}'...")
    url = f"http://google.com{topic}"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            suggestions = json.loads(response.text)
            return suggestions[:4]
    except Exception as e:
        print(f"⚠️ Scraping error: {e}")
    return [f"{topic} tips", f"{topic} tutorial", f"{topic} guide"]

def generate_ai_prompt_package():
    # 1. Read the topic from query.txt
    if not os.path.exists("query.txt"):
        print("❌ Error: query.txt file not found!")
        return
        
    with open("query.txt", "r", encoding="utf-8") as f:
        topic = f.read().strip()
        
    if not topic:
        print("❌ Error: query.txt is empty!")
        return

    # 2. Get real keywords for free
    keywords = fetch_free_keywords(topic)
    
    # 3. Read agent framework rules
    team_rules = ""
    if os.path.exists(".squad/team.md"):
        with open(".squad/team.md", "r") as f:
            team_rules = f.read()
            
    # 4. Read brand profile context
    brand_context = ""
    if os.path.exists(".squad/brand.md"):
        with open(".squad/brand.md", "r") as f:
            brand_context = f.read()

    # 5. Construct the master prompt block
    prompt = "# 🚀 CODESPACE CONTENT ENGINE GENERATOR PROMPT\n\n"
    prompt += f"**Core Topic**: {topic}\n"
    prompt += f"**Generated On**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    prompt += "Copy and paste this entire block into any free AI interface (ChatGPT, Claude, Gemini):\n\n"
    prompt += "```text\n"
    prompt += f"Act as a professional marketing team starting from 0 followers. Our core topic is: '{topic}'\n\n"
    prompt += "## Real-Time Search Keywords to Include:\n"
    for kw in keywords:
        prompt += f"- {kw}\n"
    prompt += "\n## Brand Guidelines:\n"
    prompt += brand_context if brand_context else "Provide concise, valuable content.\n"
    prompt += "\n## Team Profiles and Generation Tasks:\n"
    prompt += team_rules if team_rules else "Generate a Twitter Thread, Pinterest Pin, and Instagram Reel description."
    prompt += "\n```"
    
    # 6. Save the output directly into a 'campaigns' folder
    os.makedirs("campaigns", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_filename = f"campaigns/campaign_{timestamp}.md"
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(prompt)
        
    print(f"✅ Success! Generated prompt saved to: {output_filename}")

if __name__ == "__main__":
    generate_ai_prompt_package()
    
