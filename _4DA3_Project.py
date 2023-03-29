"""
Author/Student Name (Student ID): Ehsan Sabery Ghomy (400345079)
Professor Name: Dr. Jeff Fortuna
Course: SFWR TECH 4DA3 (Data Analytics and Big Data)
Due Date: December 21, 2022

IDE: Microsoft Visual Studio Community 2019 - Version 16.11.20
Python Environment: Python 3.8 (64-bit) (anaconda3 - Anaconda3-2020.11-Windows-x86_64)
File Name: _4DA3_Project.py

Description: Course Project (Comparing Classifiers)
"""


import numpy
import time
import sklearn.discriminant_analysis
import sklearn.neighbors



def getData():
        
    #Reading data from the file, and putting it in a matrix ROW x COL
    data = numpy.loadtxt('HTRU_2.csv', delimiter = ',')
       
    data_sorted = data[data[:,8].argsort()[::-1]]  #sorting data based on 9th column which is the class (label) in descending order.
   
       
    class_ArrayLocation = numpy.where(numpy.diff(data_sorted[:,8]))[0]+1  #shows the data's location(s) on Column 9th where classes change.

    #There are only 2 classes =>  CLASS 1 = X1 with LABEL = 1 (POSITIVE)  ----- and -----   CLASS 2 = X2 with LABEL = 0 (NEGATIVE)
    classifiedData = numpy.vsplit(data_sorted, class_ArrayLocation) #get two matrices based on two classes

    #have one matrix including the label for class 1 and class 2
    X1AndLabel1 = classifiedData[0]  
    X2AndLabel2 = classifiedData[1]

    #have two lists, one for the input 8 attributes (dimensions) and one for the label for class 1 and class 2
    X1AndLabel1 = numpy.hsplit(X1AndLabel1, [8])
    X2AndLabel2 = numpy.hsplit(X2AndLabel2, [8])

    #the input 8 attributes (dimensions) values (multivariate) for class 1 and class 2
    X1 = X1AndLabel1[0] 
    X2 = X2AndLabel2[0] 


    #the output values (label) for class 1 and class 2
    L1 = numpy.transpose(X1AndLabel1[1])
    L2 = numpy.transpose(X2AndLabel2[1])


    #keeping only 500 data points from each class for input and output
    X1 = numpy.array(X1[0:500,:])
    X2 = numpy.array(X2[0:500,:])

    L1 = numpy.array(L1[0,0:500])
    L2 = numpy.array(L2[0,0:500])

       
    #the training data with their labels
    X1_train = numpy.array(X1[0:int(len(X1)*0.75),:])
    X2_train = numpy.array(X2[0:int(len(X2)*0.75),:])
    L1_train = numpy.array(L1[0:int(len(L1)*0.75)])
    L2_train = numpy.array(L2[0:int(len(L2)*0.75)])


    #the testing data with their labels
    X1_test = numpy.array(X1[int(len(X1)*0.75):,:])
    X2_test = numpy.array(X2[int(len(X2)*0.75):,:])
    L1_test = numpy.array(L1[int(len(L1)*0.75):])
    L2_test = numpy.array(L2[int(len(L2)*0.75):])

    return X1_train, X2_train, L1_train, L2_train, X1_test, X2_test, L1_test, L2_test

    
       
        
