"""
Author/Student Name (Student ID): Ehsan Sabery Ghomy (400345079)
Professor Name: Dr. Jeff Fortuna
Course: SFWRTECH 4DM3 (Data Mining)
Due Date: April 23, 2023

IDE: Microsoft Visual Studio Community 2019 - Version 16.11.20
Python Environment: Python 3.8 (64-bit) (anaconda3 - Anaconda3-2020.11-Windows-x86_64)
File Name: _4DM3_Project.py

Description: Course Project - Comparing Classifiers


For Summary, Please refer to the file: Summary_4DM3_Project.docx
Note: This python code is not optimized at all due to time constraints.
"""


import os 
import numpy 
import random
import time
import zipfile
import shutil   #for copy and paste of a file. also for removing the non-empty directory (Used to delete the top level folder for both faces files and non faces files after image is processed.)
from PIL import Image #for image processing/editing/etc...
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt



CONST_FACES_ZIP_FILE = 'faces in the wild training.zip'         #folder path for this zip file that was given by Dr. Fortuna for another course.
CONST_NON_FACES_ZIP_FILE = 'non_faces.zip'                      #folder path for this zip file that was given by Dr. Fortuna for another course.
CONST_FACES_FOLDER = 'faces in the wild training'               #top level folder path for faces files
CONST_NON_FACES_FOLDER = 'non_faces'                            #top level folder path for non faces files
CONST_DATA_NUMPY_FILE = 'data.npy'                              #file path to processed training and testing numpy DATA file
CONST_PREVIOUS_SAVED_RESULT_IMAGE = 'display_prev_results.png'  #image file that will display the previous saved results of the 3 classifiers (svm, adaboost and logistic regression)
CONST_MAX_NUM = 5000                                            #to use for extracting the number of images (from index 0 to this number -1) (I will NOT process all images, randomize it, then choose from index 0 to this number -1).
CONST_RESIZE_PIXELS_BOTH_WAYS = 64                              #to use this number for both the pixels high and pixels across. eg. 64x64
CONST_LABEL_VALUE_FACE = 1                                      #to use for the value of the label for the faces
CONST_LABEL_VALUE_NON_FACE = -1                                 #to use for the value of the label for the non-faces



