import xml.etree.ElementTree
e = xml.etree.ElementTree.parse('load.xml').getroot()
for c in e.findall('routine'):
    print(c.get('name'))
    for i in c.findall('attr'):
        for j in i.findall('type'):
            print(j.get('name'), end=" ")
            print(j.get('command'))
        print(i.find("desc").text)
