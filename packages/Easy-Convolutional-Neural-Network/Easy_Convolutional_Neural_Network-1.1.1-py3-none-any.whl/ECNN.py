import json
from scipy.special import expit
import numpy as np
np.random.seed(1)

def function(ftype:str,z:float,prime=False,alpha=1):
    """
        type : "sigmoid,ELU,..."
        z : Pre-activation
        prime : True/False
        alpha : Default(1)
    Funtion :
    # Binary-Step (z)
    # Linear (z, alpha)
    # Sigmoid (z)
    # Tanh (z)
    # ReLU (z)
    # Leaky-ReLU (z, alpha)
    # Parameterised-ReLU (z, alpha)
    # Exponential-Linear-Unit (z, alpha)
    """
    if ftype == "Binary-Step":
        if prime == False:
            y = np.heaviside(z,0)
        else:
            y = np.zeros(z.shape, dtype=z.dtype) 
    # if ftype == "Linear":
    #     if prime == False:
    #         y = z*alpha
    #     else:
    #         y = alpha
    if ftype == "Sigmoid":
        if prime == False:
            y = expit(z)
            # y = 1/(1+np.exp(-z))
        else:
            y = (expit(z)) * (1-(expit(z)))
            # y = (1/(1+np.exp(-z))) * (1-(1/(1+np.exp(-z))))
    if ftype == "Tanh":
        if prime == False:
            y = np.tanh(z)
            # y = (np.exp(z)-np.exp(-z))/(np.exp(z)+np.exp(-z))
        else:
            y = 1.0 - np.tanh(z)**2
            # y = 1 - (np.exp(z)-np.exp(-z))/(np.exp(z)+np.exp(-z))**2
    if ftype == "ReLU":
        if prime == False:
            y = np.maximum(0,z)
        else:
            z[z<=0] = 0
            z[z>0] = 1
            y = z
    # if ftype == "Leaky-ReLU":
    #     if prime == False:
    #         y = max(alpha*z, z)
    #     else:
    #         if z > 0:
    #             y = 1
    #         else:
    #             y = alpha
    # if ftype == "Parameterised-ReLU":
    #     if prime == False:
    #         if z >= 0:
    #             y = z
    #         else:
    #             y = alpha*z
    #     else:
    #         if z >= 0:
    #             y = 1
    #         else:
    #             y = alpha
    # if ftype == "Exponential-Linear-Unit":
    #     if prime == False:
    #         if z >= 0:
    #             y = z
    #         else:
    #             y = alpha*(np.exp(z)-1)
    #     else:
    #         if z >= 0:
    #             y = z
    #         else:
    #             y = alpha*(np.exp(y))
    return y

