# ECG Analyzer
To classify ECG readings to the correct heartbeat class and to identify if it is a case of Myocardial Infraction.

## Table of contents
1. [Project Overview](#project-overview)
2. [Problem Statement](#problem-statement)<br>
   2.1 [Solution Approach](#solution-approach)
3. [Installation](#installation)
4. [Model Build](#model-build)<br>
   4.1 [Input](#input-model-build)<br>
   4.2 [Output](#output-model-build)<br>
   4.3 [Metrics](#metrics)<br>
5. [Implementation](#implementation)<br>
   5.1 [Data Reshape](#data-reshape)<br>
   5.2 [NN-Architecture](#nn-architecture)<br>
   5.3 [Transfer Learning](#transfer-learning)<br>
   5.4 [Learning Trends](#learning-trends)<br>
6. [Refinement](#refinement)
7. [Launch Web App](#launch-web-app)
8. [Results](#results)
9. [Reflection](#reflection)
10. [Improvements and Future Scope](#improvements-and-future-scope)
11. [Licensing and Acknowledgements](#licensing-and-acknowledgements)

## Project Overview
To create an application which can take one or multiple ECG readings and to give a classification of the heartbeat type along with a test for Myocardial Infraction scenario.

## Problem Statement
1. ECG readings require experienced medical personel to carefully analyze data, interpret it to know the cardiac health status. To perform this activity repeatedly many times a day can lead to errors due to fatigue.
Also there are many places in rural India where such experienced medical personel are not easily found.
This app provides a easily usable api which can classify heartbeats as per the class standards defined by the Association for the Advancement of Medical Instrumentation (AAMI).

2. In cases of suspected acute Myocardial Infraction(MI), tests and diagnosis need to be made very quickly as time is of vital importance. The app makes full use of representations in two different datasets to arrive at a quick decision identifying a acute MI scenario with high accuracy.

## Solution Approach
As the two datasets being used are capturing same data but annotated for different cardiac states(Heartbeat class vs Myocardial Infraction class) the idea is to capture representations from one dataset/model and to make use of it in the second model.
Since transfer learning in neural networks have been performing well and with tools available in all frameworks, this approach has been selected as the way to build a classifier model to detect Myocardial Infraction.
Keras is the deep learning framework selcted because of the ease of use. Since the data are already in digitized, processed format only formatting required is to convert data shapes as expected by the framework.

## Installation
With Python 3.6 installed, ensure the packages in the requirements.txt are available.<br>
If model should be rebuilt, data can be downloaded using kaggle api.Kaggle python package needs to be installed, refer notebook for more.

## Model Build
Run all the cells of the notebook ECG_Classifier_Models.ipynb, if all the cells are successfully executed two models will be saved to disk in the models folder.
If the model should be rebuilt, the data has to be downloaded from kaggle. Refere the notebook for instructions to download and build models.

### Input Model Build
To build the model we need to provide two datasets. The details of the two datasets are provided below.
Source for these datasets is [here](https://www.kaggle.com/shayanfazeli/heartbeat)

__Arrhythmia Dataset:__<br>
Number of Samples: 109446<br>
Number of Categories: 5<br>
Sampling Frequency: 125Hz<br>
Data Source: Physionet's MIT-BIH Arrhythmia Dataset<br>
Classes: ['N': 0, 'S': 1, 'V': 2, 'F': 3, 'Q': 4]<br>
Files: data\mitbih_test.csv, data\mitbih_train.csv<br>
#### Class Distribution
|Class_Name  | Count  |
| -----------| -------|
| N          | 90587  |
| S          | 2779   |
| V          | 7236   |
| F          | 803    |
| Q          | 8039   |

__PTB Diagnostic ECG Database:__<br>
Number of Samples: 14552<br>
Number of Categories: 2<br>
Sampling Frequency: 125Hz<br>
Data Source: Physionet's PTB Diagnostic Database<br>
Files: data\ptbdb_abnormal.csv, data\ptbdb_normal.csv<br>
#### Class Distribution
|Class_Name  | Count  |
| -----------| -------|
| Normal     | 4045   |
| Abnormal   | 10505  |

Input filess contains digitized ECG readings with 187 data points for each reading and also a annotated column describing the type of the reading.<br>

__Data Snapshot :__
![](https://github.com/jinujayan/Capstone_ECGAnalyzer/blob/master/images/data_snap.png)

### Output Model Build
The newly built models will be saved under the models directory
model_ECG_final.h5, 
model_MI_final.h5

### Metrics

#### PTB Diagnostic - Class Distribution
|Class 0(Normal)  | Class 1(AbNormal)  |
| ----------------| -------------------|
| 4045            | 10505              |

As the domain of application being health and involves conditions of critical cardiac care the objective is to have very high certainity in the model while identifying the positive cases (Myocardial Infraction - Abnormal).<br>
The model must maximize identification of cases where the patient has the MI condition.<br>
Also since there is an imbalances of classes in the dataset, accuracy will not be a true indicator of performance.
To achieve this the metric of choice is __Recall__ which gives us an insight on the question : Out of all the people with the condition how many of them were correctly predicted?

__Recall = TP/(TP+FN)__

Since Recall is a global metric and will be misleading when evaluated within batches, the overall model performance is evaluated on predictions with the test set for different models.

## Implementation

### Data Reshape
Each record of the input file is a sequence of float values, 187 items in a row. To be used in Keras models the input to be reshaped to 
(N,187,1)

### NN-Architecture
To extract patterns from this one dimensional data sequence Convolution 1D layers are used. Two such layers with max pooling and a regularization drop out layer is used before compressing data to get an output of class count.
To help with the training a callback is used to ensure a checkpoint is saved for each epoch and also early stopping is enabled by tracking the trends in validation loss.
The amount of learning in each batch is quantized via loss calcualted as categorical_crossentropy.

__Default model params:__

|Parameter    |Value  |
| ------------|-------|
|learning_rate| 0.001 |
|batch_size   | 250   |

### Transfer Learning
Two classifiers are built using the above architecture, ECG_CLassifier and MI_Classifier. Since the domain of data and the formats were the same, the learned weights of classifier 1 were made use of in the second model. This gaves a marked improvement in the model performance.

### Learning Trends
The trends in default model's training accuracy and error is as shown below.<br>
![](https://github.com/jinujayan/Capstone_ECGAnalyzer/blob/master/images/pre_tuning.png)

## Refinement
Once the model with default parameter values was producing a good enough result, the model was subjected to parameter tuning exercise. Some of the parameters tuned were learning_rate, batch_size.The results are as shown in the table.

__Hyperparameter tuning results__

|Learning_rate|Batch_size) |Recall(max 1)|
| ------------|------------|-------------|
|0.023        | 150        |       0.912 |
|0.001        | 150        |       0.956 |
|**0.002**    | **150**    |   **0.966** |
|0.002        | 250        |       0.963 |
|0.0015       | 300        |       0.946 |
|0.002        | 300        |       0.953 |
|0.01         | 250        |       0.935 |

__Training best model :__
![](https://github.com/jinujayan/Capstone_ECGAnalyzer/blob/master/images/Final_model.png)

## Launch Web App
1. The app can be launched either on local machine or on aws instance. Configure the config.ini file present under the conf folder  accordingly.<br>
  __For AWS:__
  deploy_type = aws<br>
  hostname = 'Public DNS (IPv4) - available under instance details (ex: ec2-54-236-63-231.compute-1.amazonaws.com)'<br>
  port = 'available port'
  
  __For Localmachine:__
  deploy_type = local<br>
  hostname = 'localhost'<br>
  port = 'available port'
  
2. Run the following command in the app's directory to run your web app.
    `python app.py`

3. For local execution go to http://localhost:port/<br>
   For aws go to http://'IPv4 Public IP':port/ <br>
   Ex: http://54.236.63.231:8891

## Results

__Home Page__
<br>

![](https://github.com/jinujayan/Capstone_ECGAnalyzer/blob/master/images/webapp_home.png)

__Data Loading__
<br>

![](https://github.com/jinujayan/Capstone_ECGAnalyzer/blob/master/images/upload_data.png)

__Analysis Report__
<br>

![](https://github.com/jinujayan/Capstone_ECGAnalyzer/blob/master/images/results.png)

## Reflection
The end to end application development can be analyzed as two separate tasks<br>
1. Process data and build a neural network model<br>
2. Build a friendly UI around the model to serve users.

During model building, the power of learned representations in model building was noticed. When the MI classifier model was trained with random initializations the recall score noticed was 0.9325
When the weights were initialized with trained weights from classifier 1 there was an improvement in the score of classifier 2 to  0.9405 with all other parameters held constant.

Attempt was made to execute hyperparameter tunings in auto mode, but the sklearn grid search api could not directly be used in this scenario. For different combinations of parameters, tests were executed manually and results listed. As an improvement more faster ways of hyperparamter tuning should be investigated.

There can be big improvments made on the web app to make it more user friendly. Latest interactive web development libraries can be explored.
The perfromance of the web app needs more tuning to reduce the latency involved.

## Improvements and Future Scope
This project makes use of the processed and annotated dataset. To make it a fully usefull app we will need to interface directly with the ECG readers, this will need functionality to work directly with the raw data coming from the ECG machines.<br>
More understanding of the hardware and availability of such datsets need to be investigated.
Only heartbeat dataset has been used in the model, experiments can be done to investigate usage of other patient medical records to arrive at a more robust model.

## Licensing and Acknowledgements
Licensing on the data set is same as applicable in the source page [here](https://www.kaggle.com/shayanfazeli/heartbeat).
The analysis notebook code, the web app are available for open use, feel free to use it like you see fit.

Some of the resources used in building the app are:<br>
[Ideas in this paper](https://arxiv.org/abs/1805.00794)<br>
[Discussion-1](https://www.sciencedirect.com/science/article/pii/S0169260715003314)<br>
[Image1](https://www.idigitalhealth.com/news/e-tattoo-ecg-scg-readings-app)<br>
