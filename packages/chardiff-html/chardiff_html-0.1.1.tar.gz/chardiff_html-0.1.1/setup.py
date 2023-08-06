# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chardiff_html']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chardiff-html',
    'version': '0.1.1',
    'description': '',
    'long_description': '# chardiff_html\n\nPython package for visualizing char diff by colorized html\n\n## Install\n\n```\npip install chardiff_html\n```\n\n## Usage\n\nThis package outputs HTML string displays char diffs, so you can use this on Jupyter notebook or [Streamlit](https://www.streamlit.io)\n\n### Jupyter Exmaple\n\n```python\nfrom chardiff_html import chardiff_jupyter\nchardiff_jupyter(\'hoge\', \'hag\')\n```\n\n[![Image from Gyazo](https://i.gyazo.com/653da7277dfcb1b238ae81fbce341846.png)](https://gyazo.com/653da7277dfcb1b238ae81fbce341846)\n\n### Streamlit Example\n\n```python\nimport streamlit as st\nfrom chardiff_html import chardiff_html\n\n"### Input"\nstr1 = st.text_area("Original Sentence", "hoge")\nstr2 = st.text_area("New Sentence", "hag")\ndiff = chardiff_html(str1, str2)\n# >>> print(diff)\n# \'h<span style="color: red; background-color: mistyrose">o</span><span style="color: green; background-color: #e0ffe5">a</span>g<span style="color: red; background-color: mistyrose">e</span>\'\n\n"### Diffs"\nst.markdown(\n    diff, unsafe_allow_html=True,\n)\n```\n\n[![Image from Gyazo](https://i.gyazo.com/96f9369d0815a393b91d2aa544c51eb3.png)](https://gyazo.com/96f9369d0815a393b91d2aa544c51eb3)\n',
    'author': 'Tomoaki Nakamura',
    'author_email': 'tyo_yo@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tyo-yo/chardiff_html',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
