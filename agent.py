import os
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def generate_with_model(model, tokenizer, system_instruction, user_prompt, max_tokens=3072):
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_prompt}
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    # Low temperature guarantees precise code refactoring without unintended feature modifications
    generated_ids = model.generate(**model_inputs, max_new_tokens=max_tokens, temperature=0.1)
    generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
    
    output = tokenizer.batch_decode(generated_ids, skip_special_tokens=True).strip()
    
    for marker in ["```html", "```"]:
        if output.startswith(marker):
            output = output.split(marker, 1)
        if output.endswith("```"):
            output = output.rsplit("```", 1)
    return output.strip()

def main():
    target_page = "dist/index.html"
    
    if not os.path.exists(target_page):
        print(f"❌ Error: Target file '{target_page}' not found.")
        sys.exit(1)
        
    with open(target_page, "r", encoding="utf-8") as f:
        existing_code = f.read().strip()
        
    print(f"🔍 Optimizing asset: {target_page}")
    print("⚙️ Initializing local optimization engine...")
    
    model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto")

    # SYSTEM INSTRUCTIONS: Enforcing size constraints, comment limits, and browser compatibility rules
    refactor_system = (
        "You are an expert Frontend Architect and Web Optimization Agent. Your sole task is to refactor "
        "and clean the provided HTML, CSS, and JavaScript code according to strict engineering constraints.\n\n"
        "STRICT CONSTRAINTS:\n"
        "1. FILE SIZE REDUCTION: Remove duplicate Tailwind utility classes, combine inline styles where possible, "
        "and prune redundant HTML nodes to ensure the smallest possible file footprint.\n"
        "2. COMMENT LIMITS: Total file comments must be kept strictly minimal. Any code comment block must "
        "be limited to exactly 2 to 3 sentences maximum.\n"
        "3. JAVASCRIPT ONE-LINERS: Refactor internal logic blocks, array filters, map states, and event listeners "
        "into concise, single-line executions (e.g., arrow functions and ternary operator chains) wherever practical.\n"
        "4. BROWSER COMPATIBILITY (2017+): All CSS and JavaScript properties must be fully compatible with 2017 "
        "browser standards (Chrome 60+, Safari 11+, Firefox 55+). You may use ES6 syntax (const/let, arrow functions, "
        "template literals), but DO NOT use ultra-modern features (like optional chaining '?.', logical assignment '||=', "
        "or native top-level await). Do not include any legacy Internet Explorer styling extensions.\n\n"
        "Output ONLY the fully modified, production-ready, complete raw HTML code. Do not include markdown "
        "wrappers, backticks, or extra conversational text."
    )
    
    refactor_prompt = (
        f"Analyze this raw code block and return an optimized version matching all target constraints:\n\n"
        f"{existing_code}"
    )

    print("⚡ Compressing layout arrays and updating code execution syntax...")
    improved_code = generate_with_model(model, tokenizer, refactor_system, refactor_prompt)

    if "<html" in improved_code or "<!DOCTYPE" in improved_code:
        with open(target_page, "w", encoding="utf-8") as f:
            f.write(improved_code)
        print(f"✅ Production code refactored and updated: {target_page}")
    else:
        print("⚠️ Warning: Output validation failed. Aborting to safeguard original file contents.")

if __name__ == "__main__":
    main()
                             