#this is the first part of the project. Images needs to be processed before training and testing them.
def imageProcessing():
    print("\n_____________________________________________________________")
    print("\nImage Processing and Putting the Data into the NumPy DATA File:\n")
    imgFileNames_Faces = []
    imgFileNames_Non_Faces = []

    #error checking for extracting the zip files.
    try:
        #extracting the zip files into 2 top level folder path for faces and non faces files.
        print("\nPlease Wait. Extracting File:",CONST_FACES_ZIP_FILE)
        with zipfile.ZipFile(CONST_FACES_ZIP_FILE, "r") as zip_ref_faces:
            zip_ref_faces.extractall("faces in the wild training")
        print("\nExtracting File:",CONST_FACES_ZIP_FILE, "Completed.")


        print("\nPlease Wait. Extracting File:", CONST_NON_FACES_ZIP_FILE)
        with zipfile.ZipFile(CONST_NON_FACES_ZIP_FILE, "r") as zip_ref_non_faces:
            zip_ref_non_faces.extractall("non_faces")

        print("\nExtracting File:", CONST_NON_FACES_ZIP_FILE, "Completed.")

    except:
        #display some failed results for the images processsing and ask user to go back to menu.
        print("Error, something went wrong with extracting the zip files.")
        print("Please Make sure File name: " + CONST_FACES_ZIP_FILE + " is not missing.")
        print("And Please Make sure File name: " + CONST_NON_FACES_ZIP_FILE + " is not missing.")
        input("\nPlease press Enter to go back to the main menu . . . ")
        print("\n\n\n")
        return;


    #going through the directory for Faces folder, and putting all the Face images file path locations into an array
    for dirname, dirnames, filenames in os.walk(CONST_FACES_FOLDER):
        # print path to all filenames.
        for filename in filenames:
            imgFileNames_Faces.append(os.path.join(dirname, filename))

    #going through the directory for non-faces folder, and putting all the face images file path locations into an array
    for dirname, dirnames, filenames in os.walk(CONST_NON_FACES_FOLDER):
        # print path to all filenames.
        for filename in filenames:
            imgFileNames_Non_Faces.append(os.path.join(dirname, filename))
    
    #each image size is 250x250
    #I want to crop it, so only 150x150 of the middle of the image is available:
    #then I want to resize it to (CONST_RESIZE_PIXELS_BOTH_WAYS x CONST_RESIZE_PIXELS_BOTH_WAYS) (i.e., 64x64 in this case)
    #also making it 1 channel (R+G+B)/3 for color to grayscale
    width, height = (250,250)
    new_width, new_height = (150,150)
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    #cropped area:
    area = (left,top,right,bottom)

    n_faces = len(imgFileNames_Faces)
    n_non_faces = len(imgFileNames_Non_Faces)

    #I want to flatten the CONST_MAX_NUM (i.e., 5000 in this case) images into (CONST_RESIZE_PIXELS_BOTH_WAYS x CONST_RESIZE_PIXELS_BOTH_WAYS) (i.e, 64x64 = 4096 in this case)
    img_Faces = numpy.empty((CONST_MAX_NUM, CONST_RESIZE_PIXELS_BOTH_WAYS*CONST_RESIZE_PIXELS_BOTH_WAYS))
    img_Non_Faces = numpy.empty((CONST_MAX_NUM, CONST_RESIZE_PIXELS_BOTH_WAYS*CONST_RESIZE_PIXELS_BOTH_WAYS))

   


    #error checking to see if there are images at least to the number of CONST_MAX_NUM. (5000 in this case)
    if (n_faces< CONST_MAX_NUM):
            print("\n\nPlease Make sure Folder name: " + CONST_FACES_FOLDER + " has at least " + str(CONST_MAX_NUM) + " Images in them.")
            print("Please press Enter and go back to the main menu,")
            input("and from there select 1 to create the NumPy DATA file if that Folder has Images in them now . . . ")
            print("\n\n\n")
            return;

    if (n_non_faces < CONST_MAX_NUM):
            print("\n\nPlease Make sure Folder name: " + CONST_NON_FACES_FOLDER + " has at least " +str(CONST_MAX_NUM) + " Images in them.")
            print("Please press Enter and go back to the main menu,")
            input("and from there select 1 to create the NumPy DATA file if that Folder has Images in them now . . . ")
            print("\n\n\n")
            return;

    #error checking to see if there are images, and each are 250x250
    try:
        #for upto CONST_MAX_NUM number of the faces images. (5000 in this case)
        print("\nPlease Wait. Processing Face Images.")
        for i in range(CONST_MAX_NUM):
            img =Image.open(imgFileNames_Faces[i])  #create image object.
            cropped_img = img.crop(area)  #crop it to 150x150 of the middle of the original image.
            resizedAndCroppedImg = cropped_img.resize((CONST_RESIZE_PIXELS_BOTH_WAYS,CONST_RESIZE_PIXELS_BOTH_WAYS), Image.ANTIALIAS) #resize it to (CONST_RESIZE_PIXELS_BOTH_WAYS x CONST_RESIZE_PIXELS_BOTH_WAYS) (64x64 in this case)
            imgArrRGB = numpy.asarray(resizedAndCroppedImg)  #change it into numpy array
            R,G,B = imgArrRGB[:,:,0], imgArrRGB[:,:,1], imgArrRGB[:,:,2] #get the R.G and B channels
            grayScaleFinalImgArr = (R+G+B)/3  #create gray scale 1 channel image
            img_Faces[i] = grayScaleFinalImgArr.reshape(-1) #flatten it to value of (CONST_RESIZE_PIXELS_BOTH_WAYS * CONST_RESIZE_PIXELS_BOTH_WAYS) (64x64 = 4096 in this case)
            img.close()
            print("=> Face Image "+ str(i+1) + "/"+ str(CONST_MAX_NUM) + " Processed.",end = '\r', flush = True)

        print("\n", CONST_MAX_NUM, "Face Images have been Processed.")

        
        #for all the non-faces images: which follows the same procedure as the above for all the faces image except there is only 1 channel grayscale already.
        print("\nPlease Wait. Processing Non-Face Images.")
        for i in range(CONST_MAX_NUM):
            img =Image.open(imgFileNames_Non_Faces[i])
            cropped_img = img.crop(area)
            resizedAndCroppedImg = cropped_img.resize((CONST_RESIZE_PIXELS_BOTH_WAYS,CONST_RESIZE_PIXELS_BOTH_WAYS), Image.ANTIALIAS)
            imgArrGrayScale = numpy.asarray(resizedAndCroppedImg)
            img_Non_Faces[i] = imgArrGrayScale.reshape(-1)
            img.close()
            print("=> Non-Face Image "+ str(i+1) + "/"+ str(CONST_MAX_NUM) + " Processed.",end = '\r', flush = True)

        print("\n", CONST_MAX_NUM, "Non-Face Images have been Processed.")
 

    
        #deleting the folders that we unzipped, because we have our data now.
        print("\nPlease Wait. Deleting Folder and Its Files:",CONST_FACES_FOLDER)
        shutil.rmtree(CONST_FACES_FOLDER)
        print("\nFolder and Its Files:", CONST_FACES_FOLDER ,"Deleted.")

        print("\nPlease Wait. Deleting Folder and Its Files:",CONST_NON_FACES_FOLDER)
        shutil.rmtree(CONST_NON_FACES_FOLDER)
        print("\nFolder and Its Files:", CONST_NON_FACES_FOLDER ,"Deleted.")


        print("\nFinalizing the Processing . . . ")

        #creating a big matrix (data) that will be randomized, and have all the CONST_MAX_NUM (5000 in this case) faces with it's respected label as the first column and all the CONST_MAX_NUM (5000 in this case) non-faces with it's respected label as the first column.
        #the reasons I randomize: to have random values for the Cross Validation part, I want for the values to be different. I want the validate splitted part have random testing data in them for each runs. (Maybe better Generalization)
        #and the reserved 25% testing data changes as well. (The testing is randomized, and when I checked, they are close to 50% face example and close to 50% non-face example, (1251 Face test examples, and 1249 non-Face test examples)
        #IF there was a big difference, I would have NOT randomized the testing part as well and only take exactly 50% for each class that was not randomized.
        label_face = numpy.empty((CONST_MAX_NUM,1))
        label_face.fill(CONST_LABEL_VALUE_FACE)
        label_non_face = numpy.empty((CONST_MAX_NUM,1))
        label_non_face.fill(CONST_LABEL_VALUE_NON_FACE)

        X = numpy.concatenate((img_Faces,img_Non_Faces))
        label = numpy.concatenate((label_face,label_non_face))
        
        data = numpy.concatenate((label,X), axis= 1)


        random.seed() #explicitly initialize the seed.
        
        #going to randomize the data
        indexes = list(range(len(data)))
        random.shuffle(indexes)

        data_shuffled = data[indexes]


        #save the images array data_shuffled to a numpy file.
        numpy.save(CONST_DATA_NUMPY_FILE,data_shuffled)
        

        #display some results, and ask user to go back to menu.
        print("\n\nImage Files for Faces and Non-Faces Processing Completed.")
        print("Both types of images with their respected labels have been shuffled and saved in a NumPy file.")
        print("Data (shuffled) NumPy file saved as: " + CONST_DATA_NUMPY_FILE + "\n\n")
        input("Please Press Enter to go Back to the Menu . . . ")
        print("\n\n\n")
    except:
        #display some failed results for the images processsing and ask user to go back to menu.
        print("\n\nImage Files for Faces and Non-Faces Processing Failed.")
        print("Please Make sure Folder name: " + CONST_FACES_FOLDER + " has at least " + str(CONST_MAX_NUM) + " Images in them.") #CONST_MAX_NUM = 5000 in this case.
        print("And Please Make sure Folder name: " + CONST_NON_FACES_FOLDER + " has at least " +str(CONST_MAX_NUM) + " Images in them.") #CONST_MAX_NUM = 5000 in this case.
        print("Also, make sure every image size is: 250x250.")
        print("\nPlease press Enter and go back to the main menu,")
        input("and from there select 1 to create the NumPy DATA file if those Folders has Images in them now AND/OR each image size is 250x250 . . . ")
        print("\n\n\n")





