from setuptools import setup

import versioneer

setup_args = dict(
    name='sphinx_holoviz_theme',
    version=versioneer.get_version(),
    url="https://github.com/pyviz-dev/sphinx_holoviz_theme",
    description="Theme for building HoloViz sites; best when used with nbsite.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="BSD-3",
    zip_safe=False,
    packages=['sphinx_holoviz_theme'],
    package_data={'sphinx_holoviz_theme': [
        'theme.conf',
        '*.html',
        'includes/*.html',
        'static/css/*.css_t',
        'static/js/*.js',
        'static/images/*.*'
    ]},
    include_package_data=True,
    entry_points = {
        'sphinx.html_themes': [
            'sphinx_holoviz_theme = sphinx_holoviz_theme',
        ]
    },
    python_requires = ">=2.7",

    install_requires =[
        "sphinx"
    ]
)

if __name__=="__main__":
    setup(**setup_args)
