# cython: languagelevel=3
# cython: profile=True
'''Generate line of sight'''

# I'm not using this function yet? I think this was meant for something else.
def get_line(start, end):
    x0, y0 = start
    x1, y1 = end
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2 * dy - dx
    y = 0

    for x in range(dx + 1):
        yield x0 + x * xx + y * yx, y0 + x * xy + y * yy
        if D > 0:
            y += 1
            D -= dx
        D += dy


MULT = [
    [1, 0, 0, -1, -1, 0, 0, 1],
    [0, 1, -1, 0, 0, -1, 1, 0],
    [0, 1, 1, 0, 0, -1, -1, 0],
    [1, 0, 0, 1, -1, 0, 0, -1],
]

cdef _get_visible_points(vantage_point, allows_light, max_distance):
    los_cache = set()
    los_cache.add(vantage_point)
    for region in range(8):
        _cast_light(
            los_cache, allows_light,
            vantage_point[0], vantage_point[1], 1, 1.0, 0.0, max_distance,
            MULT[0][region], MULT[1][region],
            MULT[2][region], MULT[3][region])

    return los_cache

def get_visible_points(vantage_point, allows_light, max_distance=30):
    return _get_visible_points(vantage_point, allows_light, max_distance)


cdef _cast_light(los_cache, allows_light, int cx, int cy, int row, float start, float end, int radius,
               int xx, int xy, int yx, int yy):
    cdef int radius_squared
    cdef int dx, dy
    cdef int X, Y
    cdef float l_slope, r_slope, new_start
    cdef bint blocked
    cdef int j = 0

    if start < end:
        return

    radius_squared = radius * radius

    for j in range(row, radius + 1):
        dx, dy = -j - 1, -j
        blocked = False

        while dx <= 0:
            dx += 1
            X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
            point = (X, Y)
            l_slope, r_slope = (dx - 0.5) / (dy + 0.5), (dx + 0.5) / (dy - 0.5)
            if start < r_slope:
                continue
            elif end > l_slope:
                break
            else:
                if dx * dx + dy * dy < radius_squared:
                    los_cache.add(point)
                if blocked:
                    if not allows_light(point):
                        new_start = r_slope
                        continue
                    else:
                        blocked = False
                        start = new_start
                else:
                    if not allows_light(point) and j < radius:
                        blocked = True
                        _cast_light(
                            los_cache, allows_light,
                            cx, cy, j + 1, start, l_slope,
                            radius, xx, xy, yx, yy)
                        new_start = r_slope
        if blocked:
            break
