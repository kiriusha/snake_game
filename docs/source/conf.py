import os
import sys

sys.path.insert(0, os.path.abspath('../../'))

project = 'Змейка'
copyright = '2024, Ваше имя'
author = 'Ваше имя'
release = '1.0'
language = 'ru'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
templates_path = ['_templates']
exclude_patterns = []
