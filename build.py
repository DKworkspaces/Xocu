import os
from jinja2 import Environment, FileSystemLoader

# Global initialization of the template compilation framework
TEMPLATE_ENV = Environment(loader=FileSystemLoader('Test'))
OUTPUT_DIR = 'dist'

def create_output_directory():
    """Ensures the production asset destination folder exists."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def render_home_page():
    """Generates the primary home entry point."""
    print("Compiling Home page...")
    template = TEMPLATE_ENV.get_template('index.html')
    context = {
        "title": "Welcome to AdminEngine",
        "hero_text": "Next-generation static site management infrastructure built with Python."
    }
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w') as f:
        f.write(template.render(context))

def render_standard_pages():
    """Loops through and renders standard informational layouts (About, Contact, Privacy)."""
    print("Compiling Standard operational pages...")
    template = TEMPLATE_ENV.get_template('about.html')
    
    pages = [
        {
            "filename": "about.html",
            "title": "About Our Enterprise",
            "content": "<p>We engineer flat-file architectures that compile rapidly, eliminate server runtime bugs, and scale securely through global distributions.</p>"
        },
        {
            "filename": "contact.html",
            "title": "Contact Engineering Support",
            "content": "<p>For framework issues, connect directly with our network engineers at <code>sysops@example.com</code>.</p>"
        },
        {
            "filename": "privacy.html",
            "title": "Privacy & Compliance Policy",
            "content": "<p>This is a zero-tracking workspace. We enforce local storage protection and inject absolutely no third-party analytic trackers.</p>"
        }
    ]
    
    for page in pages:
        with open(os.path.join(OUTPUT_DIR, page['filename']), 'w') as f:
            f.write(template.render(title=page['title'], content=page['content']))

def render_seo_hub_and_clusters():
    """Handles parsing and structural cross-linking for the Pillar and Cluster network."""
    print(" Compiling SEO Pillar Hub and associated cluster sub-pages...")
    
    # Raw database array mock for cluster pages
    cluster_dataset = [
        {
            "filename": "cluster-actions-automation.html",
            "title": "GitHub Actions Build Automation",
            "description": "Unlocking parallel workflow execution pipelines for rapid edge deployments.",
            "content": "<p>Continuous integration runners compile template targets into production assets in seconds, pushing immediate deployments directly onto global servers.</p>"
        },
        {
            "filename": "cluster-jinja-speed.html",
            "title": "Optimizing Jinja Rendering Engine",
            "description": "How to fine-tune compilation parameters for instantaneous pipeline generation.",
            "content": "<p>By using isolated string buffering and pre-compiling inherited layout files, Python handles rendering loops fast enough to process hundreds of pages in milliseconds.</p>"
        }
    ]
    
    # 1. Render the central, high-level Pillar Hub Page
    pillar_template = TEMPLATE_ENV.get_template('pillar.html')
    with open(os.path.join(OUTPUT_DIR, 'pillar.html'), 'w') as f:
        f.write(pillar_template.render(title="Core Architecture Blueprint (Pillar Hub)", clusters=cluster_dataset))
        
    # 2. Render individual detailed sub-pages (Cluster/Blogpost layout)
    cluster_template = TEMPLATE_ENV.get_template('cluster.html')
    for post in cluster_dataset:
        with open(os.path.join(OUTPUT_DIR, post['filename']), 'w') as f:
            f.write(cluster_template.render(title=post['title'], content=post['content']))

def main():
    """Central orchestration routine running within the GitHub Runner context."""
    print(" Initializing modular build execution loop...")
    create_output_directory()
    
    # Sequential execution of dedicated page compilers
    render_home_page()
    render_standard_pages()
    render_seo_hub_and_clusters()
    
    print(" Static compilation complete! All files generated in /dist directory.")

if __name__ == "__main__":
    main()
