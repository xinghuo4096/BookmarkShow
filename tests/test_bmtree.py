import codecs
import os
from bmtree import bookmark2json, simple_show, bms


def test_html2json():
    flist = (('tests/bookmarks_edge.html', 'tests/bookmarks_edge.json'),
             ('tests/bookmarks_edge_new.html', 'tests/bookmarks_edge_new.json'),
             ('tests/bookmarks_firefox.html', 'tests/bookmarks_firefox.json'),
             ('tests/bookmarks_chrome.html', 'tests/bookmarks_chrome.json'))
    for bmfile in flist:
        f1 = codecs.open(bmfile[0], 'r', 'utf-8')
        str1 = f1.read()
        f1.close()

        retstr = bookmark2json(str1)
        str1 = retstr[0]
        message = retstr[1]

        assert len(str1) > 0

        f1 = codecs.open(bmfile[1], 'w', 'utf-8')
        f1.write(str1)
        f1.close()
        assert os.path.isfile(bmfile[0])


def test_simple_show():
    outfile = simple_show()
    assert os.path.isfile(outfile)


def main():
    test_simple_show()


if __name__ == '__main__':
    main()
