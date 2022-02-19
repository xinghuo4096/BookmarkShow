
import codecs
 

from bs4 import BeautifulSoup
import bs4
 
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

f1 = codecs.open('bookmarks_edge.html', 'r', 'utf-8')  # 使用codecs包
str1 = f1.read()
f1.close()

 
soup = BeautifulSoup(str1, 'html.parser')
print(soup.title.string)
alla=soup.body.dl
i=0
for item in alla.children :  
   
    match item.name:
        case 'dt':
            print('********************************')
            print(str(i))
            i=i+1
            print(type(item))
            print(item)
        case _:
            pass
    
    
    