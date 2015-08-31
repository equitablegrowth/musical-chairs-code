from __future__ import division
import pandas as pd
import string
import csv

# This cleans the file 'qwi_ALL_se_f_n3_op_u.csv'. That file was compiled from QWI's sex by education
# files for 2015 Q3 (the most recent dataset as of 8/24/2015). Some data is missing for all quarters
# in 2015 and for the 4th quarter of 2014, so these quarters could not be analyzed. This file performs
# cleaning functions and reshapes the data into an appropriate form for replicating the graphs in
# the research note. Functions should be run in order, with the 'file' variable changed to reflect the
# correct location of the data file.

# A complete workflow might look like this:
#	data=load_data(file)
#	educdata=education_graph(data)
#	final=education_graph2(educdata,dates=[2008,2014,2])

file='/qwi_ALL_se_f_n3_op_u.csv'


def load_data(file):
	# Load the data and replace all missing values with 0s. In practice this just applies to recent
	# quarters with no data or to certain rare occupations with no observations. These observations
	# will be excluded by future functions.
	with open(file,'rU') as csvfile:
		reader=csv.reader(csvfile)
		data=[row for row in reader]

	for i,row in enumerate(data):
		for j,value in enumerate(row):
			if value=='':
				data[i][j]='0'

	return data


def education_graph(data):
	# Take data from load_data and consolidate into national data rows. Currently data is by state
	# and education level. This function collapses all states and all educations into a year/quarter
	# by industry observations. Calculate the share of workers with college degrees as % of employees 
	# with BAs over total employees (not counting those <24). Average earnings is also calculated here.

	# This function is for the all employees graphs. For the hires graphs, the function education_graph
	# _hires should be used instead.

	# Load into pandas.
	datafile=pd.DataFrame(data[1:],columns=data[0])

	# Discard columns we don't care about, and E0 and E5 rules (all education and workers age <25,
	# respectively). Some type changes for future data manipulation. Also create the emp*earn var,
	# which will be the numerator of the average earnings calculation.
	industries=set(datafile['industry'])
	datafile=datafile[['industry','year','quarter','education','EarnS','EmpS']]
	datafile=datafile[datafile['education']!='E0']
	datafile=datafile[datafile['education']!='E5']
	datafile['year']=datafile['year'].astype(float)
	datafile['quarter']=datafile['quarter'].astype(int)
	datafile['EmpS']=datafile['EmpS'].astype(int)
	datafile['EarnS']=datafile['EarnS'].astype(int)
	datafile['weighted']=datafile['EmpS']*datafile['EarnS']
	national_list=[]

	# Loop through industries and years to create observations
	for industry in industries:
		print industry
		temp_data=datafile[datafile['industry']==industry]

		for year in range(2000,2015,1):
			year_data=temp_data[temp_data['year']==year]

			for quarter in range(1,5,1):
				quarter_data=year_data[year_data['quarter']==quarter]

				try:
					total_emp=quarter_data['EmpS'].sum()
					e4_emp=quarter_data[quarter_data['education']=='E4']['EmpS'].sum()
					total_earn=quarter_data['weighted'].sum()
					average_earn=total_earn/total_emp
					educ_share=e4_emp/total_emp
				except:
					average_earn=0
					educ_share=0
					total_emp=0

				national_list.append([year,quarter,industry,average_earn,educ_share,total_emp])

	return national_list


def education_graph_hires(datafile):
	# Take data from load_data and consolidate into national data rows. Currently data is by state
	# and education level. This function collapses all states and all educations into a year/quarter
	# by industry observations. Calculate the share of workers with college degrees as % of employees 
	# with BAs over total employees (not counting those <24). Average earnings is also calculated here.

	# This function is for the hires graphs. For the all employees graphs, the function education_graph
	# should be used instead.

	# Load into pandas.
	datafile=pd.DataFrame(data[1:],columns=data[0])

	# Discard columns we don't care about, and E0 and E5 rules (all education and workers age <25,
	# respectively). Some type changes for future data manipulation. Also create the emp*earn var,
	# which will be the numerator of the average earnings calculation.
	industries=set(datafile['industry'])
	datafile=datafile[['industry','year','quarter','education','EarnHirAS','HirAS']]
	datafile=datafile[datafile['education']!='E0']
	datafile=datafile[datafile['education']!='E5']
	datafile['year']=datafile['year'].astype(float)
	datafile['quarter']=datafile['quarter'].astype(int)
	datafile['HirAS']=datafile['HirAS'].astype(int)
	datafile['EarnHirAS']=datafile['EarnHirAS'].astype(int)
	datafile['weighted']=datafile['HirAS']*datafile['EarnHirAS']
	national_list=[]

	# Loop through industries and years to create observations
	for industry in industries:
		print industry
		temp_data=datafile[datafile['industry']==industry]

		for year in range(2000,2015,1):
			year_data=temp_data[temp_data['year']==year]

			for quarter in range(1,5,1):
				quarter_data=year_data[year_data['quarter']==quarter]

				try:
					total_emp=quarter_data['HirAS'].sum()
					e4_emp=quarter_data[quarter_data['education']=='E4']['HirAS'].sum()
					total_earn=quarter_data['weighted'].sum()
					average_earn=total_earn/total_emp
					educ_share=e4_emp/total_emp
				except:
					average_earn=0
					educ_share=0
					total_emp=0

				national_list.append([year,quarter,industry,average_earn,educ_share,total_emp])

	return national_list


def education_graph2(educ_data,dates=[2008,2014,2]):
	# Finally combine start and end observations to get the change between two dates and output a
	# single row for each industry that is suitable for creating the scatter plot in the research
	# analysis. This function takes the product of either education_graph_hires or eucation_graph 
	# and a list of the start year, end year, and quarter that the analysis should be conducted on.
	industries=set([row[2] for row in educ_data])
	master=[]

	for industry in industries:
		earn_start=0
		employment=0
		for row in [row for row in educ_data if row[2]==industry]:
			if row[0]==dates[0]:
				earn_start=earn_start+row[3]
				employment=employment+row[5]

			if row[0]==dates[0] and row[1]==dates[2]:
				educ_start=row[4]
			if row[0]==dates[1]  and row[1]==dates[2]:
				educ_end=row[4]

		# Wage is multiplied by .75 because it is currently the sum of four quarters. The base variable
		# is months, so multiplying it by 3/4 averages it over quarters and then converts it from months
		# to actual quarterly earnings. Employment is divided by 4 because it is also currently just the
		# sum of 4 quarters. The headers for this should be: ['industry','start','end','educ_delta',
		# 'earnings','emp']
		master.append([industry,educ_start,educ_end,educ_end-educ_start,earn_start*.75,employment/4])
	return master


def write(file,master):
	# Once master has been created by education_graph2, this will write the data to 'file' with headers.
	with open(file,'wb') as csvfile:
		writer=csv.writer(csvfile)
		writer.writerow(['industry','start','end','educ_delta','earnings','emp'])
		for row in master:
			writer.writerow(row)




