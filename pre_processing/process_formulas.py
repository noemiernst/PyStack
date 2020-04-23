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
import sqlite3
from pre_processing.formula_ret import formula_ret
import timeit
import argparse


def formula_processing(dir_path, database):
    # Questions.pkl: A dict pickle file, key: question id, value: [question title, question body]
    with open(os.path.join(dir_path, "Questions.pkl"), "rb") as f:
        questions_dict = pickle.load(f)
    f.close()
    with open(os.path.join(dir_path, "Answers.pkl"), "rb") as f:
        answers_dict = pickle.load(f)
    f.close()

    Formulas = {"FormulaId": [], "PostId": [], "Body":[]}

    total_posts = len(questions_dict) + len(answers_dict)
    print("Total number of posts: ", total_posts)
    print("Questions: ", len(questions_dict), "  Answers: ", len(answers_dict))

    formula_index = 0
    for item in questions_dict.items():

        formulas_title, error_title = formula_ret(item[1][0])
        formulas_body, error_body = formula_ret(item[1][1])
        # parsing errors occur (total of ~6500) do not take formulas from "invalid" texts
        if not error_title and not error_body:
            for formula in formulas_title:
                Formulas["FormulaId"].append(formula_index)
                Formulas["PostId"].append(item[0])
                Formulas["Body"].append(formula)
                formula_index += 1
            for formula in formulas_body:
                Formulas["FormulaId"].append(formula_index)
                Formulas["PostId"].append(item[0])
                Formulas["Body"].append(formula)
                formula_index += 1

    df = pd.DataFrame({"FormulaId":Formulas["FormulaId"],"PostId":Formulas["PostId"],"Body":Formulas["Body"]})
    DB = sqlite3.connect(database)
    df.to_sql(name='Formulas_Posts', con=DB, if_exists='replace', index = False)
    DB.close()
    print("***********************************")
    print("output file: %s" % database)
    print("table: Formulas_Posts")

    with open(os.path.join(dir_path,"PostId_CommenterId_Text.pkl"), "rb") as f:
        comment_dict = pickle.load(f)
    f.close()

    Formulas = {"FormulaId": [], "CommentId": [], "Body":[]}

    print("Total number of comments: ", len(comment_dict))

    for item in comment_dict.items():
        formulas, error = formula_ret(item[1][3])
        if not error:
            for formula in formulas:
                Formulas["FormulaId"].append(formula_index)
                Formulas["CommentId"].append(item[0])
                Formulas["Body"].append(formula)
                formula_index += 1

    df = pd.DataFrame({"FormulaId":Formulas["FormulaId"],"CommentId":Formulas["CommentId"],"Body":Formulas["Body"]})
    DB = sqlite3.connect(database)
    df.to_sql(name='Formulas_Comments', con=DB, if_exists='replace', index = False)
    DB.close()
    print("table: Formulas")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default="../dataset/mathematics/",
                        help="input: */Questions.pkl */Answers.pkl")
    parser.add_argument("-d", "--database", default='../database/dataset.db', help="output database")
    args = parser.parse_args()
    input_file = args.input
    print("processing input file %s " % input_file)
    formula_processing(input_file, args.database)
