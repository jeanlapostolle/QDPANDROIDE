#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 10:50:10 2019

@author: qiu
"""
import heapq
import main as robot
from collide import distc
import time
from Mlp import Mlp,genererPopulation,mutation,croissement,rangementParQualite,selection

def butAtteint(position,start_time,f):
    if distc(position, robot.finish_position) < 10 :
        print("***********solution trouveeee****************\n");
        f.write("***********solution trouveeee****************\n");
        f.write("position d'arete:",position);
        f.write("temps utilise: ",time.time-start_time);
        f.close();
        plotmaze(position,"resultat_{}ieme_run_final_image.png".format(nb_run))
        return True;
    else:
        return False;
            
def eval_genomes(population,generation,nb_run):
    global solution;
    start_time = time.time()
    f=open("resultat_{}ieme_run.out".format(nb_run),"w");
    
    taillePopulation =len(population);
    for i in range(generation):
        print(i,"ieme generation")
        pos = []
        visitedPosition = set();
        ### evaluate population and add into archive of past behaviors
        for genome in population:
            #affichage de image
#            positionFinale = robot.simulationNavigation(genome);
            positionFinale = robot.simulationNavigationSansImage(genome);
            # ajouter la positionFinale dans l'ensemble de positions visitees par la population
            pos.append(positionFinale);
            # ajouter la positionFinale dans l'ensemble de positions visitees
            visitedPosition.add((positionFinale[0],positionFinale[1]));
            # verifier si le but est atteint
            if butAtteint(positionFinale,start_time,f):
                return;            
            
            # pour affichage :  to be delete
            position.append(positionFinale);
        ### calculer le score par rapport a la nouveaute pour chaque genome dans la population
        nouveaute = [0 for i in population];
        distances = [];
        heapq.heapify(distances);
        for i in range(len(population)):
            for p in visitedPosition:
                heapq.heappush(distances,distc(pos[i],p))
                nouveaute[i] = sum(distances[0:20])
            if (positionFinale[0],positionFinale[1]) in visitedPosition:
                nouveaute[i] += 10000;
        ### generer prochaine generation
        nextPopulation = [];      
        distribution = rangementParQualite(p = 0.3,taille = taillePopulation);
        for i in range(taillePopulation//2):
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
        
        #generation de graph
        if i%5 == 0 and i!=0:
            plotmaze(visitedPosition,"resultat_{}ieme_run_{}_generation_image.rgba".format(nb_run,i))

    
    

# a robot that finishes within five units of the goal counts as a solution
k = 5
cases = [[0 for i in range(200//k)] for j in range(400//k)];
N = 250
p = genererPopulation(N,[16,12,1])
probMutation = 0.005
for i in range(1,2):
    position = [];
    eval_genomes(p,6,i);
solution = None;
#### affichage

from PIL import Image, ImageDraw;
def plotmaze(position,filename):
    """position:ensemble de toutes les positions atteintes par au moins un robot 
    """
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
    
    
    for p in position:
        draw.point(p,"red");
    #    draw.ellipse([(p[0],p[1]),(p[0]+2,p[1]+2)],fill = "red");
    img.save(filename);
    img.show()