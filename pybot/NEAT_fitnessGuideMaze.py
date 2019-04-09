#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 10:50:10 2019

@author: qiu
"""
# recherche avec reseau neurone NEAT et fonction fitness d = distance(positionFinale, goal)
# il reste a ajuster les parametres dans le ficher config

import neat
import main
import random
from collide import distc
# a robot that finishes within five units of the goal counts as a solution


#def isSolution(pos,finish_position):
#    if distc(pos,finish_position)<=5:
#        return True;
#    else:
#        return False;

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        positionFinale = main.simulationNavigationSansImage(net.activate);
        genome.fitness = -distc(positionFinale, main.finish_position);
        print("robot {}: fini a la position {}, distance avec goal {}".format(genome_id,positionFinale,genome.fitness));
# Load configuration.
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'NEAT_fitnessGuideMaze_config')

# Create the population, which is the top-level object for a NEAT run.
p = neat.Population(config)

# Add a stdout reporter to show progress in the terminal.
p.add_reporter(neat.StdOutReporter(False))

# Run until a solution is found.
winner = p.run(eval_genomes,5); 

# Display the winning genome.
print('\nBest genome:\n{!s}'.format(winner))
