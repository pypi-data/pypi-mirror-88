"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2020 RedFantom
"""
import sys


def read(file_name):
    with open(file_name) as fi:
        contents = fi.read()
    return contents


def printf(*args, **kwargs):
    kwargs.update({"flush": True})
    print(*args, **kwargs)


if "linux" in sys.platform:
    try:
        from skbuild import setup
        from skbuild.command.build import build
    except ImportError:
        printf("scikit-build is required to build this project")
        printf("install with `python -m pip install scikit-build`")
        raise


    class BuildCommand(build):
        """
        Intercept the build command to build the required modules in ./build

        gttk depends on a library built from source. Building this library
        requires the following to be installed, Ubuntu package names:
        - libx11-dev
        - libgtk2.0-dev
        - libgdk-pixbuf2.0-dev
        - tcl-dev
        - tk-dev
        """

        def run(self):
            build.run(self)

    kwargs = {"install_requires": ["scikit-build"], "cmdClass": {"build": BuildCommand}}

elif "win" in sys.platform:
    import os
    import shutil
    from setuptools import setup
    import subprocess as sp
    from typing import List, Optional

    dependencies = ["pango", "cmake", "gtk2", "glib2", "tk", "toolchain", "libffi"]
    
    for dep in dependencies:
        printf("Installing dependency {}...".format(dep), end=" ")
        sp.call(["pacman", "--needed", "--noconfirm", "-S", "mingw-w64-x86_64-{}".format(dep)],
                stdout=sp.PIPE, stderr=sp.PIPE)
        printf("Done.")
    sp.call(["cmake", ".", "-G", "MinGW Makefiles"])
    sp.call(["mingw32-make"])


    class DependencyWalker(object):
        """
        Walk the dependencies of a DLL file and find all DLL files

        DLL files are searched for in all the directories specified by
        - The PATH environment variable
        - The DLL_SEARCH_PATHS environment variable
        """

        def __init__(self, dll_file: str, dependencies_exe="deps\\dependencies.exe", specials=dict()):
            if not os.path.exists(dependencies_exe):
                printf("dependencies.exe is required to find all dependency DLLs")
                raise FileNotFoundError("Invalid path specified for dependencies.exe")
            self._exe = dependencies_exe
            if not os.path.exists(dll_file):
                raise FileNotFoundError("'{}' does not specify a valid path to first file".format(dll_file))
            self._dll_file = dll_file
            self._dll_cache = {}
            self._specials = specials
            self.walked = {}

        @property
        def dependency_dll_files(self) -> List[str]:
            """Return a list of abspaths to the dependency DLL files"""
            printf("Walking dependencies of {}".format(self._dll_file))
            dlls = [self._dll_file] + list(map(self._find_dll_abs_path, self._specials.keys()))
            done = []
            while set(dlls) != set(done):  # As long as not all dlls are done, keep searching
                for dll in set(dlls) - set(done):  # Go only over not-yet done DLLs
                    if dll is None:
                        done.append(None)
                        continue
                    printf("Looking for dependencies of {}".format(dll))
                    p = sp.Popen([self._exe, "-imports", dll], stdout=sp.PIPE)
                    stdout, stderr = p.communicate()
                    new_dlls = self._parse_dependencies_output(stdout)
                    for new_dll in new_dlls:
                        p = self._find_dll_abs_path(new_dll)
                        if p is None:
                            continue
                        elif "system32" in p:
                            continue
                        elif p not in dlls:
                            dlls.append(p)
                    done.append(dll)
            return list(set(dlls) - set((None,)))

        @staticmethod
        def _parse_dependencies_output(output: bytes) -> List[str]:
            """Parse the output of the dependencies.exe command"""
            dlls: List[str] = list()
            for line in map(str.strip, output.decode().split("\n")):
                if not line.startswith("Import from module"):
                    continue
                line = line[len("Import from module"):].strip(":").strip()
                dlls.append(line)
            return dlls

        def _find_dll_abs_path(self, dll_name: str) -> Optional[str]:
            """Find the absolute path of a specific DLL file specified"""
            if dll_name in self._dll_cache:
                return self._dll_cache[dll_name]
            printf("Looking for path of {}...".format(dll_name), end="")
            for var in ("PATH", "DLL_SEARCH_DIRECTORIES"):
                printf(".", end="")
                val = os.environ.get(var, "")
                for dir in val.split(";"):
                    if not os.path.exists(dir) and os.path.isdir(dir):
                        continue
                    if dir not in self.walked:
                        self.walked[dir] = list(os.walk(dir))
                    for dirpath, subdirs, files in self.walked[dir]:
                        if dll_name in files:
                            p = os.path.join(dirpath, dll_name)
                            printf(" Found: {}".format(p))
                            self._dll_cache[dll_name] = p
                            return p
            printf("Not found.")
            self._dll_cache[dll_name] = None
            return None
        
        def copy_to_target(self, target: str):
            for p in self.dependency_dll_files:
                if os.path.basename(p) in self._specials:
                    t = os.path.join(target, *self._specials[os.path.basename(p)].split("/"), os.path.basename(p))
                    d = os.path.dirname(t)
                    if not os.path.exists(d):
                        os.makedirs(d)
                    printf("Copying special {} -> {}".format(p, t))
                    shutil.copyfile(p, t)
                else:
                    printf("Copying {}".format(p))
                    shutil.copyfile(p, os.path.join(target, os.path.basename(p)))
    
    specials={
        "libpixmap.dll": "lib/gtk-2.0/2.10.0/engines/",
        "libwimp.dll": "lib/gtk-2.0/2.10.0/engines/",
        "loaders.cache": "lib/gdk-pixbuf-2.0/2.10.0/"}  # loaders.cache is used to specify abspaths to the loaders
    specials.update({"libpixbufloader-{}.dll".format(fmt): "/lib/gdk-pixbuf-2.0/2.10.0/loaders/"
                     for fmt in ["ani", "bmp", "gif", "icns", "ico", "jpeg", "png", "pnm", "qtif", "svg", "tga", "tiff", "xbm", "xpm"]})
    DependencyWalker("libgttk.dll", specials=specials).copy_to_target("gttk")

    # If loaders.cache is not found, it must be generated
    cache_file = os.path.join("gttk", specials["loaders.cache"], "loaders.cache")
    if not os.path.exists(cache_file) or os.path.getsize(cache_file) < 1024:  # Minimum expected file size
        print("Creating loaders.cache file...")
        with open("loaders.cache", "wb") as fo:
            sp.call(["gdk-pixbuf-query-loaders"], stdout=fo)
        shutil.copyfile("loaders.cache", cache_file)
        with open(cache_file) as fi:
            print("gdk-pixbuf-query-loaders gave {} lines of output".format(len(fi.readlines())))

    kwargs = {"package_data": {"gttk": ["*.dll", "pkgIndex.tcl", "gttk.tcl"] + ["{}/{}".format(dir.strip("/"), base) for base, dir in specials.items()]}}

else:
    printf("Only Linux and Windows are currently supported by the build system")
    printf("If you wish to help design a build method for your OS, please")
    printf("contact the project author.")
    raise RuntimeError("Unsupported platform")

setup(
    name="gttk",
    version="v0.6.1",
    packages=["gttk"],
    description="GTK theme for Tkinter/ttk",
    author="The gttk/tile-gtk/gttk authors",
    url="https://github.com/RedFantom/python-gttk",
    download_url="https://github.com/RedFantom/python-gttk/releases",
    license="GNU GPLv3",
    long_description_content_type="text/markdown",
    long_description=read("README.md"),
    zip_safe=False,
    **kwargs
)
