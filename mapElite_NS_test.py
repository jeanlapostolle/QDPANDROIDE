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
import numpy as np
import heapq

class MyHeap(object):
   def __init__(self, initial=None, key=lambda x:x):
       self.key = key
       if initial:
           self._data = [(key(item), item) for item in initial]
           heapq.heapify(self._data)
       else:
           self._data = []

   def push(self, item):
       heapq.heappush(self._data, (self.key(item), item))

   def pop(self):
       return heapq.heappop(self._data)[1]

def butAtteint(positionFinale):
    if distc(positionFinale, robot.finish_position) < 10 :
        print("**************goal atteint************************")
        return True;
    else:
        return False;
def les_k_plus_petits_elements(k,l):
    return sorted(l)[0:k];
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

def select_k_position(k,position_nouveaute):
    # ordonner la liste de toutes les positions par nouveaute decroissante
    positions =[i[0] for i in sorted(position_nouveaute,key = lambda x:-x[1])];
    return positions[0:k];
def mutationFaible(nn,):
    ''' mutation en changeant quelques valeur des aretes
    '''   
    gene = nn.unroll_weights();
    nbgene = 1
    positionschoisies = np.random.choice(len(gene),nbgene,replace=False);
    for p in positionschoisies:
        gene[p] = (1/2+np.random.rand())*gene[p]
    nn.weights = nn.roll_weights(gene);
    return nn;
def varier(B):
    return [mutationFaible(g) for g in B];
def eval_genomes(nb_run):
    global probMutation;
    size_layers = (16,12,1);
    
    X = [[None for i in range(200)] for j in range(400)]
    visitedPosition = set();
    R = set();
    
    #generate and evaluate B random genomes initiales
    B = [Mlp(size_layers) for i in range(1000)]; 
    pos = [robot.simulationNavigationSansImage(genome) for genome in B];
    for genome,position in zip(B,pos):
        if X[position[0]][position[1]] == None:
            R.add(position)
            X[position[0]][position[1]] = genome;
            visitedPosition.add(position);
    
    nouveaute_position = [];
    for position in visitedPosition:
        nouveaute_position.append((position,sum(les_k_plus_petits_elements(20,[distc(position,i) for i in R]))));
            
    for generation in range(1,1001):
        
        delta = 0;
        # choisir 250 genomes dans la population par rapport a sa nouveaute
        positions = select_k_position(250,nouveaute_position);
        B = [X[position[0]][position[1]] for position in positions];
        # mutation pour generer leurs enfants
        B = varier(B);
        # evaluer les genomes
        pos = [robot.simulationNavigationSansImage(genome) for genome in B];
        # ajouter dans les grid et la list de positions  visitees dans le passe
        for genome,position in zip(B,pos):
            if X[position[0]][position[1]] == None:
                R.add(position)
                X[position[0]][position[1]] = genome;
                # ajouter la positionFinale dans l'ensemble de positions visitees
                visitedPosition.add(position);
                delta += 1;
                # si le goal est atteint
                if butAtteint(position):
                    plotmaze(visitedPosition,"./result2005/result_NS_plus_mapelite/NS_mapElite_Maze_{}_run_{}_generation_image_finale.png".format(nb_run,generation))
                    return;
        nouveaute_position = [];
        # calculer nouveaute pour tout genome de la population
        for position in visitedPosition:
            nouveaute_position.append((position,sum(les_k_plus_petits_elements(20,[distc(position,i) for i in R]))));
        # calculer nouveaute pour tout genome dans le list R
        if len(R)>1250:  #250*5
            l = [];
            for position in R:
                nvt = sum(les_k_plus_petits_elements(20,[distc(position,i) for i in visitedPosition]))
                l.append([position,nvt]);
            R =set([i[0] for i in sorted(l,key=lambda x :-x[1])[:1250]]) ;
        print("len(visitedPosition) ",len(visitedPosition))
        #generation de graph
        print("generation = ",generation );
        if generation%5 == 0 and generation!=0:
#            plotmaze(visitedPosition,"./result/noveltyGuideMaze_{}_run_{}_generation_image.png".format(nb_run,j))
            plotmaze(visitedPosition,"./result2005/result_NS_plus_mapelite/NS_mapElite_Maze_{}_run_{}_generation_image.png".format(nb_run,generation))
        if delta <20:
            probMutation += 0.005
        print("prob mutation ",probMutation);
probMutation = 0.005
for nb_run in range(1):
    eval_genomes(nb_run);
