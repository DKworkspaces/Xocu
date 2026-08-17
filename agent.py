import os
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def main():
    user_prompt = os.environ.get("USER_PROMPT", "A premium minimalist luxury portfolio landing page")
    
    print(f"🚀 Initializing completely open-source model: Qwen/Qwen2.5-Coder-1.5B-Instruct")
    model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto"
        )
        
        system_instruction = (
            "You are an elite frontend developer. Output a single, production-ready HTML file. "
            "Use Tailwind CSS via CDN for styling. Create clean modern layouts. "
            "Provide ONLY the raw HTML code without markdown styling blocks, without ```html markers, "
            "and without any extra conversational explanation."
        )
        
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ]
        
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
        
        print("⚡ Executing local compilation block...")
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=2048,
            temperature=0.3
        )
        
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        
        html_code = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        
        if html_code.startswith("```html"):
            html_code = html_code.split("```html", 1)[1]
        elif html_code.startswith("```"):
            html_code = html_code.split("```", 1)[1]
            
        if html_code.endswith("```"):
            html_code = html_code.rsplit("```", 1)[0]
            
        html_code = html_code.strip()

        os.makedirs("dist", exist_ok=True)
        output_path = os.path.join("dist", "index.html")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_code)
            
        print(f"✅ Successfully compiled raw deployment file to dist/index.html")
        
    except Exception as e:
        print(f"❌ Automation pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
