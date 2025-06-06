# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
import os
import sys
from importlib import metadata
sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, '/home/gilles/documents/repositories/virtual/venv/lib/python3.13/site-packages')

# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'dawgdad'
copyright = '2025, Gilles Pilon'
author = 'Gilles Pilon'
# version = metadata.version(project)
# release = version
release = '1.0.8'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]
# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:

# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document
master_doc = 'index'

# autodoc_dirs = ['../../dawgdad']
# autodoc_default_flags = ['members', 'undoc-members']
# autodoc_member_order = 'bysource'
# autoclass_hierarchy = 'include'

# templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

verbosity = 2
