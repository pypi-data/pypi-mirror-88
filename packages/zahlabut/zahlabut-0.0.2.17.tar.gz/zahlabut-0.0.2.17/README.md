
### LogTool is used to extract all ***Unique Errors messages*** from log files that took place in the past.
## General
As the user, you can provide the "since time" and debug level to be used for extraction of Errors/Warnings. 
For example, if something went wrong in the past, you're be able to extract Error/Warnings messages
for just that time period.
Let's say that you have all relevant log files located in: **/var/log/containers** and that the problem you are
trying to debug, happened after: **2020-08-25 12:00:00** 
<br>If so, you'll need to set the following values in **".ini"** configuration file and to provide:

    time_grep=2020-08-25 12:00:00
    log_root_dir=['var/log/containers']
    string_for_grep = ERROR
  
## Installation
    pip3 install zahlabut
## Configuration file
Prior to starting analyze process, you'll need to create and load the configuration file.
Configuration file could be any *.ini file and you can find the example/template on GitHub:  
https://github.com/zahlabut/LogToolPyPi/blob/master/conf.ini 
<br>**Note:** change the configuration according to your needs.
## Usage - Python code example
    #!/usr/bin/python3    
    from zahlabut.LogTool import *               # To import all from zahlabut LogTool package
    load_conf_file('conf.ini')                   # To load the cofiguration file (conf.ini).
    result=start_analyzing()                     # Start analyzing log files.
    print(result['Standard_Log_Results'][0])     # First item in result list (raw data) for Standard logs.
    print(result['Not_Standard_Log_Results'][0]) # First item in result list (raw data) for Not Standard logs. 
## Generated result files
LogTool result files will be generated according to the settings provided in **"conf.ini"** file.

    create_logtool_result_file=yes
    log_tool_result_file = ResultFile.log
    save_standard_logs_raw_data_file='Standard_Logs_Output.log'
    save_not_standard_logs_raw_data_file='Not_Standard_Logs_Output.log'
Once **"log_tool_result_file = ResultFile.log"** is generated you'll be able to find all the statistics + exported 
unique Error blocks in this file. Created file is generated with some simple logic (its content is divided into the sections) see
the description on the top of created result file. 
