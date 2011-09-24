# TODO: Import to the CheeseShop.
from distutils.core import setup
import setuptools
setup(
    name = "othello",
    packages = ["othello", "othello.engines"],
    version = "1.0b1",
    description = "Implementation of Othello/Reversi for AI course instruction",
    author = "Jaimie Murdock and Eric P. Nichols",
    url = "https://github.com/JaimieMurdock/othello",
    download_url = "https://github.com/JaimieMurdock/othello",
    keywords = ["machine learning", "games"],
    classifiers = [
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Education"
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
        ]
)
