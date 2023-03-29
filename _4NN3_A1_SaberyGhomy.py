"""
Author (Student Name): Ehsan Sabery Ghomy (400345079)
Professor Name: Dr. Jeff Fortuna
Course: SFWR TECH 4NN3 (Neural Networks and Deep Learning)
Due Date: October 17, 2022
IDE: Spyder 4.1.5 (ANACONDA.NAVIGATOR (anaconda3)) (Python 3.8.5)
File Name: _4NN3_A1_SaberyGhomy.py
Description: Assignment 1 - Perceptron

             1. Create 2 classes of data, both two dimensional 
             and normally distributed. Each class should have 1000 data points.
             Specifically, the mean for the first class should be [-6 0] 
             and the second class should be [6 0]. 
             Additionally, class 1 should have variances of 3 and 1 for 
             two dimensions. The covariance should be 1. Class 2 should 
             have variances of 1 and 2 for the two dimensions. 
             The covariance should be 1.
             
             Create a plot of how many errors you obtain while training 
             the perceptron over each iteration. 
             You should perform a maximum of 100 iterations (epochs). 
             Use a learning rate of 0.001.
             
             2. Repeat part 1 but with a mean of [-2 0] for the first class 
             and [2 0] for the second class.
             
             3. Create 2 classes of data, as above. Specifically, the mean 
             for the first class should be [-3 -3] and the second class 
             should be [3 3]. Additionally, class 1 should have variances 
             of 3 and 1 for two dimensions. The covariance should be 0. 
             Class 2 should have variances of 1 and 2 for the two dimensions. 
             The covariance should be 0. Perform 100 iterations of training 
             and create a plot of the data and the resulting decision 
             boundary (i.e. a line). Use a learning rate of 0.001.
             
             4. Repeat part 3 but with a mean of [-6 -6] for the first class 
             and [6 6] for the second class.
"""



import numpy
import matplotlib.pyplot
import random
#import math


