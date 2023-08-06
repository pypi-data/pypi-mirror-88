"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2020 RedFantom
"""
import contextlib
import os
import sys
from tempfile import gettempdir
import tkinter as tk
from typing import Optional, Tuple


@contextlib.contextmanager
def chdir(target):
    cwd = os.getcwd()
    try:
        os.chdir(target)
        yield
    finally:
        os.chdir(cwd)


class GTTK(object):
    """
    Class representing the GTTK extension
    """

    FOLDER = os.path.abspath(os.path.dirname(__file__))

    def __init__(self, window: tk.Tk, theme: Optional[str] = None, theme_dir_prefix: Optional[str] = None,
                 temp_dir: str = gettempdir()):
        """
        Initialize gttk and load it into a window

        :param window: Window with Tk/Tcl interpreter to load gttk for
        :param theme: GTK theme to set upon initialisation
        :param theme_dir_prefix: Prefix to the theme directory. If not
            given, defaults to the current working directory. If this
            has the special value "LIB", the script will use the
            site-packages directory where it is installed.
        :param temp_dir: Absolute path to temporary files directory that
            may be used by the library
        """
        self.tk = window.tk
        folder = os.path.dirname(os.path.abspath(__file__))

        if theme_dir_prefix is not None:
            os.environ["GTK_DATA_PREFIX"] = theme_dir_prefix

        # Create loaders.cache on win32 platforms to find pixbuf loaders properly
        if "win" in sys.platform:
            target = os.path.join(temp_dir, "loaders.cache")
            source = os.path.join(folder, "lib", "gdk-pixbuf-2.0", "2.10.0", "loaders.cache")
            with open(os.path.join(source)) as fi, open(target, "w") as fo:
                cache = fi.read()
                # loaders.cache uses double \ everywhere
                abspath = (os.path.join(folder, "lib", ) + "\\").replace("\\", "\\\\")
                cache_w_abspaths = cache.replace("lib\\\\", abspath)
                fo.write(cache_w_abspaths)
            # Set GDK_PIXBUF_MODULE_FILE to the path of the new cache file
            # GDK_PIXBUF_MODULEDIR does not do anything for plain GDK!
            os.environ["GDK_PIXBUF_MODULE_FILE"] = target

            # Set GTK_EXE_PREFIX on win32 to ensure theme engine loading
            os.environ["GTK_EXE_PREFIX"] = folder

        with chdir(folder):
            # Evaluate pkgIndex.tcl, Tcl does not handle \ as a pathsep, so with /
            self.tk.eval("set dir {0}; source {0}/pkgIndex.tcl".format(folder.replace("\\", "/")))
            self.tk.call("package", "require", "ttk::theme::gttk")

        if theme is not None:
            self.set_gtk_theme(theme)

    def get_themes_directory(self) -> str:
        """Return the directory in which GTK looks for installed themes"""
        return self.tk.call("ttk::theme::gttk::gtkDirectory", "theme")

    def get_default_files(self) -> Tuple[str]:
        """Return the files that GTK parses by default at start-up"""
        return self.tk.call("ttk::theme::gttk::gtkDirectory", "default_files")

    def get_current_theme(self) -> str:
        """Return the name of the currently active GTK theme"""
        return self.tk.call("ttk::theme::gttk::currentThemeName")

    def get_module_path(self) -> str:
        """Return the name of the module path (theme engines)"""
        return self.tk.call("ttk::theme::gttk::gtkDirectory", "module")

    def get_gtk_enum_value(self, value: int) -> str:
        """
        Return a value of a the GtkPositionType enum

        TODO: Extend gttk_GtkEnum in gttk_Init.cpp for more enums
        """
        return self.tk.call("ttk::theme::gttk::gtkEnum", "GtkPositionType", 0)

    def get_theme_colour(self, name: str) -> str:
        return self.tk.call("ttk::theme::gttk::currentThemeColour", name)

    def get_theme_colour_keys(self) -> Tuple[str]:
        return self.tk.call("ttk::theme::gttk::currentThemeColourKeys")

    def set_gtk_theme(self, theme: str):
        self.tk.call("ttk::theme::gttk::setGtkTheme", theme)
