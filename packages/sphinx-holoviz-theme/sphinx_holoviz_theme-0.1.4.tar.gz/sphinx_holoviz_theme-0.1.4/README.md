# sphinx_holoviz_theme: Theme for building HoloViz sites

|    |    |
| --- | --- |
| Build Status | [![Linux/MacOS Build Status](https://travis-ci.org/pyviz-dev/sphinx_holoviz_theme.svg?branch=master)](https://travis-ci.org/pyviz-dev/sphinx_holoviz_theme) |
| Latest dev release | [![Github tag](https://img.shields.io/github/tag/pyviz-dev/sphinx_holoviz_theme.svg?label=tag&colorB=11ccbb)](https://github.com/pyviz-dev/sphinx_holoviz_theme/tags) |
| Latest release | [![Github release](https://img.shields.io/github/release/pyviz-dev/sphinx_holoviz_theme.svg?label=tag&colorB=11ccbb)](https://github.com/pyviz-dev/sphinx_holoviz_theme/releases) [![PyPI version](https://img.shields.io/pypi/v/sphinx_holoviz_theme.svg?colorB=cc77dd)](https://pypi.python.org/pypi/sphinx_holoviz_theme) [![sphinx_holoviz_theme version](https://img.shields.io/conda/v/pyviz/sphinx_holoviz_theme.svg?colorB=4488ff&style=flat)](https://anaconda.org/pyviz/sphinx_holoviz_theme) [![conda-forge version](https://img.shields.io/conda/v/conda-forge/sphinx_holoviz_theme.svg?label=conda%7Cconda-forge&colorB=4488ff)](https://anaconda.org/conda-forge/sphinx_holoviz_theme) |

## What is it?
sphinx_holoviz_theme is the theme that is used when building sites in the
[HoloViz](https://holoviz.org) ecosystem. This theme is best used in conjunction
with [nbsite](https://github/pyviz-dev/nbsite). See the [nbsite docs](https://nbsite.pyviz.org)
for examples.

## How to use

To use this theme: `pip/conda install sphinx_holoviz_theme` and set html_theme to sphinx_holoviz_theme. To control the look and feel, change html_theme_options in conf.py:

```python
html_static_path += ['_static']
html_theme = 'sphinx_holoviz_theme'
html_theme_options = {
    'custom_css': 'site.css',
    'logo': 'nbsite-logo.png',
    'favicon': 'favicon.ico',
    'primary_color': '#F16A25',
    'primary_color_dark': '#B5501C',
    'secondary_color': '#F5C33C',
    'second_nav': False,
}
```

 - logo and favicon: provide paths relative to html_static_path (doc/_static by default)
 - primary_color, primary_color_dark and secondary_color: control the colors that the
   website uses for header, nav, links... These can be css named colors, or hex colors.
 - second_nav: Boolean indicating whether to use a second nav bar.
 - custom_css: path relative to html_static_path overriding styles.
   Styles come first from the theme's main.css_t, which is populated with the
   colors options, then extended/overridden by your site's own css.

**NOTE:** Only use the custom_css to overwrite small pieces of the css not to make
general improvements. If you have general improvements, please open a PR on the this repo.



## About HoloViz

sphinx_holoviz_theme is part of the HoloViz ecosystem for making high-level tools to simplify
visualization in Python. See [holoviz.org](http://holoviz.org) for related packages that you
can use with sphinx_holoviz_theme and [status.pyviz.org](http://status.pyviz.org) for the
current status of each HoloViz project.
