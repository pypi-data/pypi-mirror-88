import numpy as np
from scipy.stats import gaussian_kde as kde


class Bounded_2d_kde(kde):
    """Class to generate a two-dimensional KDE for a probability distribution
    functon that exists on a bounded domain
    """
    def __init__(self, pts, xlow=None, xhigh=None, ylow=None, yhigh=None,
                 *args, **kwargs):
        pts = np.atleast_2d(pts)
        assert pts.ndim == 2, 'Bounded_kde can only be two-dimensional'
        super(Bounded_2d_kde, self).__init__(pts, *args, **kwargs)
        self._xlow = xlow
        self._xhigh = xhigh
        self._ylow = ylow
        self._yhigh = yhigh

    @property
    def xlow(self):
        """The lower bound of the x domain
        """
        return self._xlow

    @property
    def xhigh(self):
        """The upper bound of the x domain
        """
        return self._xhigh

    @property
    def ylow(self):
        """The lower bound of the y domain
        """
        return self._ylow

    @property
    def yhigh(self):
        """The upper bound of the y domain
        """
        return self._yhigh

    def evaluate(self, pts):
        """Return an estimate of the density evaluated at the given
        points."""
        pts = np.atleast_2d(pts)
        assert pts.ndim == 2, 'points must be two-dimensional'
        if pts.shape[0] != 2 and pts.shape[1] == 2:
            pts = pts.T

        x, y = pts
        pdf = super(Bounded_2d_kde, self).evaluate(pts)
        if self.xlow is not None:
            pdf += super(Bounded_2d_kde, self).evaluate([2 * self.xlow - x, y])

        if self.xhigh is not None:
            pdf += super(Bounded_2d_kde, self).evaluate([2 * self.xhigh - x, y])

        if self.ylow is not None:
            pdf += super(Bounded_2d_kde, self).evaluate([x, 2 * self.ylow - y])

        if self.yhigh is not None:
            pdf += super(Bounded_2d_kde, self).evaluate([x, 2 * self.yhigh - y])

        if self.xlow is not None:
            if self.ylow is not None:
                pdf += super(Bounded_2d_kde, self).evaluate(
                    [2 * self.xlow - x, 2 * self.ylow - y])

            if self.yhigh is not None:
                pdf += super(Bounded_2d_kde, self).evaluate(
                    [2 * self.xlow - x, 2 * self.yhigh - y])

        if self.xhigh is not None:
            if self.ylow is not None:
                pdf += super(Bounded_2d_kde, self).evaluate(
                    [2 * self.xhigh - x, 2 * self.ylow - y])
            if self.yhigh is not None:
                pdf += super(Bounded_2d_kde, self).evaluate(
                    [2 * self.xhigh - x, 2 * self.yhigh - y])
        return pdf

    def __call__(self, pts):
        pts = np.atleast_2d(pts)
        if pts.shape[0] != 2 and pts.shape[1] == 2:
            pts = pts.T

        out_of_bounds = np.zeros(pts.T.shape[0], dtype='bool')

        if self.xlow is not None:
            out_of_bounds[pts.T[:, 0] < self.xlow] = True
        if self.xhigh is not None:
            out_of_bounds[pts.T[:, 0] > self.xhigh] = True
        if self.ylow is not None:
            out_of_bounds[pts.T[:, 1] < self.ylow] = True
        if self.yhigh is not None:
            out_of_bounds[pts.T[:, 1] > self.yhigh] = True

        results = self.evaluate(pts)
        results[out_of_bounds] = 0.
        return results
