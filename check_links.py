import os
import re
from urllib.parse import urlparse

def check_project():
    broken_links = []
    base_dir = '/home/digriz/projects/content-layout'
    
    # Regex to find href and src
    link_pattern = re.compile(r'<(?:link|a)[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    img_pattern = re.compile(r'<img[^>]+src=["\'](.*?)["\']', re.IGNORECASE)
    
    for root, dirs, files in os.walk(base_dir):
        # Skip node_modules or similar if they exist
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            if not file.endswith('.html'):
                continue
                
            file_path = os.path.join(root, file)
            rel_file_path = os.path.relpath(file_path, base_dir)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    content = f.read()
                except UnicodeDecodeError:
                    continue
            
            # Find all links
            hrefs = link_pattern.findall(content)
            srcs = img_pattern.findall(content)
            
            # Check all links
            for link in hrefs + srcs:
                # Ignore external, empty, or anchor-only links
                if not link or link.startswith(('http://', 'https://', 'mailto:', 'tel:', '//', '#')):
                    continue
                
                # If there's an anchor in the link, strip it for file existence check
                path_part = link.split('#')[0]
                
                if not path_part: # Link was just an anchor like index.html#foo but wait, we stripped '#', what if it's 'index.html#foo'? path_part is 'index.html'
                    continue
                
                # Resolve relative path
                target_path = os.path.normpath(os.path.join(root, path_part))
                
                if not os.path.exists(target_path):
                    broken_links.append((rel_file_path, link, target_path))

    if broken_links:
        print("Broken links found:")
        for source, link, target in broken_links:
            print(f"File: {source}")
            print(f"  Link: {link}")
            print(f"  Missing: {os.path.relpath(target, base_dir)}")
            print("-" * 40)
    else:
        print("All internal links and images are working perfectly!")

if __name__ == '__main__':
    check_project()
