import atexit
import os
import sys
from setuptools import setup
import setuptools
from setuptools.command.install import install
from tkinter import simpledialog
from tkinter import *

root = Tk()
root.withdraw()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("LICENCE", "r", encoding="utf-8") as fh:
    licence = fh.read()

class AcecptLicence(simpledialog.Dialog):
    def body(self,master):
        Label(master,text=licence)
    def buttonbox(self):
        box = Frame(self)

        w = Button(box, text="Acecpt", width=10, command=self.destroy, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        e = Button(box, text="Do Not Acecpt", width=10, command=exit)
        e.pack(side=LEFT, padx=5, pady=5)

        box.pack()


class CustomInstall(install):
    def run(self):
        def _post_install():
            def find_module_path():
                my_name = "PYCDef"
                for p in sys.path:
                    if os.path.isdir(p) and my_name in os.listdir(p):
                        return os.path.join(p, my_name)
            install_path = find_module_path()

            AcecptLicence(root,title="Acecpt Licence?")
            print("""
_____            _____  _______        
|  __ \         / ____||__   __|       
| |__) | _   _ | |        | |    _   _ 
|  ___/ | | | || |        | |   | | | |
| |     | |_| || |____    | |   | |_| |
|_|      \__, | \_____|   |_|    \__, |
          __/ |                   __/ |
         |___/                   |___/ 
            """)

        atexit.register(_post_install)
        install.run(self)

setup(
    cmdclass={"install":CustomInstall},
    name="PyCty",
    version="1.0.0",
    author="Harsha Addanki",
    author_email="none@none.org",
    description="Python C Types",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.5',
)