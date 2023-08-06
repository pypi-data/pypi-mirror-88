# chardiff_html

Python package for visualizing char diff by colorized html

## Install

```
pip install chardiff_html
```

## Usage

This package outputs HTML string displays char diffs, so you can use this on Jupyter notebook or [Streamlit](https://www.streamlit.io)

### Jupyter Exmaple

```python
from chardiff_html import chardiff_jupyter
chardiff_jupyter('hoge', 'hag')
```

[![Image from Gyazo](https://i.gyazo.com/653da7277dfcb1b238ae81fbce341846.png)](https://gyazo.com/653da7277dfcb1b238ae81fbce341846)

### Streamlit Example

```python
import streamlit as st
from chardiff_html import chardiff_html

"### Input"
str1 = st.text_area("Original Sentence", "hoge")
str2 = st.text_area("New Sentence", "hag")
diff = chardiff_html(str1, str2)
# >>> print(diff)
# 'h<span style="color: red; background-color: mistyrose">o</span><span style="color: green; background-color: #e0ffe5">a</span>g<span style="color: red; background-color: mistyrose">e</span>'

"### Diffs"
st.markdown(
    diff, unsafe_allow_html=True,
)
```

[![Image from Gyazo](https://i.gyazo.com/96f9369d0815a393b91d2aa544c51eb3.png)](https://gyazo.com/96f9369d0815a393b91d2aa544c51eb3)
