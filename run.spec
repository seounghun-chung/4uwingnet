# -*- mode: python -*-

# if you use pyqt5, this patch must be adjusted
# https://github.com/bjones1/pyinstaller/tree/pyqt5_fix

block_cipher = None


a = Analysis(['run.py'],
             pathex=['C:\\Users\\seoung\\workspace\\pytool'],
             binaries=[],
             datas=[('./config','./config'),
                    ('./gui/*.ui','./gui'),
                    ('./script','./script')],
             hiddenimports=["feature.testmanager",
                            "feature.command",
                            "feature.consolemanager",
                            "feature.dummymanager",
                            "feature.testmanager",
                            "interface.can.can",
                            "interface.lan.lan",
                            "interface.serial.serial",
                            "gui.commandwindows",
                            "gui.consolewindows",
                            "gui.controlwindows",
                            "gui.imageview",
                            "gui.mainwindows",
                            "gui.testview",                            
                            ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='run',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='run')
