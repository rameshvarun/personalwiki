import os
import re
import markdown
import jinja2
import json
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Generate a static site that can be uploaded to the server.")
  parser.add_argument("-i", "--inputdir", help="Directory from which to read input files.", type=str, required=True)
  parser.add_argument("-o", "--outputdir", help="Directory to place generated site.", type=str, required=True)
  args = parser.parse_args()

  template_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
  page_template = template_env.get_template('page.html')
  index_template = template_env.get_template('index.html')

  # Markdown processor with extensions
  md = markdown.Markdown(extensions=['toc', 'meta', 'codehilite', 'extra'])

  articles = {}

  files = []
  for path in os.listdir(args.inputdir):
    if os.path.isfile(os.path.join(args.inputdir, path)) and path[len(path) - 3:] == ".md":
      files.append(path)

  for filename in files:
    id = os.path.splitext(filename)[0]
    input = open(os.path.join(args.inputdir, filename)).read()
    output = md.convert(input)

    articles[id] = {
      "title" : md.Meta['title'][0] if 'title' in md.Meta and len(md.Meta['title']) > 0 else "",
      "tags" : md.Meta['tags'] if 'tags' in md.Meta else [],
      "body" : output,
      "id" : id,
      "description" : " ".join(md.Meta['description']) if 'description' in md.Meta else ""
    }

    out_filename = os.path.join( args.outputdir, os.path.splitext(filename)[0] + ".html" )
    out_file = open(out_filename, "w")
    out_file.write(page_template.render(
      markdown = output
    ))
    out_file.close()

  index_file = open( os.path.join(args.outputdir,  "index.json") , "w")
  index_file.write(json.dumps(articles, indent=4))
  index_file.close()

  index_html = open( os.path.join(args.outputdir,  "index.html") , "w")
  index_html.write(index_template.render(
    articles = articles.values()
  ))
  index_html.close()