#organize data for cross-validation and final testing purposes.
def organizeData(data):
    # I will use 5-fold cross-validation, so S = 5
    #[part1][part2][part3][part4][part5] is 75% of the total data      and        [test] is 25% of the total data.
    #will use part1 to part 5 for the available data part to do 5 runs to train 4 parts and validate one part in each run.
    test_X = data[int(len(data) - len(data)*0.25):,1:]
    test_Label = data[int(len(data) - len(data)*0.25):,0:1]

    n = int(len(data)*0.75) #the available data part (training and validating)

    part1_X = data[:int(n/5),1:]
    part1_Label = data[:int(n/5),0:1]

    part2_X = data[int(n/5):int(2*n/5),1:]
    part2_Label = data[int(n/5):int(2*n/5),0:1]

    part3_X = data[int(2*n/5):int(3*n/5),1:]
    part3_Label = data[int(2*n/5):int(3*n/5),0:1]

    part4_X = data[int(3*n/5):int(4*n/5),1:]
    part4_Label = data[int(3*n/5):int(4*n/5),0:1]

    part5_X = data[int(4*n/5):n,1:]
    part5_Label = data[int(4*n/5):n,0:1]

    return test_X, test_Label, part1_X, part1_Label, part2_X, part2_Label, part3_X, part3_Label, part4_X, part4_Label, part5_X, part5_Label





