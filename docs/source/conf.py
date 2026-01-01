# -- Project information -----------------------------------------------------
project = "python-gerritclient"
copyright = "2017-2025, Vitalii Kulanov"
author = "Vitalii Kulanov"

# The version info for the project
release = "1.0.0"
version = "1.0"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "cliff.sphinxext",
]

# Options for cliff.sphinxext plugin
autoprogram_cliff_application = "gerrit"

# The suffix of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = []

# Intersphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- Options for LaTeX output ------------------------------------------------
latex_documents = [
    (
        master_doc,
        "python-gerritclient.tex",
        "python-gerritclient Documentation",
        author,
        "manual",
    ),
]
