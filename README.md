### Data and cleaning script for "The Cruel Game of Musical Chairs"

This repository contains 4 files: 

1. The raw data from QWI is available in qwi_ALL_se_f_n3_op_u.csv.zip. Very little cleaning has been done to this data save for the deletion of a number of cross-tabular rows present in the QWI that are not necessary for this project.

2. The raw data can be cleaned using education.py. This file is well commented and should be accessible to those with some Python experience. It aggregates the raw data (which is by state) into national data and can output the dataset that was used to make both figures in the piece. These datasets were also used in the regression analysis.

3. If you just want to see the data that went into the figures in the article, I have included these as well. The data for Figure 1 is in all_employment_graph.csv and the data for Figure 2 is hires_graph.csv. The headers in these files are:
  *industry: the three-digit NAICS code of the industry
  *start: the share of college-educated workers in the industry in 2000
  *end: the share of college-eduated workers in the industry in 2008
  *educ-delta: the difference between start and end (the y-axis quantity)
  *earnings: *quarterly* earnings (the x-axis quantity but we have multiplied by 4 to get yearly earnings)
  *emp: the weighted number of employees (bubble size in the figures)

If you have questions about this repository, feel free to contact Austin Clemens at aclemens@equitablegrowth.org