#svm classifier
def svm():
    print("\n_____________________________________________________________")
    print("\nTraining and Testing with Support Vector Machine:\n")

    data = numpy.array([])

    try:
        data = numpy.load(CONST_DATA_NUMPY_FILE)
    except FileNotFoundError:
        print("Error, file", CONST_DATA_NUMPY_FILE, "not found. Please press Enter and go back to the main menu,")
        input("and from there select 1 to create the NumPy DATA file . . . ")
        print("\n\n\n")
        return;
    except:
        print("Error, Something Went Wrong.")
        input("Please Press Enter to go Back to the Menu . . . ")
        print("\n\n\n")
        return;


    

    #partitioning it into 5-folds and test data. 5-folds will be used (4-folds training, 1-fold validate) for 5 different runs for each parameter.
    test_X, test_Label, part1_X, part1_Label, part2_X, part2_Label, part3_X, part3_Label, part4_X, part4_Label, part5_X, part5_Label = organizeData(data)


    #for svm, I will use Polynomial of power p for my kernel function (p is the degree), I will choose 5 parameters.
    #for 5 parameters, I will use power p (degree) = {1,2,3,4,5} which I chose randomly.
    #I will run each parameter 5 times, and average them based on the errors they receive. then I will choose the lowest average error parameter, 
    

    #training starts here:

    start_time = time.time() #timing the training

    print("\nTraining Starts:")

    #cross validation part started:
    print("\nCross Validation:")
    print("S-fold = 5 (5 runs)")
    print("Kernel Function = Polynomial of power p, Parameter polynomial of power p = { 1 , 2 , 3 , 4 , 5 }\n")
    p = (1,2,3,4,5)  #Parameter polynomial of power p tuple with 5 values. #this is a sample that I used, and will choose one based on the cross validation results that give the lowest average error for a parameter.
    errors_average_param = [] #for each parameter that does 5 runs.


    for i in range(5): #5 params (each running 5 times) 
        mysvm = SVC(kernel='poly', degree = p[i])

        print("=> Parameter polynomial of power p = "+ str(p[i]) + " and run #1 . . .",end = '\r', flush = True)
        #[validate][train][train][train][train]
        run1_X = numpy.concatenate((part2_X,part3_X,part4_X,part5_X))
        run1_Label = numpy.concatenate((part2_Label,part3_Label, part4_Label,part5_Label))
        mysvm.fit(run1_X,run1_Label.reshape(-1))
        predict_run1 = mysvm.predict(part1_X)
        numErrors_run1 = numpy.sum(predict_run1 != numpy.ravel(part1_Label))

        print("=> Parameter polynomial of power p = "+ str(p[i]) + " and run #2 . . .",end = '\r', flush = True)
        #[train][validate][train][train][train]
        run2_X = numpy.concatenate((part1_X,part3_X,part4_X,part5_X))
        run2_Label = numpy.concatenate((part1_Label,part3_Label, part4_Label,part5_Label))
        mysvm.fit(run2_X,run2_Label.reshape(-1))
        predict_run2 = mysvm.predict(part2_X)
        numErrors_run2 = numpy.sum(predict_run2 != numpy.ravel(part2_Label))

        print("=> Parameter polynomial of power p = "+ str(p[i]) + " and run #3 . . . ",end = '\r', flush = True)
        #[train][train][validate][train][train]
        run3_X = numpy.concatenate((part1_X,part2_X,part4_X,part5_X))
        run3_Label = numpy.concatenate((part1_Label,part2_Label, part4_Label,part5_Label))
        mysvm.fit(run3_X,run3_Label.reshape(-1))
        predict_run3 = mysvm.predict(part3_X)
        numErrors_run3 = numpy.sum(predict_run3 != numpy.ravel(part3_Label))

        print("=> Parameter polynomial of power p = "+ str(p[i]) + " and run #4 . . . ",end = '\r', flush = True)
        #[train][train][train][validate][train]
        run4_X = numpy.concatenate((part1_X,part2_X,part3_X,part5_X))
        run4_Label = numpy.concatenate((part1_Label,part2_Label, part3_Label,part5_Label))
        mysvm.fit(run4_X,run4_Label.reshape(-1))
        predict_run4 = mysvm.predict(part4_X)
        numErrors_run4 = numpy.sum(predict_run4 != numpy.ravel(part4_Label))

        print("=> Parameter polynomial of power p = "+ str(p[i]) + " and run #5 . . . ",end = '\r', flush = True)
        #[train][train][train][train][validate]
        run5_X = numpy.concatenate((part1_X,part2_X,part3_X,part4_X))
        run5_Label = numpy.concatenate((part1_Label,part2_Label, part3_Label,part4_Label))
        mysvm.fit(run5_X,run5_Label.reshape(-1))
        predict_run5 = mysvm.predict(part5_X)
        numErrors_run5 = numpy.sum(predict_run5 != numpy.ravel(part5_Label))

        #averaged the number of errors for this parameter.
        avg = (numErrors_run1+numErrors_run2+numErrors_run3+numErrors_run4+numErrors_run5)/5
        errors_average_param.append(avg)
        print("\nFor p = " + str(p[i]) + ": (Run Errors => (#1 = " + str(numErrors_run1)+ ", #2 = " + str(numErrors_run2) +", #3 = " + str(numErrors_run3) + ", #4 = " + str(numErrors_run4) + ", #5 = " + str(numErrors_run5) + ") , Avg Error => " + str(avg) + " )\n" )


    #choosing the parameter value with the lowest errors.
    chosen_param =  p[numpy.argmin(errors_average_param)]  #extra (debugging purpose, when I changed the value here, the results changed later, therefore, the function .predict() and .decision_function() use this kernal parameter.)
    print("\nParameter polynomial of power p is chosen, which is:", chosen_param)
    print("It is for the lowest Avg Error.")
    print("Cross Validation Completed.")

   
    #I will now train the 75% of the data with this chosen_param.

    train_X = numpy.concatenate((part1_X,part2_X,part3_X,part4_X,part5_X))
    train_Label =  numpy.concatenate((part1_Label,part2_Label, part3_Label,part4_Label,part5_Label))

    print("\nTotal Number of Training Examples:", len(train_X))
    print("Total Training Face Examples:", numpy.count_nonzero(train_Label == CONST_LABEL_VALUE_FACE))   #make sure it is nonzero
    print("Total Training Non-Face Examples:", numpy.count_nonzero(train_Label == CONST_LABEL_VALUE_NON_FACE))  #make sure it is nonzero
    print("\nTraining on all the training set examples with the chosen parameter . . . ")



    obj_svm = SVC(kernel='poly', degree = chosen_param)  #for this obj_svm, you can see that I am using the degree (polynomial of power p) = chosen_param.
    obj_svm.fit(train_X,train_Label.reshape(-1))
    print("\nTraining Completed.")


    training_time = time.time() - start_time   
    #training ends here.
    



    #testing starts here:
    start_time = time.time() #timing the testing
    print("\n\nTesting Data Starts:")

    #Confusion Matrix part:
    predict_testData = obj_svm.predict(test_X)  #this one is used for Confusion Matrix based on the chosen parameter.
    
    TP = 0  #true positive
    TN = 0  #true negative
    FP = 0  #false positive
    FN = 0  #false negative

    n = len(predict_testData)

    for i in range(n):
        if predict_testData[i] == test_Label[i]: #TP or TN

            if (predict_testData[i] == CONST_LABEL_VALUE_FACE):
                TP += 1
            else:
                TN += 1

        else: #FP or FN
            if (predict_testData[i] == CONST_LABEL_VALUE_FACE):
                FP += 1
            else:
                FN += 1


   
    confusionMatrix = [[FP,TP],[TN,FN]] #the confusionMatrix in form of 2d array


            
    #ROC part (including the AUC)
    predict_testData_scores = obj_svm.decision_function(test_X)   #this one is used for the ROC curve, and Area Under the Curve based on the chosen parameter.

    svm_f_p_r, svm_t_p_r, threshold = roc_curve(test_Label, predict_testData_scores)

    auc_svm = auc(svm_f_p_r, svm_t_p_r)

    

    plt.figure(figsize=(5,5),dpi =100)
    txtLabel = "SVM (AUC = " + str(auc_svm) + ")"
    plt.plot(svm_f_p_r, svm_t_p_r, linestyle = '-', label = txtLabel)
    plt.xlabel('False Positive Rate')
    plt.ylabel("True Positive Rate")
    plt.title("SVM - ROC Curve")

    print("\nPlease View the ROC (Receiver Operating Characteristic) Curve on The Graph based on the Chosen Parameter - (SVM) . . . ")
    

    #stop time here.
    testing_time = time.time() - start_time 


    plt.legend()
    plt.show()
    
    print("\nTesting Data Completed.")
    #testing ends here:
   


    #display some results.
    print("\n\nDisplay Results (SVM):")
    print("\nParameter polynomial of power p that was chosen:", chosen_param)
    print("\nTotal time elapsed for training:", round(training_time,3), 'seconds.')
    print("\nTotal time elapsed for testing:", round(testing_time,3), 'seconds.')

    print("\nTotal Number of Test Examples:",len(test_X))
    print("Total Ground Truth Positive Examples (Face):", TP+FN)
    print("Total Ground Truth Negative Examples (Non-Face):", FP+TN)

    print("\nConfusion Matrix Results Based on the Chosen Parameter:")
    print("\nFalse Positive = " + str(confusionMatrix[0][0]))
    print("True Negative = " + str(confusionMatrix[1][0]))
    print("\nTrue Positive = " + str(confusionMatrix[0][1]))
    print("False Negative = " + str(confusionMatrix[1][1]))
    print("\nArea Under the Curve for ROC =", auc_svm)
    print("\n\nTraining and Testing with Support Vector Machine is Completed.")
    input("\n\nPlease Press Enter to go Back to the Menu . . . ")
    print("\n\n\n")





