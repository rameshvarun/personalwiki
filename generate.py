import os
import re
import markdown
import jinja2
import json
import argparse

class LinkExtension(markdown.Extension):
  def __init__(self):
    pass
  def extendMarkdown(self, md, md_globals):
    self.md = md

    # append to end of inline patterns
    LINK_RE = r'\[\[(.+?)\]\]'
    linkPattern = LinkPattern(LINK_RE)
    linkPattern.md = md
    md.inlinePatterns.add('links', linkPattern, "<not_strong")

class LinkPattern(markdown.inlinepatterns.Pattern):
    def __init__(self, pattern):
      super(LinkPattern, self).__init__(pattern)

    def handleMatch(self, m):
      words = m.group(2).split("|")
      if len(words) == 2:
        a = markdown.util.etree.Element('a')
        a.text = words[0].strip()

        link_parts = words[1].strip().split("#")

        url = link_parts[0] + ".html"
        if len(link_parts) > 1:
          url += "#" + link_parts[1].lower()

        a.set('href', url)
      else:
          a = ''
      return a

if __name__ == "__main__":
  # Command-line arguments
  parser = argparse.ArgumentParser(description="Generate a static site that can be uploaded to the server.")
  parser.add_argument("-i", "--inputdir", help="Directory from which to read input files.", type=str, required=True)
  parser.add_argument("-o", "--outputdir", help="Directory to place generated site.", type=str, required=True)
  args = parser.parse_args()

  # Load templates (One for a page, and one for the index)
  template_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
  page_template = template_env.get_template('page.html')
  index_template = template_env.get_template('index.html')

  # Markdown processor with extensions
  md = markdown.Markdown(extensions=['toc', 'meta', 'codehilite', 'extra', LinkExtension(), 'headerid'])

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
      markdown = output,
      tags = articles[id]['tags']
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
