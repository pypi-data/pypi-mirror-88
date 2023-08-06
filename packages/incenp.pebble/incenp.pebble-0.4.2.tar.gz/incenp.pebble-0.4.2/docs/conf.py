# -*- coding: utf-8 -*-

# -- General configuration ------------------------------------------------

source_suffix = '.rst'
master_doc = 'index'

copyright = u'2019 Damien Goutte-Gattat'
author = u'Damien Goutte-Gattat <dgouttegattat@incenp.org>'

language = 'en'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'

extensions = ['sphinx.ext.intersphinx']
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}


# -- Options for HTML output ----------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']


# -- Options for LaTeX output ---------------------------------------------

latex_engine = 'lualatex'

latex_elements = {
        'papersize': 'a4paper',
        'pointsize': '10pt'
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'Pebble.tex', u'Pebble Documentation',
     u'Damien Goutte-Gattat', 'manual'),
]


# -- Options for manual page output ---------------------------------------

man_pages = [
    (master_doc, 'pebble', u'Pebble Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
    (master_doc, 'Pebble', u'Pebble Documentation',
     author, 'Pebble', 'One line description of project.',
     'Miscellaneous'),
]
