#!/usr/bin/python

# This script is used to generate the sql cmd based on the mySQL bkup csv file.
# input1:  MySQL DB table bkup csv format file
# input2:  Table column name 
# output:  The script

"""
e.g.
mews_es.MEWS_SUBSCRIBER.csv
# id, iccid, imsi, msisdn
925,8961011200001251013,505720200001013,61419450013

insert into MEWS_SUBSCRIBER (iccid, imsi, msisdn) VALUES ('8961011200001251013', '505720200001013', '61419450013');

ref:
MEWS_SUBSCRIBER:
id, iccid, imsi, msisdn

MEWS_ICCID_MGMT
id, createDate, status, usedDate, eolDate, iccid, imsi

MEWS_MSISDN_MGMT
id, createDate, status, usedDate, msisdn

MEWS_SECONDARY_DEVICE
id, activationStatus, altSmdpFqdn, createDate, deviceType, displayName, eid, iccid, imei, imsi, msisdn, statusChangeDate, statusChangeReason, subscriber_id, iccidStatus, iccidStatusChangeDate, iccidNotificationType, iccidErrorDetails

MEWS_APNS_TOKEN
id, imsi, lastChangeDate, notification_name, token

~~~ TO SAVE the sql data record to a file
mysql>

SELECT * FROM MEWS_SUBSCRIBER
INTO OUTFILE '/var/lib/mysql-files/mews_subscriber.csv'
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

Query OK, 100000 rows affected (0.34 sec)

"""
import glob
import csv


# define the global parameters
global mews_db
global mews_tables
global db_header

mews_db = 'mews_es'
mews_tables = ["MEWS_SUBSCRIBER", "MEWS_ICCID_MGMT", "MEWS_MSISDN_MGMT", "MEWS_SECONDARY_DEVICE", "MEWS_APNS_TOKEN"]
db_header = {"MEWS_SUBSCRIBER": "id, iccid, imsi, msisdn", 
"MEWS_ICCID_MGMT": "id, createDate, status, usedDate, eolDate, iccid, imsi", 
"MEWS_MSISDN_MGMT": "id, createDate, status, usedDate, msisdn", 
"MEWS_SECONDARY_DEVICE": "id, activationStatus, altSmdpFqdn, createDate, deviceType, displayName, eid, iccid, imei, imsi, msisdn, statusChangeDate, statusChangeReason, subscriber_id, iccidStatus, iccidStatusChangeDate, iccidNotificationType, iccidErrorDetails", 
"MEWS_APNS_TOKEN": "id, imsi, lastChangeDate, notification_name, token"}

def csv2sql(csvfile):
    # core function to convert the csvfile (MySQL bkup file) to sql 
    """
    e.g.
    mews_es.MEWS_SUBSCRIBER.csv
    # id, iccid, imsi, msisdn
    925,8961011200001251013,505720200001013,61419450013
    
    insert into mews_es.MEWS_SUBSCRIBER (iccid, imsi, msisdn) VALUES ('8961011200001251013', '505720200001013', '61419450013');
    
    tableName = mews_es.MEWS_SUBSCRIBER
    columns = 'iccid, imsi, msisdn'
    values =  "'8961011200001251013', '505720200001013', '61419450013'"
    
    columns 
    sql_str = "insert into {} ({}) VALUES ({});".format(tableName, columns, values)
    """   
    file_name = 'mysql.' + csvfile + '.txt'
    print file_name
    sql_file = open(file_name, 'w')
    
    #columns = 'id, iccid, imsi, msisdn'
    tableName = ''
    
    for table in mews_tables:
        if table in csvfile.upper():
            columns = db_header[table]
            tableName = mews_db + '.' + table
    
    #print tableName
    #print columns
    
    if tableName != '': 
        with open(csvfile,'rb') as f:  
            datareader = csv.reader(f)           
            for row in datareader:
                #print type(row)   #  <type 'list'>
                #print row    # ['1016', '8961011200001251030', '505720200001030', '61419450030']
                # header: id, iccid, imsi, msisdn                
                values = ''                
                for item in row[:-1]:
                    if item == '\N':
                        values = values + 'NULL,'
                    elif '"' in item:
                        values = values + item + ','
                    elif "'" in item:
                        values = values + item + ','
                    else:
                        values = values + "'" + item + "',"
                
                if row[-1] != '\N':
                    values = values + "'" + row[-1] + "'"
                else:
                    values = values + "NULL"
                                
                sql_str = "insert into {} ({}) VALUES ({});".format(tableName, columns, values)                
                sql_file.write(sql_str + '\n')
                print sql_str

    sql_file.close()
    
def main():
    csv_file_lst = glob.glob("./*.csv")
    for csv_file in csv_file_lst:
        #print csv_file
        # ./dev02.MEWS_APNS_TOKEN.csv
        input_file = csv_file.replace("./", "")
        
        csv2sql(input_file)
        raw_input("Press ENTER to continue...")
        
if __name__ == "__main__":
    main()    
