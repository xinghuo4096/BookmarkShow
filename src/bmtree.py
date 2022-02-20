# TODO 准备生成html和图片

import codecs
from turtle import clear


from bs4 import BeautifulSoup, Tag
from bm import Basic, Bookmark, Folder


def bookmark2json(str1: str):
    bms_tree = Folder('root')

    soup = BeautifulSoup(str1, 'html.parser')

    if soup.body:
        retstr = "old_edge:               "
        dl = soup.body.dl  # edge
    else:
        retstr = "new edge|firefox|chrome:"
        dl = soup.dl  # firefox chrome
    loadtree(dl, bms_tree)
    strjson = bms_tree.toJSON()
    return (strjson, retstr)


def loadtree(html: Tag, bmf: Folder):
    for item in html.contents:
        if isinstance(item, Tag):
            match item.name:
                case 'dl':
                    f = Folder('dl')
                    if bmf.itemname:
                        f.name = bmf.itemname
                        bmf.itemname = ''
                    bmf.children.append(f)
                    loadtree(item, f)
                case 'dt':
                    itemname = ''
                    if item.h3:
                        itemname = item.h3.string
                        bmf.itemname = itemname
                    loadtree(item, bmf)
                case 'a':
                    assert isinstance(item, Tag)
                    title = item.string
                    if not title:
                        title = item.attrs.get('href')
                    b = Bookmark(title=title, uri=item.attrs.get('href'), icon=item.attrs.get(
                        'icon'), add_date=item.attrs.get('add_date'), last_modified=item.attrs.get('last_modified'))
                    bmf.children.append(b)
                case 'p':
                    loadtree(item, bmf)
