# -*- conding: utf-8 -*-


# this is garbage and spagetti code .....
# never analyze it deeply
# just spagetti!!!!!


import winreg
import os


findpath = ""

def find_registry_name(key, sub_key, name):
    global findpath
    if findpath != "":
        return
        
    try:
        handle = winreg.OpenKey(key, sub_key)
    except:
        pass
    for jj in range(0,10000):   # find key name... not folder
        try:
            attr_name = winreg.EnumValue(handle, jj)    # check whether there are key names
        except: # there are not key names
            attr_name = "."   
            for ii in range(0,10000):   # find sub folder
                try:
                    subpath = winreg.EnumKey(handle,ii) # get subfolder path
                except: # there are not sub directory
                    return
                find_registry_name(key, os.path.join(sub_key, subpath), name)   # newly serach 'name' in sub directory   
        if (attr_name[0] == name):  # find it. WA : there no way of escaping recursive call
            findpath = sub_key, jj
            print("find!")
            return
    handle.Close()

find_registry_name(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Class', "*JumboPacket")
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, findpath[0], access = winreg.KEY_ALL_ACCESS) as handle:
    attr_name = winreg.EnumValue(handle, findpath[1])
    print(attr_name)

    winreg.SetValueEx( handle, "*JumboPacket", 0, winreg.REG_SZ, "1514")  
    attr = winreg.QueryValueEx( handle, "*JumboPacket" )    
    print(attr)
    
    
