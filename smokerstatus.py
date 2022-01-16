# parses through medical notes and classifies patient status (Smoker, Former Smoker, Nonsmoker, Unknown)


# imports
import argparse
import pandas as pd

# eval
from eval import evaluate_fst, get_wrong_labels


def classify_patients(data_csv):

    smoker_data_df = pd.read_csv(data)

    print('in the func now')
    print(smoker_data_df)

def get_preds():

# export preds to csv (two rows, row_id + status)
    # name file datacsvname-preds.csv

# ----- evaluate ----

def get_gold(datacsv):
    """
    Gets gold labels.

    Args:
        datacsv - data in .csv format (must have columns: row_id, status)

    Returns:
        A dictionary where each key is patient-identifier/row_id (type int) and its value 
        is the patient's smoker status (Smoker, Former Smoker, Non Smoker, Unknown) (type str).
            {patient: status, patient2: status, patient3: status...}
    """

    smoker_data_df = pd.read_csv(datacsv)

    # dict, {patient identifier/row_id: status, patient2: status...}
    smoker_gold =  dict(zip(smoker_data_df.row_id, smoker_data_df.status))

    return smoker_gold



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify patient smoker status.")
    parser.add_argument("csvfile", type=str, help="Name of .csv file with data.")

    args = parser.parse_args()

    data = args.csvfile
    
    # classify
    classify_patients(data)

    # preds (format of preds should also be dict)

    print('done in main')
    
    # eval 
    gold_labels = get_gold(data)

    # evaluate_fst(gold_labels, preds, data)
    # get_wrong_labels(gold_labels, preds, data)

    print('Evaluation finished.')

