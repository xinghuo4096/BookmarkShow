 
from BookMark import basic, bookmark, folder
def test_bmbasice():
    bmb=basic('test')  
    assert len(bmb.guid)>0
    assert bmb.title==bmb.name=='test'
    assert int(bmb.last_modified)>0
    assert int(bmb.add_date)>0

    bmb=basic('test',1,2,'aaa') 
    
    assert len(bmb.guid)>0
    assert bmb.guid=='aaa'
    assert bmb.title==bmb.name=='test'
 
    assert int(bmb.add_date)==1
    assert int(bmb.last_modified)==2
    
    jstr=bmb.toJSON()
    print(jstr)
    assert len(jstr) >2

def test_bmbookmark():
    bmbm=bookmark('','https://www.baidu.com')  
    assert len(bmbm.guid)>0
    assert bmbm.title==bmbm.name=='www.baidu.com'
    assert int(bmbm.last_modified)>0
    assert int(bmbm.add_date)>0

    bmbm=bookmark('test','https://www.tianqi.com','',1,2,'aaa')     
    assert len(bmbm.guid)>0
    assert bmbm.guid=='aaa'
    assert bmbm.title=='test'
    assert bmbm.name=='test'
    assert bmbm.uri=='https://www.tianqi.com' 
    assert int(bmbm.add_date)==1
    assert int(bmbm.last_modified)==2
    
    jstr=bmbm.toJSON()
    print(jstr)
    assert len(jstr) >2

def test_bmfolder():
    bmf=folder('test')  
    assert len(bmf.guid)>0
    assert bmf.title==bmf.name=='test'
    assert int(bmf.last_modified)>0
    assert int(bmf.add_date)>0
    assert len(bmf.children)==0

    bm=bookmark('bookmark','www.baidu.com')
    bm2=bookmark('bookmark2','www.tianqi.com')
    bmf2=folder('bmf2',1,2)
     
    bmf=folder('test',[bm,bm2,bmf2],1,2,'aaa')     
    assert len(bmf.guid)>0
    
    assert bmf.title=='test'
    assert bmf.name=='test'
      
    assert int(bmf.add_date)==1
    assert int(bmf.last_modified)==2

    assert len(bmf.children)==3
    
    jstr=bmf.toJSON()
    print(jstr)
    assert len(jstr) >2
# ----
def main():
    test_bmfolder()


if __name__ == '__main__':
    main()