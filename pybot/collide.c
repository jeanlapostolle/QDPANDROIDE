int collideLineLine(double a[2],double b[2],double c[2],double d[2]){
    double db = (d[1]-c[1])*(b[0]-a[0]) - (d[0]-c[0])*(b[1]-a[1]);
    if (db == 0){ db = 0.01;}
    double uA = ((d[0]-c[0])*(a[1]-c[1]) - (d[1]-c[1])*(a[0]-c[0])) / db;
    double uB = ((b[0]-a[0])*(a[1]-c[1]) - (b[1]-a[1])*(a[0]-c[0])) / db;

    //if uA and uB are between 0-1, lines are colliding
    if (uA >= 0 && uA <= 1 && uB >= 0 && uB <= 1){return 1;}
    return 0;
  }

int collideRectLine(double r1[2], double r2[2], double r3[2], double r4[2], double l1[2], double l2[2]){
    int n = collideLineLine(r1, r2, l1, l2);
    int o = collideLineLine(r2, r3, l1, l2);
    int s = collideLineLine(r3, r4, l1, l2);
    int e = collideLineLine(r4, r1, l1, l2);
    if (n + o + s + e > 0){ return 1; }
    return 0;
}
