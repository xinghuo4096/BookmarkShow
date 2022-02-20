import json
from random import Random
import time
from types import NoneType
from urllib.parse import urlparse
import uuid


class Basic:
    def __init__(self, title: str, add_date=None, last_modified=None, guid='') -> None:
        self.title = title
        self.guid = guid

        if not add_date:
            self.add_date = now_time()
        else:
            self.add_date = str(add_date)

        if not last_modified:
            self.last_modified = now_time()
        else:
            self.last_modified = str(last_modified)

        if not title:
            title = ''
        if len(title) > 16:
            self.name = title[0:16] + ".."
        else:
            self.name = title

        if not self.guid:
            self.guid = getguid(self.title)

    def isempty(self, x):

        assert isinstance(x, tuple)
        data = x[1]

        if isinstance(data, (str, list)):
            return len(data) > 0
        else:
            if isinstance(data, int):
                return True
            else:
                if isinstance(data, NoneType):
                    return False
                else:
                    return True
        return True

    def _ggg(self, x):
        assert isinstance(x, object)
        d1 = x.__dict__
        c = dict(filter(self.isempty, d1.items()))
        return c

    def toJSON(self):
        return json.dumps(self,
                          default=self._ggg,
                          sort_keys=False, ensure_ascii=False,
                          indent='    ')


class Bookmark(Basic):
    def __init__(self,  title, uri, icon='', add_date=None, last_modified=None, guid=''):
        super().__init__(title,  add_date, last_modified, guid)

        self.icon = icon
        self.uri = uri

        if len(self.title) < 1 and len(self.uri) > 1:
            self.title = urlparse(uri).hostname

        if len(self.name) < 1 and len(self.uri) > 1:
            self.name = urlparse(uri).hostname


class Folder(Basic):
    def __init__(self,  title: str, children: list = None, add_date=None, last_modified=None, guid=''):
        super().__init__(title, add_date, last_modified, guid)

        if (children == None):
            self.children = list()
        else:
            self.children = children

        if self.title:
            self.name = self.title
        else:
            self.name = 'o'


def getguid(name):
    """
        UUID主要有五个算法,也就是五种方法来实现:

        uuid1()——基于时间戳 由MAC地址、当前时间戳、随机数生成。可以保证全球范围内的唯一性, 但MAC的使用同时带来安全性问题,局域网中可以使用IP来代替MAC。 

        uuid2()——基于分布式计算环境DCE(Python中没有这个函数) 算法与uuid1相同,不同的是把时间戳的前4位置换为POSIX的UID。 实际中很少用到该方法。 

        uuid3()——基于名字的MD5散列值 通过计算名字和命名空间的MD5散列值得到,保证了同一命名空间中不同名字的唯一性, 和不同命名空间的唯一性,但同一命名空间的同一名字生成相同的uuid。 

        uuid4()——基于随机数 由伪随机数得到,有一定的重复概率,该概率可以计算出来。 

        uuid5()——基于名字的SHA-1散列值 算法与uuid3相同,不同的是使用 Secure Hash Algorithm 1 算法 

    """
    u1 = uuid.uuid1()
    x = uuid.uuid3(u1, name)
    a = Random()

    return str(x)[24:]


def now_time():
    t = time.time()
    sdt = int(t * pow(10, 6))
    return str(sdt)
