def collideLineLine(a, b, c, d):
    db = (d[1]-c[1])*(b[0]-a[0]) - (d[0]-c[0])*(b[1]-a[1])
    if db == 0: db = 0.01
    uA = ((d[0]-c[0])*(a[1]-c[1]) - (d[1]-c[1])*(a[0]-c[0])) / db
    uB = ((b[0]-a[0])*(a[1]-c[1]) - (b[1]-a[1])*(a[0]-c[0])) / db

    #if uA and uB are between 0-1, lines are colliding
    if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1): return True
    return False

def collideRectLine(r1, r2, r3, r4, l1, l2):
    n = collideLineLine(r1, r2, l1, l2)
    o = collideLineLine(r2, r3, l1, l2)
    s = collideLineLine(r3, r4, l1, l2)
    e = collideLineLine(r4, r1, l1, l2)
    if n or o or s or e : return True
    return False
