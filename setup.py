from cx_Freeze import setup, Executable
 
# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = ["sys","os"],
                    excludes = [""], 
                    includes = ["gui.consolewindows",
                                "gui.controlwindows",
                                "gui.imageview",
                                "gui.testview",
                                "gui.commandwindows",
                                "interface.lan.lan",
                                "interface.can.can",
                                "interface.serial.serial",                                
                                "multiprocessing.pool",
                                ])
 
import sys
base = None if sys.platform=='win32' else None

executables = [
    Executable('run.py', base=base)
]
 
setup(
    name='pytool',
    version = '0.1',
    description = 'pytool @seonghun.chung',
    options = dict(build_exe = buildOptions),
    executables = executables
)