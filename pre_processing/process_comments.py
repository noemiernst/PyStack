try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
try:
    import cPickle as pickle
except ImportError:
    import pickle
import os.path
import pandas as pd
import argparse
from helper_func import sprint
import sqlite3

def comments_processing(input_file, output_file):
    print("Processing comments...")
    d = {"CommentId": [],"PostId":[],"UserId":[],"Score":[],"Text":[],"CreationDate":[]}
    comment_index = 0
    for event,elem in ET.iterparse(input_file):
            if event == "end":
                try:
                    postid = int(elem.attrib["PostId"])
                    userid = int(elem.attrib["UserId"])
                    score = int(elem.attrib["Score"])
                    creationdate = elem.attrib["CreationDate"]
                    text = elem.attrib["Text"]

                    d["Comment"].append(comment_index)
                    d["PostId"].append(postid)
                    d["UserId"].append(userid)
                    d["Score"].append(score)
                    d["CreationDate"].append(creationdate)
                    d["Text"].append(text)
                    #print elem.tag,elem.attrib
                    elem.clear()

                    comment_index +=1
                except Exception as e:
                    pass
                    #print e
    assert len(d["PostId"]) == len(d["UserId"]) and len(d["UserId"]) == len(d["Score"]) and len(d["Score"]) == len(d["CreationDate"]) and len(d["Score"]) == len(d["Text"])

    comment_dict = {}
    for comment, post, user, score, text, creation in zip(d["CommentId"], d["PostId"], d["UserId"], d["Score"], d["Text"], d["CreationDate"]):
        comment_dict[comment] = [post, user, score, text, creation]

    '''
    df = pd.DataFrame(comment_dict)

    DB = sqlite3.connect(output_file)
    df.to_sql(name='Comments', con=DB, if_exists='replace', index = False)
    DB.close()

    print("***********************************")
    print("output file: %s" % output_file)
    print("table: PostId_CommenterId")
    '''
    file_dir = os.path.dirname(os.path.abspath(input_file))
    comments_file = os.path.join(file_dir,"PostId_CommenterId_Text.pkl")

    with open(comments_file,"wb")  as f:
        pickle.dump(comment_dict,f)

if __name__ == "__main__":
    '''
    process */Comments.xml
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",default= "../dataset/mathematics/Comments.xml", help = "input: */Comments.xml, output: */Comments.csv")
    parser.add_argument("-d", "--database", default='../database/dataset.db', help="output database")
    args = parser.parse_args()
    input_file = args.input
    database_file = args.database
    print("input file %s " % input_file)
    print("database file %s " % database_file)
    comments_processing(input_file, database_file)
