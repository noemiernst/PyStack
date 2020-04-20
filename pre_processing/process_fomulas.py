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
from formula_ret import formula_ret

def process_FormulaId_QuestionId(output_dir,Formulas):
    output_file = os.path.join(output_dir,"FormulaId_PostId.csv")
    df = pd.DataFrame({"FormulaId":Formulas["FormulaId"],"PostId":Formulas["PostId"],"Body":Formulas["Body"]})
    df.to_csv(output_file,index = True, columns = ["FormulaId","PostId","Body"])

def process_formulas(dir_path):
    # Questions.pkl: A dict pickle file, key: question id, value: [question title, question body]
    with open(os.path.join(dir_path, "Questions.pkl"), "rb") as f:
        questions_dict = pickle.load(f)
    f.close()
    with open(os.path.join(dir_path, "Answers.pkl"), "rb") as f:
        answers_dict = pickle.load(f)
    f.close()

    Formulas = {}
    Formulas["FormulaId"] = []
    Formulas["PostId"] = []
    Formulas["Body"] = []

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

    for item in answers_dict.items():
        formulas, error = formula_ret(item[1])
        if not error:
            for formula in formulas:
                Formulas["FormulaId"].append(formula_index)
                Formulas["PostId"].append(item[0])
                Formulas["Body"].append(formula)
                formula_index += 1
    return Formulas

#Formulas = process_formulas("../dataset/mathematics/")
#process_FormulaId_QuestionId("../dataset/mathematics/",Formulas)
