import os
import re
import markdown
import jinja2
import json
import argparse

IN_DIR = os.getcwd() + "/Input/"
OUT_DIR = "Output/"

template_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'Templates')))
page_template = template_env.get_template('page.html')

index = {}

files = []
for path in os.listdir(IN_DIR):
  if os.path.isfile(IN_DIR + path) and path[len(path) - 3:] == ".md":
    files.append(path)

for filename in files:
  id = os.path.splitext(filename)[0]
  input = open(IN_DIR + filename).read()
  output = markdown.markdown(input, extensions=['toc'])

  index[id] = input

  out_filename = OUT_DIR + os.path.splitext(filename)[0] + ".html"
  out_file = open(out_filename, "w")
  out_file.write(page_template.render(
    markdown = output
  ))
  out_file.close()

index_file = open(OUT_DIR + "index.json", "w")
index_file.write(json.dumps(index))
index_file.close()
