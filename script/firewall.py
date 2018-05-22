# -*- conding: utf-8 -*-


# this is garbage and spagetti code .....
# never analyze it deeply
# just spagetti!!!!!

import winreg
import win32com.shell.shell as shell
import os
import sys
import ctypes

def run_as_admin(argv=None, debug=False):
    shell32 = ctypes.windll.shell32
    if argv is None and shell32.IsUserAnAdmin():
        return True

    if argv is None:
        argv = sys.argv
    if hasattr(sys, '_MEIPASS'):
        # Support pyinstaller wrapped program.
        arguments = map(str, argv[1:])
    else:
        arguments = map(str, argv)
    argument_line = u' '.join(arguments)
    executable = str(sys.executable)
    if debug:
        print('Command line: ', executable, argument_line)
    ret = shell32.ShellExecuteW(None, u"runas", executable, argument_line, None, 1)
    print(ret)
    if int(ret) <= 32:
        return False
    return None

def uac_require(): 
    asadmin = 'asadmin'
#    try:
    if sys.argv[-1] != asadmin:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + [asadmin])
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
#        sys.exit()
        return True
    else:
        return False

#    except:
#        return False

def find_registry_name2(key, sub_key, name, items):
    ret = None
    try:
        handle = winreg.OpenKey(key, sub_key)
    except:
        return
        
    currentdir_reg = list()
    try:    # find all attr name
        jj = 0
        while(True):
            attr_name = winreg.EnumValue(handle, jj)
            jj += 1
            currentdir_reg.append(attr_name[0])
    except:
        pass

    if name in currentdir_reg:
        print("find :", sub_key)
        items.append(sub_key)
        handle.Close()
        pass    # find duplicated item
#        return sub_key
    else:    
        jj = 0
        subdir_list = list()
        try: # search sub directory
            while(True):
                subdir_name = winreg.EnumKey(handle,jj)
                jj += 1
                subdir_list.append(subdir_name)
        except:
            pass

        for subdir in subdir_list:  # ennter sub directory recursively
            ret = find_registry_name2(key, os.path.join(sub_key,subdir), name, items)
            if ret is not None:
                break
    handle.Close()
    return ret

def get_registry_values(key, findpath, name):
    if type(findpath) is str:
        findpath = [findpath]
    for reg in findpath:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg, access = winreg.KEY_ALL_ACCESS) as handle:
            attr = winreg.QueryValueEx( handle, "EnableFirewall" ) 
            print(attr)
    #print(findpath[0])
    #with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, findpath[0], access = winreg.KEY_ALL_ACCESS) as handle:
    #    attr_name = winreg.EnumValue(handle, findpath[1])
    #    print(attr_name)
    #
    #    winreg.SetValueEx( handle, "*JumboPacket", 0, winreg.REG_SZ, "1514")  
    #    attr = winreg.QueryValueEx( handle, "*JumboPacket" )    
    #    print(attr)
    
    
if __name__ == '__main__':
    import time
    

    if uac_require() is True: 
        print( "continue")
        findpath = list()
        
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r'SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters'
        keyname = "EnableFirewall"
        
        ret = find_registry_name2(key, subkey, keyname, findpath)
        print(findpath)
        get_registry_values(key, findpath, keyname)        
        time.sleep(10000)
    else: 
        print("error message")



    
    

    