#adaBoost classifier
def adaBoost():
    print("\n_____________________________________________________________")
    print("\nTraining and Testing with AdaBoost:\n")

    data = numpy.array([])

    try:
        data = numpy.load(CONST_DATA_NUMPY_FILE)
    except FileNotFoundError:
        print("Error, file", CONST_DATA_NUMPY_FILE, "not found. Please press Enter and go back to the main menu,")
        input("and from there select 1 to create the NumPy DATA file . . . ")
        print("\n\n\n")
        return;
    except:
        print("Error, Something Went Wrong.")
        input("Please Press Enter to go Back to the Menu . . . ")
        print("\n\n\n")
        return;


    

    #partitioning it into 5-folds and test data. 5-folds will be used (4-folds training, 1-fold validate) for 5 different runs for each parameter.
    test_X, test_Label, part1_X, part1_Label, part2_X, part2_Label, part3_X, part3_Label, part4_X, part4_Label, part5_X, part5_Label = organizeData(data)


    #for AdaBoost, I will use the n_estimators, which is the number of weak learners for the parameter. I will choose 5 parameters.
    #for 5 parameters, I will use number of weak learners = {2,4,6,8,10} which I chose randomly.
    #I will run each parameter 5 times, and average them based on the errors they receive. then I will choose the lowest average error parameter, 
    

    #training starts here:

    start_time = time.time() #timing the training

    print("\nTraining Starts:")

    #cross validation part started:
    print("\nCross Validation:")
    print("S-fold = 5 (5 runs)")
    print("Parameter number of weak learners = { 2 , 4 , 6 , 8 , 10 }\n")
    num_weakLearners = (2,4,6,8,10)  #Parameter number of weak learners tuple with 5 values. #this is a sample that I used, and will choose one based on the cross validation results that give the lowest average error for a parameter.
    errors_average_param = [] #for each parameter that does 5 runs.


    for i in range(5): #5 params (each running 5 times) 
        myAdaBoost = AdaBoostClassifier(n_estimators = num_weakLearners[i])
        print("=> Parameter number of weak learners = "+ str( num_weakLearners[i]) + " and run #1 . . .",end = '\r', flush = True)
        #[validate][train][train][train][train]
        run1_X = numpy.concatenate((part2_X,part3_X,part4_X,part5_X))
        run1_Label = numpy.concatenate((part2_Label,part3_Label, part4_Label,part5_Label))
        myAdaBoost.fit(run1_X,run1_Label.reshape(-1))
        predict_run1 = myAdaBoost.predict(part1_X)
        numErrors_run1 = numpy.sum(predict_run1 != numpy.ravel(part1_Label))

        print("=> Parameter number of weak learners = "+ str( num_weakLearners[i]) + " and run #2 . . .",end = '\r', flush = True)
        #[train][validate][train][train][train]
        run2_X = numpy.concatenate((part1_X,part3_X,part4_X,part5_X))
        run2_Label = numpy.concatenate((part1_Label,part3_Label, part4_Label,part5_Label))
        myAdaBoost.fit(run2_X,run2_Label.reshape(-1))
        predict_run2 = myAdaBoost.predict(part2_X)
        numErrors_run2 = numpy.sum(predict_run2 != numpy.ravel(part2_Label))

        print("=> Parameter number of weak learners = "+ str( num_weakLearners[i]) + " and run #3 . . .",end = '\r', flush = True)
        #[train][train][validate][train][train]
        run3_X = numpy.concatenate((part1_X,part2_X,part4_X,part5_X))
        run3_Label = numpy.concatenate((part1_Label,part2_Label, part4_Label,part5_Label))
        myAdaBoost.fit(run3_X,run3_Label.reshape(-1))
        predict_run3 = myAdaBoost.predict(part3_X)
        numErrors_run3 = numpy.sum(predict_run3 != numpy.ravel(part3_Label))

        print("=> Parameter number of weak learners = "+ str( num_weakLearners[i]) + " and run #4 . . .",end = '\r', flush = True)
        #[train][train][train][validate][train]
        run4_X = numpy.concatenate((part1_X,part2_X,part3_X,part5_X))
        run4_Label = numpy.concatenate((part1_Label,part2_Label, part3_Label,part5_Label))
        myAdaBoost.fit(run4_X,run4_Label.reshape(-1))
        predict_run4 = myAdaBoost.predict(part4_X)
        numErrors_run4 = numpy.sum(predict_run4 != numpy.ravel(part4_Label))

        print("=> Parameter number of weak learners = "+ str( num_weakLearners[i]) + " and run #5 . . .",end = '\r', flush = True)
        #[train][train][train][train][validate]
        run5_X = numpy.concatenate((part1_X,part2_X,part3_X,part4_X))
        run5_Label = numpy.concatenate((part1_Label,part2_Label, part3_Label,part4_Label))
        myAdaBoost.fit(run5_X,run5_Label.reshape(-1))
        predict_run5 = myAdaBoost.predict(part5_X)
        numErrors_run5 = numpy.sum(predict_run5 != numpy.ravel(part5_Label))

        #averaged the number of errors for this parameter.
        avg = (numErrors_run1+numErrors_run2+numErrors_run3+numErrors_run4+numErrors_run5)/5
        errors_average_param.append(avg)
        print("\nFor # of weak learners = " + str(num_weakLearners[i]) + ": (Run Errors => (#1 = " + str(numErrors_run1)+ ", #2 = " + str(numErrors_run2) +", #3 = " + str(numErrors_run3) + ", #4 = " + str(numErrors_run4) + ", #5 = " + str(numErrors_run5) + ") , Avg Error => " + str(avg) + " )\n" )

    
    #choosing the parameter value with the lowest errors.
    chosen_param =  num_weakLearners[numpy.argmin(errors_average_param)]   #extra (debugging purpose, when I changed the value here, the results changed later, therefore, the function .predict() and .decision_function() use this number of weak learners parameter.)
    print("\nParameter number of weak learners is chosen, which is:", chosen_param)
    print("It is for the lowest Avg Error.")
    print("Cross Validation Completed.")

   
    #I will now train the 75% of the data with this chosen_param.

    train_X = numpy.concatenate((part1_X,part2_X,part3_X,part4_X,part5_X))
    train_Label =  numpy.concatenate((part1_Label,part2_Label, part3_Label,part4_Label,part5_Label))

    print("\nTotal Number of Training Examples:", len(train_X))
    print("Total Training Face Examples:", numpy.count_nonzero(train_Label == CONST_LABEL_VALUE_FACE)) #make sure it is nonzero
    print("Total Training Non-Face Examples:", numpy.count_nonzero(train_Label == CONST_LABEL_VALUE_NON_FACE)) #make sure it is nonzero
    print("\nTraining on all the training set examples with the chosen parameter . . . ")


    
    obj_adaBoost = AdaBoostClassifier(n_estimators = chosen_param)  #for this obj_adaBoost, you can see that I am using the n_estimators (number of weak learners) = chosen_param.
    obj_adaBoost.fit(train_X,train_Label.reshape(-1))
    print("\nTraining Completed.")


    training_time = time.time() - start_time   
    #training ends here.
    



    #testing starts here:
    start_time = time.time() #timing the testing
    print("\n\nTesting Data Starts:")

    #Confusion Matrix part:
    predict_testData = obj_adaBoost.predict(test_X)  #this one is used for Confusion Matrix based on the chosen parameter.
    
    TP = 0  #true positive
    TN = 0  #true negative
    FP = 0  #false positive
    FN = 0  #false negative

    n = len(predict_testData)

    for i in range(n):
        if predict_testData[i] == test_Label[i]: #TP or TN

            if (predict_testData[i] == CONST_LABEL_VALUE_FACE):
                TP += 1
            else:
                TN += 1

        else: #FP or FN
            if (predict_testData[i] == CONST_LABEL_VALUE_FACE):
                FP += 1
            else:
                FN += 1


   
    confusionMatrix = [[FP,TP],[TN,FN]] #the confusionMatrix in form of 2d array


            
    #ROC part (including the AUC)
    predict_testData_scores = obj_adaBoost.decision_function(test_X)   #this one is used for the ROC curve, and Area Under the Curve based on the chosen parameter.

    adaboost_f_p_r, adaboost_t_p_r, threshold = roc_curve(test_Label, predict_testData_scores)

    auc_adaboost = auc(adaboost_f_p_r, adaboost_t_p_r)

    

    plt.figure(figsize=(5,5),dpi =100)
    txtLabel = "AdaBoost (AUC = " + str(auc_adaboost) + ")"
    plt.plot(adaboost_f_p_r, adaboost_t_p_r, linestyle = '-', label = txtLabel)
    plt.xlabel('False Positive Rate')
    plt.ylabel("True Positive Rate")
    plt.title("AdaBoost - ROC Curve")

    print("\nPlease View the ROC (Receiver Operating Characteristic) Curve on The Graph based on the Chosen Parameter - (AdaBoost) . . . ")
    

    #stop time here.
    testing_time = time.time() - start_time 


    plt.legend()
    plt.show()
    
    print("\nTesting Data Completed.")
    #testing ends here:
   


    #display some results.
    print("\n\nDisplay Results (AdaBoost):")
    print("\nParameter number of weak learners that was chosen:", chosen_param)
    print("\nTotal time elapsed for training:", round(training_time,3), 'seconds.')
    print("\nTotal time elapsed for testing:", round(testing_time,3), 'seconds.')

    print("\nTotal Number of Test Examples:",len(test_X))
    print("Total Ground Truth Positive Examples (Face):", TP+FN)
    print("Total Ground Truth Negative Examples (Non-Face):", FP+TN)

    print("\nConfusion Matrix Results Based on the Chosen Parameter:")
    print("\nFalse Positive = " + str(confusionMatrix[0][0]))
    print("True Negative = " + str(confusionMatrix[1][0]))
    print("\nTrue Positive = " + str(confusionMatrix[0][1]))
    print("False Negative = " + str(confusionMatrix[1][1]))
    print("\nArea Under the Curve for ROC =", auc_adaboost)
    print("\n\nTraining and Testing with AdaBoost is Completed.")
    input("\n\nPlease Press Enter to go Back to the Menu . . . ")
    print("\n\n\n")







