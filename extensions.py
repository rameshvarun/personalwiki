import markdown
from markdown.inlinepatterns import Pattern

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
