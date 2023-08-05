# https://github.com/whardier/fuchar/blob/master/src/fuchar/__init__.py

# ┏━╸╻ ╻┏━╸╻ ╻┏━┓┏━┓       ╻┏┓╻╻╺┳╸
# ┣╸ ┃ ┃┃  ┣━┫┣━┫┣┳┛       ┃┃┗┫┃ ┃
# ╹  ┗━┛┗━╸╹ ╹╹ ╹╹┗╸╹╺━╸╺━╸╹╹ ╹╹ ╹ ╺━╸╺━╸

# SPDX-License-Identifier: MIT

# MIT License

# Copyright (c) 2020 Shane R. Spencer

# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
from typing import Dict, List

__all__ = ["render_string"]


def fuchar_render(
    s: str,
    chars: Dict[str, List[str]],
    newline: str = os.linesep,
    prefix: str = "",
    postfix: str = "",
    ignore_missing: bool = False,
    skinny_whitespace: bool = False,
) -> str:

    line_0 = prefix
    line_1 = prefix
    line_2 = prefix

    for c in s:

        if c not in chars:
            if ignore_missing:
                char = chars.get(" ", ("", "", ""))
            else:
                char = (" ", " ", c)
        else:
            char = chars[c]

        if c == " " and skinny_whitespace:
            char = (" ", " ", " ")

        line_0 = "".join((line_0, char[0]))
        line_1 = "".join((line_1, char[1]))
        line_2 = "".join((line_2, char[2]))

    line_0 = line_0 + postfix
    line_1 = line_1 + postfix
    line_2 = line_2 + postfix

    return newline.join((line_0, line_1, line_2))
