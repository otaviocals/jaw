# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=["/home/cals/Projects/python_webcrawler"],
             binaries=None,
             datas=[
("xpopup.py","."),
("notification.py","."),
("file.py","."),
("tools.py","."),
("xbase.py","."),
("form.py","."),
("logo.png","."),
("phantomjs","."),
("logo.ico",".")],
             hiddenimports=["six","packaging","packaging.version","packaging.specifiers","packaging.requirements","appdirs"],
             hookspath=["."],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Webscraper de Taxa de Juros',
          debug=False,
          strip=False,
          upx=True,
	  icon='logo.ico',
          console=False )
