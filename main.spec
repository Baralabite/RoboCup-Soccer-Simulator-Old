# -*- mode: python -*-
a = Analysis(['main.py'],
             pathex=['C:\\Users\\John\\Documents\\Aptana Studio 3 Workspace\\RoboCup Soccer Simulator'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'main.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
