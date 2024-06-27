

def mid_point(p1, p2, xl, xr, yb, yt):
    i = 1
    t1, t2, s1, s2 = 0, 0, 0, 0
    if s1 == 0 and s2 == 0:
        return 'see'
    else:
        if t1*t2 != 0:
            return 'not see'
        else:
            r = p1
            if i > 2:
                if t1*t2 == 0:
                    return 'see'
                else:
                    return 'not see'
            if s2 == 0:
                p1 = p2
                p2 = r
                i += 1
                