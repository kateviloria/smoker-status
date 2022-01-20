# parses through medical notes and classifies patient status (Smoker, Former Smoker, Nonsmoker, Unknown)


# imports
import argparse
import pandas as pd
import os

# import functions
from rules import baseline, smoker_in_household, find_nonsmokers, find_former_smokers, smoked_past, find_current_smokers, no_doubles, make_final_labels
from eval import evaluate, get_wrong_labels

eval_output_dir = 'eval-output'

# keep an open data function in case different formats are given in the future?
    # left for file conversion etc. 
def open_data(data_csv):

    data_df = pd.read_csv(data_csv)

    return data_df


def classify_patients(smoker_data_df):
    """
    Calls functions from rules.py to classify each patient's smoking status.

    Args:
        - smoker_data_df - pandas dataframe (row_id/patient identifier, status, text)

    Returns:
        - list of tuples [(indentifier, pred_label), (an_identifier, pred_label), ...]
    """

    identifiers = smoker_data_df['row_id'].to_list()
    statuses = smoker_data_df['status'].to_list()
    med_notes = smoker_data_df['text'].to_list()

    # check row numbers
    assert len(identifiers) == len(statuses) == len(med_notes), 'Three columns are not the same lengths.'


    # ---- GENERAL DATA PREP ---- 
    # tokenize/split each row text into words eg. ['a', 'word', 'another', 'more'...]
    split_words = [nltk.word_tokenize(every_text)for every_text in med_notes] 

    # ---- PUT THROUGH RULES FUNCTIONS ----
    unknown_labels_from_baseline = baseline(split_words)
    unknown_labels_smoker_in_household = smoker_in_household(split_words)
    # amalgamate unknown labels
    unknown_labels = unknown_labels_from_baseline + unknown_labels_smoker_in_household

    nonsmoker_labels = find_nonsmokers(split_words) 

    former_smoker_labels = find_former_smokers(split_words)
    former_smoker_labels_past = smoked_past(split_words)
    # amalgamate former smoker labels
    formersmoker_labels = former_smoker_labels + former_smoker_labels_past 

    smoker_labels = find_current_smokers(split_words)

    # ---- CHECK FOR LABEL OVERLAPS ----
    unknown_labels_unique, nonsmoker_labels_unique = no_doubles(unknown_labels, nonsmoker_labels)
    nonsmoker_labels_unique, formersmoker_labels_unique = no_doubles(nonsmoker_labels_unique, formersmoker_labels)
    formersmoker_labels_unique, smoker_labels_unique = no_doubles(formersmoker_labels_unique, smoker_labels)

    # ---- FINALISE LABELS ----
    data_length = len(identifiers)

    # initialise list of labels with all 'Unknown' labels
    final_labels = ['Unknown'] * data_length 

    nonsmoker_added = (final_labels, nonsmoker_labels_unique, 'Nonsmoker')
    formersmoker_added = (nonsmoker_added, formersmoker_labels_unique, 'Former Smoker')
    smoker_added = (formersmoker_added, smoker_labels_unique, 'Smoker')

    # zip preds with identifiers
    identifier_preds = list(zip(identifiers, smoker_added))

    return identifier_preds


def export_preds(pred_labels, datacsv):
    """
    Takes label preds and exports as .csv.

    Args:
        - pred_labels - list of tuples where each tuple is (identifier, label)
        - datacsv - name of source .csv of data

    Returns:
        - dictionary where key is patient identifier and value is predicted smoking status
            eg. {23456: 'Nonsmoker', 34256: 'Unknown', ... }
    """

    # export to csv
    preds_df = pd.DataFrame(pred_labels, columns=['row_id','smoking_status'])

    data_name = datacsv[:-4]
    preds_path = os.path.join(eval_output_dir, data_name, '-preds.csv')
    preds_df.to_csv(preds_path, index=False)

    # makes two lists, identifiers and label predictions
    identifiers, preds = map(list, zip(*pred_labels))

    # converts to dictionary, prepare for eval.py
    identifier_label_dict = dict(zip(identifiers, preds))

    return identifier_label_dict


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

    # open file
    data_df = open_data(data)
    
    # classify
    print('Classifying data...')
    preds = classify_patients(data_df)
    preds_dict = export_preds(preds, data)
    
    # eval 
    print('Evaluating...')
    gold_labels = get_gold(data)
    evaluate(gold_labels, preds_dict, data)
    get_wrong_labels(gold_labels, preds_dict, data)

    print('Evaluation finished!')

