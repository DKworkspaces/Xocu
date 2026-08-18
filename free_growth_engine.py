import os
from datetime import datetime

# Direct imports from task processing vectors
from task_keyword_classifier import harvest_and_classify_keywords
from task_serp_tracker import track_rankings_and_difficulty
from task_page_analyzer import calculate_onpage_keyword_density

def execute_workbench_system():
    # 1. Parse operational criteria inputs
    if not os.path.exists("query.txt"):
        print("❌ System Error: query.txt element missing!")
        return
    with open("query.txt", "r", encoding="utf-8") as f:
        seed_keyword = f.read().strip()
    if not seed_keyword:
        print("❌ System Error: query.txt element contains no data!")
        return

    print(f"🚀 Initializing Free Multi-Engine SEO Workbench Framework for: '{seed_keyword}'\n")

    # 2. Trigger task matrix operations
    keyword_silos = harvest_and_classify_keywords(seed_keyword)
    serp_standings, calculated_difficulty = track_rankings_and_difficulty(seed_keyword)
    
    # Isolate top active competitor URL node destination to test keyword footprint density
    top_competitor_url = None
    for record in serp_standings:
        if record["rank"] == 1 and "http" in record["url"]:
            top_competitor_url = record["url"]
            break
            
    if top_competitor_url:
        competitor_density = calculate_onpage_keyword_density(top_competitor_url, seed_keyword)
    else:
        competitor_density = "N/A (No direct ranking links scraped to review text parameters)"

    # 3. Format the Production Grade Markdown Summary Report
    report = f"# 📊 ADVANCED MULTI-ENGINE SEO AUDIT & INTELLIGENCE REPORT\n"
    report += f"**Core Seed Target**: `{seed_keyword}`\n"
    report += f"**System Assessment Clock**: {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC\n\n"
    
    report += f"## ⚔️ ALGOTHMIC COMPETITION METRICS\n"
    report += f"- **Calculated Keyword Difficulty (KD%)**: {calculated_difficulty}\n"
    report += f"- **Top Competitor On-Page Density Matrix**: `{competitor_density}`\n\n"
    
    report += "## 🎯 SEARCH INTENT CLASSIFICATION ENGINE (KEYWORD SILOS)\n"
    report += "The system mapped related variants across Google/Bing suggestions and categorized user intent profiles:\n"
    for item in keyword_silos[:10]: # Surface the top 10 most relevant nodes
        report += f"- **Keyword**: `{item['keyword']}`\n"
        report += f"  - *Intent Profile*: {item['intent']} | *Structural Type*: {item['type']}\n"
    report += "\n"

    report += "## 🔎 LIVE MULTI-ENGINE ORGANIC POSITION TRACKING\n"
    report += "Current top real-time search placements tracking the immediate front battleground:\n"
    if serp_standings:
        for match in serp_standings:
            report += f"- [**{match['engine']} Rank #{match['rank']}**] - {match['title']}\n"
            report += f"  - *Source URL Endpoint*: {match['url']}\n"
    else:
        report += "- *Zero organic platform visibility nodes returned. Verify parameters or location configuration blocks.*\n"

    # 4. Commit results output record to local directory logs
    os.makedirs("research_reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_target_path = f"research_reports/advanced_seo_audit_{timestamp}.md"
    
    with open(log_target_path, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"\n✅ Audit Finalized successfully! Clean data summary matrix committed to: {log_target_path}")

if __name__ == "__main__":
    execute_workbench_system()
    
