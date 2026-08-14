import json
from jinja2 import Environment, FileSystemLoader

def build_bio():
    # Load profile data from the JSON file
    with open('data.json', 'r', encoding='utf-8') as json_file:
        user_data = json.load(json_file)
    
    # Set up Jinja2 environment and load the template
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('bio.html')
    
    # Render template with JSON data
    output_html = template.render(user_data)
    
    # Save directly to index.html for GitHub Pages compatibility
    with open('index.html', 'w', encoding='utf-8') as output_file:
        output_file.write(output_html)
        
    print("✨ Successfully generated index.html from data.json!")

if __name__ == "__main__":
    build_bio()
