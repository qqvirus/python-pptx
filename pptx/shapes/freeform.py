# encoding: utf-8

"""Objects related to construction of freeform shapes."""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from collections import Sequence

from pptx.util import lazyproperty


class FreeformBuilder(Sequence):
    """Allows a freeform shape to be specified and created.

    The initial pen position is provided on construction. From there, drawing
    proceeds using successive calls to draw line segments. The freeform shape
    may be closed by calling the :meth:`close` method.

    A shape may have more than one contour, in which case overlapping areas
    are "subtracted". A contour is a sequence of line segments beginning with
    a "move-to" operation. A move-to operation is automatically inserted in
    each new freeform; additional move-to ops can be inserted with the
    `.move_to()` method.
    """

    def __init__(self, shapes, start_x, start_y, x_scale, y_scale):
        super(FreeformBuilder, self).__init__()
        self._shapes = shapes
        self._start_x = start_x
        self._start_y = start_y
        self._x_scale = x_scale
        self._y_scale = y_scale

    def __getitem__(self, idx):
        return self._drawing_operations.__getitem__(idx)

    def __iter__(self):
        return self._drawing_operations.__iter__()

    def __len__(self):
        return self._drawing_operations.__len__()

    @classmethod
    def new(cls, shapes, start_x, start_y, x_scale, y_scale):
        """Return a new |FreeformBuilder| object.

        The initial pen location is specified (in local coordinates) by
        (*start_x*, *start_y*).
        """
        return cls(
            shapes, int(round(start_x)), int(round(start_y)),
            x_scale, y_scale
        )

    def add_line_segments(self, vertices, close=True):
        """Add a straight line segment to each point in *vertices*.

        *vertices* must be an iterable of (x, y) pairs (2-tuples). Each x and
        y value is rounded to the nearest integer before use. The optional
        *close* parameter determines whether the resulting contour is
        *closed* or left *open*.

        Returns this |FreeformBuilder| object so it can be used in chained
        calls.
        """
        for x, y in vertices:
            self._add_line_segment(x, y)
        if close:
            self._add_close()
        return self

    def _add_close(self):
        """Add a close |_Close| operation to the drawing sequence."""
        raise NotImplementedError

    def _add_line_segment(self, x, y):
        """Add a |_LineSegment| operation to the drawing sequence."""
        raise NotImplementedError

    @lazyproperty
    def _drawing_operations(self):
        """Return the sequence of drawing operation objects for freeform."""
        return []