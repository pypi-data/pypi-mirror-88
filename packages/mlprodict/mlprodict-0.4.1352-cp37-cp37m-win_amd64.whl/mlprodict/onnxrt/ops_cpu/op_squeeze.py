# -*- encoding: utf-8 -*-
# pylint: disable=E0203,E1101,C0111
"""
@file
@brief Runtime operator.
"""
import numpy
from ._op import OpRunUnaryNum


class Squeeze(OpRunUnaryNum):

    atts = {'axes': [], 'keepdims': 1}

    def __init__(self, onnx_node, desc=None, **options):
        OpRunUnaryNum.__init__(self, onnx_node, desc=desc,
                               expected_attributes=Squeeze.atts,
                               **options)
        if isinstance(self.axes, numpy.ndarray):
            self.axes = tuple(self.axes)
        elif self.axes in [[], tuple()]:
            self.axes = None
        elif isinstance(self.axes, list):
            self.axes = tuple(self.axes)

    def _run(self, data):  # pylint: disable=W0221
        if isinstance(self.axes, (tuple, list)):
            sq = data
            for a in reversed(self.axes):
                sq = numpy.squeeze(sq, axis=a)
        else:
            sq = numpy.squeeze(data, axis=self.axes)
        return (sq, )

    def _infer_shapes(self, x):  # pylint: disable=W0221
        return (x.squeeze(axis=self.axes), )
