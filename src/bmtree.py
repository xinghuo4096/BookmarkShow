
import codecs


from bs4 import BeautifulSoup, Tag
import bs4
from BookMark import basic, bookmark, folder


def loadtree(html: Tag, bmf: folder):
    for item in html.contents:
        if isinstance(item, Tag):
            match item.name:
                case 'dl':
                    f = folder('dl')
                    bmf.children.append(f)
                    loadtree(item, f)

                case 'dt':
                    f = folder('dl')
                    bmf.children.append(f)
                    loadtree(item, f)

                case 'a':
                    assert isinstance(item, Tag)
                    title = item.string
                    if not title:
                        title = item.attrs.get('href')
                    b = bookmark(title=title, uri=item.attrs.get('href'), icon=item.attrs.get(
                        'icon'), add_date=item.attrs.get('add_date'), last_modified=item.attrs.get('last_modified'))
                    return b
                case 'h3':
                    bmf.name=item.string


f1 = codecs.open('src/bookmarks_edge.html', 'r', 'utf-8')  # 使用codecs包
str1 = f1.read()
f1.close()

bms_tree = folder('root')

soup = BeautifulSoup(str1, 'html.parser')
dl = soup.body.dl


loadtree(dl, bms_tree)
str1 = bms_tree.toJSON()
print(str1)
print('ok')
