# GTK Theme for Python's tkinter/ttk
![Build Status](https://api.travis-ci.com/TkinterEP/python-gttk.svg?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/80y25364onq2anmw/branch/master?svg=true)](https://ci.appveyor.com/project/RedFantom/python-gttk/branch/master)

Would you like to have a more native look for your Tkinter application?
Are the themes provided in [ttkthemes](https://github.com/TkinterEP/ttkthemes)
not to your liking?

This package provides a version of [`gtkTtk`](https://github.com/Geballin/gtkTtk),
formerly [`tilegtk`](https://github.com/xiaq/tile-gtk) packaged for
usage with Python. Simply follow the installation instructions and all
required files are installed to the site package directory.

## Installation
Currently, a build process for Linux and Windows is available. If you
would like  to use the package on OS X, please let me know so we can
work on a build system.

### Wheels
Currently, wheels are provided for Windows. The Linux wheels are built
with Travis-CI and are thus not `manylinux` wheels. Therefore, building
yourself is recommended when using Linux (either from the source dist
from PyPI or this repository). Feel free to open an issue if you
encounter any problems building!

### Linux
These instructions are for Ubuntu, Python 3.5 or higher. Any lower 
version may work, but is not supported. On other distributions, package 
names may be different.
```bash
# Build Tools
sudo apt install build-essential cmake
# Required Libraries
sudo apt install libgtk2.0-dev libglib2.0-dev tcl-dev tk-dev
# Required Python packages
python -m pip install scikit-build

python setup.py install 
``` 

### Windows (64-bit only)
These instructions assume you have [MSYS2](https://www.msys2.org/)
installed, with the MinGW toolchain. The `setup.py` script will check
the additional build dependencies and install them when required.

Both the MSYS `bin` directory as well as the MinGW `bin` directory must
be on the `PATH` to run the `setup.py` script. Usually, these folders
are `C:\msys64\usr\bin` and `C:\msys64\mingw64\bin`, but they may differ
for your installation.

In addition to this, the `setup.py` script expects the `Dependencies` 
program found [here](https://github.com/lucasg/Dependencies) to be 
installed under `deps/Dependencies.exe` by default. This tool is used
to find all DLL-files necessary to run `gttk` without any external files.

If you have satisfied all requirements, assuming you want to install 
the package *outside* of your MSYS installation:
```bash
# Replace C:\Python with the path to your Python setup
# The MSYS version of Python is on PATH and thus you should use an abspath!
C:\Python\python.exe setup.py install
``` 

The binary distribution of `gttk` will come with all DLL-files known to
be required to run it. These DLL-files are generally available under
their own specific licenses, as covered in the files that are found in
the MSYS directory `/share/licenses`.

## Usage
Simply import the package and instantiate the `GTTK` class. Then the 
theme will become available for usage in a `ttk.Style`.
```python
import tkinter as tk
from tkinter import ttk
from gttk import GTTK

window = tk.Tk()
gttk = GTTK(window)
style = ttk.Style()
style.theme_use("gttk")
print(gttk.get_current_theme()) # Prints the active GTK theme
gttk.set_gtk_theme("Yaru") # Sets GTK theme, provided by developer
ttk.Button(window, text="Destroy", command=window.destroy).pack()

window.mainloop()
```

If you encounter an error because you are running in the repository, 
directory, make sure to disallow imports from the working directory
before importing `gttk`:
```python
import sys
sys.path = sys.path[2:]
import gttk
```

## Screenshots
`gttk` should work with any GTK theme you can throw at it, but below
are the themes Yaru and Adwaita as examples.

![Yaru Example](https://raw.githubusercontent.com/RedFantom/python-gttk/master/screenshots/yaru.png)
![Adapta Example](https://raw.githubusercontent.com/RedFantom/python-gttk/master/screenshots/adwaita.png)

## License and Copyright
This repository provides a wrapper around `gttk`, which is a renamed 
version of `gtkTtk`, which in turn is a renamed version of `tile-gtk`.
The original `tile-gtk` is available under hte MIT License. This version
is available only under GNU GPLv3.

```
python-gttk 
Copyright (c) 2008-2012 Georgios Petasis
Copyright (c) 2012 Cheer Xiao
Copyright (c) 2019-2020 Géballin
Copyright (c) 2020 RedFantom

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```

## Project State
`tile-gtk`, `gtkTtk` and hence also `gttk` are far from perfect. You may
encounter various graphical artifacts when using particular themes,
while others work without flaws.

You are welcome to report any issues, and pull requests are even better.
Currently the package can only be built for Linux-based systems and 
attempts to create a process for building on Windows using MSYS and
CMake have proven unfruitful. If you would like to give it a go, 
feel free to contact me.
