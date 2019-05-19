from math import sqrt


def collideLineLine(a, b, c, d):
    db = (d[1] - c[1]) * (b[0] - a[0]) - (d[0] - c[0]) * (b[1] - a[1])
    if db == 0:
        db = 0.01
    uA = ((d[0] - c[0]) * (a[1] - c[1]) - (d[1] - c[1]) * (a[0] - c[0])) / db
    uB = ((b[0] - a[0]) * (a[1] - c[1]) - (b[1] - a[1]) * (a[0] - c[0])) / db

    # if uA and uB are between 0-1, lines are colliding
    if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
        return True
    return False


def collideRectLine(r1, r2, r3, r4, l1, l2):
    n = collideLineLine(r1, r2, l1, l2)
    o = collideLineLine(r2, r3, l1, l2)
    s = collideLineLine(r3, r4, l1, l2)
    e = collideLineLine(r4, r1, l1, l2)
    if n or o or s or e:
        return True
    return False


def distc(p1, p2):
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def collidePointLine(p, l1, l2):
    d1 = distc(p, l1)
    d2 = distc(p, l2)
    ll = distc(l1, l2)

    buff = 0.1
    if d1 + d2 >= ll - buff and d1 + d2 <= ll + buff:
        return True
    return False


def distPointLine(C, A, B):
    num = (C[0] - A[0])(B[0] - A[0]) + (C[1] - A[1])(B[1] - A[1])
    return num / sqrt(distc(A, B))


def droite(A, B):
    if B[0] - A[0] == 0:
        return (0, 0)
    a = (B[1] - A[1]) / (B[0] - A[0])
    b = A[1] - a * A[0]
    return a, b


def evalPointDroite(p, droite):
    a, b = droite
    return a * p[0] - p[1] + b


def intersect(l1, l2, l3, l4):
    a, b = droite(l1, l2)
    ap, bp = droite(l3, l4)
    if a - ap == 0:
        return None
    x = (bp - b) / (a - ap)
    y = a * x + b
    return x, y