#logistic Regression
def logisticRegression():
    print("\n_____________________________________________________________")
    print("\nTraining and Testing with Logistic Regression:\n")

    data = numpy.array([])

    try:
        data = numpy.load(CONST_DATA_NUMPY_FILE)
    except FileNotFoundError:
        print("Error, file", CONST_DATA_NUMPY_FILE, "not found. Please press Enter and go back to the main menu,")
        input("and from there select 1 to create the NumPy DATA file . . . ")
        print("\n\n\n")
        return;
    except:
        print("Error, Something Went Wrong.")
        input("Please Press Enter to go Back to the Menu . . . ")
        print("\n\n\n")
        return;


    

    #partitioning it into 5-folds and test data. 5-folds will be used (4-folds training, 1-fold validate) for 5 different runs for each parameter.
    test_X, test_Label, part1_X, part1_Label, part2_X, part2_Label, part3_X, part3_Label, part4_X, part4_Label, part5_X, part5_Label = organizeData(data)


    #for Logistic Regression, I will use the tolerance for stopping criteria (tol) as my parameter for the solver = saga. I will choose 5 parameters.
    #I will also use the maximum number of iterations taken for the solvers to converge (max_iter) of 100000 which I chose randomly.
    #for 5 parameters, I will use number of tol_value = {0.001,0.01,0.1,1,10} which I chose randomly.
    #I will run each parameter 5 times, and average them based on the errors they receive. then I will choose the lowest average error parameter, 
    

    #training starts here:

    start_time = time.time() #timing the training

    print("\nTraining Starts:")

    #cross validation part started:
    print("\nCross Validation:")
    print("S-fold = 5 (5 runs)")
    print("Parameter tolerance for stopping criteria - tol = { 0.001 , 0.01 , 0.1 , 1 , 10 }\n")
    tol_value = (0.001,0.01,0.1,1,10)  #Parameter tolerance for stopping criteria tol tuple with 5 values. #this is a sample that I used, and will choose one based on the cross validation results that give the lowest average error for a parameter.
    errors_average_param = [] #for each parameter that does 5 runs.

    
    for i in range(5): #5 params (each running 5 times) 
        mylr = LogisticRegression(tol=tol_value[i], solver='saga', max_iter = 100000)
        print("=> Parameter tolerance for stopping criteria - tol = "+ str(tol_value[i]) + " and run #1 . . .",end = '\r', flush = True)
        #[validate][train][train][train][train]
        run1_X = numpy.concatenate((part2_X,part3_X,part4_X,part5_X))
        run1_Label = numpy.concatenate((part2_Label,part3_Label, part4_Label,part5_Label))
        mylr.fit(run1_X,run1_Label.reshape(-1))
        predict_run1 = mylr.predict(part1_X)
        numErrors_run1 = numpy.sum(predict_run1 != numpy.ravel(part1_Label))

        print("=> Parameter tolerance for stopping criteria - tol = "+ str(tol_value[i]) + " and run #2 . . .",end = '\r', flush = True)
        #[train][validate][train][train][train]
        run2_X = numpy.concatenate((part1_X,part3_X,part4_X,part5_X))
        run2_Label = numpy.concatenate((part1_Label,part3_Label, part4_Label,part5_Label))
        mylr.fit(run2_X,run2_Label.reshape(-1))
        predict_run2 = mylr.predict(part2_X)
        numErrors_run2 = numpy.sum(predict_run2 != numpy.ravel(part2_Label))

        print("=> Parameter tolerance for stopping criteria - tol = "+ str(tol_value[i]) + " and run #3 . . .",end = '\r', flush = True)
        #[train][train][validate][train][train]
        run3_X = numpy.concatenate((part1_X,part2_X,part4_X,part5_X))
        run3_Label = numpy.concatenate((part1_Label,part2_Label, part4_Label,part5_Label))
        mylr.fit(run3_X,run3_Label.reshape(-1))
        predict_run3 = mylr.predict(part3_X)
        numErrors_run3 = numpy.sum(predict_run3 != numpy.ravel(part3_Label))

        print("=> Parameter tolerance for stopping criteria - tol = "+ str(tol_value[i]) + " and run #4 . . .",end = '\r', flush = True)
        #[train][train][train][validate][train]
        run4_X = numpy.concatenate((part1_X,part2_X,part3_X,part5_X))
        run4_Label = numpy.concatenate((part1_Label,part2_Label, part3_Label,part5_Label))
        mylr.fit(run4_X,run4_Label.reshape(-1))
        predict_run4 = mylr.predict(part4_X)
        numErrors_run4 = numpy.sum(predict_run4 != numpy.ravel(part4_Label))

        print("=> Parameter tolerance for stopping criteria - tol = "+ str(tol_value[i]) + " and run #5 . . .",end = '\r', flush = True)
        #[train][train][train][train][validate]
        run5_X = numpy.concatenate((part1_X,part2_X,part3_X,part4_X))
        run5_Label = numpy.concatenate((part1_Label,part2_Label, part3_Label,part4_Label))
        mylr.fit(run5_X,run5_Label.reshape(-1))
        predict_run5 = mylr.predict(part5_X)
        numErrors_run5 = numpy.sum(predict_run5 != numpy.ravel(part5_Label))

        #averaged the number of errors for this parameter.
        avg = (numErrors_run1+numErrors_run2+numErrors_run3+numErrors_run4+numErrors_run5)/5
        errors_average_param.append(avg)
        print("\nFor tol = " + str(tol_value[i]) + ": (Run Errors => (#1 = " + str(numErrors_run1)+ ", #2 = " + str(numErrors_run2) +", #3 = " + str(numErrors_run3) + ", #4 = " + str(numErrors_run4) + ", #5 = " + str(numErrors_run5) + ") , Avg Error => " + str(avg) + " )\n" )

    
    #choosing the parameter value with the lowest errors.
    chosen_param =  tol_value[numpy.argmin(errors_average_param)]   #extra (debugging purpose, when I changed the value here, the results changed later, therefore, the function .predict() and .decision_function() use this number for tolerance for stopping criteria (tol) parameter.)
    print("\nParameter tolerance for stopping criteria (tol) is chosen, which is:", chosen_param)
    print("It is for the lowest Avg Error.")
    print("Cross Validation Completed.")

   
    #I will now train the 75% of the data with this chosen_param.

    train_X = numpy.concatenate((part1_X,part2_X,part3_X,part4_X,part5_X))
    train_Label =  numpy.concatenate((part1_Label,part2_Label, part3_Label,part4_Label,part5_Label))

    print("\nTotal Number of Training Examples:", len(train_X))
    print("Total Training Face Examples:", numpy.count_nonzero(train_Label == CONST_LABEL_VALUE_FACE)) #make sure it is nonzero
    print("Total Training Non-Face Examples:", numpy.count_nonzero(train_Label == CONST_LABEL_VALUE_NON_FACE)) #make sure it is nonzero
    print("\nTraining on all the training set examples with the chosen parameter . . . ")


  
    obj_lr = LogisticRegression(tol=chosen_param, solver='saga', max_iter = 100000)  #for this obj_lr, you can see that I am using the tol (tolerance for stopping criteria value) = chosen_param.
    obj_lr.fit(train_X,train_Label.reshape(-1))
    print("\nTraining Completed.")


    training_time = time.time() - start_time   
    #training ends here.
    



    #testing starts here:
    start_time = time.time() #timing the testing
    print("\n\nTesting Data Starts:")

    #Confusion Matrix part:
    predict_testData = obj_lr.predict(test_X)  #this one is used for Confusion Matrix based on the chosen parameter.
    
    TP = 0  #true positive
    TN = 0  #true negative
    FP = 0  #false positive
    FN = 0  #false negative

    n = len(predict_testData)

    for i in range(n):
        if predict_testData[i] == test_Label[i]: #TP or TN

            if (predict_testData[i] == CONST_LABEL_VALUE_FACE):
                TP += 1
            else:
                TN += 1

        else: #FP or FN
            if (predict_testData[i] == CONST_LABEL_VALUE_FACE):
                FP += 1
            else:
                FN += 1


   
    confusionMatrix = [[FP,TP],[TN,FN]] #the confusionMatrix in form of 2d array


            
    #ROC part (including the AUC)
    predict_testData_scores = obj_lr.decision_function(test_X)   #this one is used for the ROC curve, and Area Under the Curve based on the chosen parameter.

    lr_f_p_r, lr_t_p_r, threshold = roc_curve(test_Label, predict_testData_scores)

    auc_lr = auc(lr_f_p_r, lr_t_p_r)

    

    plt.figure(figsize=(5,5),dpi =100)
    txtLabel = "Logistic Regression (AUC = " + str(auc_lr) + ")"
    plt.plot(lr_f_p_r, lr_t_p_r, linestyle = '-', label = txtLabel)
    plt.xlabel('False Positive Rate')
    plt.ylabel("True Positive Rate")
    plt.title("Logistic Regression - ROC Curve")

    print("\nPlease View the ROC (Receiver Operating Characteristic) Curve on The Graph based on the Chosen Parameter - (Logistic Regression) . . . ")
    

    #stop time here.
    testing_time = time.time() - start_time 


    plt.legend()
    plt.show()
    
    print("\nTesting Data Completed.")
    #testing ends here:
   


    #display some results.
    print("\n\nDisplay Results (Logistic Regression):")
    print("\nParameter tolerance for stopping criteria (tol) value that was chosen:", chosen_param)
    print("\nTotal time elapsed for training:", round(training_time,3), 'seconds.')
    print("\nTotal time elapsed for testing:", round(testing_time,3), 'seconds.')

    print("\nTotal Number of Test Examples:",len(test_X))
    print("Total Ground Truth Positive Examples (Face):", TP+FN)
    print("Total Ground Truth Negative Examples (Non-Face):", FP+TN)

    print("\nConfusion Matrix Results Based on the Chosen Parameter:")
    print("\nFalse Positive = " + str(confusionMatrix[0][0]))
    print("True Negative = " + str(confusionMatrix[1][0]))
    print("\nTrue Positive = " + str(confusionMatrix[0][1]))
    print("False Negative = " + str(confusionMatrix[1][1]))
    print("\nArea Under the Curve for ROC =", auc_lr)
    print("\n\nTraining and Testing with Logistic Regression is Completed.")
    input("\n\nPlease Press Enter to go Back to the Menu . . . ")
    print("\n\n\n")





