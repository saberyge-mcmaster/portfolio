"""
Author/Student Name (Student ID): Ehsan Sabery Ghomy (400345079)
Professor Name: Dr. Jeff Fortuna
Course: SFWR TECH 4NN3 (Neural Networks and Deep Learning)
Due Date: December 24, 2022

IDE: Microsoft Visual Studio Community 2019 - Version 16.11.20
Python Environment: Python 3.8 (64-bit) (anaconda3 - Anaconda3-2020.11-Windows-x86_64)
File Name: _4NN3_Project.py

Description: Course Project Neural Network (MLP) for Face Detection


For Summary, Please refer to the file: Summary_4NN3_Project.docx
Note: This python code is not optimized at all due to time constraints.
"""

import os 
import numpy 
import random
import copy
import math
import time
import shutil   #for copy and paste of a file.
from PIL import Image, ImageFont, ImageDraw, ImageEnhance  #for image processing/editing/etc...

CONST_FACES_FOLDER = '../faces in the wild training' #folder path for faces
CONST_NON_FACES_FOLDER = '../non_faces'              #folder path for non faces
CONST_FACES_NUMPY_FILE = '../Faces.npy'              #file path to processed faces numpy file
CONST_NON_FACES_NUMPY_FILE = '../Non_Faces.npy'      #file path to processed non_faces numpy file
CONST_SMALLEST_WEIGHTS_FILE = '../Smallest_Weights.txt'  #file path for smallest weights file (errors,end of epoch index, training time, 31 (30 + 1 threshold) output weights, 1025(1024 + 1 threshold)x30 hidden layer weights)
CONST_WEIGHTS_FILE = '../Weights.txt'                   #file path for current weights file before end of max epoch index [49], it will be saved into weights final at the end and be deleted. (errors,end of epoch index, training time, 31 (30 + 1 threshold) output weights, 1025(1024 + 1 threshold)x30 hidden layer weights)
CONST_WEIGHTS_FINAL_FILE = '../Weights_Final.txt'       #file path for final weights file when epoch index is end of [49], (errors,end of epoch index, training time, 31 (30 + 1 threshold) output weights, 1025(1024 + 1 threshold)x30 hidden layer weights)
CONST_TESTING_IMAGE_FILE = '../testing/test images/1442313353nasa-small.jpg'   #just using 1 image, the NASA picture image for Testing.
CONST_IMAGE_RESULT_FILE = '../TestingImage_Result.png'   #image for the result of the testing with bounding border around the detected faces.
CONST_DISPLAY_RESULTS_FILE = '../Results.txt'     #file that has (FP,TP,TN,FN) for confusion matrix, and testing time

CONST_EPOCH_MAX = 50  #I set the max epoch to 50, and wanted to train all the images.
CONST_ALPHA = 0.001  #Set this alpha or learning rate to 0.001

#this function will draw a box around the locations in the image.
#the color is green, and it writes a text value "FACE"
#drawing is referred to the drawing object on the testing image.
#this function is used in testingData() function
def drawBorder(drawing,x1_in,y1_in,color_hexVal="#00FF00",textVal="FACE"): 
    
    draw = drawing
    
    x1= x1_in  #starting point x direction
    x2 = x1+32 #I want to add 32 which is the same as the image patch size and the input images new size after processing.
    y1=y1_in  #starting point y direction
    y2=y1+32 #I want to add 32 which is the same as the image patch size and the input images new size after processing.
    coords = [(x1,y1),(x2,y2)]
    
    top_left = coords[0]
    bottom_right = coords[1]
    top_right = (coords[1][0],coords[0][1])
    bottom_left = (coords[0][0],coords[1][1])

    #drawing the box shape by 4 lines.
    draw.line([top_left,top_right],fill=color_hexVal)
    draw.line([top_right,bottom_right],fill=color_hexVal)
    draw.line([bottom_right,bottom_left],fill=color_hexVal)
    draw.line([bottom_left,top_left],fill=color_hexVal)

    #drawing the text, with x1+3 so it does not hit the border.
    draw.text((x1+3, y1), textVal,font=ImageFont.truetype("arial"),fill=color_hexVal)

    #return it , so in the for loop, i can draw more 4 lines (box) shapes if needed.
    return draw

 
    

