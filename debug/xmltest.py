import xmltodict
import collections

def xmlparse(e, depth, o):
    depth += 1
    if type(e) is str:
        print(depth, end= " ")    
        print(e)
        o.append([depth,e])

    if type(e) is list:
        for attr in e:
            xmlparse(attr, depth,o)
        
    if type(e) is collections.OrderedDict:
        for attr in e:
            xmlparse(e[attr], depth, o)
        
with open('load.xml') as fd:
    doc = xmltodict.parse(fd.read())
for mainattr in doc["main"]:
#    parentitem = QStandardItem(mainattr)
    print(mainattr)
    for subattr in doc["main"][mainattr]:
        for jj in (doc["main"][mainattr][subattr]):
            print(jj.items())
            
o = []
#xmlparse(doc, 0, o)
#print(o)
#print(doc["main"]["routine"]["attr"][0]["type"]["@name"])
#print(doc["main"])
#print("\n\n")
#
#for ii in doc["main"]:
#    print(ii)
#    print(doc["main"][ii])

    
    
    
#for ii in doc["main"]["session"]["attr"]:
#    print(ii['type'])
#    print(ii['desc'])
    
