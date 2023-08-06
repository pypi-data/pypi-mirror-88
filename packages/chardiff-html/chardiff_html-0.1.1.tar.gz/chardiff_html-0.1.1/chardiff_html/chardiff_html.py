import difflib


def chardiff_html(
    str1: str,
    str2: str,
    del_font_color: str = "red",
    del_background_color: str = "mistyrose",
    ins_font_color: str = "green",
    ins_background_color: str = "#e0ffe5",
    **kwargs,
):
    """
    Notes:
        Colors can be specified by color name or color code.
        kwargs are passed to difflib.ndiff
    """
    # State meaning:: ' ': equal, '+': insert, '-': delete
    prev_state, state = " ", " "
    output = ""
    for diff in difflib.ndiff(str1, str2, **kwargs):
        prev_state = state
        state, _, char = diff

        if state == prev_state:
            output += char
            continue

        if prev_state != " ":
            output += "</span>"

        if state == "+":
            output += f'<span style="color: {ins_font_color}; background-color: {ins_background_color}">'
        elif state == "-":
            output += f'<span style="color: {del_font_color}; background-color: {del_background_color}">'
        output += char

    if state != " ":
        output += "</span>"
    return output


class ChardiffJupyter:
    def __init__(self, html):
        self.html = html

    def __str__(self):
        return self.html

    def _repr_html_(self):
        return self.html


def chardiff_jupyter(*args, **kwargs):
    html = chardiff_html(*args, **kwargs)
    return ChardiffJupyter(html)
