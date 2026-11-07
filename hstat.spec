# -*- mode: python ; coding: utf-8 -*-
# Đóng gói thành 1 file .exe:  python -m PyInstaller --noconfirm --clean hstat.spec
from pathlib import Path

HERE = Path(SPECPATH)
NAME = "HeptacontakaienneagonStat"

# DLL không đưa vào exe:
#  - icuuc.dll: Qt dùng ICU có sẵn của Windows 10/11 (System32)
#  - opengl32sw.dll: OpenGL phần mềm (~20 MB), app vẽ bằng QPainter nên không cần
DROP_BINARIES = {"icuuc.dll", "opengl32sw.dll"}

a = Analysis(
    [str(HERE / "run.py")],
    pathex=[str(HERE)],
    datas=[(str(HERE / "hstat" / "assets"), "hstat/assets")],
    hiddenimports=[],
    excludes=["tkinter", "unittest", "pydoc", "test", "lib2to3"],
    noarchive=False,
)
a.binaries = [b for b in a.binaries if Path(b[0]).name.lower() not in DROP_BINARIES]
# Bản dịch có sẵn của Qt không có tiếng Việt → bỏ cho nhẹ
a.datas = [d for d in a.datas if "translations" not in Path(d[0]).parts]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=NAME,
    icon=str(HERE / "hstat" / "assets" / "app.ico"),
    version=str(HERE / "packaging" / "version_info.txt"),
    console=False,          # ứng dụng cửa sổ, không hiện cửa sổ đen
    upx=False,
    runtime_tmpdir=None,
)
