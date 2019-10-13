import os
import urllib.request
import pandas as pd
import numpy as np
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import json
import plotly
import plotly.figure_factory as ff
import plotly.offline as py
import plotly.graph_objs as go
#import cufflinks as cf
#cf.go_offline()
import keras
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv1D, MaxPooling1D, GlobalAveragePooling1D
from keras.optimizers import SGD
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import argparse
from keras import backend as K

#STATIC_DIR = os.path.abspath('../ECG_Analysis/app/static')

app = Flask(__name__,static_url_path='/static')
app.secret_key = os.urandom(24)

ALLOWED_EXTENSIONS = set(['csv', 'xlsx','xls'])

my_parser = argparse.ArgumentParser(description='Arguments for the main program')
my_parser.add_argument("host", type=str,help='hostname')
my_parser.add_argument("port",type=int,help='port number')
args = my_parser.parse_args()
print(args.host)
print(args.port)
#app.run(host=args.host, port=args.port)

@app.route('/')
def upload_form():
	"""
    Method implementing the home url, it call the index.html to render a home page view

    @param 
        
    @return: Rendered html view
	"""
	
	return render_template('index.html',host="localhost", port=args.port)

def allowed_file(filename):
	"""
    Receives input from the home page, the input can either be a file with list of
	 ecg readings for anlysis, or a demo data string.
	 Display the plotted graph, the predicted classes in tabular form.


    @param file - Input analysis file / demo string
    @param If file, index of the row t obe plotted
    
    @return: Rendered html page
	"""
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods=['GET','POST'])
def uploader():

	if request.method == 'POST':
        # check if the post request has the file part
		
		test_flag = ''
		if 'file' in request.files:
			test_flag = 'file'
		else:
			test_flag = 'demo'
			demo_data = request.form['samplevalue']
		
		if test_flag == 'demo' :
			demo_data = demo_data.split(',')
			demo_data = [ float(val) for val in demo_data]
			
			out_df, graphJSON = predictionHandler(demo_data = demo_data)
			print("Show the shape of output DF")
			print(out_df.shape)
			colorscale = [[0, '#4d004c'],[.5, '#f2e5ff'],[1, '#ffffff']]
			table = ff.create_table(out_df, colorscale=colorscale, height_constant = 20)
			print(table)
			print("***********")
			#table.to_html()
			print("DBG1")
			pp_table = table.to_html()
			print("DBG2")
			print(table)
			
			return render_template('response.html', table = pp_table, graphplot = graphJSON)

			
		else:
			file = request.files['file']
			if file.filename == '':
				flash('No file selected for uploading')
				return redirect(request.url)
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(filename)
				flash('File successfully uploaded...call the handler now..')

				extension = file.filename.split('.')[1]
				plot_index = request.form['plot_sample']
				
				out_df, graphJSON = predictionHandler(file.filename,extension,plot_index= plot_index)
								
				colorscale = [[0, '#4d004c'],[.5, '#f2e5ff'],[1, '#ffffff']]
				table = ff.create_table(out_df, colorscale=colorscale, height_constant = 20)
				table.to_html()
				pp_table = table.to_html()
				
				return render_template('response.html', table = pp_table, graphplot = graphJSON)
			else:
				flash('Allowed file types are csv,xls,xlsx')
				return redirect(request.url)
	

def predictionHandler(test_file=False,extension='', plot_index=1, demo_data=[]):
	"""
    Method to call the inference on the model and to create the graph objects


    @param test_fileile - Input analysis file
    @param plot_index - The index of the data file to be plotted
    @param demo_data - The demo data string

    @return - Valid dataframe, graph json object
	"""
	plot_index = int(plot_index)
	if test_file:
		if extension == "csv":
			df = pd.read_csv(test_file)
		elif (extension == "xls" or extension == "xlsx"):
			df = pd.read_excel(test_file)
		else:
			raise ValueError('Input file with unexpected extension, please use csv, xlsx,xls files')
		test_rec = df.values
		test_rec = test_rec.reshape(test_rec.shape[0], test_rec.shape[1],1)
		
	
	else:
		test_rec =  np.array(demo_data)
		test_rec = test_rec.reshape(1, test_rec.shape[0],1)

		df_data = np.array(demo_data)
		df_data = df_data.reshape(1,df_data.shape[0])
		
		df = pd.DataFrame(data=df_data)
	
	model_ECG_loaded = load_model('../models/model_ECG_final.h5')
	model_MI_loaded = load_model('../models/model_MI_final.h5')
	print("models loaded...")
	out_classes = model_ECG_loaded.predict(test_rec)
	print("prediction completed..")
	ECG_class = np.argmax(out_classes,axis=1)	

	out_classes = model_MI_loaded.predict(test_rec)
	MI_class = np.argmax(out_classes,axis=1)

	out_df = pd.DataFrame(columns =['ECG_Class', 'MI_Class'], data = np.array([ECG_class, MI_class]).transpose())
	out_df['User_id'] = out_df.index+1
	out_df = out_df[['User_id', 'ECG_Class','MI_Class']]
	ecg_clas_mapper = {0:'N', 1:'S', 2:'V', 3:'F',4:'Q'}
	MI_class_mapper = {0:'Normal', 1:'Abnormal'}

	out_df.ECG_Class = out_df.ECG_Class.map(ecg_clas_mapper)
	out_df.MI_Class = out_df.MI_Class.map(MI_class_mapper)

	ecg_class = out_df.iloc[plot_index-1].ECG_Class
	mi_class = out_df.iloc[plot_index-1].MI_Class
	if mi_class == 0:
		mi_class = 'Normal'
	else:
		mi_class = 'Abnormality'
	graphs = createECGGraph(df,plot_index,ecg_class,mi_class)
	graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
	return out_df,graphJSON


def createECGGraph(df, plot_index, ecg_class, mi_class):
	"""
    Method to create the line plot graph object


    @param df  - The intermediate dataframe with predicted classes
    @param plot_index - The index of the data file to be plotted
    @param ecg_class - The ecg calss identified for the index being plotted
	@param mi_class - The Myocardial Infraction calss identified for the index being plotted

    @return: Valid plotly graph object
	"""

	df_index = plot_index-1
	
	xvals = list(range(0, df.iloc[df_index].count()))
	yvals = list(df.iloc[df_index].values)

	graphs = [
       			 {
            		'data': [
               	 	{
						"x": xvals,
						"y":yvals,
						"type": "scatter"
        	
					}
            				],

            		'layout': {
                		'title': f"ECG Readings for the record# {plot_index}, ECG class = {ecg_class} <br> MI tests shows {mi_class}",
                	'yaxis': {
                    	'title': "ECG Readings"
                			},
                	'xaxis': {
                    	'title': "Time instance"
                			}
            					}
        		}
			]

	return graphs


if __name__ == "__main__":
	#host, port = handleArgParser()
	app.run(host=args.host, port=args.port,threaded=False)