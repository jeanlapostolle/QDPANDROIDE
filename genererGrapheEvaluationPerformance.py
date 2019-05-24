#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 17:02:53 2019

@author: 3503860
"""
import math
import matplotlib.pyplot as plt
###  genererGrapheEvaluation
def dist(p0,p):
    x0,y0 = p0;
    x,y = p;
    return math.sqrt((x-x0)**2 + (y-y0)**2);
def read(fn,n):
    positions = [];
    f = open(fn,"r");
    for i in range(n):
        line = f.readline();
        line = line.replace('(','');
        line = line.replace(')','');
        try:
            x,y = line.split(', ');
        except:
            print(i);
        x = int(x);
        y = int(y);
        positions.append([x,y])
    f.close();
    return positions;

def evaluation_performance(positions):
    distances = [];
    
    for i in range(n):
        d = 0;
        for j in range(len(positions)):
            k = dist(positions[j][i],pe)
            d += k;
        d = d/len(positions);
        distances.append(d);
    
    max_dist = dist(ps,pe);
    evaluation = [0];
    for d in distances:
        if max_dist - d > evaluation[-1]:
            evaluation.append(max_dist-d);
        else:
            evaluation.append(evaluation[-1]);
    return evaluation;

# fitness
#n = 125000 # nb_lignes
n = 101000
nf = 6  # nb_fichiers
fpositions = [];
ps = [40,60]  #position start
pe = [370,150];   # position goal
for i in range(nf):
    fn = "./rf/fitness_{}_run_125000evaluations.txt".format(i);
    fpositions.append(read(fn,n));
fit_evaluation_performance = evaluation_performance(fpositions);
plt.title("Evaluation de performance avec nb_evaluations")
X=[0]
Y=[0];
for i,j in zip(fit_evaluation_performance,range(n)):
    if fit_evaluation_performance[j] != X[-1]:
        X.append(fit_evaluation_performance[j]);
        Y.append(j);
X.append(X[-1]);
Y.append(n);
plt.plot(Y,X,label="Fitness search");


# NS
npositions = [];
#n = 124900
n = 101000
npositions.append(read("./rf/novelty_1_run_125000.txt",n));
npositions.append(read("./rf/novelty_2_run_105235.txt",105235));
npositions[1] = npositions[1]+[(40,60) for i in range(40000)]
npositions.append(read("./rf/novelty_3_run_102351evaluations.txt",102351));
npositions[2] = npositions[2]+[(40,60) for i in range(40000)]
npositions.append(read("./rf/novelty_4_run_125000evaluations.txt",n));
npositions.append(read("./rf/novelty_5_run_125000evaluations.txt",n));
npositions.append(read("./2305/novelty_91_run.txt",n));
npositions.append(read("./2305/novelty_92_run.txt",n));
nov_evaluation_performance = evaluation_performance(npositions);
X=[0]
Y=[0];
for i,j in zip(nov_evaluation_performance,range(n)):
    if nov_evaluation_performance[j] != X[-1]:
        X.append(nov_evaluation_performance[j]);
        Y.append(j);
X.append(X[-1]);
Y.append(n);
plt.plot(Y,X,label="Novelty search");


# NS+ map ellites
mpositions = [];
MAP = {7,8}
n = 101000
mpositions.append(read("./rf/map_7_run_39629evaluations.txt",39629));
mpositions[0] = mpositions[0]+[[40,60] for i in range(90000)]
mpositions.append(read("./2305/map_230504_run_mutationfaible_101000evaluations.txt",n));
mpositions.append(read("./2305/map_230578_run_mutationfaible_101000evaluations.txt",n));
mpositions.append(read("./2305/map_778_run_mutationfaible.txt",n));
mpositions.append(read("./2305/map_779_run_mutationfaible.txt",n));
map_evaluation_performance = evaluation_performance(mpositions);
X=[0]
Y=[0];
for i,j in zip(map_evaluation_performance,range(n)):
    if nov_evaluation_performance[j] != X[-1]:
        X.append(map_evaluation_performance[j]);
        Y.append(j);
plt.plot(Y,X,label="Map-elites + novelty search");
plt.legend()
plt.show();



    
    