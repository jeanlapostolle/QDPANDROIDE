# -*- coding: utf-8 -*-
"""
Methods:
    __init__()
    predict(X)
    initialize_weights()
    unroll_weights(rolled_data)
    roll_weights(unrolled_data)
    sigmoid(z)
    tanh(z)
 """   
import random
import numpy as np
class Mlp():


    def __init__(self, size_layers,act_func1="tanh",act_func2="sigmoid"):

        self.size_layers = size_layers
        self.act_f1      = act_func1
        self.act_f2      = act_func2

        # Ramdomly initialize weights
        self.initialize_weights()
        
    def predict(self, X):
        A = X.copy()+[1];
        C = [];
        for i in range(self.size_layers[1]):
            B = self.weights[0][i];
            C.append(self.tanh(np.dot(A,B)));
        C = C + [1]
        D = self.weights[1][0]
        assert len(C) == 13
        assert len(D) == 13;
        out = self.sigmoid(np.dot(C, D))
        assert isinstance(out,float)
        return out

    def initialize_weights(self):

        self.weights = [[],[]]
        
        for i in range(self.size_layers[1]):
            self.weights[0].append([random.uniform(-2.,2) for i in range(self.size_layers[0]+1)]);#premier couche  17-->12
        self.weights[1].append([random.uniform(-2,2) for i in range(self.size_layers[1]+1)]);  # deuxieme couche 13 --> 1

        
    def unroll_weights(self):
        unrolled_array = []
        for i in range(self.size_layers[1]):
            unrolled_array += self.weights[0][i];
        unrolled_array = list(np.concatenate((unrolled_array,self.weights[1][0])));
        return unrolled_array
    def roll_weights(self,data):
        b = data[-self.size_layers[1]-1:];
        c = np.reshape(data[:-self.size_layers[1]-1],(self.size_layers[1],self.size_layers[0]+1));
        a = [list(i) for i in c];
        return [a,[b]]

    def sigmoid(self, z):
        result = 1.0 / (1.0 + np.exp(-z))
        return result
    def tanh(self, z):
        result = np.tanh(z)       
        return result


def croissement(nn1,nn2):
    gene1 = nn1.unroll_weights();
    gene2 = nn2.unroll_weights();
    a_gene1 = [];
    b_gene2 = [];
    for i in range(len(gene1)):
        if random.randint(1,3) == 1:
            a_gene1.append(gene1[i]);
            b_gene2.append(gene2[i]);
        else:
            a_gene1.append(gene2[i]);
            b_gene2.append(gene1[i]);
    a_nn = Mlp(nn1.size_layers);
    b_nn = Mlp(nn2.size_layers);
    a_nn.weights = a_nn.roll_weights(np.array(a_gene1));
    b_nn.weights = b_nn.roll_weights(np.array(b_gene2));    
    return a_nn,b_nn        

def mutation(nn,probaMutation):
    ''' mutation en changeant quelques valeur des aretes
    '''   
    if np.random.rand()>= probaMutation:
        return nn;
    gene = nn.unroll_weights();
    nbgene = random.randint(0,len(gene));
    positionschoisies = np.random.choice(len(gene),nbgene,replace=False);
    for p in positionschoisies:
        gene[p] = (1/2+np.random.rand())*gene[p]
    nn.weights = nn.roll_weights(gene);
    return nn;

# generer une Population initiale de taille N
def genererPopulation(N,size_layers):
    population = [];
    for i in range(N):
        individu = Mlp(size_layers)
        population.append(individu);
    return population;

def selection(population,scores,distribution):
    population = [x for x,_ in sorted(zip(population,scores),key=lambda x
                        :x[1])]; # ordoner les individus par distance decroissante
    x,y = np.random.choice(range(len(population)),2,replace=False,p=distribution);
    return population[x],population[y];

# rangement par qualite
def rangementParQualite(p,taille):
    '''generer une distribution pour selectionner des individus
    '''
    distribution = [p*pow((1-p),n) for n in range(taille)];
    distribution[0] = distribution[0]+(1-sum(distribution));
    return distribution;
