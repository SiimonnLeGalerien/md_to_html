import sys
import os
import shutil
from parser import extract_title, markdown_to_html_node

def copy_dir(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    dirs = os.listdir(src)
    for dir in dirs:
        if os.path.isfile(src+"/"+dir):
            shutil.copy(src+"/"+dir, dst+"/"+dir)
        else:
            os.mkdir(dst+"/"+dir)
            copy_dir(src+"/"+dir, dst+"/"+dir)

def generate_page(from_path, template_path, dest_path, basepath):
    print("Generating page from " + from_path + " to " + dest_path + " using " + template_path)
    markdown = None
    template = None
    with open(from_path) as md:
        markdown = md.read()
    with open(template_path) as tmp:
        template = tmp.read()
    template = template.replace("{{ Title  }}", extract_title(markdown))
    template = template.replace("{{ Content }}", markdown_to_html_node(markdown).to_html())
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dirs = os.listdir(dir_path_content)
    for dir in dirs:
        if os.path.isfile(dir_path_content+"/"+dir):
            generate_page(dir_path_content+"/"+dir, template_path, dest_dir_path+"/"+dir.replace(".md", ".html"), basepath)
        else:
            generate_pages_recursive(dir_path_content+"/"+dir, template_path, dest_dir_path+"/"+dir, basepath)

def main():
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    copy_dir("static", "docs")
    if sys.argv[1] is None:
        generate_pages_recursive("content", "template.html", "docs", "/")
    else:
        generate_pages_recursive("content", "template.html", "docs", sys.argv[1])
main()
