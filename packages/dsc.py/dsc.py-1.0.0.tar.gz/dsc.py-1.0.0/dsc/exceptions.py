# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2020 wulf

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__all__ = (
    'Unauthorized',
    'BadRequest',
    'RequestEntityTooLarge',
    'Forbidden',
    'NotFound',
    'RateLimitedError'
)


class Unauthorized(ConnectionRefusedError):
    """The token passed is invalid"""


class BadRequest(ConnectionError):
    """The request was malformed"""


class RequestEntityTooLarge(ConnectionRefusedError):
    """The slug passed was too long"""


class Forbidden(ConnectionRefusedError):
    """The user is requesting premium features without actually having premium, or the token was invalid"""


class NotFound(AttributeError):
    """The link couldn't be found"""


class RateLimitedError(RuntimeError):
    """A long rate-limit has been exhausted."""

