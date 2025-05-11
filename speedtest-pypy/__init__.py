"""
SpeedTest++ - Python Implementation
A command-line tool for testing internet connection performance
"""

from .core import SpeedTest
from .models import ServerInfo
from .network import NetworkTester

__version__ = "1.0.0"
__author__ = "cociweb"
__license__ = "MIT"

__all__ = ["SpeedTest", "ServerInfo", "NetworkTester"]