class Perceptron(object):
    
    def __init__(self, mean1, mean2, cov1, cov2, data_points, learning_rate, epochs, title):
        self.__mean1 = mean1                    #Mean1
        self.__mean2 = mean2                    #Mean2
        self.__cov1 = cov1                      #Covariance_Matrix 1
        self.__cov2 = cov2                      #Covariance_Matrix 2
        self.__data_points = data_points        #data_points (n)
        self.__learning_rate = learning_rate    #learning_rate (c)
        self.__epochs = epochs                  #epochs (max iterations)
        self.__title = title                    #the title
        
        #create 2 classes of data, class1_Data and class2_Data, each 2-Dimension (x1, x2) and normally distributed (inputs)
        self.__class1_Data = numpy.random.multivariate_normal(self.__mean1, self.__cov1, self.__data_points)
        self.__class2_Data = numpy.random.multivariate_normal(self.__mean2, self.__cov2, self.__data_points)
        
        
        #concatenate both classes of data, so class2_Data under class1_Data.
        self.__X = numpy.concatenate((self.__class1_Data, self.__class2_Data), axis=0)
        
        #augmented data matrix - add one column of ones for bias (Threshold)
        self.__X = numpy.concatenate((numpy.ones((self.__data_points * 2, 1)), self.__X), axis=1)
     
        
        #create labels (actual output) for both classes of Data.
        
        # for  class1_Data, actual output is zero.
        self.__t = numpy.zeros((self.__data_points,1)) 
        
        # for class2_Data, actual output is one.
        self.__t = numpy.concatenate((self.__t, numpy.ones((self.__data_points,1))), axis=0)
        
        
        
        #initialize weights - w  where w[0] is for bias (Threshold), w[1] is for first input x1, w[2] is for second input x2.
        random.seed()
        self.__w = numpy.transpose(numpy.array([random.random() -0.5, random.random() - 0.5, random.random() - 0.5]))
     
 
        self.__x_axis_training_epoch = []  #x axis label for training epoch.
        self.__y_axis_error = [] #y axis label for the number of errors.
        
        
        #To have the smallestError with its weights. [0] is Threshold weight, [1] is x1 Weight, [2] is x2 Weight, [3] is smallest errors.
        self.__smallestError = [self.__w[0], self.__w[1], self.__w[2], self.__data_points *2]
        
        print("\n\n" + self.__title + ":")
        
        
        #the algorithm
        for epoch in range(self.__epochs):
            totalError = 0
            for i in range(self.__data_points * 2):
                #this is the perceptron algorithm
                
                #implement the calculation of the output (prediction) (z)
                #using Vectors
                z = 1 if (numpy.dot(self.__X[i,:],self.__w)>=0) else 0
                
                
                #can also do for finding z when having -> import math <-  at the top:
                #z = math.ceil((numpy.sign(numpy.dot(self.__X[i,:],self.__w))+1)/2)
                
                
                #calculate the error and update weights
                # delta w_i = c*(t-z)*x_i
                # w_new = w_old + delta w
                error = self.__t[i] - z
                self.__w += self.__learning_rate * (error) * self.__X[i,:]
                
                #for our own reporting use:
                totalError += abs(error)
                
            print("epoch #%-5s" %(epoch+1) , "=> Total Error: " + str(int(totalError[0])))
            self.__x_axis_training_epoch.append(epoch+1)
            self.__y_axis_error.append(totalError)
            
            if self.__smallestError[3] > totalError:
                self.__smallestError =  [self.__w[0], self.__w[1], self.__w[2], totalError]
        
        
        self.__slope = (-self.__smallestError[1])/self.__smallestError[2] #slope of smallest error in given number of training epochs.
        self.__y_int = (-self.__smallestError[0])/self.__smallestError[2] #y-int of smallest error in given number of training epochs.
       
        print("\nSmallest Error: " + str(int(self.__smallestError[3])) + ".")
        print("Smallest Error Weight for Threshold:", self.__smallestError[0])
        print("Smallest Error Weight for First Input x1:", self.__smallestError[1])    
        print("Smallest Error Weight for Second Input x2:", self.__smallestError[2]) 
        
        print("\nThe Slope for Smallest Error: " + str(self.__slope))
        print("The Y-Intercept for Smallest Error: " + str(self.__y_int))
        
        print("End of " + self.__title)
    
    
    
    
    #To display the scatter data with the resulting decision boundary (i.e. a line)
    def displayPlot_ScatterData_And_A_Line(self):
        
        fig, ax = matplotlib.pyplot.subplots()
        
        ax.scatter(self.__class1_Data[:,0], #x axis (Horizontal) x1
                   self.__class1_Data[:,1], #y axis (Vertial)    x2
                   c='b', marker = ".")
        
        ax.scatter(self.__class2_Data[:,0], #x axis (Horizontal) x1
                   self.__class2_Data[:,1], #y axis (Vertical)   x2
                   c='r', marker = ".")
        
        ax.axline((0,self.__y_int), slope= self.__slope, color='#929591') #color = gray
        
        
        matplotlib.pyplot.xlabel("First Input (x1)\n\nBlue = Class 1, Red = Class 2, Gray= A Line")
        matplotlib.pyplot.ylabel("Second Input (x2)")
        matplotlib.pyplot.title(self.__title + " - Scatter Data with Resulting Decision Boundary")
        matplotlib.pyplot.show()
        
           
        
    #To display the plot of number of errors for each training epochs.
    def displayPlot_TotalErrors(self):
        matplotlib.pyplot.plot(self.__x_axis_training_epoch, self.__y_axis_error)
        matplotlib.pyplot.xlabel("Training Epoch")
        matplotlib.pyplot.ylabel("Errors")
        matplotlib.pyplot.title(self.__title + " - Total Errors")
        matplotlib.pyplot.show()
            
            
    
                
    



def assignment1_4NN3():  
    Part1 = Perceptron([-6,0],             #Mean1
                       [6, 0],             #Mean2
                       [[3,1],[1,1]],      #Covariance_Matrix 1
                       [[1,1],[1,2]],      #Covariance_Matrix 2
                       1000,               #data_points
                       0.001,              #learning_rate
                       100,                #epochs
                       "Part 1")           #title
    
    Part1.displayPlot_TotalErrors()


    Part2 = Perceptron([-2,0],             #Mean1
                       [2, 0],             #Mean2
                       [[3,1],[1,1]],      #Covariance_Matrix 1
                       [[1,1],[1,2]],      #Covariance_Matrix 2
                       1000,               #data_points
                       0.001,              #learning_rate
                       100,                #epochs
                       "Part 2")           #title

    Part2.displayPlot_TotalErrors()
    
    Part3 = Perceptron([-3,-3],            #Mean1
                       [3, 3],             #Mean2
                       [[3,0],[0,1]],      #Covariance_Matrix 1
                       [[1,0],[0,2]],      #Covariance_Matrix 2
                       1000,               #data_points
                       0.001,              #learning_rate
                       100,                #epochs
                       "Part 3")           #title
    
    Part3.displayPlot_ScatterData_And_A_Line()
    
    Part4 = Perceptron([-6,-6],            #Mean1
                       [6, 6],             #Mean2
                       [[3,0],[0,1]],      #Covariance_Matrix 1
                       [[1,0],[0,2]],      #Covariance_Matrix 2
                       1000,               #data_points
                       0.001,              #learning_rate
                       100,                #epochs
                       "Part 4")           #title
    
    Part4.displayPlot_ScatterData_And_A_Line()
    





def main(): 
    assignment1_4NN3()
    input('End of Assignment 1. Please press Enter to continue...')




main()
    

#End of File: _4NN3_A1_SaberyGhomy.py























