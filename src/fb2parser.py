import sys, os, codecs
from templite import Templite
import pdb

try:
    from elementtree.ElementTree import XML
except:
    from xml.etree.ElementTree import XML

# These are templates indexed by tag name.
# So, for example, when we find a "title" tag,
# the template should figure out how to produce correct
# html from it.

templates = {

    "title" : Templite("<h1>${print text}$${print children2html(tag)}$</h1>"),
    "p" : Templite("""<p>${print text}$${print children2html(tag)}$</p>"""),
}
    
def tag2html(tag):
    tpl = Templite("${print text}$${print children2html(tag)}$")
    if "}" in tag.tag:
        tagname = tag.tag.split("}")[1]
    else:
        tagname = tag.tag
    if tag.text:
        text=tag.text
    else:
        text = ""
    tpl = templates.get(tagname, tpl)
    rendered = tpl.render(tag=tag, text=text, children2html=children2html,tag2html=tag2html)
    return rendered
    
def children2html(tag):
    children = tag.getchildren
    if children:
        html=[]
        for c in tag.getchildren():
            t=tag2html(c)+ (c.tail or "")
            html.append(t)
        return "\n".join(html)
    else:
        return tag.text
    
class FB2Document(object):
    """A class that parses and provides
    data about an FictionBook file"""

    def __init__(self, fname):
        # Will traverse the tree and try to generate HTML from all nodes
        f = open(fname,'r')
        data = f.read()
        doc = XML(data)
        f.close()
        
        #TODO: stylesheet, description, binary

        # The body element contains the book proper
        body = doc.find('{http://www.gribuser.ru/xml/fictionbook/2.0}body')
        self.html = tag2html(body)
        
    def getData(self, path):
        """Return the contents of a file in the binary tags of the document"""
        pass

def main(fname):
    doc = FB2Document(sys.argv[1])

if __name__ == "__main__":
    main(sys.argv[1])
