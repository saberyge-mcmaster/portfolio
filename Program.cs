/*
 * Author/Student Name (Student ID): Ehsan Sabery Ghomy (400345079)
 * Professor Name: Dr. Jeff Fortuna
 * Course: SFWR TECH 4CC3 (Parallel Programming)
 * Due Date: December 23, 2022
 * 
 * IDE: Microsoft Visual Studio Community 2019 - Version 16.11.20
 * Target Framework: .NET Core 3.1 (Out of support)
 * Programming Language: C#
 * File Name: Program.cs
 * 
 * Description: Course Project (Parallel Alphabetical Sort of Names)
 * 
 * 
 * Write-up:
 *      I chose QuickSort to do for this project on a given file name names.txt with 10000 firstnames and lastnames.
 *      
 *      
 *      
 *      I started with doing SEQUENTIAL Part First:
 *      
 *      I started with doing basic QuickSort algorithm to do on numbers, once that worked =>
 *      I started with doing QuickSort algorithm on sorting just the Last name, once that worked =>
 *      I started to do QuickSort by having lastname first, then a space, then firstname, 
 *              to do both sorts (by lastname then by first name) in one attempt and using string.compare(), 
 *              and when string.compare() value was 0 or -1, I would exchange values, once that worked =>
 *      I checked to see if the values from my Custom QuickSort is the same with the given .NET sorting function, once that worked =>
 *      
 *      
 *      
 *      I started with doing PARALLEL Part Second:
 *      
 *      I started doing 1 partition called (q1) and have 2 threads to work on before q1 in CustomQuickSort as Sequentially 
 *              and after q1 in CustomQuickSort as Sequentially (which is working on the 2 parts at the same time separately),
 *              and combine them together once they finished, with the q1 index already being sorted. 
 *              And that DID WORK, however, the timing for PARALLEL Part was longer than the SEQUENTIAL PART on the Release Mode, so =>
 *      I started doing 3 partitions (q1 to q3) and have 4 threads 
 *              (working on the 4 parts at the same time separately and combine them together once they finished), 
 *              and playing around with partition parameters, until the sorting worked, however, the timing for PARALLEL Part 
 *              was only faster by about 0 to 1 milliseconds than the SEQUENTIAL Part on the Release Mode, so =>
 *      I started doing 7 partitions (q1 to q7) and have 8 threads 
 *              (working on the 8 parts at the same time separately and combine them together once they finished), 
 *              and again playing around with partition parameters, until the sorting worked, however, the timing for PARALLEL Part 
 *              was only faster by about 1 milliseconds than the SEQUENTIAL Part on the Release Mode, so =>
 *      I started doing 15 partitions (q1 to q15) and have 16 threads
 *              (working on the 16 parts at the same time separately and combine them together once they finished),
 *              and as always playing around with partition parameters, until the sorting worked, this time, the timing for PARALLEL Part 
 *              was faster by about 2 to 4 milliseconds than the SEQUENTIAL Part on the Release Mode, so I stopped at 16 threads.
 *              
 * 
 * 
 * 
 * Extra Notes:  Timing in Debug Mode vs Release Mode on My Laptop (8 Cores, 16 Logical Processors, Windows 10 Home):
 * 
 * Debug Mode Attempt 1:  SEQUENTIAL   Sorting Code took 24 milliseconds to execute.
 * Debug Mode Attempt 1:  PARALLEL     Sorting Code took 76 milliseconds to execute.
 * 
 * Debug Mode Attempt 2:  SEQUENTIAL   Sorting Code took 24 milliseconds to execute.
 * Debug Mode Attempt 2:  PARALLEL     Sorting Code took 82 milliseconds to execute.
 * 
 * Debug Mode Attempt 3:  SEQUENTIAL   Sorting Code took 26 milliseconds to execute.
 * Debug Mode Attempt 3:  PARALLEL     Sorting Code took 78 milliseconds to execute.
 * 
 * 
 * Release Mode Attempt 1:  SEQUENTIAL Sorting Code took 18 milliseconds to execute.
 * Release Mode Attempt 1:  PARALLEL   Sorting Code took 15 milliseconds to execute.
 * 
 * Release Mode Attempt 2:  SEQUENTIAL Sorting Code took 19 milliseconds to execute.
 * Release Mode Attempt 2:  PARALLEL   Sorting Code took 15 milliseconds to execute.
 * 
 * Release Mode Attempt 3:  SEQUENTIAL Sorting Code took 18 milliseconds to execute.
 * Release Mode Attempt 3:  PARALLEL   Sorting Code took 16 milliseconds to execute.
 */


