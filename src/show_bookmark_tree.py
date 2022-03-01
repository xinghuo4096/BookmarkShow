from bmtree import echar_show, simple_show

outfile = simple_show()
outfile = simple_show(infile='tests/bookmarks_firefox.html',
                      outfile='outdata/show_bookmarks_firefox.html')
outfile = echar_show(infile='tests/bookmarks_edge.html',
                     outfile='outdata/show_bookmarks_edge.html', is_cdn_jsdelivr=True)
