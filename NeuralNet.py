import numpy
import scipy.special
from PIL import Image
import random
from tkinter import *
#import Tkinter

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
        #print(self.weightsHidden)
        #print("______________")
        #print(inputs)
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

    def convertNumbers(self, matrix):
        #print(matrix)
        array = matrix.getA1();
        array.astype(float)
        floatArray = numpy.zeros(len(array), dtype=float)
        #print(array)
        for i in range(len(array)):
            if(array[i] == 0.0):
                array[i] = 0.1
                floatArray[i] = 0.1
            elif(array[i] == 1.0):
                #print("JO")
                array[i] = 0.99
                floatArray[i] = 0.99
                #print(floatArray[i])
            else:
                print("FAIL")
        #return numpy.array(array,ndmin=2)
        print(floatArray)
        print("______________")
        return floatArray

if __name__ == "__main__":
    n = neuralNetwork(25,15,10,0.01)
    #root = tk.Tk()
    master = Tk()
    w = Canvas(master, width=250, height=200)
    w.pack()

    #print(numpy.array([1,1,1],ndmin=2))
    zero = numpy.matrix([[0, 0, 1, 0, 0],
                        [0, 1, 0, 1, 0],
                        [0, 1, 0, 1, 0],
                        [0, 1, 0, 1, 0],
                        [0, 0, 1, 0, 0]])

    one = numpy.matrix([ [0, 1, 1, 0, 0],
                         [0, 0, 1, 0, 0],
                         [0, 0, 1, 0, 0],
                         [0, 0, 1, 0, 0],
                         [0, 1, 1, 1, 0]])

    two = numpy.matrix([[0, 1, 1, 1, 0],
                        [0, 0, 0, 1, 0],
                        [0, 0, 0, 1, 0],
                        [0, 0, 1, 0, 0],
                        [0, 1, 1, 1, 0]])

    three = numpy.matrix([[0, 1, 1, 1, 0],
                          [0, 0, 0, 1, 0],
                          [0, 0, 1, 0, 0],
                          [0, 0, 0, 1, 0],
                          [0, 1, 1, 1, 0]])

    four = numpy.matrix([ [0, 1, 0, 1, 0],
                          [0, 1, 0, 1, 0],
                          [0, 1, 1, 1, 0],
                          [0, 0, 0, 1, 0],
                          [0, 0, 0, 1, 0]])

    five = numpy.matrix([ [0, 1, 1, 1, 0],
                          [0, 1, 0, 1, 0],
                          [0, 1, 1, 0, 0],
                          [0, 0, 0, 1, 0],
                          [0, 1, 1, 1, 0]])

    six = numpy.matrix([ [0, 1, 1, 1, 0],
                         [0, 1, 0, 0, 0],
                         [0, 1, 1, 1, 0],
                         [0, 1, 0, 1, 0],
                         [0, 1, 1, 1, 0]])

    seven = numpy.matrix([[0, 1, 1, 1, 0],
                          [0, 0, 0, 1, 0],
                          [0, 0, 0, 1, 0],
                          [0, 0, 0, 1, 0],
                          [0, 0, 0, 1, 0]])

    eight = numpy.matrix([[0, 1, 1, 1, 0],
                          [0, 1, 0, 1, 0],
                          [0, 0, 1, 0, 0],
                          [0, 1, 0, 1, 0],
                          [0, 1, 1, 1, 0]])

    nine = numpy.matrix( [[0, 1, 1, 1, 0],
                          [0, 1, 0, 1, 0],
                          [0, 1, 1, 1, 0],
                          [0, 0, 0, 1, 0],
                          [0, 1, 1, 1, 0]])

    #print(numpy.dot(numpy.array([1,2,3], ndmin=2).T,numpy.array([1,2,3,4,5,6], ndmin=2)))
    #img = Image.new('1', (50,50))

    #print(n.convertNumbers(zero))
    #img.show()
    zero = n.convertNumbers(zero)
    one = n.convertNumbers(one)
    two = n.convertNumbers(two)
    three = n.convertNumbers(three)
    four = n.convertNumbers(four)
    five = n.convertNumbers(five)
    six = n.convertNumbers(six)
    seven = n.convertNumbers(seven)
    eight = n.convertNumbers(eight)
    nine = n.convertNumbers(nine)

    for i in range(5000):
        n.train(zero, [0.99, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        n.train(one,  [0.1, 0.99, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        n.train(two,  [0.1, 0.1, 0.99, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        n.train(three,[0.1, 0.1, 0.1, 0.99, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        n.train(four, [0.1, 0.1, 0.1, 0.1, 0.99, 0.1, 0.1, 0.1, 0.1, 0.1])
        n.train(five, [0.1, 0.1, 0.1, 0.1, 0.1, 0.99, 0.1, 0.1, 0.1, 0.1])
        n.train(six,  [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.99, 0.1, 0.1, 0.1])
        n.train(seven,[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.99, 0.1, 0.1])
        n.train(eight,[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.99, 0.1])
        n.train(nine, [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.99])

    #print(n.query([[1,1,1]]))
    #print(n.query([[0,1,0]]))
    #print(n.query([[1,0,0]]))
    #print(n.query([[0,0,1]]))
    print(n.query(four))
    #root = Tk()
    size = 10
    gap = 5
    margin = 10
    """
    for i in range(5):
        x1 = i*(gap+size)+margin
        x2 = x1+size
        for j in range(5):

            y1 = j*(gap+size)+margin
            y2 = y1+size
            #print(x1,y1,x2,y2)
            #x1 y1 x2 y2
            w.create_rectangle(x1,y1,x2,y2, fill="white", outline="")
    """
    #w.pack()

    #mainloop()