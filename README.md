# Crab_Toolset
Set of codes that make large/group crab submissions easier. 


These codes were created to handle private MC production in the context of the CMS experiment.
Usage is simple but requires matching confing file names.

**CrabTask_manager.py**
Use it to check the status of several running jobs in sequence. It prints to the terminal the number of running jobs, failed jobs and finished jobs and saves the full output of each "crab status -d ..." in a .log file for further inspection. The resulting dataset of finished jobs is sequentially saved in .txt file, which can be used as input to the CrabTask_large_submission_handler.py . 
Moreover, there is a flag for authomatic resubmision of failed jobs, which when "True", also saves the output of "crab resubmit -d ..." in the same .log file.


TO RUN: 
```python3 CrabTask_manager.py "Keyword"```
Keyword -- a word to filter the Tasks that are going to be checked. E.g: using "miniAOD" only files containing "miniAOD" in the name are considered. If no keyword is provided all files are                           inspected. (This code assumes by default the folder crab_projects)


**CrabTask_large_submission_handler.py**
Use it to submit a large amount of Tasks to the grid, ensuring consistency of output names and a smother submission. This code uses as inputs a .py crab config file and a .txt file containing the directories of the data to be processed. It alters the crab config file according to the submission to be done. The name of the pset.py files present in the working directory must match the names given in this python file. If so they are automatically selected based on the input .txt file name. There is a flag set to "False" by default test before submitting. If the crab config file is being correctly updated then turn it "True" and run it. The code saves in a .log file the output of "crab submit -d..." to further inspect if the submission yield any warning.


TO RUN: python3 CrabTask_large_submission_handler.py 



TODO:
in a future commit I will make all the required parameters (pset names and flags) appear on the top of the code for even more simple usage.
