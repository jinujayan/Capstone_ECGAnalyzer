# ECG Analyzer
To classify ECG readings to the correct beat class and to identify if it is a case of Myocardial Infraction

## Table of contents
1. [Project Overview](#project-overview)
2. [Problem Statement](#problem-statement)
3. [Installation](#installation)
4. [Model Build](#model-build)<br>
   4.1 [Input](#input-model-build)<br>
   4.2 [Output](#output-model-build)<br>
5. [Launch Web App](#launch web app)
6. [Results](#results)

## Project Overview
To create an application which can take one or multiple ECG readings and to give a classification of the heartbeat type along with a test for Myocardial Infraction scenario.

## Problem Statement
1. ECG readings require experienced medical personel to carefully analyze data, interpret it to know the cardiac health status. To perform this activity repeatedly many times a day can lead to errors due to fatigue.
Also there are many places in rural India where such experienced medical personel are not easily found.
This app provides a easily usable api which can classify heartbeats as per the class standards defined by the Association for the Advancement of Medical Instrumentation (AAMI).

2. In cases of suspected acute Myocardial Infraction(MI), tests and diagnosis need to be made very quickly as time is of vital importance. The app makes full use of representations in two different datasets to arrive at a quick decision identifying a acute MI scenario with high accuracy.

## Installation
With Python 3.6 installed, ensure the packages in the requirements.txt are available.<br>

## Model Build
Run all the cells of the notebook ECG_Classifier_Models.ipynb, if all the cells are successfully executed two models will be saved to disk in the models folder.

## Input Model Build
To build the model we need to provide two datasets.

__Arrhythmia Dataset:__<br>
Number of Samples: 109446<br>
Number of Categories: 5<br>
Sampling Frequency: 125Hz<br>
Data Source: Physionet's MIT-BIH Arrhythmia Dataset<br>
Classes: ['N': 0, 'S': 1, 'V': 2, 'F': 3, 'Q': 4]<br>
Path: data\arrhythmia_dataset<br>
Files: mitbih_test.scv, mitbih_train.csv<br>

__PTB Diagnostic ECG Database:__<br>
Number of Samples: 14552<br>
Number of Categories: 2<br>
Sampling Frequency: 125Hz<br>
Data Source: Physionet's PTB Diagnostic Database<br>
Path: data\ptb_dataset<br>
Files: ptbdb_abnormal.scv, ptbdb_normal.csv<br>


## Output Model Build
The newly build models will be saved under the models directory
model_ECG_final.h5
model_MI_final.h5

## Launch Web App
1. The can be run either on local machine or on aws instance. Configure the config.ini file present under the conf folder.
For AWS:
  deploy_type = aws
  hostname = <publicly accessible name of the instance>
  port = <availabl port>
  
2. Run the following command in the app's directory to run your web app.
    `python app.py`

3. For local execution go to http://localhost:<port>/
For aws go to http://<public IP>:<port>/

## Results

__Home Page__
<br>

![](https://github.com/jinujayan/DisasterResponse_ML_Pipeline/blob/master/images/HomePage_top.png)

__Category class distribution__
<br>
![](https://github.com/jinujayan/DisasterResponse_ML_Pipeline/blob/master/images/Barplot_group.png)
