# Evaluate accuracy, precision, recall, and F1 of smokerstatus.py
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
# from sklearn.metrics import classification_report TRY THIS LATER


# import functions
# from smokerstatus import get_gold

def evaluate_fst(gold_labels, preds):
    """
    Calculates, displays, and exports metrics of model preds compared to gold labels.

    Args:
        - gold_labels - (type dict) {patient-identifier: status, patient-identifier: status...}
        - preds - (type dict) {patient-identifier: predicted-status, ...}

    Returns:
        - prints 
        - exports .txt file
        - displays confusion matrix *** does it pop up automatically when used in script? double check
    """

    gold_patients = list(gold_labels.keys())
    gold_statuses = list(gold_labels.values())

    pred_patients = list(preds.keys())
    pred_statuses = list(preds.values())

    # check that patient lists are exactly the same
    assert gold_patients == pred_patients, 'Patient identifier lists are not identical.' 

    # check status lists are same lengths
    assert len(gold_statuses) == len(pred_statuses), 'Status lists are not identical lengths.'

    # begin calculations

# print on terminal statistics

# export statistics as text file
    # if possible, take all the incorrect instances and include in text file

    # txt file name as csvname-eval.txt