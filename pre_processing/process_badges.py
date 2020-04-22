try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import os.path
import pandas as pd
import argparse
import sqlite3

def badges_processing(file_name, output_file):
    index = []
    UserId = []
    BadgeName = []
    BadgeDate = []

    for event,elem in ET.iterparse(file_name):
        if event == "end":
            try:
                #print elem.tag,elem.attrib
                ind = int(elem.attrib["Id"])
                userid = int(elem.attrib["UserId"])
                badgename = elem.attrib["Name"]
                badgedate = elem.attrib["Date"]
                #print ind,userid,badgename,badgedate
                index.append(ind)
                UserId.append(userid)
                BadgeName.append(badgename)
                BadgeDate.append(badgedate)
                elem.clear()
            except Exception as e:
                pass

    df =pd.DataFrame({"UserId":UserId,"BadgeName":BadgeName,"BadgeDate":BadgeDate})
    DB = sqlite3.connect(output_file)
    df.to_sql(name='Badges', con=DB, if_exists='replace', index = False)
    DB.close()

if __name__ == "__main__":
    '''
    process */Badges.xml
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",default= "dataset/mathematics/Badges.xml", help = "input: */Badges.xml, output: */Badges.csv")
    parser.add_argument("-d", "--database", default='../database/dataset.db', help="output database")
    args = parser.parse_args()
    input_file = args.input
    database_file = args.database
    print("input file %s " % input_file)
    print("database file %s " % database_file)
    badges_processing(input_file, database_file)
