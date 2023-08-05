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
import subprocess
import crema

sys.path.insert(0, os.path.abspath(os.path.join("..", "..")))

try:
    import numpydoc
except ModuleNotFoundError:
    subprocess.run(["pip", "install", "numpydoc"], check=True)


# -- Project information -----------------------------------------------------
project = "crema"
copyright = "2020, Donavan See"
author = "William E. Fondrie, Donavan See, William S. Noble"
version = str(crema.__version__)
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "numpydoc",
    "sphinx_rtd_theme",
    "sphinx.ext.intersphinx",
    "sphinxarg.ext",
    "nbsphinx",
]

nbsphinx_execute = "never"

autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "inherited-members": True,
    "member-order": "bysource",
}

numpydoc_show_class_members = True
numpydoc_show_inherited_class_members = True
numpydoc_attributes_as_param_list = True
intersphinx_mapping = {
    "pandas": ("https://pandas.pydata.org/docs", None),
    "sklearn": ("https://scikit-learn.org/stable", None),
    "numpy": ("https://docs.scipy.org/doc/numpy", None),
    "matplotlib": ("https://matplotlib.org", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
# html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

master_doc = "index"
source_suffix = ".rst"

html_theme_options = {
    "style_nav_header_background": "#343131",
    "logo_only": True,
}

html_css_files = [
    "custom.css",
]

html_logo = "_static/crema_logo_caramel_light.png"