#this is the first part of the project.
#image needs to be processed in order to train them.
def imageTrainingProcessing():
    print("\n_____________________________________________________________")
    print("\nImage Processing for Training Data:\n")
    imgFileNames_Faces = []
    imgFileNames_Non_Faces = []
    
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
    #then I want to resize it to 32x32
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

    #I want to flatten the images into 1024 which is 32x32
    img_Faces = numpy.empty((n_faces,1024))
    img_Non_Faces = numpy.empty((n_non_faces,1024))

    #error checking to see if there are images.
    if (n_faces==0):
            print("\n\nPlease Make sure Folder name: " + CONST_FACES_FOLDER + " has Images in them.")
            print("Please press Enter and go back to the main menu,")
            input("and from there select 1 to create the file if that Folder has Images in them now . . . ")
            print("\n")
            return;
    if (n_non_faces == 0):
            print("\n\nPlease Make sure Folder name: " + CONST_NON_FACES_FOLDER + " has Images in them.")
            print("Please press Enter and go back to the main menu,")
            input("and from there select 1 to create the file if that Folder has Images in them now . . . ")
            print("\n")
            return;

    #error checking to see if there are images, and each are 250x250
    try:
        #for all the faces images.
        for i in range(n_faces):
            img =Image.open(imgFileNames_Faces[i])  #create image object.
            cropped_img = img.crop(area)  #crop it to 150x150 of the middle of the original image.
            resizedAndCroppedImg = cropped_img.resize((32,32), Image.ANTIALIAS) #resize it to 32x32
            imgArrRGB = numpy.asarray(resizedAndCroppedImg)  #change it into numpy array
            R,G,B = imgArrRGB[:,:,0], imgArrRGB[:,:,1], imgArrRGB[:,:,2] #get the R.G and B channels
            grayScaleFinalImgArr = (R+G+B)/3  #create gray scale 1 channel image
            img_Faces[i] = grayScaleFinalImgArr.reshape(-1) #flatten it to 1024
            img.close()
            print("=> Face Image "+ str(i+1) + "/"+ str(n_faces) + " Processed.",end = '\r', flush = True)

        #for all the non-faces images: which follows the same procedure as the above for all the faces image except there is only 1 channel grayscale already.
        for i in range(n_non_faces):
            img =Image.open(imgFileNames_Non_Faces[i])
            cropped_img = img.crop(area)
            resizedAndCroppedImg = cropped_img.resize((32,32), Image.ANTIALIAS)
            imgArrGrayScale = numpy.asarray(resizedAndCroppedImg)
            img_Non_Faces[i] = imgArrGrayScale.reshape(-1)
            img.close()
            print("=> Non-Face Image "+ str(i+1) + "/"+ str(n_non_faces) + " Processed.",end = '\r', flush = True)
 

    
        #save the images array to numpy files
        numpy.save(CONST_FACES_NUMPY_FILE,img_Faces)
        numpy.save(CONST_NON_FACES_NUMPY_FILE,img_Non_Faces)

        #display some results, and ask user to go back to menu.
        print("\n\nImage Files for Faces and Non-Faces Processing Completed.")
        print("Faces numpy file saved as: " + CONST_FACES_NUMPY_FILE)
        print("Non-Faces numpy file saved as: " +  CONST_NON_FACES_NUMPY_FILE + "\n\n")
        input("Please Press Enter to go Back to the Menu . . . ")
        print("\n")
    except:
        #display some failed results for the images processsing and ask user to go back to menu.
        print("\n\nImage Files for Faces and Non-Faces Processing Failed.")
        print("Please Make sure Folder name: " + CONST_NON_FACES_FOLDER + " has Images in them.")
        print("And Please Make sure Folder name: " + CONST_FACES_FOLDER + " has Images in them.")
        print("Also, make sure every image size is: 250x250.")
        print("\nPlease press Enter and go back to the main menu,")
        input("and from there select 1 to create the files if those Folders has Images in them now AND/OR each image size is 250x250 . . . ")
        print("\n")


