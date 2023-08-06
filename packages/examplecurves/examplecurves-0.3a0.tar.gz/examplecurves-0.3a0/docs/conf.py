# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

module_path = os.path.abspath('../.')
sys.path.insert(0, module_path)


# -- Project information -----------------------------------------------------

project = 'examplecurves'
copyright = '2020, David Scheliga'
author = 'David Scheliga'

# The full version, including alpha/beta/rc tags
release = "0.2a0"


# -- General configuration ---------------------------------------------------

# Read-the-docs expects a 'contents.rst' if not set
master_doc = 'index'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'matplotlib.sphinxext.plot_directive',
    'sphinx.ext.autodoc',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx_rtd_theme',
    'sphinx.ext.doctest'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# autodoc configuration
autoclass_content = "both"

# autosummary configuration
autosummary_generate=True

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Jupyter notebooks with the suffix .ipynb.txt are normally not very useful, so if you
# want to avoid the additional suffix, set html_sourcelink_suffix to the empty string:
html_sourcelink_suffix = ''

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {
    'canonical_url': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': 'white',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}