#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 10:50:10 2019

@author: qiu
"""
import main as robot

from collide import distc

from Mlp import Mlp,genererPopulation,mutation,croissement,rangementParQualite,selection


def eval_genomes(population,generation):
    global solution;
    taillePopulation =len(population);
    for i in range(generation):
        print(i,"ieme generation")
        pos = []
        dis = []
        ### evaluation des reseaux neurones
        for genome in population:
            #affichage de image
#            positionFinale = robot.simulationNavigation(genome);
            positionFinale = robot.simulationNavigationSansImage(genome);
            position.append(positionFinale);
            # evaluation
            pos.append(positionFinale);
            dis.append(10000-distc(positionFinale,robot.finish_position),)
            print("--> la position finale {}".format(positionFinale));
            if distc(positionFinale, robot.finish_position) < 10 :
                print("***********solution trouveeee****************");
                solution = population[i];
                break;
        ### generer prochaine generation
        nextPopulation = [];      
        distribution = rangementParQualite(p = 0.3,taille = taillePopulation);
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
    
    

# a robot that finishes within five units of the goal counts as a solution
k = 5
cases = [[0 for i in range(200//k)] for j in range(400//k)];
position = [];
N = 10
p = genererPopulation(N,[16,12,1])
probMutation = 0.005
eval_genomes(p,20);
solution = None;

#### affichage

from PIL import Image, ImageDraw;
h = 400;
l = 200;
o = (0,0)
size = (h,l);
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
draw.ellipse([robot.start_position,(robot.start_position[0]+5,robot.start_position[1]+5)],fill = 0);
#draw.ellipse([(3,18),(4,23)],fill = 1);
#img.show()

#img.save('/home/wei/Documents/QDPY/mywork/novelty search/mediumMap.bmp');



for p in position:
    draw.point(p,"red");
#    draw.ellipse([(p[0],p[1]),(p[0]+2,p[1]+2)],fill = "red");
img.show()