#this part is for training the data:
def trainingData():
    print("\n_____________________________________________________________")
    print("\nTraining Data:\n")

    Faces = numpy.array([])
    Non_Faces = numpy.array([])

    #error checking to see if image array numpy files exists. and making sure it has images in them.
    try:
        Faces = numpy.load(CONST_FACES_NUMPY_FILE)
        Non_Faces = numpy.load(CONST_NON_FACES_NUMPY_FILE)
    except:
        print("\n\nFile names: " + CONST_FACES_NUMPY_FILE + " AND/OR " + CONST_NON_FACES_NUMPY_FILE + " were not found.")
        input("Please press Enter and go back to the main menu, and from there select 1 to create the files . . . ")
        print("\n")
    else:
        if (len(Faces)==0):
            print("\n\nPlease Make sure Folder name: " + CONST_FACES_FOLDER + " has Images in them.")
            print("Please press Enter and go back to the main menu,")
            input("and from there select 1 to create the file if that Folder has Images in them now . . . ")
            print("\n")
            return;
        if (len(Non_Faces)== 0):
            print("\n\nPlease Make sure Folder name: " + CONST_NON_FACES_FOLDER + " has Images in them.")
            print("Please press Enter and go back to the main menu,")
            input("and from there select 1 to create the file if that Folder has Images in them now . . . ")
            print("\n")
            return;

        #start of MLP part.
        
        #Class 1 (Face) has label of 1 AND Class 2 (Non-Face) has label of 0.
        Label = numpy.concatenate((numpy.ones(len(Faces)),numpy.zeros(len(Non_Faces)))) #for labels
        X = numpy.concatenate((Faces,Non_Faces)) #having classes input array of the images into 1 big matrix.
        X = numpy.concatenate((numpy.ones((len(X),1)),X), axis = 1) #appending 1 for threshold, so each image now has flatten 1025 data points.
        random.seed() #explicitly initialize the seed.

        #going to randomize the training data's order for better generalization. If there is a weights file here that is not weights final (i.e. program crashed in the middle of training) and not equal end of Epoch MAX index [49] and this reruns, the indexes will be different, but it will not be a big issue, maybe, even more better generalization.
        indexes = list(range(len(X)))
        random.shuffle(indexes)

        X_shuffled = X[indexes]
        Label_shuffled = Label[indexes]


        outputError = numpy.empty((len(X_shuffled),1))  #this one I need for comparing the error.
        
        #smallest error
        smallest_Error = len(X_shuffled) #setting it to maximum of the training data.
        

        w_hidden = []  #it has 30 x 1025 weights 
        w_output = numpy.array([])  #it has 31 output weights

        

        #check to see if file CONST_WEIGHTS_FILE exists:

        #creating a array for the file
        fileW = []
        epochNum=0  # to set for current epoch num, incase a program is closed before training upto last epoch number and get the value from a file CONST_WEIGHTS_FILE
        trainingTime=0 #doing the same for trainingTime so you get the value from a file CONST_WEIGHTS_FILE

        #error checking to see if CONST_WEIGHTS_FILE file exists.
        try:
            fileW = open(CONST_WEIGHTS_FILE,'r')
            fileW.close()
        except FileNotFoundError:
            #going to create the file here. CONST_WEIGHTS_FILE
            #1024 + 1
            #creating 30 hidden weights array of 1025 input data
            for i in range(30):
                w_hidden.append(numpy.random.uniform(low=-1.0,high=1.0, size=(1025,1))) #between -1 and 1

            #30 + 1
            #creating 31 output weights between -1 and 1
            w_output = numpy.transpose(numpy.array([2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1,
                                                    2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1,
                                                    2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1,
                                                    2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1,
                                                    2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1,
                                                    2*random.random()-1]))

            strLine = "-1,0,0" #-1 is flag, but that index is used for errors., 0 for epoch index at the end of, 0 for training time
            for i in range(31): #putting the init weights output into file
                strLine += "," + str(w_output[i])
            for i in range(30):  #putting the init weights hidden into file
                for j in range(1025):
                    strLine += "," + str(w_hidden[i][j][0])

            
            #writting to file
            fileW = open(CONST_WEIGHTS_FILE,'w')
            fileW.write(strLine)
            fileW.close()

         

        else:
            fileW = open(CONST_WEIGHTS_FILE, 'r') #file exists
            arr = fileW.read()
            fileW.close()
            arr = arr.split(',')
            #checking for flag error, that means epoch index [0] is not completed: so I will re initialize the weights.
            if (arr[0] == "-1"):
                #also remove the file CONST_WEIGHTS_FILE
                os.remove(CONST_WEIGHTS_FILE)
                
                #recreate the weights with new values.
                for i in range(30):
                    w_hidden.append(numpy.random.uniform(low=-1.0,high=1.0, size=(1025,1)))

                #30 + 1
                w_output = numpy.transpose(numpy.array([2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1,
                                                        2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1,
                                                        2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1,
                                                        2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1,
                                                        2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1, 2*random.random()-1,
                                                        2*random.random()-1]))
                #recreate the strLine with new weights values
                strLine = "-1,0,0"
                for i in range(31):
                    strLine += "," + str(w_output[i])
                for i in range(30):
                    for j in range(1025):
                        strLine += "," + str(w_hidden[i][j][0])

            
                #recreate the file with new weights values
                fileW = open(CONST_WEIGHTS_FILE,'w')
                fileW.write(strLine)
                fileW.close()

             
            else:
                #file did exist, and epoch has completed at least one index [0]
                smallest_Error = int(arr[0]) #setting the smallest_error as the first one.
                epochNum = int(arr[1]) +1   #setting the epochNum, but increasing it by 1, so if 0, that is the end of 0, so next starts at 1
                trainingTime = float(arr[2])  #having the training time

                #having the weights from the file for output weights
                w_output = numpy.transpose(numpy.array([float(arr[3]), float(arr[4]),float(arr[5]),float(arr[6]),float(arr[7]),float(arr[8]),
                                                        float(arr[9]), float(arr[10]),float(arr[11]),float(arr[12]),float(arr[13]),float(arr[14]),
                                                        float(arr[15]), float(arr[16]),float(arr[17]),float(arr[18]),float(arr[19]),float(arr[20]),
                                                        float(arr[21]), float(arr[22]),float(arr[23]),float(arr[24]),float(arr[25]),float(arr[26]),
                                                        float(arr[27]), float(arr[28]),float(arr[29]),float(arr[30]),float(arr[31]),float(arr[32]),
                                                        float(arr[33])]))
                #having the weights from the file for hidden layer weights
                w_hidden = numpy.empty([30,1025,1], dtype=float)
                for i in range(30):
                    for j in range(1025):
                        w_hidden[i,j,0]= float(arr[34 + i*1025 + j])

               




        start_time = time.time() #timing the training

        #start the training
        for epoch in range(epochNum,CONST_EPOCH_MAX):
            
            totalError = 0
            for i in range(len(X_shuffled)):
                #forward calculation (using sigmoid function)
                input_30 = []
                z_30 = []
                for j in range(30):
                    input_30.append(numpy.clip(numpy.dot(X_shuffled[i,:],w_hidden[j]),-500,500)) #must use clip or exception raises for overflow
                    z_30.append(1/(1 + math.exp(-input_30[j]))) #doing the sigmoid function
                
                xhidden = [1, z_30[0],z_30[1],z_30[2], z_30[3],z_30[4],z_30[5], z_30[6],z_30[7],z_30[8], z_30[9],z_30[10],z_30[11],
                           z_30[12],z_30[13],z_30[14], z_30[15],z_30[16],z_30[17], z_30[18],z_30[19],z_30[20], z_30[21],z_30[22],z_30[23],
                           z_30[24],z_30[25],z_30[26], z_30[27],z_30[28],z_30[29]]

                input_31 = numpy.clip(numpy.dot(xhidden,w_output),-500,500) #again use clip here.
                z_31 = 1/(1 + math.exp(-input_31))

                #prediction of the output.
                prediction = round(z_31,0)
                outputError[i] = abs( Label_shuffled[i] - prediction)
                totalError = totalError + int(outputError[i])

                #backward propagation of the error.
                #update the error
                error_31 = z_31 * (1-z_31)*(Label_shuffled[i] - z_31) #output node

                error_30 = []

                for j in range(30):
                    error_30.append(z_30[j]*(1-z_30[j])*(error_31*w_output[j]))

                #updating the output weight
                w_output = w_output + [CONST_ALPHA*error_31, CONST_ALPHA*error_31*z_30[0], CONST_ALPHA*error_31*z_30[1],CONST_ALPHA*error_31*z_30[2],
                                       CONST_ALPHA*error_31*z_30[3],CONST_ALPHA*error_31*z_30[4],CONST_ALPHA*error_31*z_30[5],CONST_ALPHA*error_31*z_30[6],
                                       CONST_ALPHA*error_31*z_30[7],CONST_ALPHA*error_31*z_30[8],CONST_ALPHA*error_31*z_30[9],CONST_ALPHA*error_31*z_30[10],
                                       CONST_ALPHA*error_31*z_30[11],CONST_ALPHA*error_31*z_30[12],CONST_ALPHA*error_31*z_30[13],CONST_ALPHA*error_31*z_30[14],
                                       CONST_ALPHA*error_31*z_30[15],CONST_ALPHA*error_31*z_30[16],CONST_ALPHA*error_31*z_30[17],CONST_ALPHA*error_31*z_30[18],
                                       CONST_ALPHA*error_31*z_30[19],CONST_ALPHA*error_31*z_30[20],CONST_ALPHA*error_31*z_30[21],CONST_ALPHA*error_31*z_30[22],
                                       CONST_ALPHA*error_31*z_30[23],CONST_ALPHA*error_31*z_30[24],CONST_ALPHA*error_31*z_30[25],CONST_ALPHA*error_31*z_30[26],
                                       CONST_ALPHA*error_31*z_30[27],CONST_ALPHA*error_31*z_30[28],CONST_ALPHA*error_31*z_30[29]] 
                
                #updating the hidden layer weights
                w_30_delta = []
                #for the first one delta
                for j in range(30):
                    w_30_delta.append(numpy.empty((1025,1)))
                    w_30_delta[j][0] = CONST_ALPHA* error_30[j]

                #for the rest delta
                for j in range(1,1025):
                    for k in range(30):
                        w_30_delta[k][j] = CONST_ALPHA * error_30[k]*X_shuffled[i,j]
               
                #w_new = w_old + w_delta
                for j in range(30):
                    w_hidden[j] = w_hidden[j] + w_30_delta[j]
                #display current image trained for current epoch
                print("Training Epoch = " + str(epoch+1) + "/"+str(CONST_EPOCH_MAX) + ", Image = " + str(i+1) + "/" +str(len(X_shuffled)))

            
            #printing the total error for the finished current epoch.
            print("\nTraining Epoch = " + str(epoch+1) + "/"+str(CONST_EPOCH_MAX) + " Completed. Error = " + str(totalError) + "\n")
            
            
            elapsed_time = time.time() - start_time #elapsed time for training time for the current epoch when ended.
            start_time = time.time()   #restarting the training time quickly
            trainingTime += elapsed_time #training time be incremented by the elapsed time.

            #update CONST_WEIGHTS_FILE  
            strLine = str(totalError) + "," + str(epoch) + "," + str(trainingTime)
            for i in range(31):
                strLine += "," + str(w_output[i])
            for i in range(30):
                for j in range(1025):
                    strLine += "," + str(w_hidden[i][j][0])

            

            fileW = open(CONST_WEIGHTS_FILE,'w')
            fileW.write(strLine)
            fileW.close()

            #error checking for the smalllest weights file
            try:
                fileW = open(CONST_SMALLEST_WEIGHTS_FILE,'r')
                fileW.close()
            except FileNotFoundError:
                    #if totalError is smaller than smallest_Error value,  and no smallest weights file found:
                    if (smallest_Error > totalError):
                        smallest_Error = totalError  #set new for smallest_Error          
                        #update Smallest_Weights file
                        fileW = open(CONST_SMALLEST_WEIGHTS_FILE,'w')
                        fileW.write(strLine) #strLine was set for weight file, so will use it here  for the smallest weights file.
                        fileW.close()
            else:
                #file smallest weights found.
                fileW = open(CONST_SMALLEST_WEIGHTS_FILE, 'r')
                arr2 = fileW.read()
                fileW.close()
                arr2 = arr2.split(',')
                #if totalError is smaller than the errors found inside the smallest weights file:
                if (int(arr2[0]) > totalError):
                    smallest_Error = totalError   #set new for smallest_Error                          
                    #update Smallest_Weights file
                    fileW = open(CONST_SMALLEST_WEIGHTS_FILE,'w')
                    fileW.write(strLine) #strLine was set for weight file, so will use it here  for the smallest weights file.
                    fileW.close()


                 

        
        #training has completed.
        #display some results.
        print("\n\nTraining Data has Completed.")
        print("Total time elapsed for training:", round(trainingTime,3), 'seconds.')

        #error checking to see if copy file from weights is successful to final weight and reading the file smallest weights.
        try:
            shutil.copy2(CONST_WEIGHTS_FILE, CONST_WEIGHTS_FINAL_FILE) #copy weights file into final weights file since the training is completed.
            os.remove(CONST_WEIGHTS_FILE) #remove the weights file.
            fileW = open(CONST_SMALLEST_WEIGHTS_FILE, 'r')  #open smallest weights file. to display the smallest error and ask user to go back to menu.
            arr3 = fileW.read()
            fileW.close()
            arr3 = arr3.split(',')
            print("The Smallest Error is: " + arr3[0])
            print("The Weights for the Smallest Error is saved in file: " + CONST_SMALLEST_WEIGHTS_FILE )
        
            input("Please Press Enter to go Back to the Menu . . . ")
            print("\n")

        except FileNotFoundError:
            #making the final file as smallest weight file since smallest weight file does not exists.
            print("Sorry, file: " + CONST_SMALLEST_WEIGHTS_FILE + " Not found.")
            print("The File: " + CONST_WEIGHTS_FINAL_FILE + " which is the last EPOCH NUMBER for Training will be placed into file: " + CONST_SMALLEST_WEIGHTS_FILE  )          
            #error checking again:
            try:
                shutil.copy2(CONST_WEIGHTS_FINAL_FILE, CONST_SMALLEST_WEIGHTS_FILE) #copy final weights final into smallest weights file and then displaying smallest error and ask user to back to the menu.
                fileW = open(CONST_SMALLEST_WEIGHTS_FILE, 'r')
                arr3 = fileW.read()
                fileW.close()
                arr3 = arr3.split(',')
                print("The Smallest Error is: " + arr3[0])
                print("The Weights for the Smallest Error is saved in file: " + CONST_SMALLEST_WEIGHTS_FILE )
        
                input("Please Press Enter to go Back to the Menu . . . ")
                print("\n")
            except FileNotFoundError:
                #smallest weights file did not copy properly, all the training failed, have to redo training. it will let the user know and asks user to go back to menu.
                print("Sorry, file: " + CONST_SMALLEST_WEIGHTS_FILE + " Not found.")
                print("Program failed . . .")
                input("Please Press Enter to go Back to the Menu and press 2 there and then Enter to Re-Train the Data . . . ")
                print("\n")


