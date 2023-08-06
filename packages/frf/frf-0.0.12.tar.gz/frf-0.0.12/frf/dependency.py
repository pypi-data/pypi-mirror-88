"""Declares various functions to inject dependencies."""
import ioc

from fastapi import Depends


def Injected(name, *args, **kwargs):
    """Like :func:`fastapi.Depends`, but takes the identifier of a dependency
    that is injected through :mod:`ioc`.
    """
    return Depends(lambda: ioc.require(name), *args, **kwargs)
