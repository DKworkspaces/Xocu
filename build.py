import os
from jinja2 import Environment, FileSystemLoader

# Global initialization of the template compilation framework
TEMPLATE_ENV = Environment(loader=FileSystemLoader('Test'))
OUTPUT_DIR = 'dist'

def create_output_directory():
    """Ensures the production asset destination folder exists."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def standard_pages(input_page,context,output_page):
    """Generates the primary home entry point."""
    GLOBAL_SITE_DATA ={"site_name": "MyAgency Digital"}
    
    print("Compiling standard "+ output_page +" page...")
    template = TEMPLATE_ENV.get_template(input_page)
    combined_context = {**GLOBAL_SITE_DATA, **context}

    with open(os.path.join(OUTPUT_DIR, output_page), 'w') as f:
        f.write(template.render(combined_context))

def render_standard_pages():
    STATIC_SEO = {
    "home": {
        "url":"https://www.github.com",
        "title": "Expert Python Web Development Services",
        "desc": "Scale your business with high-performance Python web applications. We specialize in Flask, FastAPI, and custom SEO architectures."
    },
    "about": {
        "url":"https://www.github.com/about",
        "title": "About Us",
        "desc": "Meet the engineering team building sustainable, lightning-fast digital solutions for modern businesses globally."
    },
    "contact": {
        "url":"https://www.github.com/contact",
        "title": "Contact Our Engineering Team",
        "desc": "Get a free technical consultation. Drop us a line regarding your next backend application or custom automation project."
    },
    "privacy": {
        "url":"https://www.github.com/privacy",
        "title": "Privacy Policy",
        "desc": "Read how we securely handle user interactions, cookie analytics, and data encryption to stay fully GDPR compliant."
    }
    }

    
    standard_pages('index.html',STATIC_SEO["home"],'index.html')
    standard_pages('about.html',STATIC_SEO["about"],'about.html')
    standard_pages('contact.html',STATIC_SEO["contact"],'contact.html')
    standard_pages('privacy.html',STATIC_SEO["privacy"],'privacy.html')



def main():
    """Central orchestration routine running within the GitHub Runner context."""
    print(" Initializing modular build execution loop...")
    create_output_directory()
    
    # Sequential execution of dedicated page compilers
    
    render_standard_pages()
    
    print(" Static compilation complete! All files generated in /dist directory.")

if __name__ == "__main__":
    main()
