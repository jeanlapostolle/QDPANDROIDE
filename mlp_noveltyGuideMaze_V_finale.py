#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 10:50:10 2019

@author: qiu
"""
import heapq
import main as robot
from collide import distc
from Mlp import Mlp,genererPopulation,mutation,croissement,rangementParQualite,selection
from PIL import Image, ImageDraw;

def butAtteint(positionFinale):
    if distc(positionFinale, robot.finish_position) < 10 :
        print("**************goal atteint************************")
        return True;
    else:
        return False;   
def plotmaze(visitedPosition,filename):
    """position:ensemble de toutes les positions atteintes par au moins un robot 
    """
    print("plotmaze, len(visitedPosition) =",len(visitedPosition));
    h = 400;
    l = 200;
    o = (0,0)
    img = Image.new('RGBA', (h, l),(255,255,255))
    draw = ImageDraw.Draw(img);
    draw.line([o,(h-1,0)],fill = 0);
    draw.line([o,(0,l-1)],fill = 0);
    draw.line([(0,l-1),(h-1,l-1)],fill = 0);
    draw.line([(h-1,0),(h-1,l-1)],fill = 0);
    draw.line([(50,80),(340,200)],fill = 0);
    draw.line([(120,0),(70,50)],fill = 0);
    draw.line([(220,0),(170,70)],fill = 0);
    draw.line([(350,0),(300,100)],fill = 0);
    draw.line([(350,140),(380,200)],fill = 0);
    draw.line([(120,60),(150,125)],fill = 0);
    draw.line([(220,85),(250,190)],fill = 0);
    #goal
    draw.ellipse([(370,150),(380,160)],fill = 0);
    #start
    draw.ellipse([(3,20),(13,30)],fill = 0);
    #draw.ellipse([(3,18),(4,23)],fill = 1);
    #img.show()
    
    
    for p in visitedPosition:
        draw.point(p,"red");
    #    draw.ellipse([(p[0],p[1]),(p[0]+2,p[1]+2)],fill = "red");
    img.save(filename);
    
def les_k_plus_petits_elements(k,l):
    t = l[:k];
    for e in l[k:]:
        x = None;
        m = None
        for i in range(len(t)):
            if t[i]>e:
                if x == None:
                    x = i;
                    m = t[i]
                elif t[i]>m:
                    x = i;
                    m = t[i]
        if x != None:
            t[x] = e;
    return t;
def eval_genomes(population,generation,nb_run):
    global test_var1
    global test_var2
    global solution;
    global probMutation
    global position
    k = 20; #nombre de voisins les plus proches
    visitedPosition = set();
    R = set();
    for j in range(1,generation+1):
        print(j,"-ieme generation")
        delta = 0;
        pos = []
        nouveaute = []
        ### evaluate population and add into archive of past behaviors
        for genome in population:
            #affichage de image
#            positionFinale = robot.simulationNavigation(genome);
            positionFinale = robot.simulationNavigationSansImage(genome);
            # ajouter la positionFinale dans l'ensemble de positions visitees par la population
            pos.append(positionFinale);
            # ajouter la positionFinale dans la list R
            R.add(positionFinale);
            # MAJ de nouveaute
            if (positionFinale) not in visitedPosition:
                nouveaute.append(10000)
            else:
                nouveaute.append(0);
            
            # ajouter la positionFinale dans l'ensemble de positions visitees
            if positionFinale not in visitedPosition:
                visitedPosition.add(positionFinale);
                delta += 1;
            # verifier si le but est atteint
            if butAtteint(positionFinale):
                plotmaze(visitedPosition,"./result2005soir/novelty/noveltyGuideMaze_{}_run_{}_generation_image_finale.png".format(nb_run,j))
#                plotmaze(visitedPosition,"./test/result_pb5sur1000p01_250000evaluations/noveltyGuideMaze_{}_run_{}_generation_image_finale.png".format(nb_run,j))
                return;    
            
            
        ### calculer le nouveaute par rapport a ses distances avec les voisins pour chaque genome dans la population
#        print("visitedPosition: ",visitedPosition);
        for i in range(len(population)):
            #calculer les distances entre cette position et toutes les autres positions visitees
            distances = [];
            heapq.heapify(distances);
            for p in R:
                heapq.heappush(distances,distc(pos[i],p))
            nouveaute[i] += sum([heapq.heappop(distances) for d in range(k+1)]);
#            print("len(distance) :",len(distances))
#            print("len(visitedPOsition) :",len(visitedPosition));
#            print("positionFi ", pos[i]);
#            print("pos[i] nouveaute: ",nouveaute[i]);
#        print("nouveaute: ",nouveaute) 
#        print("pos : ",pos);
        
        ### generer prochaine generation
        nextPopulation = [];      
        distribution = rangementParQualite(p = 0.1,taille = len(population));
        for i in range(len(population)//2):
            #selection
            individu1,individu2 = selection(population,nouveaute,distribution); 
            #croisement
            individu3,individu4 = croissement(individu1,individu2);
            #mutation
            individu3 = mutation(individu3,probMutation);
            individu4 = mutation(individu4,probMutation);
            #ajouter dans la prochaine population
            nextPopulation.append(individu3);
            nextPopulation.append(individu4);
        population = nextPopulation;
        # R ne retenir que les 1250 positions de nouveaute les plus haute
        if len(R)>1250:  #250*5
            l = [];
            for position in R:
                nvt = sum(les_k_plus_petits_elements(20,[distc(position,i) for i in visitedPosition]))
                l.append([position,nvt]);
            R =set([i[0] for i in sorted(l,key=lambda x :-x[1])[:1250]]) ;
        # adjuster la probabilite de mutatioin dynamiquement    
        if delta <20:
            probMutation += 0.005
        print("prob mutation ",probMutation);
        
        #generation de graph
        print("j=", j);
        if j%50 == 0 and j!=0:
            plotmaze(visitedPosition,"./result2005soir/novelty/noveltyGuideMaze_{}_run_{}_generation_image.png".format(nb_run,j))
#            plotmaze(visitedPosition,"./test/noveltyGuideMaze_{}_run_{}_generation_image.png".format(nb_run,j))


# a robot that finishes within five units of the goal counts as a solution
N = 250 #taille population
p = genererPopulation(N,[16,12,1])
probMutation = 0.005
nb_generation = 1000
for nb_run in range(1,2):
    position = [];
    eval_genomes(p,nb_generation,nb_run);