class neural_network:
    def __init__(self):
        self.network = []
    
    def make(self,nb_input:int,hidden_layer_list:list,nb_output:int,output_function:str):
        """
        # nb_input:
        Nombre de neurone dans l'inputLayer
        
        # hidden_layer_list :
        Liste des couches de l'hiddenLayer avec le nombre de neurone et leurs fonction d'activation
        
        # nb_output :
        Nombre de neurone de sortie

        # output_function :
        Fonction d'activation des neurones de l'outputLayer
        
        Fonctions :
            Tanh (z)
            Sigmoid (z)
            ReLU (z)
            Binary-Step (z)
        """
        # On reinitialise le réseau
        self.network = []
        # [[hiddenlayer1_function,hiddenlayer1,hiddenlayer1_weights,hiddenlayer1_delta,hiddenlayer1_error],[hiddenlayer2,hiddenlayer2_weights,hiddenlayer2_delta,hiddenlayer2_error],[outputlayer,outputlayer_weights,outputlayer_delta,outputlayer_error]]
        #pour chaque hiddenlayer de la liste définie
        for hidden_layer_x,hidden_layer in enumerate(hidden_layer_list):
            # on créé une couche vide
            temp = []
            # on ajoute la fonction d'activation
            temp.append(hidden_layer[1])
            # on genere des 0 pour les activation
            temp.append(0)
            # on genere des valeurs aleatoire pour les poids
            if hidden_layer_x == 0:
                # on prend le nombre de neurone de l'inputLayer
                temp.append(2*np.random.random((nb_input,hidden_layer[0]))-1)
            else:
                # on prend le nombre de neurone de la couche precedante 
                temp.append(2*np.random.random((hidden_layer_list[hidden_layer_x-1][0],hidden_layer[0]))-1)
            temp.append(0)
            temp.append(0)
            self.network.append(temp)

        # on créé une couche vide
        temp = []
        # on ajoute la fonction d'activation
        temp.append(output_function)
        # on genere des 0 pour les activation
        temp.append(0)
        # on genere des valeurs aleatoire pour les poids
        temp.append(2*np.random.random((hidden_layer_list[-1][0],nb_output))-1)
        temp.append(0)
        temp.append(0)
        self.network.append(temp)

    def train(self,input_dataset:list,expected_output:list,iteration:int,display=False):
        input_layer = np.array(input_dataset)
        # Pour chaque iteration
        for i in range(iteration):
            #----FEED FORWARD----#
            self.feedforward(input_layer)
            #--------------------#
            #----BACK PROPAGATION----#
            # Pour chaque couche de notre reseau a l'envert
            for layer_x in range(len(self.network)):
                layer_x_temp = len(self.network)-1 - layer_x
                # Si la couche est celle de l'output
                if layer_x_temp == len(self.network)-1:
                    # Calcul du cout
                    self.network[-1][4] = (np.array(expected_output)-self.network[-1][1])
                    # Calcul de la correction
                    self.network[-1][3] = self.network[-1][4]*function(self.network[-1][0],self.network[-1][1],prime=True)
                    if display == True:
                        print("====="+str(i)+"=====\nCout : \n"+str(self.network[-1][4])+"\n=====###=====")
                else:
                    # Calcul l'erreur de la couche
                    self.network[layer_x_temp][4] = np.dot(self.network[layer_x_temp+1][3],self.network[layer_x_temp+1][2].T)
                    # Calcul de la correction
                    self.network[layer_x_temp][3] = self.network[layer_x_temp][4]*function(self.network[layer_x_temp][0],self.network[layer_x_temp][1],prime=True)
            # Application de la correction
            # Pour chaque couche de notre reseau
            for layer_x in range(len(self.network)):
                # Si c'est la premiere couche
                if layer_x == 0:
                    # On met a jour les poids
                    self.network[0][2] += np.dot(input_layer.T,self.network[0][3])
                else:
                    # On met a jour les poids
                    self.network[layer_x][2] += np.dot(self.network[layer_x-1][1].T,self.network[layer_x][3])
            #------------------------#

    def feedforward(self,input_layer):
        # Pour chaque couche de notre reseau de neurone
        for layer_x in range(len(self.network)):
            # On verifie si la couche est la premiere
            if layer_x == 0:
                # On calcule la couche par rapport à l'inputLayer
                preactivation = np.dot(input_layer,self.network[layer_x][2])
                self.network[layer_x][1] = function(self.network[layer_x][0],preactivation)
            else:
                # On calcule la couche par rapport à la couche precedante
                preactivation = np.dot(self.network[layer_x-1][1],self.network[layer_x][2])
                self.network[layer_x][1] = function(self.network[layer_x][0],preactivation)

    def predict(self,input_layer:list):
        input_layer = np.array(input_layer)
        self.feedforward(input_layer)
        return self.network[-1][1]

    def save(self,path:str):
        """
        PATH : folder
        """
        if path != "":
            if path[-1] != '/' and path[-1] != '\\':
                path += '/'
            if path == "/" or path == "\\":
                path = ""
        # Default_data est la pour associer des fonction au layer
        default_data = []
        # default_data = [fonctionlayer1,fonctionlayer2,...]
        # sauvegarde des array
        # pour chaque couche du reseau de neurone
        for layer_x,layer in enumerate(self.network):
            # on ajoute la fonction de la couche
            default_data.append(layer[0])
            # on save la couche
            np.savez(path+str(layer_x),layer[2])
        #on sauvegarde le default
        with open(path+"default.txt","w") as outfile:
            json.dump(default_data,outfile)

    def load(self,path:str):
        """
        PATH : folder
        """
        if path != "":
            if path[-1] != '/' and path[-1] != '\\':
                path += '/'
            if path == "/" or path == "\\":
                path = ""
        # on reinitialise le network
        self.network = []
        # on charge la config
        with open(path+"default.txt") as json_file:
            function_list = json.load(json_file)
        # on charge les couches
        for x_layer,layer_function in enumerate(function_list):
            # on charge les poids de la couche
            weights_data = np.load(path+str(x_layer)+".npz")["arr_0"]
            # on créé une couche vide
            temp = []
            # on ajoute la fonction d'activation
            temp.append(layer_function)
            # on genere des 0 pour les activation
            temp.append(0)
            # on ajoute les poids
            temp.append(weights_data)
            temp.append(0)
            temp.append(0)
            self.network.append(temp)
