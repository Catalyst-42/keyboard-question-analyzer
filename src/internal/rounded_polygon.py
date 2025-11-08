import numpy as np
from matplotlib import patches, path
from matplotlib.transforms import Bbox


class RoundedPolygon(patches.PathPatch):
    def __init__(self, xy, pad=0.3, **kwargs):
        self.xy = np.array(xy)
        self.pad = pad

        p = path.Path(*self.__round(xy=xy, pad=pad))
        super().__init__(path=p, **kwargs)

    def __round(self, xy, pad):
        n = len(xy)

        for i in range(0, n):
            x0, x1, x2 = np.atleast_1d(xy[i - 1], xy[i], xy[(i + 1) % n])

            d01, d12 = x1 - x0, x2 - x1
            d01, d12 = d01 / np.linalg.norm(d01), d12 / np.linalg.norm(d12)

            x00 = x0 + pad * d01
            x01 = x1 - pad * d01
            x10 = x1 + pad * d12
            # x11 = x2 - pad * d12

            if i == 0:
                verts = [x00, x01, x1, x10]
            else:
                verts += [x01, x1, x10]
                
        codes = [path.Path.MOVETO] + n * [path.Path.LINETO, path.Path.CURVE3, path.Path.CURVE3]

        return np.atleast_1d(verts, codes)

    def get_bbox(self):
        x_coords = self.xy[:, 0]
        y_coords = self.xy[:, 1]
        x0, x1 = np.min(x_coords), np.max(x_coords)
        y0, y1 = np.min(y_coords), np.max(y_coords)

        return Bbox.from_bounds(x0, y0, x1 - x0, y1 - y0)
