# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""The package dsl (domain-specific language) is a set of decorators for component manipulations.

You can utilize this package to build :class:`azure.ml.component.Component` and
:class:`azure.ml.component.Pipeline`.
"""

from ._component.component import _component
from ._pipeline import pipeline

__all__ = [
    '_component',
    'pipeline',
]
