#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 10:50:10 2019

@author: qiu
"""
import main as robot

from collide import distc

from Mlp import Mlp,genererPopulation,mutation,croissement,rangementParQualite,selection

from PIL import Image, ImageDraw;


def butAtteint(positionFinale):
    if distc(positionFinale, robot.finish_position) < 10 :
        return True;
    else:
        return False;
    
def plotmaze(visitedPositions,filename):
    """position:ensemble de toutes les positions atteintes par au moins un robot 
    """
    print("plotmaze, len(visitedPositions) =",len(visitedPositions));
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
    
    
    for p in visitedPositions:
        draw.point(p,"red");
    #    draw.ellipse([(p[0],p[1]),(p[0]+2,p[1]+2)],fill = "red");
    img.save(filename);


def eval_genomes(population,generation,nb_run):
    global solution;
    global probMutation
    taillePopulation =len(population);
    visitedPositions = set();
    for j in range(generation):
        print(j,"-ieme generation")
        pos = []
        dis = []
        delta = 0;
        ### evaluation des reseaux neurones
        for genome in population:
            #affichage de image
#            positionFinale = robot.simulationNavigation(genome);
            positionFinale = robot.simulationNavigationSansImage(genome);
            if positionFinale not in visitedPositions:
                visitedPositions.add(positionFinale);
                delta += 1;
            # evaluation
            pos.append(positionFinale);
            dis.append(10000-distc(positionFinale,robot.finish_position))
            if butAtteint(positionFinale):
                plotmaze(visitedPositions,"./result1805/result_pb5sur1000p01_250000evaluations/fitnessGuideMaze_{}_run_{}_generation_image_finale.png".format(nb_run,j))
                return;   
        ### generer prochaine generation
        nextPopulation = [];      
        distribution = rangementParQualite(p = 0.1,taille = taillePopulation);
        for i in range(taillePopulation//2):
            #selection
            individu1,individu2 = selection(population,dis,distribution); 
            #croisement
            individu3,individu4 = croissement(individu1,individu2);
            #mutation
            individu3 = mutation(individu3,probMutation);
            individu4 = mutation(individu4,probMutation);
            #ajouter dans la prochaine population
            nextPopulation.append(individu3);
            nextPopulation.append(individu4);
        population = nextPopulation;
        if delta <20:
            probMutation += 0.005
        ### plot
        #generation de graph
        if j%50 == 0 and j!=0:
            plotmaze(visitedPositions,"./result1805/result_pb5sur1000p01_250000evaluations/fitnessGuideMaze_{}_run_{}_generation_image.png".format(nb_run,j))

    
    

## main
N = 250  #taille de population
probMutation = 0.005 ## probabilite de mutation
solution = None
for nb_run in range(1,2):
    p = genererPopulation(N,[16,12,1])
    eval_genomes(p,1000,nb_run);
