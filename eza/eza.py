# -*- coding: utf-8 -*-

ARCHIVE_DIR_NAME = "archive"
ARCHIVE_DIR_SUFFIX = "%Y-%m-%d"
ARCHIVE_DIR_DESKTOPINI = '''[.ShellClassInfo]
IconResource={ICON_SPEC}
[ViewState]
Mode=
Vid=
FolderType=Generic
'''

import sys
import os
import datetime

from ctypes import c_int, WINFUNCTYPE, windll
from ctypes.wintypes import HWND, LPCWSTR, UINT
prototype = WINFUNCTYPE(c_int, HWND, LPCWSTR, LPCWSTR, UINT)
MessageBox = prototype(("MessageBoxW", windll.user32), ((1, "hwnd", 0), (1, "text", None), (1, "caption", None), (1, "flags", 0)))

MB_ICONERROR = 16
MB_ICONINFORMATION = 64
MB_OK = 0


def get_archive_dir(path):
    p, f = os.path.split(path)
    if len(p) == 0:
        ret = ARCHIVE_DIR_NAME
    else:
        ret = p + os.path.sep + ARCHIVE_DIR_NAME
    ret += os.path.sep + datetime.date.today().strftime(ARCHIVE_DIR_SUFFIX)
    return ret, ret + os.path.sep + f


def make_sure_archive_basedir(path):
    if not os.path.exists(path):
        icon_spec = os.getenv('EZA_FOLDER_ICON', '')
        os.mkdir(path)
        os.system("attrib +S \"%s\"" % path)
        dti = path + os.path.sep + "desktop.ini"
        f = open(dti, "w")
        f.write(ARCHIVE_DIR_DESKTOPINI.format(**{'ICON_SPEC': icon_spec}))
        f.close()
        os.system("attrib +S +H \"%s\"" % dti)
    elif not os.path.isdir(path):
        return False
    return True


def make_sure_archive_dir(path):
    b, d = os.path.split(path)
    if not make_sure_archive_basedir(b):
        return False
    if not os.path.exists(path):
        os.mkdir(path)
        if not os.path.exists(path):
            return False
    return True


def main():
    for a in sys.argv[1:]:
        a = unicode(a, "mbcs")
        dir, new = get_archive_dir(a)
        if not make_sure_archive_dir(dir):
            MessageBox(0, u"ディレクトリ \"%s\" が作成できなかった" % dir, None, MB_ICONERROR)
            continue
        #MessageBox(0, "from: %s\r\nto: %s" % (a, new), "order", MB_ICONINFORMATION)
        os.rename(a, new)


if __name__ == "__main__":
    main()

