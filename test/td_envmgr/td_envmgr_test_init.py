#-----------------------------------------------------------------------------
# File : td_envmgr_test_init.py
# Description : Initialise the environment and prepare for testing
#-----------------------------------------------------------------------------
import teradata
import os


# this will test python and jenkins
import teradata
udaexec = teradata.UdaExec(appName="test1",version=1)
session = udaexec.connect(method='ODBC', system="192.168.31.142", username='dbc', password='dbc')
exit(0)