# https://github.com/whardier/fuchar/blob/master/src/fuchar/__main__.py

# ┏━╸╻ ╻┏━╸╻ ╻┏━┓┏━┓       ┏┳┓┏━┓╻┏┓╻
# ┣╸ ┃ ┃┃  ┣━┫┣━┫┣┳┛       ┃┃┃┣━┫┃┃┗┫
# ╹  ┗━┛┗━╸╹ ╹╹ ╹╹┗╸╹╺━╸╺━╸╹ ╹╹ ╹╹╹ ╹╺━╸╺━╸

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

from argparse import ArgumentParser
from importlib import import_module

from fuchar import fuchar_render


def main():

    parser = ArgumentParser()

    parser.add_argument("-n", "--font-name", type=str, default="fuchar")
    parser.add_argument("-i", "--ignore-missing", action="store_true")
    parser.add_argument("-s", "--prefix-string", type=str, default="")
    parser.add_argument("-e", "--postfix-string", type=str, default="")
    parser.add_argument("-k", "--skinny-whitespace", action="store_true", default="")
    parser.add_argument("string", type=str, nargs="+")

    args = parser.parse_args()

    try:
        font = import_module("fuchar.fonts." + args.font_name)
    except ModuleNotFoundError:
        print("Font not found")
        return

    print(
        fuchar_render(
            " ".join(args.string),
            chars=font.chars,
            prefix=args.prefix_string,
            postfix=args.postfix_string,
            ignore_missing=args.ignore_missing,
            skinny_whitespace=args.skinny_whitespace,
        )
    )


if __name__ == "__main__":
    main()
