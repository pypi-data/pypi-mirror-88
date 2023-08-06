# https://github.com/whardier/objectify/blob/master/src/objectify/__init__.py

# ┏━┓┏┓  ┏┓┏━╸┏━╸╺┳╸╻┏━╸╻ ╻       ╻┏┓╻╻╺┳╸
# ┃ ┃┣┻┓  ┃┣╸ ┃   ┃ ┃┣╸ ┗┳┛       ┃┃┗┫┃ ┃
# ┗━┛┗━┛┗━┛┗━╸┗━╸ ╹ ╹╹   ╹ ╹╺━╸╺━╸╹╹ ╹╹ ╹ ╺━╸╺━╸

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


from typing import Any, Iterator, Optional, Tuple


def obj_collapse_iter(
    obj: Any, canonical: bool = True, _path: Optional[Tuple[Any, ...]] = None
) -> Iterator[Tuple[Any, Any]]:

    if not _path:
        _path = tuple()

    __path: Tuple[Any, ...] = tuple()

    if isinstance(obj, dict):

        if canonical:
            __path = (obj.__class__,)

        for _key, _obj in obj.items():

            if canonical:
                __path = __path + (_key, _obj.__class__)
            else:
                __path = __path + (_key,)

            for _next in obj_collapse_iter(
                _obj, canonical=canonical, _path=_path + __path
            ):
                yield _next

    elif isinstance(obj, list) or isinstance(obj, set):
        for _enumerator, _obj in enumerate(obj):

            if not canonical:
                __path = (_enumerator,)
            else:
                __path = tuple()

            for _next in obj_collapse_iter(
                _obj, canonical=canonical, _path=_path + __path
            ):
                yield _next

    else:
        yield (_path, obj)


def obj_collapse(obj: Any, *args, **kwargs):
    return list(obj_collapse_iter(obj, *args, **kwargs))


__all__ = [
    "obj_collapse_iter",
    "obj_collapse",
]
