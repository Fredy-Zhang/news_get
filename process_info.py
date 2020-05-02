#  Merge the source code
import os
data_folder = "Data/websites/raw/"
filenames = [os.path.join(data_folder, filename)
            for filename in os.listdir(data_folder)]

text_output_folder = "Data/websites/textonly/"
os.system("mkdir -p Data/websites/textonly/")

from lxml.html import parse, submit_form
from lxml import etree

skip_node_types = ["script", "head", "style", etree.Comment]

def get_text_from_file(filename):
    with open(filename) as inf:
        html_tree = parse(inf)
    return get_text_from_node(html_tree.getroot())

def get_text_from_node(node):
    if len(node) == 0:
        if node.text and len(node.text) > 100:
            return node.text
        else:
            return " "
    results = (get_text_from_node(child) for child in node 
               if child.tag not in skip_node_types)
    return "\n".join(r for r in results if len(r) > 1)

num = 0
for filename in os.listdir(data_folder):
    text = get_text_from_file(os.path.join(data_folder, filename))
    print("No. ", num, "   ", filename)
    num += 1
    with open(os.path.join(text_output_folder, filename), "w") as outf:
        outf.write(text)
