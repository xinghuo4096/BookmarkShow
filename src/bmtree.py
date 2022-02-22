# TODO 准备生成html和图片

import codecs
import json
import os
import time
from turtle import clear

from bs4 import BeautifulSoup, Tag
from pyecharts import options as opts
from pyecharts.charts import Tree
from pyecharts.commons import utils
from pyecharts.globals import CurrentConfig, ThemeType

from bm import Basic, Bookmark, Bookmarks, Folder

bms = Bookmarks()
bms.folder_count = bms.bookmark_count = 0


def bookmark2json(str1: str):
    bms_tree = Folder('root')

    soup = BeautifulSoup(str1, 'html.parser')

    if soup.body:
        retstr = "old_edge:               "
        dl = soup.body.dl  # edge
    else:
        retstr = "new edge|firefox|chrome:"
        dl = soup.dl  # firefox chrome

    bms = Bookmarks()
    bms.folder_count = bms.bookmark_count = 0

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
                    bms.folder_count += 1
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
                    bms.bookmark_count += 1
                case 'p':
                    loadtree(item, bmf)


def load_html(filename: str) -> str:
    f1 = codecs.open(filename, 'r', 'utf-8')
    str1 = f1.read()
    f1.close()
    return str1


def save(filename: str, html: str):
    f1 = codecs.open(filename, 'w', 'utf-8')
    f1.write(html)
    f1.close()


def load_chardata(infile='tests/bookmarks_edge_new.html') -> list:
    str1 = load_html(filename=infile)

    strret = bookmark2json(str1)[0]
    strjson = json.loads(strret)
    # TODO test will del
    savejson = json.dumps(strjson)
    save('test.json', savejson)
    save('test2.json', strret)
    listjson = [strjson]
    return listjson


def simple_show(infile='tests/bookmarks_edge_new.html', outfile='outdata/show_bookmarks_edge_new.html'):

    load_chardata(infile=infile)

    w = (bms.folder_count) * 100
    h = (bms.bookmark_count) / (bms.folder_count) * 450

    w = 1280 if w < 1280 else w

    echar_show(infile=infile, outfile=outfile,
               tree_depth=2, w=w, h=h, is_cdn_jsdelivr=True)
    return outfile


def echar_show(infile='tests/bookmarks_edge_new.html', outfile='outdata/show_bookmarks_edge_new.html', tree_depth=2, w=1280, h=720, is_cdn_jsdelivr=True):

    data = load_chardata(infile)
    series_name = '书签:'+infile

    if (is_cdn_jsdelivr):
        CurrentConfig.ONLINE_HOST = "https://cdn.jsdelivr.net/npm/echarts@latest/dist/"

    ffbmformater = """
        function (params) {   
            showstr='';                             
            if (typeof(params.data.title) != 'undefined')
               {	showstr+='Title:'+params.data.title}            
            if (typeof(params.data.uri) != 'undefined')            
               {	showstr+='\\n<br/>uri:'+params.data.uri}                 
            return showstr
        }
        """
    assert isinstance(outfile, str)
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ctree = Tree(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE,
                                         page_title='FfBmM Show' + localtime,
                                         width=str(w) + 'px',
                                         height=str(h) + 'px'))

    ctree.set_global_opts(title_opts=opts.TitleOpts(title='Bookmarks show'))
    ctree.add(series_name,
              data,
              orient='LR',
              pos_top='1%',
              pos_bottom='1%',
              is_roam=False,
              initial_tree_depth=tree_depth,
              layout='orthogonal',
              edge_fork_position='190%',
              itemstyle_opts=opts.ItemStyleOpts(color='red'),
              label_opts=opts.LabelOpts(color="blue"),
              tooltip_opts=opts.TooltipOpts(
                  background_color='rgba(193,203,215, 0.8)',
                  is_show=True,
                  trigger='item',
                  trigger_on='mousemove',
                  formatter=utils.JsCode(ffbmformater)))
    ctree.render(outfile)

    if os.path.isfile(outfile) and is_cdn_jsdelivr:
        fix_cdn_jsdelivr(outfile)


def fix_cdn_jsdelivr(outfile):
    f = codecs.open(outfile, "r", "utf-8")
    s = f.read()
    f.close()
    assert len(s) > 0

    s = s.replace('dist/themes/vintage.js', 'theme/vintage.min.js')

    f = codecs.open(outfile, "w", "utf-8")
    s = f.write(s)
    f.close()
