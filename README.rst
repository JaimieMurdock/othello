Othello
===========
This module is an implementation of the game Othello/Reversi in Python. It was
developed in Spring 2008 by `Eric P. Nichols <http://ericpnichols.com/>`_ for
the Fall 2008 version of CSCI-B351/COGS-Q351 Intro to Artificial Intelligence at
Indiana Univeristy. The original idea was from `John Paxton <http://www.cs.montana.edu/paxton/>`_'s 
similar AI course at Montana State University, Bozeman. The project was refactored and migrated to 
Python 2.7 by `Jaimie Murdock <http://jamram.net/>`_ in Fall 2011.

This is meant to be an educational open-source project. We welcome forking our
repo and developing additional game engines, and encourage pull requests for 
well-documented examples. 

Additional ideas for contribution:

*   Several TODO comments in __init__.py
*   Tournament infrastructure (to be implemented in tournament.py)
*   GUI for visualization of games with round-stepping functionality.
*   Standardized logging and log readers for replay.

Usage
----------
human - random game
    ``python __init__.py human random``
human - human game
    ``python __init__.py human human``
