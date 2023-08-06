import os 

__all__ = ['gui','backend']
__version__ = '0.0.1'
__author__ = 'Derek Fujimoto'

# ~ icon_path = os.path.join(os.path.dirname(__file__),'images','icon.gif')

from rigur.gui.rigur import rigur

def main():
    rigur()