def fld(X1_train, X2_train, L1_train, L2_train, X1_test, X2_test, L1_test, L2_test):

    TP = 0  #true positive
    TN = 0  #true negative
    FP = 0  #false positive
    FN = 0  #false negative


    #X1 = Positive class,  X2 = Negative class

    X_train = numpy.concatenate((X1_train,X2_train))
    L_train = numpy.concatenate((L1_train,L2_train))

    lda = sklearn.discriminant_analysis.LinearDiscriminantAnalysis()



    #training:
    training_start_time = time.time_ns()

    lda.fit(X_train,L_train)

    training_time = time.time_ns() - training_start_time   #in nanoseconds




    #testing:
    testing_start_time = time.time_ns()

    X1_predict = lda.predict(X1_test)
    X2_predict = lda.predict(X2_test)
 
    testing_time = time.time_ns() - testing_start_time  #in nanoseconds



    #confusion matrix:
   
    n = len(X1_predict)  #length X1_predict and X2_predict are the same, so I will use 1 for this variable.

    for i in range(n):
        if X1_predict[i] == L1_test[i]:
            TP = TP + 1
        else:
            FN = FN + 1 

        if X2_predict[i] == L2_test[i]:
            TN = TN + 1
        else:
            FP = FP + 1
            
    #confusion matrix in percentage
    TP = TP/n *100
    FN = FN/n * 100
    TN =TN/n * 100
    FP = FP/n * 100

    confusionMatrix = [[FP,TP],[TN,FN]]




    #display results:
    print("_____________________________________________________________________")
    print("\nFishers Linear Discriminant:")
    print("\nThe Confusion Matrix is as follows:")
    print("False Positive = " + str(round(confusionMatrix[0][0],2)) + "%")
    print("True Positive = " + str(round(confusionMatrix[0][1],2)) + "%")
    print("True Negative = " + str(round(confusionMatrix[1][0],2)) + "%")
    print("False Negative = " + str(round(confusionMatrix[1][1],2)) + "%")
    print("\nTraining Time = "+ str(round(training_time/10e9,6)) + " seconds.")
    print("Testing Time = "+ str(round(testing_time/10e9,6)) + " seconds.")
    print("_____________________________________________________________________\n")

    
        

def knn(X1_train, X2_train, L1_train, L2_train, X1_test, X2_test, L1_test, L2_test):
    TP = 0  #true positive
    TN = 0  #true negative
    FP = 0  #false positive
    FN = 0  #false negative


    #X1 = Positive class,  X2 = Negative class

    X_train = numpy.concatenate((X1_train,X2_train))
    L_train = numpy.concatenate((L1_train,L2_train))

    knn = sklearn.neighbors.KNeighborsClassifier()  #n_neighbors default = 5
    



    #training:
    training_start_time = time.time_ns()

    knn.fit(X_train,L_train)

    training_time = time.time_ns() - training_start_time   #in nanoseconds




    #testing:
    testing_start_time = time.time_ns()

    X1_predict = knn.predict(X1_test)
    X2_predict = knn.predict(X2_test)
 
    testing_time = time.time_ns() - testing_start_time  #in nanoseconds



    #confusion matrix:
   
    n = len(X1_predict)  #length X1_predict and X2_predict are the same, so I will use 1 for this variable.

    for i in range(n):
        if X1_predict[i] == L1_test[i]:
            TP = TP + 1
        else:
            FN = FN + 1 

        if X2_predict[i] == L2_test[i]:
            TN = TN + 1
        else:
            FP = FP + 1
            
    #confusion matrix in percentage
    TP = TP/n *100
    FN = FN/n * 100
    TN =TN/n * 100
    FP = FP/n * 100

    confusionMatrix = [[FP,TP],[TN,FN]]




    #display results:
    print("K Nearest Neighbors:")
    print("\nThe Confusion Matrix is as follows:")
    print("False Positive = " + str(round(confusionMatrix[0][0],2)) + "%")
    print("True Positive = " + str(round(confusionMatrix[0][1],2)) + "%")
    print("True Negative = " + str(round(confusionMatrix[1][0],2)) + "%")
    print("False Negative = " + str(round(confusionMatrix[1][1],2)) + "%")
    print("\nTraining Time = "+ str(round(training_time/10e9,6)) + " seconds.")
    print("Testing Time = "+ str(round(testing_time/10e9,6)) + " seconds.")
    print("_____________________________________________________________________\n")

   


      
def courseProject():

    try:
        X1_train, X2_train, L1_train, L2_train, X1_test, X2_test, L1_test, L2_test = getData()  #getting data

        fld(X1_train, X2_train, L1_train, L2_train, X1_test, X2_test, L1_test, L2_test) #first classifier using Fishers Linear Discriminant by using Linear Discriminant Analysis
        
        knn(X1_train, X2_train, L1_train, L2_train, X1_test, X2_test, L1_test, L2_test) #second classifier using K Nearest Neighbors

        input('End of Course Project. Please press Enter to continue...')

    except FileNotFoundError:
        print("Error, file was not found.\n" )
    
    except:
        print("Error, something went wrong...\n")





def main():
    courseProject()
    


main()
        

#End of File: _4DA3_Project.py