using System;
using System.Collections.Generic;
using System.IO;
using System.Diagnostics;


namespace _4CC3_Project
{
    public class Name //This Class is for getting and setting firstname and lastname.
    {
        public Name(string fname, string lname)
        {
            this.firstName = fname;
            this.lastName = lname;
        }
        public string firstName { get; set; }
        public string lastName { get; set; }
    }

    public class ParamValues_QS //This class is for getting and setting a list of Names class and p (beginning) and r (end) to make it an (object) when passing it to the CustomQuickSort Method. AND/OR passing its (object's attributes) to the CustomPartition Method.
    {
        public ParamValues_QS(List<Name> A, int p, int r)
        {
            this.A = A;
            this.p = p;
            this.r = r;
        }
        public List<Name> A { get; set; }
        public int p { get; set; }
        public int r { get; set; }
    }

    public class Program  //This class includes CustomPartition, CustomQuickSort, and the Main methods.
    {
        public static int CustomPartition(List<Name> A, int p, int r) 
        {
            //This custom partition method, by having lastname first, then a space, then firstname, to do both sorts (by lastname then by first name) in one attempt by string.Compare();
            //(A) is the array, (p) is the beginning, (r) is the end.

            string byLastByFirst_x = A[r].lastName + " " + A[r].firstName;

            int i = p - 1;
            for (int j = p; j < r; j++)
            {
                string byLastByFirst_j = A[j].lastName + " " + A[j].firstName;
                int compare = string.Compare(byLastByFirst_j, byLastByFirst_x);
                if (compare == 0 || compare == -1) //This condition is same as the Partition function for QuickSort Algorithm that does (if (A[j] <= x) then do ...)
                {
                    i++;
                    (A[i].firstName, A[j].firstName) = (A[j].firstName, A[i].firstName);  //exchange
                    (A[i].lastName, A[j].lastName) = (A[j].lastName, A[i].lastName);     //exchange
                }
            }
            (A[i + 1].firstName, A[r].firstName) = (A[r].firstName, A[i + 1].firstName);  //exchange
            (A[i + 1].lastName, A[r].lastName) = (A[r].lastName, A[i + 1].lastName);      //exchange
            return i + 1;
        }

        public static void CustomQuickSort(object o)
        {
            //This is the Custom QuickSort method.
            ParamValues_QS obj = (ParamValues_QS)o;  //this object includes: (A) is the array, (p) is the beginning, (r) is the end.

            int p = obj.p;
            int r = obj.r;

            if (p < r)
            {
                int q = CustomPartition(obj.A, obj.p, obj.r);

                obj.p = p;
                obj.r = q - 1;
                CustomQuickSort((object)obj);
                obj.p = q + 1;
                obj.r = r;
                CustomQuickSort((object)obj);
            }
        }

