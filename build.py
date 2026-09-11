import os
from jinja2 import Environment, FileSystemLoader

# Global initialization of the template compilation framework
TEMPLATE_ENV = Environment(loader=FileSystemLoader('Test'))
OUTPUT_DIR = 'dist'
GLOBAL_SITE_DATA ={"site_name": "MyAgency Digital"}

def create_output_directory():
    """Ensures the production asset destination folder exists."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def standard_pages(input_page,context,output_page):
    """Generates the primary home entry point."""
    # 1. Compute the full, absolute target file path
    target_file_path = os.path.join(OUTPUT_DIR, output_page)
    
    # 2. Extract just the directory component (e.g., 'dist/blogs/fastapi-seo-optimization')
    target_dir = os.path.dirname(target_file_path)
    
    # 3. Automatically create the directory stack if missing
    if target_dir and not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)


    
    print("Compiling standard "+ output_page +" page...")
    template = TEMPLATE_ENV.get_template(input_page)
    combined_context = {**GLOBAL_SITE_DATA, **context}

    with open(target_file_path, 'w') as f:
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
      "policy": {
        "url":"https://www.github.com/privacy",
        "title": "Privacy Policy",
        "desc": "Read how we securely handle user interactions, cookie analytics, and data encryption to stay fully GDPR compliant."
      }
    }
    standard_pages('index.html',STATIC_SEO["home"],'index.html')
    standard_pages('about.html',STATIC_SEO["about"],'about.html')
    standard_pages('contact.html',STATIC_SEO["contact"],'contact.html')
    standard_pages('policy.html',STATIC_SEO["policy"],'policy.html')

def build_topic_clusters():
    TOPIC_CLUSTERS = {
      "python-web-dev": {
        "is_pillar": True,
        "filename": "python-web-development",
        "title": "The Ultimate Guide to Python Web Development | Pillar",
        "desc": "A comprehensive pillar resource detailing modern Python backend options, frameworks, and architecture patterns.",
        "h1": "Python Web Development Architecture",
        "intro": "Welcome to our comprehensive hub for python web development methodologies.",
        "subtopics": [
            {
                "title": "FastAPI Async Optimization Guide", 
                "filename": "fastapi-async-optimization",
                "anchor_text": "Optimize your endpoints with FastAPI Async strategies."
            },
            {
                "title": "Scaling Flask Apps in Production", 
                "filename": "flask-production-scaling",
                "anchor_text": "Discover deep horizontal scaling practices for legacy Flask codebases."
            },
            {
                "title": "Advanced Jinja2 Template Engineering", 
                "filename": "jinja2-advanced-templates",
                "anchor_text": "Master modular layouts and SEO component caching with Jinja2."
            }
        ]
      }
    }
    for cluster_id, data in TOPIC_CLUSTERS.items():
        # 1. Compile the Main Pillar Page
        pillar_context = {
            "title": data["title"],
            "desc": data["desc"],
            "url": f"https://github.com/{data['filename']}",
            "h1": data["h1"],
            "intro": data["intro"],
            "subtopics": data["subtopics"] # Passes all spoke links to the hub
        }
        standard_pages("pillar.html", pillar_context, data["filename"]+"/index.html")
        
        # 2. Compile every Subtopic Cluster Page under this Hub
        for subtopic in data["subtopics"]:
            cluster_context = {
                "title": f"{subtopic['title']} | DevCorp Insights",
                "desc": f"Deep dive documentation on {subtopic['title']}.",
                "url": f"https://github.com/{subtopic['filename']}",
                "h1": subtopic["title"],
                
                # CRITICAL SEO: Give the spoke page complete context about its parent Pillar
                "parent_pillar": {
                    "filename": data["filename"],
                    "anchor_text": "Return to the Core Python Web Development Guide"
                }
            }
            standard_pages("cluster.html", cluster_context, subtopic["filename"]+"/index.html")

def build_flat_blog():
    BLOG_POSTS = [
    {
        "slug": "fastapi-seo-optimization", # Flat url will be /fastapi-seo-optimization
        "title": "Optimizing FastAPI Apps for Search Visibility",
        "desc": "A complete architectural breakdown of async speed and flat URL routing configuration."
    },
    {
        "slug": "jinja2-template-inheritance-tricks",
        "title": "Advanced Jinja2 Architecture Snippets",
        "desc": "Master layouts, functional macros, and schema parameters within static compilations."
    }
    ]
    for post in BLOG_POSTS:
        post_context = {
            "title": post["title"],
            "desc": post["desc"],
            # Clean flat URL definition
            "url": f"https://github.com/blogs/{post['slug']}/index.html",
            "post_content": "<h1>" + post["title"] + "</h1><p>Deep-dive context follows...</p>"
        }
        
        # Output directly into OUTPUT_DIR root as 'slug.html'
        # Nginx/Apache configurations can serve this smoothly without showing the '.html' extension
        output_filename = f"blogs/{post['slug']}/index.html"
        standard_pages("blog_post.html", post_context, output_filename)


def main():
    """Central orchestration routine running within the GitHub Runner context."""
    print(" Initializing modular build execution loop...")
    create_output_directory()
    
    # Sequential execution of dedicated page compilers
    
    render_standard_pages()
    # Execute the builder
    # errored build_topic_clusters()
    build_flat_blog()

    print(" Static compilation complete! All files generated in /dist directory.")

if __name__ == "__main__":
    main()
