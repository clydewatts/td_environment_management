#-----------------------------------------------------------------------------
# File : td_envmgr_test_init.py
# Description : Initialise the environment and prepare for testing
#-----------------------------------------------------------------------------
import teradata
import os
import logging


def udaexec_set_defaults(udaexec):
    """This will set the defaults if udaexec is not present"""
    if 'DBADMIN_ENVCONFIG' not in udaexec.config:
        udaexec.config['DBADMIN_ENVCONFIG'] = 'DBADMIN_ENVCONFIG'
    if 'DBADMIN' not in udaexec.config:
        udaexec.config['DBADMIN'] = 'DBADMIN'
    if 'DBADMIN_SP' not in udaexec.config:
        udaexec.config['DBADMIN_SP'] = 'DBADMIN'
    if 'ROOT_DB' not in udaexec.config:
        udaexec.config['ROOT_DB'] = 'DBC'

def main():
    """Main"""
    udaexec = teradata.UdaExec(appName="test1" ,version=1)
    # Where am i
    logging.info("PWD={}".format(os.path.curdir))
    # Get environment variable for config
    session = udaexec.connect(method='ODBC', system="192.168.31.142", username='dbc', password='dbc')
    udaexec_set_defaults(udaexec)
    # Delete from databases
    session.execute("DELETE DATABASE ${DBADMIN_ENVCONFIG}" ,ignoreErrors = [3802])
    session.execute("DELETE DATABASE ${DBADMIN_SP}" ,ignoreErrors = [3802])
    session.execute("DELETE DATABASE ${DBADMIN}" ,ignoreErrors = [3802])
    # Drop databases
    session.execute("DROP DATABASE ${DBADMIN_ENVCONFIG}" ,ignoreErrors = [3802])
    session.execute("DROP DATABASE ${DBADMIN_SP}" ,ignoreErrors = [3802])
    session.execute("DROP DATABASE ${DBADMIN}" ,ignoreErrors = [3802])
    # Create database
    session.execute(file="../../ddl/DBADMIN.ddl")

if __name__ == '__main__':
    main()