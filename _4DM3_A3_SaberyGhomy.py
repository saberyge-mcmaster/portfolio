"""
Author/Student Name (Student ID): Ehsan Sabery Ghomy (400345079)
Professor Name: Dr. Jeff Fortuna
Course: SFWR TECH 4DM3 (Data Mining)
Due Date: April 12, 2023

IDE: Microsoft Visual Studio Community 2019 - Version 16.11.20
Python Environment: Python 3.8 (64-bit) (anaconda3 - Anaconda3-2020.11-Windows-x86_64)
File Name: _4DM3_A3_SaberyGhomy.py




Description: Assignment 3 - Naïve Bayesian Classification


**** There are two files created based on the data given on two tables: trainingData.xlsx and testingData.xlsx



Question 1. Consider the following data for purchasing automobiles: (trainingData.xlsx)


Where each attribute is described as:
Purchase $ = {very high, high, medium, low}
Maintenance $ = {very high, high, medium, low}
# of Doors = {2, 4}
Trunk Size = {large, medium, small}
Safety = {high, medium, low}
Acceptability = {acceptable, unacceptable}


Note that all of the attributes are nominal, so there is no need to use a normal distribution model. 
Construct a Naïve Bayesian Classifier assuming that Acceptability is the target attribute and classify the 
following data (testingData.xlsx). Report the number of errors that you make.




Additional Notes (Assumptions): 

If I cannot classify an example (i.e., both probability values are equal, or both values are 0,) 
which will result in prediction being unknown,
I will assume it is an error.

"""


import numpy
import pandas
import copy
import math



def getRawData():
    trainingData= pandas.DataFrame.to_numpy(pandas.read_excel('trainingData.xlsx', header=None))
    trainingData = trainingData[2:,1:]
    testingData = pandas.DataFrame.to_numpy(pandas.read_excel('testingData.xlsx', header=None))
    testingData = testingData[1:,1:]
    return trainingData, testingData