#this part will test the data based on the smallest weights file that was gotten from the training part which includes the weights.
def testingData():
    print("\n_____________________________________________________________")
    print("\nTesting Data:\n")
    testing_images = []  #making 151641 patching images based on one testing image file, the nasa one, which is 640x280
    #151641 = (640 - 32 +1 )*(280 -32 +1 ) because I want 32x32 patching images because the training images were 32x32

    #error checking to see if testing image is there:
    try:
        img = Image.open(CONST_TESTING_IMAGE_FILE)
        imgRGB = numpy.asarray(img)
        img.close()
        R,G,B = imgRGB[:,:,0], imgRGB[:,:,1], imgRGB[:,:,2]  
        grayScaleFinalImg = (R+G+B)/3  #again making it grayscale, one channel.

        # Generating patches from an image
        print("Creating all patches for the only test image: " + CONST_TESTING_IMAGE_FILE)
     
        imgPatchSize = (32,32)  #32x32


        #create the patched images

        # sliding in horizontal direction
        for i in range(grayScaleFinalImg.shape[0]-imgPatchSize[0]+1):          #.shape[0] = 280   =>  280-32+1
            # sliding in vertical direction
            for j in range(grayScaleFinalImg.shape[1]-imgPatchSize[1]+1):      #.shape[1] = 640  =>    640-32+1
                testing_images.append(grayScaleFinalImg[:,:][i:i+imgPatchSize[0],j:j+imgPatchSize[1]])  

   
        print("All patches created.")
    except:
        print("Sorry, file: " + CONST_TESTING_IMAGE_FILE + " Not found.")
        print("Program failed . . .")
        input("Please Press Enter to go Back to the Menu and press 3 there and then Enter once you have the image . . . ")
        print("\n")
        return


    arr = []  #is used to get everything from the file smallest weights.

    #error checking to see if smallest weights file exists:
    try:
        fileW = open(CONST_SMALLEST_WEIGHTS_FILE, 'r')
        arr = fileW.read()
        fileW.close()
        arr = arr.split(',')     
    except FileNotFoundError:
        print("\n\nSorry, file: " + CONST_SMALLEST_WEIGHTS_FILE + " Not found.")
        print("Make sure you have done Processing the Training Images and Trained the data.")
        input("Please Press Enter to go Back to the Menu . . . ")
        print("\n")
        return




    #Testing images:
    
    #setting the weights (output and hidden) to the values from the smallest weights file:
    w_output = numpy.transpose(numpy.array([float(arr[3]), float(arr[4]),float(arr[5]),float(arr[6]),float(arr[7]),float(arr[8]),
                                            float(arr[9]), float(arr[10]),float(arr[11]),float(arr[12]),float(arr[13]),float(arr[14]),
                                            float(arr[15]), float(arr[16]),float(arr[17]),float(arr[18]),float(arr[19]),float(arr[20]),
                                            float(arr[21]), float(arr[22]),float(arr[23]),float(arr[24]),float(arr[25]),float(arr[26]),
                                            float(arr[27]), float(arr[28]),float(arr[29]),float(arr[30]),float(arr[31]),float(arr[32]),
                                            float(arr[33])]))
    w_hidden = numpy.empty([30,1025,1], dtype=float)
    for i in range(30):
        for j in range(1025):
            w_hidden[i,j,0]= float(arr[34 + i*1025 + j])

    print("\nTesting Part:\n")

    #setting rows and cols and pixels for easier access.
    rows_ = 280-32+1  
    cols_ = 640-32+1
    pixels_ = 1024


    prediction_test = numpy.empty([rows_,cols_])  #this is a 2d array for the predictions. it is empty. will be filled later.
    Label_Test = numpy.zeros([rows_,cols_])       #this is a 2d array for labels, GROUND TRUTH, initially, I set all to zero (Non-Face), will fix later for the 23 faces so this 2d array will have 23  1s (Faces)


    #timing starts for testing:
    start_time = time.time()
    
    testing_images = numpy.array(testing_images) #this is the 151641 patched images, making it as numpy array
    
   
    testing_images = testing_images.reshape((rows_,cols_,pixels_)) #reshaping it such that it is a 2d list, and each element inside this 2d has (1024 elements which is flattened version of the 32x32)
   
    
    #testing it in a 2d way:
    for i in range(rows_):
        for j in range(cols_):
       
            #forward calculation (using sigmoid function)
            input_30 = []
            z_30 = []
       
            for j2 in range(30):
                inputimage_pixels = numpy.concatenate((1,testing_images[i,j]),axis =None)  # need to add threashold to the beginning of the image.
                input_30.append(numpy.clip(numpy.dot(inputimage_pixels,w_hidden[j2]),-500,500)) #numpy.dot the image here. also making sure numpy.clip is used here to prevent overflow error.
                z_30.append(1/(1 + math.exp(-input_30[j2])))
                
            xhidden = [1, z_30[0],z_30[1],z_30[2], z_30[3],z_30[4],z_30[5], z_30[6],z_30[7],z_30[8], z_30[9],z_30[10],z_30[11],
                        z_30[12],z_30[13],z_30[14], z_30[15],z_30[16],z_30[17], z_30[18],z_30[19],z_30[20], z_30[21],z_30[22],z_30[23],
                        z_30[24],z_30[25],z_30[26], z_30[27],z_30[28],z_30[29]]

            input_31 = numpy.clip(numpy.dot(xhidden,w_output),-500,500) #again use clip here.
            z_31 = 1/(1 + math.exp(-input_31))

            #prediction of the output.
            prediction_test[i,j] = round(z_31,0)

        print("Images In Row " + str(i+1) + "/" + str(rows_) + " Tested.") #once each row is completed, it will display that it was tested, that row of images.
            


    
    #by using paint, finding the top left of the face for each 23 faces pixels and adding it to this  2d array: for x and y coords of each 23 images. for GROUND TRUTH.        
    TrueFacesCoords = [[38,66],[122,71],[197,51],[257,52],[317,57],[393,55],[462,52],[523,56],[21,120],[95,108],[175,92],[231,117],
                   [291,114],[353,100],[416,111],[475,100],[560,88],[54,171],[154,173],[253,173],[344,162],[455,156],[564,164]]
                

    #opening the testing image, to start drawing the boundary box around the GROUND TRUTH DETECTED FACES:
    source_imgDraw = Image.open(CONST_TESTING_IMAGE_FILE).convert("RGBA")
    draw = ImageDraw.Draw(source_imgDraw)
    


    #fixing if multiple faces detected:

    #each 1px (1 pixel) bellow was an image 32x32 that started at that px (x,y) that was classified, and gave us prediction_test value,
    #if ALL of these pixels are predicted as Face (1), TrueFacesCoords = Face (1), otherwise, TrueFacesCoors = No-Face (0)
    #And all other pixels will turn to No-Face (0).
   
    #bounding box,  all 9 (3x3) images must be Face, so the prediction at GROUND TRUTH index is TP:  each of these is the coords for top-left of each image:
    #[ 1px top left  ][      1px top      ][  1px top right ]
    #[    1px left   ][1px TrueFacesCoords][    1px right   ]
    #[1px bottom left][     1px bottom    ][1px bottom right]
 
    
    #for the 23 images:
    for i in range(len(TrueFacesCoords)):
        Label_Test[TrueFacesCoords[i][1],TrueFacesCoords[i][0]] = 1  #making sure the Label is set to 1 here.
        if prediction_test[TrueFacesCoords[i][1],TrueFacesCoords[i][0]] == 1:
            flag = True #to see if all 9 images are face or not.
            y1= TrueFacesCoords[i][0]-1 #starting from 1 px left (y (vertical) is ROW here) and (x (horizontal) is COL here)
            x1= TrueFacesCoords[i][1]+1 #starting from 1 px top
            for y in range(y1,y1+3): #starting from ROW to ROW +2, so 3 (from left to right)
                for x in range(x1,x1-3,-1): #starting from COL to COL-2, so 3 (from top to bottom) going down.
                    #prediction_test indexes are flipped because image dimension is COL * ROW, but this prediction_test array is ROW * COL.
                    if prediction_test[x][y] == 0: #we just need one of these 9 to be 0, and make flag false, and prediction will be set to 0 at the GROUND TRUTH index
                        flag = False
                    #prediction_test indexes are flipped because image dimension is COL * ROW, but this prediction_test array is ROW * COL.
                    prediction_test[x][y]=0 #we will make all 9 to 0, if flag = True after the end of this nested loop, we will set the prediction to 1 at the GROUND TRUTH index
                   
            if flag == True:  #all 9 images predicted as Face, so at slightly different locations, 9 locations, 1px left/right/top/bottom and each is 32x32 image, Face was detected, so GROUND TRUTH index this location is set to 1 (Face) for prediction.   
                prediction_test[TrueFacesCoords[i][1],TrueFacesCoords[i][0]]=1 #set ground truth index
                draw = drawBorder(draw,TrueFacesCoords[i][0],TrueFacesCoords[i][1]) #draw the box (boundry box) at ground truth index location. #x and y,  or COL,ROW where arrays are ROW,COL
   

    #now we stop the timing and get the testing_time
    testing_time = time.time() - start_time

    source_imgDraw.show() #we will display the final tested image which includes boundry boxes around predicted GROUND TRUTH faces to the user. the user can close it.
    
    #setting up the Confusion matrix:

    TP = 0  #true positive (Face) Detected Face where There actually is a face.
    TN = 0  #true negative (Non-Face) Detected Non-Face where there actually is no-face.
    FP = 0  #false positive - detected a face where there isn't one.
    FN = 0  #false negative - detected a non-face where there is a face.

    #confusion matrix algorithm:
    for i in range(rows_):
        for j in range(cols_):
            if prediction_test[i,j] == Label_Test[i,j]:
                if (prediction_test[i,j] == 1):
                    TP = TP+1
                else:
                    TN = TN +1
            else:
                if (prediction_test[i,j] == 1):
                    FP = FP +1
                else:
                    FN = FN +1
    
    confusionMatrix = [[FP,TP],[TN,FN]] #the confusionMatrix in form of 2d array

    
    #display results:
    print("\nTesting Time = "+ str(round(testing_time,3)) + " seconds.\n")
    
    print("Total Images Classified: "+ str(rows_*cols_) + "\nThere are " + str(len(TrueFacesCoords))+ " Ground Truth Face (Positive) Images.")
    print("And there are " + str(rows_*cols_ - len(TrueFacesCoords)) + " Ground Truth Non-Face (Negative) Images.\n")
    
    print("Confusion Matrix Results Include:")
    print("False Positive = " + str(confusionMatrix[0][0]))
    print("True Positive = " + str(confusionMatrix[0][1]))
    print("True Negative = " + str(confusionMatrix[1][0]))
    print("False Negative = " + str(confusionMatrix[1][1]))
    

   
    #save the image that has boundry boxes for each GROUND TRUTH location that is predicted correctly:
    source_imgDraw.save(CONST_IMAGE_RESULT_FILE, 'PNG')
    source_imgDraw.close() #closing the image.

    print("\nPlease view the Image Result.")
    print("Also, the Image Result is saved in: " + CONST_IMAGE_RESULT_FILE)

    #creating a text file Results that has the confusionMatrix and the testing time in seconds in it.
    strLine = str(confusionMatrix[0][0]) + "," + str(confusionMatrix[0][1]) + "," + str(confusionMatrix[1][0]) + "," +str(confusionMatrix[1][1]) + "," + str(testing_time)
    fileW = open(CONST_DISPLAY_RESULTS_FILE,'w')
    fileW.write(strLine)
    fileW.close()

    print("Confusion Matrix and Testing Time is saved in file: " + CONST_DISPLAY_RESULTS_FILE  )


    print("\n\nTesting The Image File has Completed.")
    input("Please Press Enter to go Back to the Menu . . . ") #asking user to go back to menu.
    print("\n")


