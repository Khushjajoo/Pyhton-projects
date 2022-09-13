import matplotlib.pyplot as plt
import csv
import numpy as np
from numpy.lib.function_base import gradient

class Housingcosts:
    def __init__(self):
        self.costs = [] # list of costs
        self.items = [] # list of items
    
    def read_csv(self, filename): # read csv file
        with open(filename, 'r') as csvfile:
            read = csv.reader(csvfile)
            next(read)
            for row in read:
                self.costs.append(float(row[-1]))
                self.items.append(row[1:-1])              
            self.items = np.matrix(self.items)
            self.items = self.items.astype(np.float)
            self.costs = np.matrix(self.costs).T
            self.costs = self.costs.astype(np.float)

    def len(self): # number of records in the dataset
            return self.items.shape[0]

    def mean(self): # mean value of the costs
           return np.mean(self.costs)

    def max(self): # maximal cost
        return np.amax(self.costs)
            
    def min(self): # minimal cost
        return np.amin(self.costs)

    def deviation(self): # standard deviation of the costs
        return np.std(self.costs)
            
    def plot(self): 
        plt.hist(self.costs, bins=30) # plotting histogram of the costs
        plt.xlabel("Price") # x-axis label
        plt.ylabel("Frequency") # y-axis label
        plt.show()

    def pred(self, weight): # calculatiing predicted value based on current weight and feature values
        return np.dot(self.items, weight)

    def loss (self, p): # calculates the loss based on a set of predicted sale price and the correct sale price
        return np.sum(np.square(self.costs - p))/self.len()

    def gradient(self, p): # calculates the gradient based on a set of predicted sale price and the correct sale price
        return -2 * np.dot(self.items.T, self.costs - p) / self.len()

    def update (self, weight, rate, gradient): # updates the weight based on the gradient and the learning rate
        return weight - rate * gradient

if __name__ == "__main__":
    ob = Housingcosts()
    ob.read_csv('train.csv')
    print ("Length is: ", ob.len()) 
    print ("Mean is: ", ob.mean())
    print ("Max is: ", ob.max())
    print ("Min is: ", ob.min())
    print ("Standard Deviation is: ", ob.deviation())
    ob.plot()

    weight = np.matrix([np.random.uniform(low=-1, high=1) for i in range(ob.items.shape[1])]).T # initializing the weight

    arr1 = [] # array for storing the loss values for learning rate 10 ** -11
    arr2 = [] # array for storing the loss values for learning rate 10 ** -12
    i = 0
    j = 0

    while i < 500: # 500 iterations as instucted
        i = i + 1
        pred  = ob.pred(weight) # calculating predicted value
        loss = ob.loss(pred) # calculating loss
        grad = ob.gradient(pred) # calculating gradient
        weight = ob.update(weight, 10 ** -11, grad) # updating weight
        print ("Iteration: ", i, "Loss: ", loss)
        arr1.append(loss.item()) # appending the loss values for learning rate 10 ** -11

    while j < 500: # 500 iterations as instucted
        j = j + 1
        pred  = ob.pred(weight) # calculating the predicted value
        loss = ob.loss(pred) # calculating the loss
        grad = ob.gradient(pred) # calculating the gradient
        weight = ob.update(weight, 10 ** -12, grad) # updating the weight
        print ("Iteration: ", j, "Loss: ", loss)
        arr2.append(loss.item()) # appending the loss values for learning rate 10 ** -12

    plt.plot(arr1) # plotting the loss values for learning rate 10 ** -11
    plt.plot(arr2) # plotting the loss values for learning rate 10 ** -12
    plt.legend (['MSE w/a=10^-11', 'MSE w/a=10^-12']) # labeling the plot
    plt.xlabel('Iterations') # labeling the x-axis
    plt.ylabel('MSE')  # labeling the y-axis
    plt.show() 