def question1(trainingData,testingData):
    
    #training part

    n = len(trainingData) #total number of training data



    #number of each 'Acceptability' column's classes (Label)
    
    #it will give an array of bool values where if index is acceptable, it is True, if not acceptable, it is False
    #then, it will count up (sum) all the True values in that array.
    num_acceptable = numpy.all(trainingData[:,[5]]==['acceptable'],axis=1).sum()

    #it will give an array of bool values where if index is unacceptable, it is True, if not unacceptable, it is False
    #then, it will count up (sum) all the True values in that array.
    num_unacceptable = numpy.all(trainingData[:,[5]]==['unacceptable'],axis=1).sum()




    #probability of each 'Acceptability' column's classes (Label)
    prob_acceptable = num_acceptable/n
    prob_unacceptable = num_unacceptable/n




    #Probability of 'Purchase $' column's sets that are either acceptable or unacceptable


    #it will give an array of bool values where if (col[5] is acceptable AND col[0] is very high), it is True, otherwise, it is False
    #then, it will count up (sum) all the True values in that array. Then will divide by num_acceptable to give the probability.
    prob_purchase_very_high_a = numpy.all(trainingData[:,[0,5]]==['very high','acceptable'],axis=1).sum()/num_acceptable

    #it will give an array of bool values where if (col[5] is unacceptable AND col[0] is very high), it is True, otherwise, it is False
    #then, it will count up (sum) all the True values in that array. Then will divide by num_unacceptable to give the probability.
    # (This concept is the same for the rest of the code, but with different col index values.)
    prob_purchase_very_high_u = numpy.all(trainingData[:,[0,5]]==['very high','unacceptable'],axis=1).sum()/num_unacceptable



    prob_purchase_high_a= numpy.all(trainingData[:,[0,5]]==['high','acceptable'],axis=1).sum()/num_acceptable
    prob_purchase_high_u= numpy.all(trainingData[:,[0,5]]==['high','unacceptable'],axis=1).sum()/num_unacceptable

    prob_purchase_medium_a =  numpy.all(trainingData[:,[0,5]]==['medium','acceptable'],axis=1).sum()/num_acceptable
    prob_purchase_medium_u =  numpy.all(trainingData[:,[0,5]]==['medium','unacceptable'],axis=1).sum()/num_unacceptable
    
    prob_purchase_low_a = numpy.all(trainingData[:,[0,5]]==['low','acceptable'],axis=1).sum()/num_acceptable
    prob_purchase_low_u = numpy.all(trainingData[:,[0,5]]==['low','unacceptable'],axis=1).sum()/num_unacceptable
    

    #Probability of 'Maintenance $' column's sets that are either acceptable or unacceptable
    prob_maintenance_very_high_a = numpy.all(trainingData[:,[1,5]]==['very high','acceptable'],axis=1).sum()/num_acceptable
    prob_maintenance_very_high_u = numpy.all(trainingData[:,[1,5]]==['very high','unacceptable'],axis=1).sum()/num_unacceptable

    prob_maintenance_high_a= numpy.all(trainingData[:,[1,5]]==['high','acceptable'],axis=1).sum()/num_acceptable
    prob_maintenance_high_u= numpy.all(trainingData[:,[1,5]]==['high','unacceptable'],axis=1).sum()/num_unacceptable

    prob_maintenance_medium_a =  numpy.all(trainingData[:,[1,5]]==['medium','acceptable'],axis=1).sum()/num_acceptable
    prob_maintenance_medium_u =  numpy.all(trainingData[:,[1,5]]==['medium','unacceptable'],axis=1).sum()/num_unacceptable
    
    prob_maintenance_low_a = numpy.all(trainingData[:,[1,5]]==['low','acceptable'],axis=1).sum()/num_acceptable
    prob_maintenance_low_u = numpy.all(trainingData[:,[1,5]]==['low','unacceptable'],axis=1).sum()/num_unacceptable
    


    #Probability of '# of Doors' column's sets that are either acceptable or unacceptable
    #because it is number (int) for this column, I will turn them into string, otherwise, it will not work, even when turning the inside of the index to int value.

    trainingData[trainingData==2] = '2'
    prob_doors_2_a = numpy.all(trainingData[:,[2,5]]==['2','acceptable'],axis=1).sum()/num_acceptable
    prob_doors_2_u = numpy.all(trainingData[:,[2,5]]==['2','unacceptable'],axis=1).sum()/num_unacceptable

    trainingData[trainingData==4] = '4'
    prob_doors_4_a= numpy.all(trainingData[:,[2,5]]==['4','acceptable'],axis=1).sum()/num_acceptable
    prob_doors_4_u= numpy.all(trainingData[:,[2,5]]==['4','unacceptable'],axis=1).sum()/num_unacceptable
    

    #Probability of 'Trunk Size' column's sets that are either acceptable or unacceptable
    prob_trunk_size_large_a= numpy.all(trainingData[:,[3,5]]==['large','acceptable'],axis=1).sum()/num_acceptable
    prob_trunk_size_large_u= numpy.all(trainingData[:,[3,5]]==['large','unacceptable'],axis=1).sum()/num_unacceptable

    prob_trunk_size_medium_a =  numpy.all(trainingData[:,[3,5]]==['medium','acceptable'],axis=1).sum()/num_acceptable
    prob_trunk_size_medium_u =  numpy.all(trainingData[:,[3,5]]==['medium','unacceptable'],axis=1).sum()/num_unacceptable
    
    prob_trunk_size_small_a = numpy.all(trainingData[:,[3,5]]==['small','acceptable'],axis=1).sum()/num_acceptable
    prob_trunk_size_small_u = numpy.all(trainingData[:,[3,5]]==['small','unacceptable'],axis=1).sum()/num_unacceptable
    

    #Probability of 'Safety' column's sets that are either aceeptable or unacceptable
    prob_safety_high_a= numpy.all(trainingData[:,[4,5]]==['high','acceptable'],axis=1).sum()/num_acceptable
    prob_safety_high_u= numpy.all(trainingData[:,[4,5]]==['high','unacceptable'],axis=1).sum()/num_unacceptable

    prob_safety_medium_a =  numpy.all(trainingData[:,[4,5]]==['medium','acceptable'],axis=1).sum()/num_acceptable
    prob_safety_medium_u =  numpy.all(trainingData[:,[4,5]]==['medium','unacceptable'],axis=1).sum()/num_unacceptable
    
    prob_safety_low_a = numpy.all(trainingData[:,[4,5]]==['low','acceptable'],axis=1).sum()/num_acceptable
    prob_safety_low_u = numpy.all(trainingData[:,[4,5]]==['low','unacceptable'],axis=1).sum()/num_unacceptable
    

    #display results
    print("Training Part:")
    print('\nTotal number of training examples:',n)
    print('Total number of (acceptable) class:',num_acceptable)
    print('Total number of (unacceptable) class:',num_unacceptable)
    
    print("\nProbability of the Class Label:")
    print('P(acceptable):', prob_acceptable)
    print('P(unacceptable):', prob_unacceptable)

    print("\nProbability of the Column Purchase $:")
    print('P(very high | acceptable):', prob_purchase_very_high_a)
    print('P(high | acceptable):', prob_purchase_high_a)
    print('P(medium | acceptable):', prob_purchase_medium_a)
    print('P(low | acceptable):', prob_purchase_low_a)
    print('P(very high | unacceptable):', prob_purchase_very_high_u)
    print('P(high | unacceptable):', prob_purchase_high_u)
    print('P(medium | unacceptable):', prob_purchase_medium_u)
    print('P(low | unacceptable):', prob_purchase_low_u)

    print("\nProbability of the Column Maintenance $:")
    print('P(very high | acceptable):', prob_maintenance_very_high_a)
    print('P(high | acceptable):', prob_maintenance_high_a)
    print('P(medium | acceptable):', prob_maintenance_medium_a)
    print('P(low | acceptable):', prob_maintenance_low_a)
    print('P(very high | unacceptable):', prob_maintenance_very_high_u)
    print('P(high | unacceptable):', prob_maintenance_high_u)
    print('P(medium | unacceptable):', prob_maintenance_medium_u)
    print('P(low | unacceptable):', prob_maintenance_low_u)

    print("\nProbability of the Column # of Doors:")
    print('P(2 | acceptable):',prob_doors_2_a)
    print('P(4 | acceptable):',prob_doors_4_a)
    print('P(2 | unacceptable):',prob_doors_2_u)
    print('P(4 | unacceptable):',prob_doors_4_u)

    print("\nProbability of the Column Trunk Size:")
    print('P(large | acceptable):',prob_trunk_size_large_a)
    print('P(medium | acceptable):',prob_trunk_size_medium_a)
    print('P(small | acceptable):',prob_trunk_size_small_a)
    print('P(large | unacceptable):',prob_trunk_size_large_u)
    print('P(medium | unacceptable):',prob_trunk_size_medium_u)
    print('P(small | unacceptable):',prob_trunk_size_small_u)



    print("\nProbability of the Column Safety:")
    print('P(high | acceptable):',prob_safety_high_a)
    print('P(medium | acceptable):',prob_safety_medium_a)
    print('P(low | acceptable):',prob_safety_low_a)
    print('P(high | unacceptable):',prob_safety_high_u)
    print('P(medium | unacceptable):',prob_safety_medium_u)
    print('P(low | unacceptable):',prob_safety_low_u)



    #testing part:

    print("\nTesting Part:")

    n_testing = len(testingData)

    total_num_errors=0

    for i in range(n_testing):
        display_text_a = 'P(A)*'
        display_equation_a = "(" + str(prob_acceptable) + ")"
        prob_a = prob_acceptable

        display_text_u = 'P(U)*'
        display_equation_u = "(" +  str(prob_unacceptable) + ")"
        prob_u = prob_unacceptable
    
        #checking Purchase column
        if (testingData[i][0].lower() == 'very high'):
            display_text_a += 'P(very high_purchase |A)*'
            display_equation_a +=  "("+ str(prob_purchase_very_high_a)+ ")"
            prob_a *= prob_purchase_very_high_a
            
            display_text_u += 'P(very high__purchase |U)*'
            display_equation_u +=  "("+ str(prob_purchase_very_high_u)+ ")"
            prob_u *= prob_purchase_very_high_u

        elif (testingData[i][0].lower() == 'high'):
            display_text_a += 'P(high__purchase |A)*'
            display_equation_a +=  "("+ str(prob_purchase_high_a)+ ")"
            prob_a *= prob_purchase_high_a

            display_text_u += 'P(high__purchase |U)*'
            display_equation_u +=  "("+ str(prob_purchase_high_u)+ ")"
            prob_u *= prob_purchase_high_u

        elif (testingData[i][0].lower() == 'medium'):
            display_text_a += 'P(medium__purchase |A)*'
            display_equation_a +=  "("+ str(prob_purchase_medium_a)+ ")"
            prob_a *= prob_purchase_medium_a

            display_text_u += 'P(medium__purchase |U)*'
            display_equation_u +=  "("+ str(prob_purchase_medium_u)+ ")"
            prob_u *= prob_purchase_medium_u

        elif (testingData[i][0].lower() == 'low'):
            display_text_a += 'P(low__purchase |A)*'
            display_equation_a +=  "("+ str(prob_purchase_low_a)+ ")"
            prob_a *= prob_purchase_low_a

            display_text_u += 'P(low__purchase |U)*'
            display_equation_u +=  "("+ str(prob_purchase_low_u)+ ")"
            prob_u *= prob_purchase_low_u

        #
        #checking Maintenance column
        if (testingData[i][1].lower() == 'very high'):
            display_text_a += 'P(very high_maintenance |A)*'
            display_equation_a +=  "("+ str(prob_maintenance_very_high_a)+ ")"
            prob_a *= prob_maintenance_very_high_a

            display_text_u += 'P(very high_maintenance |U)*'
            display_equation_u +=  "("+ str(prob_maintenance_very_high_u)+ ")"
            prob_u *= prob_maintenance_very_high_u

        elif (testingData[i][1].lower() == 'high'):
            display_text_a += 'P(high_maintenance |A)*'
            display_equation_a +=  "("+ str(prob_maintenance_high_a)+ ")"
            prob_a *= prob_maintenance_high_a

            display_text_u += 'P(high_maintenance |U)*'
            display_equation_u +=  "("+ str(prob_maintenance_high_u)+ ")"
            prob_u *= prob_maintenance_high_u

        elif (testingData[i][1].lower() == 'medium'):
            display_text_a += 'P(medium_maintenance |A)*'
            display_equation_a +=  "("+ str(prob_maintenance_medium_a)+ ")"
            prob_a *= prob_maintenance_medium_a

            display_text_u += 'P(medium_maintenance |U)*'
            display_equation_u +=  "("+ str(prob_maintenance_medium_u)+ ")"
            prob_u *= prob_maintenance_medium_u

        elif (testingData[i][1].lower() == 'low'):
            display_text_a += 'P(low_maintenance |A)*'
            display_equation_a +=  "("+ str(prob_maintenance_low_a)+ ")"
            prob_a *= prob_maintenance_low_a

            display_text_u += 'P(low_maintenance |U)*'
            display_equation_u +=  "("+ str(prob_maintenance_low_u)+ ")"
            prob_u *= prob_maintenance_low_u

        #
        #checking # of Doors column
        if (testingData[i][2] == 2):
            display_text_a += 'P(2_#_doors |A)*'
            display_equation_a +=  "("+ str(prob_doors_2_a)+ ")"
            prob_a *= prob_doors_2_a

            display_text_u += 'P(2_#_doors |U)*'
            display_equation_u +=  "("+ str(prob_doors_2_u)+ ")"
            prob_u *= prob_doors_2_u

        elif (testingData[i][2] == 4):
            display_text_a += 'P(4_#_doors |A)*'
            display_equation_a +=  "("+ str(prob_doors_4_a)+ ")"
            prob_a *= prob_doors_4_a

            display_text_u += 'P(4_#_doors |U)*'
            display_equation_u +=  "("+ str(prob_doors_4_u)+ ")"
            prob_u *= prob_doors_4_u

        #
        #checking Trunk Size column
        if (testingData[i][3].lower() == 'large'):
            display_text_a += 'P(large_trunk_size |A)*'
            display_equation_a +=  "("+ str(prob_trunk_size_large_a)+ ")"
            prob_a *= prob_trunk_size_large_a

            display_text_u += 'P(large_trunk_size |U)*'
            display_equation_u +=  "("+ str(prob_trunk_size_large_u)+ ")"
            prob_u *= prob_trunk_size_large_u

        elif (testingData[i][3].lower() == 'medium'):
            display_text_a += 'P(medium_trunk_size |A)*'
            display_equation_a +=  "("+ str(prob_trunk_size_medium_a)+ ")"
            prob_a *= prob_trunk_size_medium_a

            display_text_u += 'P(medium_trunk_size |U)*'
            display_equation_u +=  "("+ str(prob_trunk_size_medium_u)+ ")"
            prob_u *= prob_trunk_size_medium_u

        elif (testingData[i][3].lower() == 'small'):
            display_text_a += 'P(small_trunk_size |A)*'
            display_equation_a +=  "("+ str(prob_trunk_size_small_a)+ ")"
            prob_a *= prob_trunk_size_small_a

            display_text_u += 'P(small_trunk_size |U)*'
            display_equation_u +=  "("+ str(prob_trunk_size_small_u)+ ")"
            prob_u *= prob_trunk_size_small_u
        

        #
        #checking Safety column
        if (testingData[i][4].lower() == 'high'):
            display_text_a += 'P(high_safety |A)'
            display_equation_a +=  "("+ str(prob_safety_high_a)+ ")"
            prob_a *= prob_safety_high_a

            display_text_u += 'P(high_safety |U)'
            display_equation_u +=  "("+ str(prob_safety_high_u)+ ")"
            prob_u *= prob_safety_high_u

        elif (testingData[i][4].lower() == 'medium'):
            display_text_a += 'P(medium_safety |A)'
            display_equation_a +=  "("+ str(prob_safety_medium_a)+ ")"
            prob_a *= prob_safety_medium_a

            display_text_u += 'P(medium_safety |U)'
            display_equation_u +=  "("+ str(prob_safety_medium_u)+ ")"
            prob_u *= prob_safety_medium_u

        elif (testingData[i][4].lower() == 'low'):
            display_text_a += 'P(low_safety |A)'
            display_equation_a +=  "("+ str(prob_safety_low_a)+ ")"
            prob_a *= prob_safety_low_a

            display_text_u += 'P(low_safety |U)'
            display_equation_u +=  "("+ str(prob_safety_low_u)+ ")"
            prob_u *= prob_safety_low_u

        ##display some results
        print("\nClassifying: " + str(i+1) + "/"+str(n_testing) + ":")
        print("The unseen sample X = <" + testingData[i][0].lower() + "_purchase, "+ testingData[i][1].lower()
              + "_maintenance, "+ str(testingData[i][2]) + "_#_doors, " + testingData[i][3].lower()
              + "_trunk_size, " + testingData[i][4].lower() + "_safety>")
        print("\nP(A|X):")
        print("= "+display_text_a)
        print("= "+ display_equation_a)
        print("= " + str(prob_a))

        print("\nP(U|X):")
        print("= "+display_text_u)
        print("= "+ display_equation_u)
        print("= " + str(prob_u))
        
        #calculate/display classification:
        label = ""

        if (prob_a > prob_u):
            label = "acceptable"
        elif (prob_u > prob_a):
            label = "unacceptable"
        else:
            label = "unknown"  #either 0 or they are the same

        print("\nTherefore, we predict: " + label)

        #checking for error.
        if (label == testingData[i][5]):
            print("Our prediction is Correct!")
        else:
            total_num_errors += 1
            if (label == 'acceptable' or label == 'unacceptable'):
                print("Our prediction is Incorrect.")
            else:
                print("Our prediction is Unknown.")

    #
    print("\n----------------------------------------------------------------")
    print("For any prediction that is Unknown, I will assume it is an error.")
    print("After classifying " + str(n_testing) + " unseen samples, we got " + str(total_num_errors) + " errors.")
    print("Therefore, our predictions were correct for " + str(n_testing-total_num_errors) + "/" + str(n_testing) + ".")
    



def main():
    try:
        trainingData, testingData = getRawData() #getting the training Data and testing Data
    except FileNotFoundError:
        print("Error, trainingData.xlsx and/or testingData.xlsx not found.")
        input("Please press Enter key to close the program...")
        return

    question1(trainingData,testingData)
    print("\nEnd of Assignment 3.")
    input("Please press Enter key to close the program...")
    




main()



#End of File: _4DM3_A3_SaberyGhomy.py