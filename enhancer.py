import os
import sys
import re
import requests

def clean_ai_output(raw_text):
    """Removes thinking blocks and clean markdown wraps from the response payload."""
    clean_text = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL)
    for marker in ["```html", "```css", "```javascript", "```js", "```"]:
        if clean_text.strip().startswith(marker):
            clean_text = clean_text.split(marker, 1)[1]
        if clean_text.strip().endswith("```"):
            clean_text = clean_text.rsplit("```", 1)[0]
    return clean_text.strip()

def main():
    src_dir = "src"
    dist_dir = "dist"
    
    html_path = os.path.join(src_dir, "index.html")
    css_path = os.path.join(src_dir, "styles.css")
    js_path = os.path.join(src_dir, "script.js")
    
    if not os.path.exists(html_path):
        print(f"❌ Error: Source 'index.html' missing inside '{src_dir}/' folder.")
        sys.exit(1)
        
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read().strip()
        
    css_content = open(css_path, "r", encoding="utf-8").read().strip() if os.path.exists(css_path) else ""
    js_content = open(js_path, "r", encoding="utf-8").read().strip() if os.path.exists(js_path) else ""

    system_instruction = (
        "You are an expert Frontend Architect. Combine the provided HTML, CSS, and JS components "
        "into a single highly optimized, clean production webpage code block.\n\n"
        "STRICT CONSTRAINTS:\n"
        "1. FILE SIZE: Minimize formatting space. Inline CSS inside a <style> block and JS inside a <script> block.\n"
        "2. COMMENTS: Limit all comments strictly to 2-3 sentences max per block.\n"
        "3. JS ONE-LINERS: Refactor simple functions and selectors to ES6 arrow function one-liners.\n"
        "4. BROWSER COMPATIBILITY: Restrict syntax to 2017+ browser standards. Do not output modern properties "
        "like optional chaining (?.) or nullish coalescing (??) that cause syntax crashes on old engines.\n\n"
        "Output ONLY raw complete HTML code structure. Do not use markdown wraps."
    )
    
    user_prompt = (
        f"Optimize and bundle these code assets:\n\n"
        f"--- RAW HTML ---\n{html_content}\n\n"
        f"--- RAW CSS ---\n{css_content}\n\n"
        f"--- RAW JS ---\n{js_content}"
    )

    payload = {
        "model": "qwen2.5-coder:1.5b-instruct",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ],
        "options": {
            "temperature": 0.1
        },
        "stream": False
    }

    try:
        print("⚡ Sending components to internal virtual machine model instance...")
        response = requests.post("http://localhost:11434/api/chat", json=payload, timeout=180)
        response.raise_for_status()
        
        raw_text = response.json()["message"]["content"]
        enhanced_code = clean_ai_output(raw_text)
        
        if "<html" in enhanced_code.lower() or "<!doctype" in enhanced_code.lower():
            os.makedirs(dist_dir, exist_ok=True)
            output_file = os.path.join(dist_dir, "index.html")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(enhanced_code)
            print(f"✅ Success! Enhanced bundle built perfectly inside: {output_file}")
        else:
            print("❌ Failure: AI generated file was missing critical markup tags. Preserving original code.")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
  
