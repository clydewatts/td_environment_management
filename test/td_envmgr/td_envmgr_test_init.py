#-----------------------------------------------------------------------------
# File : td_envmgr_test_init.py
# Description : Initialise the environment and prepare for testing
#-----------------------------------------------------------------------------
import teradata
import os


# this will test python and jenkins
import teradata
udaexec = teradata.UdaExec(appName="test1",version=1)
exit(0)