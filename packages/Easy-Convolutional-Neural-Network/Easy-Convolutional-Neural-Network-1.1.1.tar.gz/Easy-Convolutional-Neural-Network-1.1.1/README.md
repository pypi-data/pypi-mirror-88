# ECNN

Simplify the creation of convolutional neural network


## Installation

Run the following to install:
```python
pip install Easy-Convolutional-Neural-Network
```


## Usage
```python
from ECNN import *

####Initialise network####
my_network = ECNN.neural_network()

#Config the network
nb_input = 4
hidden_layer = [
    [5,'Sigmoid'],# First layer with 5 neurons and have Sigmoid function
    [3,'Tanh'],
    [6,'ReLU']
]
nb_output = 1
output_function = 'Sigmoid'
#Function :
# Tanh (z)
# Sigmoid (z)
# ReLU (z)
# Binary-Step (z)

my_network.make(nb_input,hidden_layer,nb_output,output_function)

# Make the dataset
input_dataset = [
    [0,0,0,1],
    [0,0,1,1],
    [0,1,1,1],
    [1,0,1,0],
    [1,1,1,1]
]
# Make the expected values
expected = [
    [0],
    [0],
    [1],
    [0],
    [1]
]
# Train with dataset
iteration = 2000
# Start the training
my_network.train(input_dataset,expected,iteration,display=True)

# Make prediction values
test_inputs = [1,1,1,0]
print(my_network.predict(test_inputs)) 

# Save the network
my_network.save("networkData/")

# Load other network
my_network.load("networkData2/")
```


```bash
$ pip install -e .[dev]
```