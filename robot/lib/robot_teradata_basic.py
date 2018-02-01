import teradata
import logging
import subprocess
import os
# Need this for exports
import csv

from robot.api.deco import keyword


## ---------------------------------------------------------------------------------------------------------------------
## Python Module : robot_terdata_basic.py
## Description : This module is used to support basic teradata robot tests
##----------------------------------------------------------------------------------------------------------------------

class robot_teradata_basic():
    """Class td_proto : this is a prototype robot test class"""
    ## -----------------------------------------------------------------------------------------------------------------
    #  ROBOT setting
    # -------------------------------------------------------------------------------------------------------------------
    # SCOPE can TEST SUITE,TEST CASE,GLOBAL
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    # VERSION
    ROBOT_LIBRARY_VERSION = '0.1'

    # Expliclty defining static key works
    # __all__ = ['example_keyword']

    def __init__(self, appConfigFile=None, system=None, username=None, password=None, external_dns=None):
        """Initialise
        appConfigFile = local udaexec.ini
        system = system to logon to
        username = user name
        password = password
        external_dbs = external DNS
        """
        if "ODBCINI" not in os.environ:
            os.environ["ODBCINI"] = """/opt/teradata/client/ODBC_64/odbc.ini"""
        self.udaexec = teradata.UdaExec(appName="td_proto", version=1,
                                        appConfigFile="""C:/Users/CW171001.TD/PycharmProjects/robot_prototype/udaexec.ini""")
        self.session = None

    # --------------------------------------------------------------------------------------------------
    # TJC Specific logon function - runs under linux
    # --------------------------------------------------------------------------------------------------

    def tjc_passwd(self, system, username):
        """Get password from tjc - returns rc -- 0 OK , passwd , msg"""
        rc = -1
        passwd = None
        errorMsg = None
        p = subprocess.Popen(['/opt/tjc/bin/tjc_passwd', '-s', system, '-u', username],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        rc = p.returncode
        if rc == 0:
            passwd = out.strip().replace("\n", '')
        return (rc, passwd, errorMsg)

    # --------------------------------------------------------------------------------------------------
    # Keyword : connect to teradata using external dsn
    # Parameters : external_dsn
    # Description : Connects to teradata using odbc external dsn - found one of udaexec.ini files
    # --------------------------------------------------------------------------------------------------
    @keyword('connect to teradata using external dsn', tags=['Teradata', ])
    def connect_using_external_dsn(self, external_dsn=None):
        """Connect to teradata using exertnal dsn as defined in local udaexec.ini"""
        # if already connected then close session
        if self.session is not None:
            self.session.close()
        self.session = self.udaexec.connect(externalDSN=external_dsn)

    # --------------------------------------------------------------------------------------------------
    # Keyword : connect to teradata using username
    # Parameters : system , username , password
    # Description : Connects to teradata using odbc system , username + password
    #                 if password = TJC then TJC is used to resolve password
    # --------------------------------------------------------------------------------------------------

    @keyword('connect to teradata using username', tags=['Teradata', ])
    def connect_using_username(self, system, username, password):
        """Connect to teradata using exertnal dsn as defined in local udaexec.ini"""
        # if already connected then close session
        if self.session is not None:
            self.session.close()
        # use tjc

        if password == 'TJC':
            logging.info("Using tjc password")
            (rc, password, errorMsg) = self.tjc_passwd(system, username)
        self.session = self.udaexec.connect(system=system, username=username, password=password, method='ODBC')

    # --------------------------------------------------------------------------------------------------
    # Keyword : run sql file
    # Parameters : filename
    # Description : Runs sql file on teradata for active session
    # --------------------------------------------------------------------------------------------------

    @keyword('run sql file', tags=['Teradata', ])
    def run_sql_file(self, filename, **kwargs):
        """This will run a sql script - does not return anything used for smoke testing"""
        logging.info("kwargs={}".format(kwargs))
        if "UDAEXEC" in kwargs:
            logging.info("UDAEXEC found")
            for key, value in kwargs["UDAEXEC"].items():
                logging.info("{}={}".format(key, value))
                self.udaexec.config[key] = value
                logging.info("udaexec {} = {}".format(key, self.udaexec.config[key]))
        try:
            self.session.execute(file=filename)
        except teradata.DatabaseError as e:
            sql_code = e.code;
            sql_state = e.sqlState;
            error_text = e.msg
            status = 'ERROR'
            # re throw exception
        return (sql_code, error_text)

    # -------------------------------------------------------------------------------------------------
    # Keyword : udaexec set variable
    # Parameters : Keywork , ValueError
    # Returns : Nothing
    # Description : Sets udaexec config variable
    # -------------------------------------------------------------------------------------------------
    @keyword('udaexec set variable', tags=['Teradata', ])
    def udaexec_set_variable(self, key, value):
        self.udaexec.config[key] = value

    # --------------------------------------------------------------------------------------------------
    # Keyword : run sql count
    # Parameters : sql statement
    # Returns : status , count , sql_code , error_text
    # Description : Returns the status NO ROWS , ROWS , count of rows , error code , and error text
    # --------------------------------------------------------------------------------------------------

    @keyword('run sql count', tags=['Teradata', ])
    def run_sql_count(self, sql):
        """This will run sql - expects a count back"""
        sql_code = 0
        count = 0
        error_text = ''
        status = "UNKOWN"
        try:
            row = self.session.execute(sql).fetchone()
            if row is None:
                status = 'NO ROWS'
            else:
                status = 'ROWS'
                # comment status
                count = row[0]

        except teradata.DatabaseError as e:
            sql_code = e.code
            sql_state = e.sqlState
            error_text = e.msg
            status = 'ERROR'
            # re throw exception
        return (status, count, sql_code, error_text)

    # --------------------------------------------------------------------------------------------------
    # Keyword : run sql
    # Parameters : sql statement
    # Returns : sql_code , error_text
    # Description :  runs sql and returns error code , and error text
    # --------------------------------------------------------------------------------------------------

    @keyword('run sql', tags=['Teradata', ])
    def run_sql(self, sql):
        """This will run sql - expects a count back"""
        sql_code = 0
        error_text = ''
        status = "UNKOWN"
        try:
            self.session.execute(sql)
        except teradata.DatabaseError as e:
            sql_code = e.code;
            sql_state = e.sqlState;
            error_text = e.msg
            status = 'ERROR'
            # re throw exception
        return (sql_code, error_text)

    # --------------------------------------------------------------------------------------------------
    # Keyword : run BTQ sql file
    # Parameters : filename
    # Returns : sql_code , error_text
    # Description :  runs sql file in bteq mode and returns error code , and error text
    # --------------------------------------------------------------------------------------------------
    @keyword('run BTQ sql file', tags=['Teradata', ])
    def run_btq_sql_file(self, filename, **kwargs):
        """This will run a sql script - does not return anything used for smoke testing"""
        logging.info("kwargs={}".format(kwargs))
        if "UDAEXEC" in kwargs:
            logging.info("UDAEXEC found")
            for key, value in kwargs["UDAEXEC"].items():
                logging.info("{}={}".format(key, value))
                self.udaexec.config[key] = value
                logging.info("udaexec {} = {}".format(key, self.udaexec.config[key]))
        try:
            self.session.execute(file=filename, fileType='bteq')
        except teradata.DatabaseError as e:
            sql_code = e.code;
            sql_state = e.sqlState;
            error_text = e.msg
            status = 'ERROR'
            # re throw exception
        return (sql_code, error_text)

    # --------------------------------------------------------------------------------------------------
    # Keyword : run teradata select and return one column of rows
    # Parameters : select statement
    # Returns : rowslist sql_code , error_text
    # Description :  runs sql
    # --------------------------------------------------------------------------------------------------
    @keyword('run teradata select and return one column of rows', tags=['Teradata', ])
    def run_teradata_select_and_return_one_column_of_rows(self, sql):
        """This will run sql - expects a count back"""
        sql_code = 0
        count = 0
        error_text = ''
        status = "UNKOWN"
        row_list = []
        try:
            status = 'NO ROWS'
            for row in self.session.execute(sql):
                status = 'ROWS'
                # comment status
                row_list.append(row[0])
        except teradata.DatabaseError as e:
            sql_code = e.code
            sql_state = e.sqlState
            error_text = e.msg
            status = 'ERROR'
            # re throw exception
        return (status, row_list, sql_code, error_text)

    # --------------------------------------------------------------------------------------------------
    # Keyword : run_sql_file_and_export_csv
    # Parameters : filename , csv filename
    # Description : Runs sql file on teradata for active session
    #               and exports result as csv file - excel format
    # --------------------------------------------------------------------------------------------------

    @keyword('run sql file and export csv', tags=['Teradata', ])
    def run_sql_file_and_export_csv(self, filename, csv_file, **kwargs):
        """This will run a sql script - does not return anything used for smoke testing"""
        sql_code = -1
        sql_state = 0
        error_text = "UNKNOWN"
        status = '';
        logging.info("kwargs={}".format(kwargs))
        if "UDAEXEC" in kwargs:
            logging.info("UDAEXEC found")
            for key, value in kwargs["UDAEXEC"].items():
                logging.info("{}={}".format(key, value))
                self.udaexec.config[key] = value
                logging.info("udaexec {} = {}".format(key, self.udaexec.config[key]))
        try:
            file_csv = open(csv_file, 'wb')
            csv_writer = csv.writer(file_csv, delimiter='|',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            # may be better way of doing this
            for row in self.session.execute(file=filename):
                r = []
                for x in row:
                    r.append(x)
                csv_writer.writerow(r)

            sql_code = 0
            sql_state = 0
            error_text = ""
            status = ''
        except teradata.DatabaseError as e:
            sql_code = e.code;
            sql_state = e.sqlState;
            error_text = e.msg
            status = 'ERROR'
            # re throw exception
        return (sql_code, error_text)


if __name__ == '__main__':
    x = robot_teradata_basic()
    x.connect_using_external_dsn("PRIMARK")
    x.connect_using_username(system='192.168.88.136', username='dbc', password='dbc')
    x.teradata_role_exits('BOB')
