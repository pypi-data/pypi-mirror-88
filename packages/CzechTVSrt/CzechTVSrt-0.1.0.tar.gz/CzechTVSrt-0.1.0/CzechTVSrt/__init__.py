# -*- coding: utf-8 -*-
"""Scraper for Czech TV subtitles.
 
Sources:
    * https://www.ceskatelevize.cz/ivysilani
Todo:
"""

import pkg_resources

from .czechtv import *

try:
    __version__ = pkg_resources.get_distribution("CzechTVSrt").version
except:
    __version__ = None
