import os
import sys
import requests
import json

def fetch_free_keywords(topic):
    """Scrapes Google Autocomplete for real, high-volume keywords for free."""
    print(f"🔍 Scraping Google trends for: '{topic}'...")
    url = f"http://google.com{topic}"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            suggestions = json.loads(response.text)
            return suggestions[1][:4]  # Extracts top 4 search suggestions safely
    except Exception as e:
        print(f"⚠️ Scraping error: {e}")
    return [f"{topic} tips", f"{topic} tutorial", f"{topic} guide"]

def generate_ai_prompt_package(topic):
    keywords = fetch_free_keywords(topic)
    
    # Read agent framework rules
    team_rules = ""
    if os.path.exists(".squad/team.md"):
        with open(".squad/team.md", "r") as f:
            team_rules = f.read()
            
    # Read brand profile context
    brand_context = ""
    if os.path.exists(".squad/brand.md"):
        with open(".squad/brand.md", "r") as f:
            brand_context = f.read()

    # Construct the master prompt block
    prompt = "### 🚀 CODESPACE CONTENT ENGINE GENERATOR PROMPT\n\n"
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
    
    # Print the clean output directly to the system logs so GitHub Actions can grab it
    print(prompt)

if __name__ == "__main__":
    # Pull the topic directly from the GitHub Issue title argument
    if len(sys.argv) > 1:
        # Combine arguments in case the title has spaces
        issue_title = " ".join(sys.argv[1:])
        generate_ai_prompt_package(issue_title)
    else:
        print("No issue title provided.")
