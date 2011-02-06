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

# TODO: some 30 mote templates
templates = {
    "body" : Templite("""
    <!DOCTYPE html 
         PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
         "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
    <html xmlns='http://www.w3.org/1999/xhtml'> 
    <head></head><body>${print text}$${print children2html(tag)}$</h1></body></html>
    """),
    
    "title" : Templite("<h1>${print text}$${print children2html(tag)}$</h1>"),
    
    "p" : Templite("""<p>${print text}$${print children2html(tag)}$</p>"""),
    
    "image": Templite("""<img src="${print tag.attrib["{http://www.w3.org/1999/xlink}href"][1:]}$"/>"""),
    
    "strong": Templite("""<b>${print text}$${print children2html(tag)}$</b>"""),
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

        # Handle binary tags
        binelems = doc.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}binary')
        self.binaries = {}
        for b in binelems:
            print b.attrib['id']
            self.binaries[b.attrib['id']] = b.text.decode('base64')
        
        # The description element contains metadata
        description = doc.find('{http://www.gribuser.ru/xml/fictionbook/2.0}description')
        
        # Cover page
        coverpage=description.findall('.//{http://www.gribuser.ru/xml/fictionbook/2.0}coverpage')
        if coverpage:
            print "LINK:", coverpage[0][0].attrib["{http://www.w3.org/1999/xlink}href"][1:]
            self.coverpage=tag2html(coverpage[0])
            open("cover.html","w+").write(self.coverpage)

        
        
        # The body element contains the book proper
        body = doc.find('{http://www.gribuser.ru/xml/fictionbook/2.0}body')
        self.html = tag2html(body)
        
        #TODO: create TOC
        self.tocentries = ["Cover","Book"]

    def getData(self, path):
        """Return the contents of a file in the binary tags of the document, or the document itself for Book"""
        print "PATH:", path
        if path == "Book":
            return self.html.encode('utf-8')
        elif path == "Cover":
            return self.coverpage.encode('utf-8')        
        elif path in self.binaries:
            return self.binaries[path]
            
        print "Requested unkown path:", path
        return "Missing"

def main(fname):
    doc = FB2Document(sys.argv[1])

if __name__ == "__main__":
    main(sys.argv[1])