        static void Main(string[] args) //The Main Method.
        {
            //INITIALIZATION PART START ______________________________________________________________________________________________
            int THREAD_MAX_IS_16 = 16;  //Maximum number of Threads to run the Parallel sorting part is 16. (((PLEASE DO NOT CHANGE))).

            List<Name> Names_SEQ, Names_PAR;  //have two separate Lists for SEQUENTIAL and PARALLEL sorting.

            Names_SEQ = new List<Name>();
            Names_PAR = new List<Name>();

            //setting up the threads for Maximum number of threads.
            System.Threading.ParameterizedThreadStart ts = new System.Threading.ParameterizedThreadStart(CustomQuickSort);
            System.Threading.Thread[] threads_PAR = new System.Threading.Thread[THREAD_MAX_IS_16];

            for (int i = 0; i < THREAD_MAX_IS_16; i++)
            {
                threads_PAR[i] = new System.Threading.Thread(ts);
            }


            // populate the list of names from a file
            using (StreamReader sr = new StreamReader("names.txt"))
            {
                while (sr.Peek() >= 0)
                {
                    string[] s = sr.ReadLine().Split(' ');
                    Names_SEQ.Add(new Name(s[0], s[1])); //I want to have SEQUENTIAL list.
                    Names_PAR.Add(new Name(s[0], s[1])); //I want to have PARALLEL list.

                }
            }

            Stopwatch stopwatch; //for timing purposes.
            //INITIALIZATION PART END ______________________________________________________________________________________________

            //**********************************************************************************************************************

            //SEQUENTIAL PART START ______________________________________________________________________________________________
            Console.WriteLine("_________________________________________________________");
            Console.WriteLine("SEQUENTIAL Sorting:\n");

            // time the sort 
            stopwatch = Stopwatch.StartNew();


            ParamValues_QS o_SEQ = new ParamValues_QS(Names_SEQ, 0, Names_SEQ.Count - 1); //need to make this object to pass it to the CustomQuickSort Method.

            CustomQuickSort((object)o_SEQ);

            List<Name> sortedNames_SEQ = Names_SEQ;  //although Names_SEQ is sorted, I just want to make a new variable calling it sortedNames_SEQ.


            stopwatch.Stop();

            Console.WriteLine("SEQUENTIAL Sorting Code took {0} milliseconds to execute.\n", stopwatch.ElapsedMilliseconds);
            Console.WriteLine("_________________________________________________________\n");

            //SEQUENTIAL PART END ______________________________________________________________________________________________


            //**********************************************************************************************************************

            //PARALLEL PART START ______________________________________________________________________________________________
            Console.WriteLine("PARALLEL Sorting:\n");

            // time the sort 
            stopwatch = Stopwatch.StartNew();

            //will create 16 parts of the Names_PAR, so I can pass each one to different object of ParamValues_QS
            List<Name> Names_PAR_1, Names_PAR_2, Names_PAR_3, Names_PAR_4, Names_PAR_5, Names_PAR_6, Names_PAR_7, Names_PAR_8;
            List<Name> Names_PAR_9, Names_PAR_10, Names_PAR_11, Names_PAR_12, Names_PAR_13, Names_PAR_14, Names_PAR_15, Names_PAR_16;

            //will create 16 objects to pass it to different threads.
            ParamValues_QS o_PAR1, o_PAR2, o_PAR3, o_PAR4, o_PAR5, o_PAR6, o_PAR7, o_PAR8;
            ParamValues_QS o_PAR9, o_PAR10, o_PAR11, o_PAR12, o_PAR13, o_PAR14, o_PAR15, o_PAR16;

            Names_PAR_1 = new List<Name>();
            Names_PAR_2 = new List<Name>();
            Names_PAR_3 = new List<Name>();
            Names_PAR_4 = new List<Name>();
            Names_PAR_5 = new List<Name>();
            Names_PAR_6 = new List<Name>();
            Names_PAR_7 = new List<Name>();
            Names_PAR_8 = new List<Name>();
            Names_PAR_9 = new List<Name>();
            Names_PAR_10 = new List<Name>();
            Names_PAR_11 = new List<Name>();
            Names_PAR_12 = new List<Name>();
            Names_PAR_13 = new List<Name>();
            Names_PAR_14 = new List<Name>();
            Names_PAR_15 = new List<Name>();
            Names_PAR_16 = new List<Name>();

            ParamValues_QS o_PAR = new ParamValues_QS(Names_PAR, 0, Names_PAR.Count - 1); //need to make this object to pass its attributes into CustomPartition to divide the Names_Par into 16 parts.

            //this is based on a tree (Tree Traversals):
            //                   1
            //         2                     3
            //    4         5           6           7
            // 8     9   10   11     12   13     14   15


            //For CustomPartition to find the temp_q1 to temp_q15 values: AND Assuming (p < r) for the 16 CustomPartitions. Therefore (n must be larger than 16).
            // obj.p = p;                      //lower part
            // obj.r = q - 1;                  //lower part
            // CustomQuickSort((object)obj);   
            // obj.p = q + 1;                  //upper part 
            // obj.r = r;                      //upper part
            // CustomQuickSort((object)obj);  


            int temp_q1 = CustomPartition(o_PAR.A, o_PAR.p, o_PAR.r);            // 1  is root
            int temp_q2 = CustomPartition(o_PAR.A, o_PAR.p, temp_q1 - 1);        // 2  is from 1 lower
            int temp_q4 = CustomPartition(o_PAR.A, o_PAR.p, temp_q2 - 1);        // 4  is from 2 lower 
            int temp_q8 = CustomPartition(o_PAR.A, o_PAR.p, temp_q4 - 1);        // 8  is from 4 lower
            int temp_q9 = CustomPartition(o_PAR.A, temp_q4 - 1, temp_q2 - 1);    // 9  is from 4 upper
            int temp_q5 = CustomPartition(o_PAR.A, temp_q2 - 1, temp_q1 - 1);    // 5  is from 2 upper
            int temp_q10 = CustomPartition(o_PAR.A, temp_q2 - 1, temp_q5 - 1);   // 10 is from 5 lower
            int temp_q11 = CustomPartition(o_PAR.A, temp_q5 - 1, temp_q1 - 1);   // 11 is from 5 upper
            int temp_q3 = CustomPartition(o_PAR.A, temp_q1 + 1, o_PAR.r);        // 3  is from 1 upper
            int temp_q6 = CustomPartition(o_PAR.A, temp_q1 + 1, temp_q3 - 1);    // 6  is from 3 lower
            int temp_q12 = CustomPartition(o_PAR.A, temp_q1 + 1, temp_q6 - 1);   // 12 is from 6 lower
            int temp_q13 = CustomPartition(o_PAR.A, temp_q6 + 1, temp_q3 - 1);   // 13 is from 6 upper
            int temp_q7 = CustomPartition(o_PAR.A, temp_q3 + 1, o_PAR.r);        // 7  is from 3 upper
            int temp_q14 = CustomPartition(o_PAR.A, temp_q3 + 1, temp_q7 - 1);   // 14 is from 7 lower
            int temp_q15 = CustomPartition(o_PAR.A, temp_q7 + 1, o_PAR.r); ;     // 15 is from 7 upper
       
            //which ever node is visited TWICE (Inorder Traversal), from left to right.
            //this way I can have 16 partials in order from smallest to largest.
            int q1 = temp_q8;
            int q2 = temp_q4;
            int q3 = temp_q9;
            int q4 = temp_q2;
            int q5 = temp_q10;
            int q6 = temp_q5;
            int q7 = temp_q11;
            int q8 = temp_q1;
            int q9 = temp_q12;
            int q10 = temp_q6;
            int q11 = temp_q13;
            int q12 = temp_q3;
            int q13 = temp_q14;
            int q14 = temp_q7;
            int q15 = temp_q15;

            //putting the firstname and lastname into each of 16 parts based on the index.
            //since we did CustomPartitions, which was part of SEQUENTIAL part of the PARALLEL part,
            //we do not care for index values at =q1,=q2,=q3,..., upto =q15 since those indexes for Names_PAR are already sorted.
            //using switch statement for faster processing.

            for (int i = 0; i < Names_PAR.Count; i++)
            {
                switch (i)
                {
                    case int n when (n < q1):
                        Names_PAR_1.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                    case int n when (n > q1 && n < q2):
                        Names_PAR_2.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                    case int n when (n > q2 && n < q3):
                        Names_PAR_3.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                    case int n when (n > q3 && n < q4):
                        Names_PAR_4.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                    case int n when (n > q4 && n < q5):
                        Names_PAR_5.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                    case int n when (n > q5 && n < q6):
                        Names_PAR_6.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                    case int n when (n > q6 && n < q7):
                        Names_PAR_7.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                    case int n when (n > q7 && n < q8):
                        Names_PAR_8.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                    case int n when (n > q8 && n < q9):
                        Names_PAR_9.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                    case int n when (n > q9 && n < q10):
                        Names_PAR_10.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                    case int n when (n > q10) && n < q11:
                        Names_PAR_11.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                    case int n when (n > q11 && n < q12):
                        Names_PAR_12.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                    case int n when (n > q12 && n < q13):
                        Names_PAR_13.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                    case int n when (n > q13 && n < q14):
                        Names_PAR_14.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                    case int n when (n > q14 && n < q15):
                        Names_PAR_15.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                    case int n when (n > q15):
                        Names_PAR_16.Add(new Name(Names_PAR[i].firstName, Names_PAR[i].lastName));
                        break;
                }
            }

            //now we have the partial Names, we give those into 16 object parts.
            o_PAR1 = new ParamValues_QS(Names_PAR_1, 0, Names_PAR_1.Count - 1);
            o_PAR2 = new ParamValues_QS(Names_PAR_2, 0, Names_PAR_2.Count - 1);
            o_PAR3 = new ParamValues_QS(Names_PAR_3, 0, Names_PAR_3.Count - 1);
            o_PAR4 = new ParamValues_QS(Names_PAR_4, 0, Names_PAR_4.Count - 1);
            o_PAR5 = new ParamValues_QS(Names_PAR_5, 0, Names_PAR_5.Count - 1);
            o_PAR6 = new ParamValues_QS(Names_PAR_6, 0, Names_PAR_6.Count - 1);
            o_PAR7 = new ParamValues_QS(Names_PAR_7, 0, Names_PAR_7.Count - 1);
            o_PAR8 = new ParamValues_QS(Names_PAR_8, 0, Names_PAR_8.Count - 1);
            o_PAR9 = new ParamValues_QS(Names_PAR_9, 0, Names_PAR_9.Count - 1);
            o_PAR10 = new ParamValues_QS(Names_PAR_10, 0, Names_PAR_10.Count - 1);
            o_PAR11 = new ParamValues_QS(Names_PAR_11, 0, Names_PAR_11.Count - 1);
            o_PAR12 = new ParamValues_QS(Names_PAR_12, 0, Names_PAR_12.Count - 1);
            o_PAR13 = new ParamValues_QS(Names_PAR_13, 0, Names_PAR_13.Count - 1);
            o_PAR14 = new ParamValues_QS(Names_PAR_14, 0, Names_PAR_14.Count - 1);
            o_PAR15 = new ParamValues_QS(Names_PAR_15, 0, Names_PAR_15.Count - 1);
            o_PAR16 = new ParamValues_QS(Names_PAR_16, 0, Names_PAR_16.Count - 1);

            //now we give those 16 object parts to 16 different threads that will start.
            threads_PAR[0].Start((object)o_PAR1);
            threads_PAR[1].Start((object)o_PAR2);
            threads_PAR[2].Start((object)o_PAR3);
            threads_PAR[3].Start((object)o_PAR4);
            threads_PAR[4].Start((object)o_PAR5);
            threads_PAR[5].Start((object)o_PAR6);
            threads_PAR[6].Start((object)o_PAR7);
            threads_PAR[7].Start((object)o_PAR8);
            threads_PAR[8].Start((object)o_PAR9);
            threads_PAR[9].Start((object)o_PAR10);
            threads_PAR[10].Start((object)o_PAR11);
            threads_PAR[11].Start((object)o_PAR12);
            threads_PAR[12].Start((object)o_PAR13);
            threads_PAR[13].Start((object)o_PAR14);
            threads_PAR[14].Start((object)o_PAR15);
            threads_PAR[15].Start((object)o_PAR16);

            threads_PAR[0].Join(); //this part must be SEQUENTIAL, so we have to wait until first thread is completed.
                                   //since the next for loop index starts from 0. However, remember that the remaining 15 threads are working separately beside the first thread at the same time.

            //this part we will update the Names_PAR based on the threads that are finished. remember that the remaining 15 threads are working now or are completed.
            //using switch statement for faster processing.
            //this part is the PARALLEL part with sequential steps when index is met.
            //however, for majority of the threads, they are completed when index is reached there,
            //so the thread threads_PAR[ Greater than 0 ].Join(); code has a higher chance to move to the next line of code instead of waiting for that thread to complete because it is already completed.
            for (int i = 0; i < Names_PAR.Count; i++)
            {
                switch (i)
                {
                    case int n when (n < q1):
                        Names_PAR[i].firstName = Names_PAR_1[i].firstName;
                        Names_PAR[i].lastName = Names_PAR_1[i].lastName;
                        break;
                    case int n when (n == q1): //since 'q1' index is already sorted. we will just make sure this thread 'threads_PAR[1]' which is the second thread is completed if not already to move on to the next part. this algorithm is the same for indexes at  =q2,=q3,..., upto =q15.
                        threads_PAR[1].Join();
                        break;
                    case int n when (n > q1 && n < q2):  //have to fix indexes because Names_PAR_2 has lower index value than Names_PAR, it is same for the rest which are Names_PAR_3 to Names_PAR_16.
                        Names_PAR[i].firstName = Names_PAR_2[i - q1 - 1].firstName;
                        Names_PAR[i].lastName = Names_PAR_2[i - q1 - 1].lastName;
                        break;
                    case int n when (n == q2):
                        threads_PAR[2].Join();
                        break;
                    case int n when (n > q2 && n < q3):
                        Names_PAR[i].firstName = Names_PAR_3[i - q2 - 1].firstName;
                        Names_PAR[i].lastName = Names_PAR_3[i - q2 - 1].lastName;
                        break;
                    case int n when (n == q3):
                        threads_PAR[3].Join();
                        break;
                    case int n when (n > q3 && n < q4):
                        Names_PAR[i].firstName = Names_PAR_4[i - q3 - 1].firstName;
                        Names_PAR[i].lastName = Names_PAR_4[i - q3 - 1].lastName;
                        break;
                    case int n when (n == q4):
                        threads_PAR[4].Join();
                        break;
                    case int n when (n > q4 && n < q5):
                        Names_PAR[i].firstName = Names_PAR_5[i - q4 - 1].firstName;
                        Names_PAR[i].lastName = Names_PAR_5[i - q4 - 1].lastName;
                        break;
                    case int n when (n == q5):
                        threads_PAR[5].Join();
                        break;
                    case int n when (n > q5 && n < q6):
                        Names_PAR[i].firstName = Names_PAR_6[i - q5 - 1].firstName;
                        Names_PAR[i].lastName = Names_PAR_6[i - q5 - 1].lastName;
                        break;
                    case int n when (n == q6):
                        threads_PAR[6].Join();
                        break;
                    case int n when (n > q6 && n < q7):
                        Names_PAR[i].firstName = Names_PAR_7[i - q6 - 1].firstName;
                        Names_PAR[i].lastName = Names_PAR_7[i - q6 - 1].lastName;
                        break;
                    case int n when (n == q7):
                        threads_PAR[7].Join();
                        break;
                    case int n when (n > q7 && n < q8):
                        Names_PAR[i].firstName = Names_PAR_8[i - q7 - 1].firstName;
                        Names_PAR[i].lastName = Names_PAR_8[i - q7 - 1].lastName;
                        break;
                    case int n when (n == q8):
                        threads_PAR[8].Join();
                        break;
                    case int n when (n > q8 && n < q9):
                        Names_PAR[i].firstName = Names_PAR_9[i - q8 - 1].firstName;
                        Names_PAR[i].lastName = Names_PAR_9[i - q8 - 1].lastName;
                        break;
                    case int n when (n == q9):
                        threads_PAR[9].Join();
                        break;
                    case int n when (n > q9 && n < q10):
                        Names_PAR[i].firstName = Names_PAR_10[i - q9 - 1].firstName;
                        Names_PAR[i].lastName = Names_PAR_10[i - q9 - 1].lastName;
                        break;
                    case int n when (n == q10):
                        threads_PAR[10].Join();
                        break;
                    case int n when (n > q10 && n < q11):
                        Names_PAR[i].firstName = Names_PAR_11[i - q10 - 1].firstName;
                        Names_PAR[i].lastName = Names_PAR_11[i - q10 - 1].lastName;
                        break;
                    case int n when (n == q11):
                        threads_PAR[11].Join();
                        break;
                    case int n when (n > q11 && n < q12):
                        Names_PAR[i].firstName = Names_PAR_12[i - q11 - 1].firstName;
                        Names_PAR[i].lastName = Names_PAR_12[i - q11 - 1].lastName;
                        break;
                    case int n when (n == q12):
                        threads_PAR[12].Join();
                        break;
                    case int n when (n > q12 && n < q13):
                        Names_PAR[i].firstName = Names_PAR_13[i - q12 - 1].firstName;
                        Names_PAR[i].lastName = Names_PAR_13[i - q12 - 1].lastName;
                        break;
                    case int n when (n == q13):
                        threads_PAR[13].Join();
                        break;
                    case int n when (n > q13 && n < q14):
                        Names_PAR[i].firstName = Names_PAR_14[i - q13 - 1].firstName;
                        Names_PAR[i].lastName = Names_PAR_14[i - q13 - 1].lastName;
                        break;
                    case int n when (n == q14):
                        threads_PAR[14].Join();
                        break;
                    case int n when (n > q14 && n < q15):
                        Names_PAR[i].firstName = Names_PAR_15[i - q14 - 1].firstName;
                        Names_PAR[i].lastName = Names_PAR_15[i - q14 - 1].lastName;
                        break;
                    case int n when (n == q15):
                        threads_PAR[15].Join();
                        break;
                    case int n when (n > q15): //this part is to work on the last fragment part of the Name_PAR.
                        Names_PAR[i].firstName = Names_PAR_16[i - q15 - 1].firstName;
                        Names_PAR[i].lastName = Names_PAR_16[i - q15 - 1].lastName;
                        break;
                }
            }

            List<Name> sortedNames_PAR = Names_PAR; //although Names_PAR is sorted, I just want to make a new variable calling it sortedNames_PAR.

            stopwatch.Stop();

            Console.WriteLine("PARALLEL Sorting Code took {0} milliseconds to execute.\n", stopwatch.ElapsedMilliseconds);
            Console.WriteLine("_________________________________________________________\n");

            //PARALLEL PART END ______________________________________________________________________________________________

            //**********************************************************************************************************************

            //FINALIZE PART START ______________________________________________________________________________________________

            //Going to check if the sorted names for both SEQUENTIAL and PARALLEL parts are the same.
            //the sequential part was already tested with the code given to us that was .NET sort, and those were the same. 
            //but I am putting this code here to see if Sequential and Parallel are the same for testing purposes, which they are.
            
            string outPutVal = "CORRECT.";
            for (int i = 0; i < sortedNames_SEQ.Count; i++)
            {
                if (sortedNames_SEQ[i].firstName != sortedNames_PAR[i].firstName)
                {
                    outPutVal = "WRONG.";
                }
                if (sortedNames_SEQ[i].lastName != sortedNames_PAR[i].lastName)
                {
                    outPutVal = "WRONG.";
                }
            }

            Console.WriteLine("The Sequential and Parallel Sorted Values are: " + outPutVal);

            Console.WriteLine("\nEnd of Course Project. Please Press Enter to Exit...");
            Console.ReadLine();
            //FINALIZE PART END ______________________________________________________________________________________________
        }
    }
}


//End of File: Program.cs