#this function, will display a previous saved results for the comparison of the 3 classifiers (svm, adaboost and logistic regression)
def displaySavedResults():
    print("\n_____________________________________________________________")
    print("\nDisplay Previous Saved Results for the Comparison of the 3 Classifiers\n")

    try:      
        source_imgDraw = Image.open(CONST_PREVIOUS_SAVED_RESULT_IMAGE).convert("RGBA")
        source_imgDraw.show()
        source_imgDraw.close()
        print("\nPlease View the Image for the comparison of the 3 classifiers that was done previously . . . ")
        input("\n\nPlease Press Enter to go Back to the Menu . . . ")
        print("\n\n\n")

    except:
        print('Error, please make sure the file: ' + CONST_PREVIOUS_SAVED_RESULT_IMAGE + " is not missing or is not corrupted.")
        input("\n\nPlease Press Enter to go Back to the Menu . . . ")
        print("\n\n\n")
        







#this is a simple menu that will call the functions at the top based on the user input:
def menu():
    menuSelect= "-1"  #initial value
    #display the menu string:
    textStr = "_____________________________________________________________"
    textStr +=  "\n4DM3 Final Project\n\n"
    textStr += "1 = Image Processing and Putting the Data into the NumPy DATA File\n"
    textStr += "2 = Training and Testing with Support Vector Machine\n"
    textStr += "3 = Training and Testing with AdaBoost\n"
    textStr += "4 = Training and Testing with Logistic Regression\n"
    textStr += "5 = Display Previous Saved Results for the Comparison of the 3 Classifiers\n"
    textStr += "0 = Exit the Program\n\n"
  

    while menuSelect != "0":   #run until user inputs "0" when in menu.  
        print(textStr) #display the menu
        menuSelect =input("Please type your choice and press Enter: ") #ask the user to enter their choice and either (it will call a function or rerunning the menu, or exiting the program)
        if menuSelect == "1":
            imageProcessing()
        elif menuSelect == "2":
            svm()
        elif menuSelect == "3":
            adaBoost()
        elif menuSelect == "4":
            logisticRegression()
        elif menuSelect == "5":
            displaySavedResults()

       






#the main() function (method) that will run the menu() function.
def main():
    menu()




main() #calling the main() function.



#End of File: _4DM3_Project.py