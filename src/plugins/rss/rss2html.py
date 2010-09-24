import os, sys, codecs
from feedparser import parse
from templite import Templite

f = codecs.open('feed.tmpl', 'r', 'utf-8')
feedtmpl = Templite(f.read())
f.close()

f = codecs.open('post.tmpl', 'r', 'utf-8')
posttmpl = Templite(f.read())
f.close()

data = parse(sys.argv[1])

f=codecs.open(os.path.join('trss','out.html'),'w+','utf-8')
f.write(feedtmpl.render(feed=data.feed, posts = data.entries))
f.close()

for i, post in enumerate(data.entries):
    f=codecs.open(os.path.join('trss','%s.html'%i),'w+','utf-8')
    f.write(posttmpl.render(post = post))
    f.close()
    
    