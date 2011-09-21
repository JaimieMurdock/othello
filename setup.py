# chardet's setup.py
from distutils.core import setup
import setuptools
setup(
    name = "othello",
    packages = ["othello", "othello.engines"],
    version = "1.0b1",
    description = "Implementation of Othello/Reversi",
    author = "Jaimie Murdock and Eric P. Nichols",
    url = "http://www.github.com/JaimieMurdock/othello",
    download_url = "http://www.github.com/JaimieMurdock/othello",
    keywords = ["machine learning", "games"],
    classifiers = [
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Operating System :: OS Independent",
        "Topic :: Education"
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
        ]
)
