# Passions
Helping people find their passions since 2020-07-19.
This repository focuses on the technical components, mainly in the career mapping and paths.
## Overview
##### Testing
The user fills out a survey to determine their initial education, experience, and confidence in the career path. As well, once possible careers are chosen, they are demonstrated to the user in a clear way to gauge interest
##### Career Mapping
This allows the user to be shown broad categories, and slowly define their areas of interest.
##### Career Paths
Once a few options have been chosen, paths can be seen on how to get to the job of their choosing.
##### Training & Resources
Related courses and routes to success are provided to the user. Feedback is given to gauge how interested they are in the educational resources they have been provided.

## This Repository
##### What it is
This contains all of the code required to gather the data and analyze it to extract the career paths and mappings. The tfidf folder intially clusters the job titles (the 'posTitle' column) into more standard naming. From there, the prerequisite graph/trees can be made in the paths folder. As well, which people had what job is analyzed to create a map of all the tfidf clusters (standardized job titles) so that they can be clustered further to provide job categories to the user. 
##### How to use it
The dataset used is from https://www.kaggle.com/killbot/linkedin-profiles-and-jobs-data, which contains a dump.csv. Running init.py in the top level directory will clean this data, add the tfidf and map groupings, and create the preqrequisite graph so the the usage files can be run.