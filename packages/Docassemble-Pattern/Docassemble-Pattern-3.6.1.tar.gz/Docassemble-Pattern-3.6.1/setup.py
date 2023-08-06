#### PATTERN #######################################################################################

from __future__ import print_function

import sys
import os

from io import open

from setuptools import setup

#from docassemble_pattern import __version__

#---------------------------------------------------------------------------------------------------
# "python setup.py zip" will create the zipped distribution and checksum.

# if sys.argv[-1] == "zip":

#     import zipfile
#     import hashlib
#     import re

#     n = "docassemble_pattern-%s.zip" % __version__
#     p = os.path.join(os.path.dirname(os.path.realpath(__file__)))
#     z = zipfile.ZipFile(os.path.join(p, "..", n), "w", zipfile.ZIP_DEFLATED)
#     for root, folders, files in os.walk(p):
#         for f in files:
#             f = os.path.join(root, f)
#             # Exclude private settings.
#             if f.endswith(os.path.join("web", "api.py")):
#                 d = "#--- PRIVATE"
#                 s = open(f, "r", encoding="utf-8").read().split(d)
#                 x = open(f, "w", encoding="utf-8")
#                 x.write(s[0])
#                 x.close()
#             # Exclude revision history (.git).
#             # Exclude development files (.dev).
#             if not re.search(r"\.DS|\.git[^i]|\.pyc|\.dev|tmp", f):
#                 z.write(f, os.path.join("docassemble_pattern-" + __version__, os.path.relpath(f, p)))
#             if f.endswith(os.path.join("web", "api.py")):
#                 x = open(f, "w", encoding="utf-8")
#                 x.write(d.join(s))
#                 x.close()
#     z.close()
#     print(n)
#     print(hashlib.sha256(open(z.filename).read()).hexdigest())
#     sys.exit(0)

#---------------------------------------------------------------------------------------------------
# "python setup.py install" will install /docassemble_pattern in /site-packages.

setup(
            name = "Docassemble-Pattern",
         version = "3.6.1",
     description = "Fork of pattern for use with docassemble",
         license = "BSD",
          author = "Tom De Smedt, Jonathan Pyle",
    author_email = "jhpyle@gmail.com",
             url = "https://docassemble.org",
        packages = [
        "docassemble_pattern",
        "docassemble_pattern.text",
        "docassemble_pattern.text.de",
        "docassemble_pattern.text.en",
        "docassemble_pattern.text.en.wordlist",
        "docassemble_pattern.text.en.wordnet",
        "docassemble_pattern.text.ru",
        "docassemble_pattern.text.ru.wordlist",
        "docassemble_pattern.text.es",
        "docassemble_pattern.text.fr",
        "docassemble_pattern.text.it",
        "docassemble_pattern.text.nl",
        "docassemble_pattern.vector",
        "docassemble_pattern.vector.svm"
    ],
    package_data = {
        "docassemble_pattern.text.de"         : ["*.txt", "*.xml"],
        "docassemble_pattern.text.en"         : ["*.txt", "*.xml", "*.slp"],
        "docassemble_pattern.text.en.wordlist": ["*.txt"],
        "docassemble_pattern.text.en.wordnet" : ["*.txt", "dict/*"],
        "docassemble_pattern.text.ru": ["*.txt", "*.xml", "*.slp"],
        "docassemble_pattern.text.ru.wordlist": ["*.txt"],
        "docassemble_pattern.text.es"         : ["*.txt", "*.xml"],
        "docassemble_pattern.text.fr"         : ["*.txt", "*.xml"],
        "docassemble_pattern.text.it"         : ["*.txt", "*.xml"],
        "docassemble_pattern.text.nl"         : ["*.txt", "*.xml"],
        "docassemble_pattern.vector"          : ["*.txt"],
        "docassemble_pattern.vector.svm"      : ["*.txt"]
    },
    py_modules = [],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: Dutch",
        "Natural Language :: English",
        "Natural Language :: French",
        "Natural Language :: German",
        "Natural Language :: Italian",
        "Natural Language :: Spanish",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic"
    ],
    install_requires = [
        "future==0.18.2",
        "numpy==1.19.4",
        "scipy==1.5.4",
        "nltk==3.5"
    ],
    zip_safe = False
)
