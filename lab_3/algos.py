from Point import Point, Pixel, INTENSE_MAX

EPS = 1e-7


def sign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0


def dda(p1: Point, p2: Point, count_steps=False):
    points = list()
    steps = 1
    if p1 == p2:
        p = Pixel(p1.x, p1.y)
        points.append(p)
    else:
        if abs(p1.x - p2.x) >= abs(p1.y - p2.y):
            length = abs(p1.x - p2.x)
        else:
            length = abs(p1.y - p2.y)
        dx = (p2.x - p1.x) / length
        dy = (p2.y - p1.y) / length

        x, y = p1.x, p1.y
        for i in range(int(length) + 1):
            if not count_steps:
                points.append(Pixel(round(x), round(y)))
            elif round(x + dx) != round(x) and round(y + dy) != round(y):
                steps += 1

            x += dx
            y += dy

    if count_steps:
        return steps

    return points


def brez_float(p1: Point, p2: Point, count_steps=False):
    points = list()
    steps = 1
    if p1 == p2:
        p = Pixel(p1.x, p1.y)
        points.append(p)
    else:
        dx = p2.x - p1.x
        dy = p2.y - p1.y

        sx = sign(dx)
        sy = sign(dy)

        dy = abs(dy)
        dx = abs(dx)

        if dy > dx:
            dx, dy = dy, dx
            exchange = 1
        else:
            exchange = 0

        k = dy / dx
        e = k - 0.5
        x = p1.x
        y = p1.y

        last_x = x
        last_y = y

        while x != p2.x or y != p2.y:
            if not count_steps:
                points.append(Pixel(x, y))

            # if e >= 0:
            if abs(e) <= EPS or e > 0:    # e >= 0
                if exchange == 1:
                    x += sx
                else:
                    y += sy
                e -= 1

            if exchange == 0:
                x += sx
            else:
                y += sy
            e += k

            if count_steps:
                if last_x != x and last_y != y:
                    steps += 1
                last_x = x
                last_y = y

    if count_steps:
        return steps
    return points


def brez_int(p1: Point, p2: Point, count_steps=False):
    points = list()
    steps = 1
    if p1 == p2:
        p = Pixel(p1.x, p1.y)
        points.append(p)
    else:
        dx = p2.x - p1.x
        dy = p2.y - p1.y

        sx = sign(dx)
        sy = sign(dy)

        dy = abs(dy)
        dx = abs(dx)

        if dy > dx:
            dx, dy = dy, dx
            exchange = 1
        else:
            exchange = 0

        e = 2 * dy - dx
        x = p1.x
        y = p1.y

        last_x = x
        last_y = y

        while x != p2.x or y != p2.y:
            if not count_steps:
                points.append(Pixel(x, y))

            if e >= 0:
                if exchange == 1:
                    x += sx
                else:
                    y += sy
                e -= 2 * dx  # float: (e -= 1)

            if exchange == 0:
                x += sx
            else:
                y += sy
            e += 2 * dy  # float: (e += k)

            if count_steps:
                if last_x != x and last_y != y:
                    steps += 1
                last_x = x
                last_y = y

        if count_steps:
            return steps
    return points


def brez_smooth(p1: Point, p2: Point, count_steps=False):
    points = list()
    steps = 1
    if p1 == p2:
        p = Pixel(p1.x, p1.y)
        points.append(p)
    else:
        dx = p2.x - p1.x
        dy = p2.y - p1.y

        sx = sign(dx)
        sy = sign(dy)

        dy = abs(dy)
        dx = abs(dx)

        if dy > dx:
            dx, dy = dy, dx
            exchange = 1
        else:
            exchange = 0

        k = dy / dx * INTENSE_MAX
        e = INTENSE_MAX / 2
        w = INTENSE_MAX - k
        x = p1.x
        y = p1.y

        last_x = x
        last_y = y

        while x != p2.x or y != p2.y:
            if not count_steps:
                points.append(Pixel(x, y, round(e)))

            if e < w:
                if exchange == 0:
                    x += sx
                else:
                    y += sy
                e += k
            else:
                x += sx
                y += sy
                e -= w

            if count_steps:
                if last_x != x and last_y != y:
                    steps += 1
                last_x = x
                last_y = y

    if count_steps:
        return steps
    return points


def wu(p1: Point, p2: Point, count_steps=False):
    points = list()
    steps = 1
    if p1 == p2:
        p = Pixel(p1.x, p1.y)
        points.append(p)
    else:
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        exchange = abs(y2 - y1) > abs(x2 - x1)

        if exchange:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0:
            k = 1
        else:
            k = dy / dx

        # first endpoint
        xend = round(x1)
        yend = y1 + k * (xend - x1)
        xpx1 = xend
        y = yend + k

        # second endpoint
        xend = int(x2 + 0.5)
        xpx2 = xend

        last_x = xpx1
        last_y = y1

        if exchange:
            for x in range(xpx1, xpx2):
                intens = round(INTENSE_MAX * (y - int(y)))
                points.append(Pixel(int(y), x + 1, INTENSE_MAX - intens))
                points.append(Pixel(int(y) + 1, x + 1, intens))

                if count_steps:
                    if last_x != x and last_y != round(y):
                        steps += 1
                    last_x = x
                    last_y = round(y)

                y += k
        else:
            for x in range(xpx1, xpx2):
                intens = round(INTENSE_MAX * (y - int(y)))
                points.append(Pixel(x + 1, int(y), INTENSE_MAX - intens))
                points.append(Pixel(x + 1, int(y) + 1, intens))

                if count_steps:
                    if last_x != x and last_y != round(y):
                        steps += 1
                    last_x = x
                    last_y = round(y)

                y += k
    if count_steps:
        return steps

    return points


def lib(p1: Point, p2: Point):
    return []


if __name__ == '__main__':
    p1 = Point(702, 608)
    p2 = Point(1096, 539)
    points1 = brez_float(p1, p2)
    points2 = dda(p1, p2)
    for i in range(len(points1)):
        if points1[i] != points2[i]:
            print(points1[i - 1], points2[i - 1])
            print(points1[i], points2[i])
            print(points1[i + 1], points2[i + 1])

    # p1 = Point(702, 608)
    # p2 = Point(1078, 471)
    # points1 = brez_float(p1, p2)
    # points2 = brez_int(p1, p2)
    # for i in range(len(points1)):
    #     if points1[i] != points2[i]:
    #         print(points1[i - 1], points2[i - 1])
    #         print(points1[i], points2[i])
    #         print(points1[i + 1], points2[i + 1])
