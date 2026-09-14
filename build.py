import os
from jinja2 import Environment, FileSystemLoader

def load_json_file(file_path):
    """Safely opens and reads a JSON file, converting it into a Python dictionary."""
    import json
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

# Global initialization of the template compilation framework
TEMPLATE_ENV = Environment(loader=FileSystemLoader('Test'))
OUTPUT_DIR = 'dist'

web = load_json_file('Json/website.json')
comp = load_json_file('Json/company.json')

GLOBAL_SITE_DATA = {"comp": comp,"web": web}




def create_output_directory():
    """Ensures the production asset destination folder exists."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def standard_pages(input_page,context,output_page):
    """Generates the primary home entry point."""
    target_file_path = os.path.join(OUTPUT_DIR, output_page)
    target_dir = os.path.dirname(target_file_path)
    if target_dir and not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    
    print("Compiling standard "+ output_page +" page...")
    template = TEMPLATE_ENV.get_template(input_page)
    combined_context = {**GLOBAL_SITE_DATA,**context}
    
    with open(target_file_path, 'w') as f:
        f.write(template.render(combined_context))

def render_standard_pages():
    """
    {
    "page": {
        "url": "https://techcraftinsights.com",
        "title": "The Future of AI: Trends to Watch",
        "desc": "An in-depth look at upcoming AI breakthroughs.",
        "vid": {"url": "https://techcraftinsights.com","w": "1920","h": "1080"},
        "img": {"url": "https://techcraftinsights.com","alt": "Abstract digital network visualization","w": "1200","h": "630"},
        "pin": {"url": "https://techcraftinsights.com","w": "1000","h": "1500"}
    },
    "type": "article",
    "author": {"handler": "@alex_dev_26},
    "card": "summary_large_image",
    "article": {
        "pub": "2026-03-15","mod": "2026-03-18",
    "author_url": "https://techcraftinsights.com",
    "about": ["Artificial Intelligence", "Web Development", "Tech Trends"]
    }
    }
    """
    STATIC_SEO = {
      "home": {
        "url":"/","is_home": true,
        "title": "Home | Hall of Documentary",
        "desc": "Explore the invisible forces shaping our world. We connect the dots between historical echoes, scientific breakthroughs, and modern geopolitics through cinematic, deep-dive investigative journalism.",
        "img": {"url": "https://techcraftinsights.com","alt": "Abstract digital network visualization","w": "1200","h": "630"},
        "pin": {"url": "https://techcraftinsights.com","w": "1000","h": "1500"}
      },
      "about": {
        "url":"/about.html","is_about": true,
        "title": "About Our Mission and Story",
        "desc": "Meet the team uncovering the hidden currents of global power, human history, and technological friction. Learn why we treat blogging like high-production documentary filmmaking.",
        "img": {"url": "https://techcraftinsights.com","alt": "Abstract digital network visualization","w": "1200","h": "630"},
        "pin": {"url": "https://techcraftinsights.com","w": "1000","h": "1500"}
      },
      "contact": {
        "url":"/contact.html","is_contact": true,
        "title": "Contact With Our Team",
        "desc": "Have a tip, a story pitch, or want to collaborate on a deep dive? Get in touch with our editorial team. Let’s map out the world’s most compelling narratives together.",
        "img": {"url": "https://techcraftinsights.com","alt": "Abstract digital network visualization","w": "1200","h": "630"},
        "pin": {"url": "https://techcraftinsights.com","w": "1000","h": "1500"}
      },
      "privacy": {
        "url":"/privacy.html","is_privacy": true,
        "title": "Privacy Policy | How We Protect Your Data",
        "desc": "Read our privacy policy to understand how we collect, protect, and use your data. Your privacy is paramount as we explore global narratives.",
        "img": {"url": "https://techcraftinsights.com","alt": "Abstract digital network visualization","w": "1200","h": "630"},
        "pin": {"url": "https://techcraftinsights.com","w": "1000","h": "1500"}
      },
      "editorial": {
        "url":"/editorial.html","is_editorial": true,
        "title": "Editorial Policy | Our Standards & Ethics",
        "desc": "Discover our rigorous editorial standards. Learn how we maintain objective, independent, and high-quality storytelling at the intersection of history, science, and global politics.",
        "img": {"url": "https://techcraftinsights.com","alt": "Abstract digital network visualization","w": "1200","h": "630"},
        "pin": {"url": "https://techcraftinsights.com","w": "1000","h": "1500"}
      },
      "terms": {
        "url":"/terms.html","is_terms": true,
        "title": "Terms of Service | User Agreement & Guidelines",
        "desc": "Review the terms of service governing your use of our platform. Read our guidelines for community conduct, intellectual property, and content usage.",
        "img": {"url": "https://techcraftinsights.com","alt": "Abstract digital network visualization","w": "1200","h": "630"},
        "pin": {"url": "https://techcraftinsights.com","w": "1000","h": "1500"}
      },
      "fact": {
        "url":"/fact.html","is_fact": true,
        "title": "Fact-Checking Policy | Our Commitment to Accuracy",
        "desc": "Accuracy is our foundational rule. Learn about our multi-layered fact-checking process, primary source verification, and how we correct errors transparently.",
        "img": {"url": "https://techcraftinsights.com","alt": "Abstract digital network visualization","w": "1200","h": "630"},
        "pin": {"url": "https://techcraftinsights.com","w": "1000","h": "1500"}
      }
    }
    standard_pages('page/index.html',{"page": STATIC_SEO["home"]},'index.html')
    standard_pages('page/about.html',{"page": STATIC_SEO["about"]},'about.html')
    standard_pages('page/contact.html',{"page": STATIC_SEO["contact"]},'contact.html')
    standard_pages('page/privacy.html',{"page": STATIC_SEO["privacy"]},'privacy.html')
    standard_pages('page/terms.html',{"page": STATIC_SEO["editorial"]},'terms.html')
    standard_pages('page/editorial.html',{"page": STATIC_SEO["terms"]},'editorial.html')
    standard_pages('page/fact.html',{"page": STATIC_SEO["fact"]},'fact.html')

def build_topic_clusters():
    TOPIC_CLUSTERS = {
      "python-web-dev": {
        "is_pillar": True,
        "filename": "python-web-development.html",
        "title": "The Ultimate Guide to Python Web Development | Pillar",
        "desc": "A comprehensive pillar resource detailing modern Python backend options, frameworks, and architecture patterns.",
        "h1": "Python Web Development Architecture",
        "intro": "Welcome to our comprehensive hub for python web development methodologies.",
        "subtopics": [
            {
                "title": "FastAPI Async Optimization Guide", 
                "filename": "python-web-development/fastapi-async-optimization.html",
                "anchor_text": "Optimize your endpoints with FastAPI Async strategies."
            },
            {
                "title": "Scaling Flask App n", 
                "filename": "python-web-development/flask-production-scaling.html",
                "anchor_text": "Discover deep horizontal scaling practices for legacy Flask codebases."
            },
            {
                "title": "Advanced Jinja2 Template Engineering", 
                "filename": "python-web-development/jinja2-advanced-templates.html",
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
            "url": f"https://github.com/pillar/{data['filename']}",
            "h1": data["h1"],
            "intro": data["intro"],
            "subtopics": data["subtopics"] # Passes all spoke links to the hub
        }
        standard_pages("page/pillar.html",{"page": pillar_context},"pillar/"+ data["filename"])
        
        # 2. Compile every Subtopic Cluster Page under this Hub
        for subtopic in data["subtopics"]:
            cluster_context = {
                "title": f"{subtopic['title']} | DevCorp Insights",
                "desc": f"Deep dive documentation on {subtopic['title']}.",
                "url": f"https://github.com/pillar/{subtopic['filename']}",
                "h1": subtopic["title"],
                
                # CRITICAL SEO: Give the spoke page complete context about its parent Pillar
                "parent_pillar": {
                    "filename": data["filename"],
                    "anchor_text": "Return to the Core Python Web Development Guide"
                }
            }
            standard_pages("page/cluster.html",{"page": cluster_context},"pillar/"+ subtopic["filename"])

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
            "url": f"https://github.com/blogs/{post['slug']}.html",
            "post_content": "<h1>" + post["title"] + "</h1><p>Deep-dive context follows...</p>"
        }
        output_filename = f"blogs/{post['slug']}.html"
        standard_pages("page/blog_post.html",{"page": post_context}, output_filename)

def generate_custom_robots():
    # 1. Define your dynamic configuration and rules data
    robots_data = {
        "base_url": "https://github.com",
        "include_sitemap": True,
        "custom_header_comment": "Production Robots Rules - Last updated: 2026",
        
        # Define rules for different web scrapers and search bots
        "user_agent_groups": [
            {
                "user_agent": "*",  # General rules for all bots
                "disallows": [
                    "/admin/",
                    "/private/checkout",
                    "/*?search=",   # Block search query parameters to prevent duplicate content
                    "/api/v1/"
                ],
                "allows": [
                    "/api/public/"  # Override to allow specific API endpoints
                ]
            },
            {
                "user_agent": "BadBotName",  # Block a specific aggressive scraper entirely
                "disallows": ["/"]
            },
            {
                "user_agent": "yandex",  # Apply a rate limit delay for specific search engines
                "disallows": ["/secret-forum/"],
                "allows": [],
                "crawl_delay": 5
            }
        ]
    }
    standard_pages('robots.txt',robots_data,'robots.txt')
    
def generate_feeds():
    from datetime import datetime, timezone
    
    # 1. Global Feed Metadata
    now = datetime.now(timezone.utc)
    site_meta = {
        "base_url": "https://example.com",
        "site_name": "My Custom Dev Blog",
        "site_description": "Exploring Python, automation, and system architecture.",
        "language": "en-us",
        "default_author": "Engineering Team",
        # Format dates according to specifications
        "build_date": now.strftime("%a, %d %b %Y %H:%M:%S GMT"),       # RSS (RFC 822)
        "build_date_atom": now.strftime("%Y-%m-%dT%H:%M:%SZ")          # Atom (ISO 8601)
    }

    # 2. Raw Content Items (Simulating a database or markdown source)
    raw_posts = [
        {
            "title": "Building Custom Crawlers Safely",
            "url": "/blog/building-crawlers",
            "content": "<p>An in-depth look at implementing rate limiting and robots parsing.</p>",
            "author": "dev-team@example.com",
            "timestamp": datetime(2026, 9, 11, 12, 0, 0, tzinfo=timezone.utc)
        },
        {
            "title": "An Intro to Semantic HTML Structure",
            "url": "/blog/semantic-html",
            "content": "<p>Why choosing the correct elements makes a massive difference for accessibility.</p>",
            "author": "seo-lead@example.com",
            "timestamp": datetime(2026, 9, 10, 15, 30, 0, tzinfo=timezone.utc)
        }
    ]

    # 3. Format item dates for each specific feed specification
    processed_items = []
    for post in raw_posts:
        processed_items.append({
            **post,
            "date_rss": post["timestamp"].strftime("%a, %d %b %Y %H:%M:%S GMT"),
            "date_atom": post["timestamp"].strftime("%Y-%m-%dT%H:%M:%SZ")
        })
    standard_pages('feed_rss.j2',{**site_meta, "items": processed_items},'feed.xml')
    standard_pages('feed_atom.j2',{**site_meta, "items": processed_items},'atom.xml')
    
def generate_sitemap():
    site_meta = {"domain": "https://example.com"}

    # Grouping items structurally
    items = {
      # Core static pages
      "static_pages": [
        {"slug": "", "changefreq": "daily", "priority": "1.0"},       # Homepage
        {"slug": "about.html", "changefreq": "monthly", "priority": "0.5"},
        {"slug": "contact.html", "changefreq": "monthly", "priority": "0.5"},
        {"slug": "privacy.html", "changefreq": "yearly", "priority": "0.3"},
      ],
      # Topic Clusters (Pillar pages and their sub-pages)
      "topic_clusters": [
        {
            "pillar_slug": "pillar/artificial-intelligence", # Main Hub/Pillar
            "updated_at": "2026-09-10",
            "priority": "0.8",
            "sub_topics": [                                  # Cluster Content
                {"slug": "pillar/artificial-intelligence/machine-learning-basics.html", "updated_at": "2026-09-11"},
                {"slug": "pillar/artificial-intelligence/natural-language-processing.html", "updated_at": "2026-09-05"},
            ]
        },
        {
            "pillar_slug": "pillar/web-development",          # Another Pillar
            "updated_at": "2026-08-20",
            "priority": "0.8",
            "sub_topics": [
                {"slug": "pillar/web-development/learning-django.html", "updated_at": "2026-08-25"},
            ]
        }
      ],
     "posts": [
                {"slug": "blog/machine-learning-basics.html", "updated_at": "2026-09-11"},     # Flat URL
                {"slug": "blog/natural-language-processing.html", "updated_at": "2026-09-05"}, # Flat URL
      ]
    }

    # Pass everything into your single payload variable
    standard_pages('sitemap.j2',{**site_meta, "items": items},'sitemap.xml')
    
def error_page():
        standard_pages('404.html',{},'404.html')
   
            
def main():
    """Central orchestration routine running within the GitHub Runner context."""
    print(" Initializing modular build execution loop...")
    create_output_directory()
    
    # Sequential execution of dedicated page compilers
    # its working 
    render_standard_pages()
    # build_topic_clusters()
    # build_flat_blog()
    generate_custom_robots()
    generate_feeds()
    generate_sitemap()
    error_page()
    print(" Static compilation complete! All files generated in /dist directory.")

if __name__ == "__main__":
    main()
