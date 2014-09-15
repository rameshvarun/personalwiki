import os
import re
import markdown
import jinja2
import json
import argparse
import errno
import shutil

from extensions import LinkExtension

if __name__ == "__main__":
  # Command-line arguments
  parser = argparse.ArgumentParser(description="Generate a static site that can be uploaded to the server.")
  parser.add_argument("-i", "--inputdir", help="Directory from which to read input files.", type=str, required=True)
  parser.add_argument("-o", "--outputdir", help="Directory to place generated site.", type=str, required=True)
  parser.add_argument("-r", "--root", help="Path to the root of the wiki.", type=str, required=True)
  args = parser.parse_args()

  # Load templates (One for a page, and one for the index)
  template_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
  page_template = template_env.get_template('page.html')
  index_template = template_env.get_template('index.html')

  # Markdown processor with extensions
  md = markdown.Markdown(extensions=['toc', 'meta', 'codehilite', 'extra', LinkExtension(), 'headerid', 'linkify'])

  articles = {}

  files = []
  assets = []
  def scan_dir(dir):
    for path in os.listdir(dir):
      file_path = os.path.join(dir, path)
      if os.path.isfile(file_path):
        if path[len(path) - 3:] == ".md":
          files.append(file_path)
        else:
          assets.append(file_path)
      elif os.path.isdir(file_path):
        scan_dir(file_path)


  scan_dir(args.inputdir)

  for filename in files:
    relpath = os.path.relpath(filename, args.inputdir)

    id = os.path.splitext(relpath)[0]
    input = open(os.path.join(args.inputdir, relpath)).read()
    output = md.convert(input)

    articles[id] = {
      "title" : md.Meta['title'][0] if 'title' in md.Meta and len(md.Meta['title']) > 0 else "",
      "tags" : md.Meta['tags'] if 'tags' in md.Meta else [],
      "body" : output,
      "id" : id,
      "description" : " ".join(md.Meta['description']) if 'description' in md.Meta else ""
    }

    out_filename = os.path.join( args.outputdir, os.path.splitext(relpath)[0] + ".html" )

    # Ensure that the directories exist to make this file
    try:
      os.makedirs(os.path.dirname(out_filename))
    except OSError as exc:
      if exc.errno == errno.EEXIST:
          pass

    out_file = open(out_filename, "w")
    out_file.write(page_template.render(
      markdown = output,
      tags = articles[id]['tags'],
      path_to_root = args.root
    ))
    out_file.close()

  # Copy over assets
  for asset in assets:
    relpath = os.path.relpath(asset, args.inputdir)
    out_filename = os.path.join( args.outputdir, relpath)
    shutil.copyfile(asset, out_filename)

  index_file = open( os.path.join(args.outputdir,  "index.json") , "w")
  index_file.write(json.dumps(articles, indent=4))
  index_file.close()

  index_html = open( os.path.join(args.outputdir,  "index.html") , "w")
  index_html.write(index_template.render(
    articles = articles.values()
  ))
  index_html.close()
