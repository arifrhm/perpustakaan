import sys
import os


# Menambahkan jalur folder root (folder di atas folder tests) ke sys.path
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_folder)