#this is a final stage of the project, if all the files that are used here are available, it will display the important results:       
def displayResults():
    #print("Display:\n")
    print("\n_____________________________________________________________")
    print("\nDisplay Results:\n")
    #prediction_test= numpy.load('../predict.npy')

    ##totalError = numpy.sum(prediction_test != Label_Test)
   
    #for use later when displaying that says how many images was tested.
    rows_ =249
    cols_ =609

    #error checking if all files exists/ user had gone through all the steps:  (I will include all the files in this project .zip file)
    try:
        #display the tested image that has boundry boxes for each GROUND TRUTH faces location that is predicted correctly:
        source_imgDraw = Image.open(CONST_IMAGE_RESULT_FILE).convert("RGBA")
        source_imgDraw.show()
        source_imgDraw.close()


        #getting the confusion matrix and the testing time and later will display it.
        fileW = open(CONST_DISPLAY_RESULTS_FILE,'r')
        arr = fileW.read()
        fileW.close()
        arr = arr.split(',')
        testing_time = float(arr[4])

        FP = int(arr[0])
        TP = int(arr[1])
        TN = int(arr[2])
        FN = int(arr[3])

        confusionMatrix = [[FP,TP],[TN,FN]]
        
     
       
       
        print("\nOnly 1 Testing Image was used.")
        print("Please view the Image Result which only displays the bounding box over the faces it detected.")

        #getting the number of faces and non faces used for training:
        Faces = numpy.load(CONST_FACES_NUMPY_FILE)
        Non_Faces = numpy.load(CONST_NON_FACES_NUMPY_FILE)
        print("\nThe number of Faces that was trained per epochs: "+str(len(Faces)))
        print("The number of Faces that was trained per epochs: "+str(len(Non_Faces)))
        print("The number of epochs used for training are:",CONST_EPOCH_MAX) #displaying epoch max
        print("The alpha (learning rate) used is:",CONST_ALPHA)  #displaying learning rate
        
        #getting the smallest error and at the end of which epoch it happened and display it
        fileW = open(CONST_SMALLEST_WEIGHTS_FILE, 'r')
        arr3 = fileW.read()
        fileW.close()
        arr3 = arr3.split(',')
        print("\nThe Smallest Error is: " + arr3[0] + " that happened at the end of epoch: " + str(int(arr3[1])+1))

        #getting the final weights file to get the training time at the end of epoch, which should be equal to epoch max, instead of [49] i will use 50 here.
        #and displaying it.
        fileW = open(CONST_WEIGHTS_FINAL_FILE , 'r')
        arr3 = fileW.read()
        fileW.close()
        arr3 = arr3.split(',')
        training_time = float(arr3[2])
        print("\nTraining Time = "+ str(round(training_time,3)) + " seconds at the end of epoch: "+str(int(arr3[1])+1))
        training_time = training_time /3600
        print("Training Time in hours =",round(training_time,2))

        #will use the coords here for the ground truth locations, however, just using the len of this which is 23.
        TrueFacesCoords = [[38,66],[122,71],[197,51],[257,52],[317,57],[393,55],[462,52],[523,56],[21,120],[95,108],[175,92],[231,117],
                   [291,114],[353,100],[416,111],[475,100],[560,88],[54,171],[154,173],[253,173],[344,162],[455,156],[564,164]]
        
        #display testing time:
        print("\nTesting Time = "+ str(round(testing_time,3)) + " seconds.")
        testing_time /= 3600
        print("Testing Time in hours =", round(testing_time,2))

        #displaying total number of images that classfied (151641) or rows_*cols_
        #displaying the GROUND TRUTH for both Faces and Non-Faces
        print("\nTotal Images Classified: "+ str(rows_*cols_) + "\nThere are " + str(len(TrueFacesCoords))+ " Ground Truth Face (Positive) Images.")
        print("And there are " + str(rows_*cols_ - len(TrueFacesCoords)) + " Ground Truth Non-Face (Negative) Images.\n")
    
        #displaying the confusion matrix:
        print("Confusion Matrix Results Include:")
        print("False Positive = " + str(confusionMatrix[0][0]))
        print("True Positive = " + str(confusionMatrix[0][1]))
        print("True Negative = " + str(confusionMatrix[1][0]))
        print("False Negative = " + str(confusionMatrix[1][1]))


        print("\n\nDisplaying the Result Completed.")
        input("Please Press Enter to go Back to the Menu . . . ")  #ask user to go back to the menu.
        print("\n")
     

    except:
        #if error happend, any files is missing, etc... and it asking user to go back to the menu.
        print("Error . . .")
        print("Please Makes sure No Files are missing and/or go back and do Process Image/Train/Test.")
        input("Please Press Enter to go Back to the Menu . . . ")
        print("\n")




#this is a simple menu that will call the functions at the top based on the user input:
def menu():
    menuSelect= "-1"  #init
    #display the menu string:
    textStr = "_____________________________________________________________"
    textStr +=  "\n4NN3 Final Project\n\n"
    textStr += "1 = Image Processing for Training Data\n"
    textStr += "2 = Training Data\n"
    textStr += "3 = Testing Data\n"
    textStr += "4 = Display Results\n"
    textStr += "0 = Exit the Program\n\n"
  

    while menuSelect != "0":   #run until user inputs "0" when in menu.  
        print(textStr) #display the menu
        menuSelect =input("Please type your choice and press Enter: ") #a sk user to enter their choice and either (it will call a function or rerunning the menu, or exiting the program)
        if menuSelect == "1":
            imageTrainingProcessing()
        elif menuSelect == "2":
            trainingData()
        elif menuSelect == "3":
            testingData()
        elif menuSelect == "4":
            displayResults()
       



#the main() function (method) that will run the menu() function.
def main():
    menu()


main() #calling the main() function.


#End of File: _4NN3_Project.py

   







