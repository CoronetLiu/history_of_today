# -*- coding: utf-8 -*-
import json

class OutputResultModel(object):
    def __init__(self, year, title):
        self.year = year
        self.title = title
    def to_json(self):
        return dict(title = self.title, year = self.year)

class OutPutResultChild(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.lists = []

    def add(self, model):
        self.lists.append(model)
    def to_json(self):
        #print(self.id , self.name , len(self.lists))
        return dict(lists = self.lists, name = self.name, id = self.id)

class OutPutResult(OutPutResultChild):
    def __init__(self, month, day):
        self.month = month
        self.day = day
        self.res = []

    def add(self, model):
        self.res.append(model)
    def to_json(self):
        return dict(res = self.res, month = self.month, day = self.day)

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        else:
            return json.JSONEncoder.default(self, obj)

class HtmlOutputer(object):

    def __init__(self):
        self.datas = []

    def write_file(self, data):
        filename = 'files/{}-{}.json'.format(data[0], data[1])
        print(filename)
        with open(filename, mode = 'w', encoding = 'utf-8') as f:
            f.write(data[2])

    def collect_data(self, new_url, new_data):
        if new_data is None:
            return None
        print("month : %d ; day : %d ; url : %s" % new_url)
        month = new_url[0]
        day = new_url[1]
        result = OutPutResult(month, day)
        
        for k in new_data.keys():
            #print(k,len(v))
            child = OutPutResultChild(k[0], k[1])
            for c in new_data.get(k):
                model = OutputResultModel(c[0], c[1])                
                child.add(model)
            result.add(child)
        
        cont = json.dumps(result.to_json(), ensure_ascii = False, sort_keys = False, cls = ComplexEncoder)
        #print(cont)
        data = (month, day, cont)
        #self.datas.append(data)
        self.write_file(data)
    

    def output_json(self):
        for data in self.datas:
            self.write_file(data)