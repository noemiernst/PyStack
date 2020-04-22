try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import os.path
import pandas as pd
import argparse
import sqlite3

def bounty_processing(input_file, output_file):
    d = {"PostId":[],"BountyAmount":[]}
    for event,elem in ET.iterparse(input_file):
            if event == "end":
                try:
                    if "BountyAmount" in elem.attrib:
                        postid = int(elem.attrib["PostId"])
                        bounty = int(elem.attrib["BountyAmount"])
                        d["PostId"].append(postid)
                        d["BountyAmount"].append(bounty)
                    #print elem.tag,elem.attrib
                    elem.clear()
                except Exception as e:
                    pass
                    #print e

    answerid_questionid_file = os.path.join(os.path.dirname(input_file),"AnswerId_QuestionId.csv")
    answerid_questionid = pd.read_csv(answerid_questionid_file)

    question_bounty = {"QuestionId":[],"Bounty":[]}
    for postid,bounty in zip(d["PostId"],d["BountyAmount"]):
        if answerid_questionid[answerid_questionid["QuestionId"] == postid].index.tolist():
            question_bounty["QuestionId"].append(postid)
            question_bounty["Bounty"].append(bounty)

    df = pd.DataFrame(question_bounty)
    DB = sqlite3.connect(output_file)
    df.to_sql(name='QuestionId_BountyId', con=DB, if_exists='replace', index = False)
    DB.close()

if __name__ == "__main__":
    '''
    process */Votes.xml
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",default= "../dataset/mathematics/Votes.xml", help = "input: */Votes.xml, output: */QuestionId_Bounty.csv")
    parser.add_argument("-d", "--database", default='../database/dataset.db', help="output database")
    args = parser.parse_args()
    input_file = args.input
    database_file = args.database
    print("input file %s " % input_file)
    print("database file %s " % database_file)
    bounty_processing(input_file, database_file)

