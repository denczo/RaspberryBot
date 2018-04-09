import numpy
import scipy.special
from PIL import Image
import random

#https://stackoverflow.com/questions/32105954/how-can-i-write-a-binary-array-as-an-image-in-python

class neuralNetwork:

    def __init__(self, inputNodes, hiddenNodes, outputNodes, learningRate):
        self.inputNodes = inputNodes
        self.hiddenNodes = hiddenNodes
        self.outputNodes = outputNodes
        self.learningRate = learningRate

        self.weightsHidden = (numpy.random.rand(self.hiddenNodes, self.inputNodes) - 0.5)
        self.weightsOutput = (numpy.random.rand(self.hiddenNodes, self.outputNodes) - 0.5)

        self.activation_function = lambda x: scipy.special.expit(x)
        pass

    def train(self, input_list, target_list):

        inputs = numpy.array(input_list, ndmin=2).T
        targets =  numpy.array(target_list, ndmin=2).T
        hidden_inputs = numpy.dot(self.weightsHidden,inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = numpy.dot(self.weightsOutput.T,hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        output_errors = targets - final_outputs
        hidden_errors = numpy.dot(self.weightsOutput, output_errors)

       # #print((output_errors*final_outputs*(1.0 - final_outputs)).T)
      #  print(hidden_outputs)
     #   print(numpy.transpose((hidden_outputs)))
        #print("_________")
        #print(numpy.dot((output_errors*final_outputs*(1.0 - final_outputs)),hidden_outputs.T ))
        #print(numpy.dot(hidden_outputs,(output_errors*final_outputs*(1.0 - final_outputs)).T ).T)
        #print("_________")
        self.weightsOutput += self.learningRate * numpy.dot((output_errors*final_outputs*(1.0 - final_outputs)), hidden_outputs.T).T
        self.weightsHidden += self.learningRate * numpy.dot(hidden_errors*hidden_outputs*(1.0 - hidden_outputs),numpy.transpose(inputs))

    def query(self, inputs_list):
        inputs = numpy.array(inputs_list, ndmin=2).T
        hidden_inputs = numpy.dot(self.weightsHidden, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        #print(self.weightsOutput)
        #print(hidden_outputs)
        final_inputs = numpy.dot(self.weightsOutput.T,hidden_outputs)
        #print(final_inputs)
        final_outputs = self.activation_function(final_inputs)
        return final_outputs


if __name__ == "__main__":
    n = neuralNetwork(3,3,7,0.3)

    #print(numpy.array([1,1,1],ndmin=2).T)

    #R G B

    #R G B C Y M W
    """
    for i in range(1000):
               # R G B
        n.train([0.1,0.1,0.99],[0.1,0.1,0.99])
        n.train([0.1,0.99,0.1],[0.1,0.99,0.1])
        n.train([0.1,0.99,0.99],[0.1,0.99,0.99])
        n.train([0.99,0.1,0.1],[0.99,0.1,0.1])
        n.train([0.99,0.1,0.99],[0.99,0.1,0.99])
        n.train([0.99,0.99,0.1],[0.99,0.99,0.1])
        n.train([0.99,0.99,0.99],[0.99,0.99,0.99])
    """

    #print(numpy.dot(numpy.array([1,2,3], ndmin=2).T,numpy.array([1,2,3,4,5,6], ndmin=2)))
    img = Image.new('1', (50,50))


    for i in range(5000):
        # R G B
        n.train([0.1, 0.1, 0.99], [0.1, 0.1, 0.99, 0.1, 0.1, 0.1, 0.1])
        n.train([0.1, 0.99, 0.1], [0.1, 0.99, 0.1, 0.1, 0.1, 0.1, 0.1])
        n.train([0.1, 0.99, 0.99], [0.1, 0.99, 0.99, 0.1, 0.1, 0.1, 0.1])
        n.train([0.99, 0.1, 0.1], [0.99, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        n.train([0.99, 0.1, 0.99], [0.99, 0.1, 0.99, 0.1, 0.1, 0.1, 0.1])
        n.train([0.99, 0.99, 0.1], [0.99, 0.99, 0.1, 0.1, 0.1, 0.1, 0.1])
        n.train([0.99, 0.99, 0.99], [0.99, 0.99, 0.99, 0.1, 0.1, 0.1, 0.1])

    #print(n.query([[1,1,1]]))
    #print(n.query([[0,1,0]]))
    #print(n.query([[1,0,0]]))
    print(n.query([[0,0,1]]))
