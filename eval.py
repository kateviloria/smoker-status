# Evaluate accuracy, precision, recall, and F1 of smokerstatus.py

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from sklearn.metrics import balanced_accuracy_score 

import pandas as pd
import os


# import functions
# from smokerstatus import get_gold

# export statistics as text file
    # if possible, take all the incorrect instances and include in text file

    # txt file name as csvname-eval.txt

eval_output_dir = 'eval-output'

def evaluate(gold_labels, preds, datacsv):
    """
    Calculates, displays, and exports metrics of model preds compared to gold labels.

    Args:
        - gold_labels - (type dict) {patient-identifier: status, patient-identifier: status...}
        - preds - (type dict) {patient-identifier: predicted-status, ...}
        - datacsv - name of source .csv file 


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

    # --- begin calculations ---

    # confusion matrix
    cm = confusion_matrix(gold_statuses, pred_statuses)

    disp = ConfusionMatrixDisplay(confusion_matrix = cm, 
                    display_labels = ['Former', 'Non', 'Smoker', 'Unknown'])
    disp.plot(cmap="YlOrRd") # GDK ERROR? 

    # save confusion matrix
    data_name = datacsv[:-4]

    fig_name = data_name + '-cm.png'
    cm_path = os.path.join(eval_output_dir, fig_name)
    #cm_path = data_name + '-cm.png'
    plt.savefig(cm_path)

    # classification report - precision, recall, F1, support (# of samples for each class)
    label_names = ['Former Smoker', 'Non Smoker', 'Smoker', 'Unknown'] # alphabetised 

    class_report = classification_report(gold_statuses, pred_statuses, target_names = label_names)
    print('Classification Report')
    print(class_report)
    
    # for exporting class report to .csv
    class_report_dict = classification_report(gold_statuses, pred_statuses, 
                                     target_names = label_names,
                                     output_dict = True)
    classreport_df = pd.DataFrame.from_dict(class_report_dict).transpose()

    # trying to send to dir instead
    report_name = data_name + '-classreport.csv'
    cr_path = os.path.join(eval_output_dir, report_name)

    # cr_path = data_name + '-classreport.csv'
    classreport_df.to_csv(cr_path, index=False)

    print('Exported classification report to ', cr_path)

    # accuracy (normalize = True --> fraction of correctly classified samples, 
        # vs False -->  number of correctly classified samples)
    # accuracy = accuracy_score(gold_statuses, pred_statuses)

    # balanced accuracy score
        # average of recall obtained on each class
        # ** is this appropriate? think about this 
    # balanced_accuracy = balanced_accuracy_score(gold_statuses, pred_statuses)
      
    # precision
        # true positives / (true positives + false positives)
        # ability not to label as positive a sample that is negative
        # micro: globally --> total true positives, false negatives, and false positives
        # macro: each label --> unweighted mean (doesn't consider label imbalance)
        # weighted: metrics for each label, average weighted by support 
        #       --> F-score not btwn precision&recall
    # precision = precision_score(gold_statuses, pred_statuses, average=None)

    # recall

    # F1

# print all wrong instances in .csv
    # gold, pred, identifier

def get_wrong_labels(gold_labels, preds, datacsv):
    """
    Identify instances that are labelled wrong and what they were labelled. 

    Args:
        - gold_labels - (type dict) {patient-identifier: status, patient-identifier: status...}
        - preds - (type dict) {patient-identifier: predicted-status, ...}
        - datacsv - dataname
    
    Returns:
        - exports .csv file (gold, predicted, identifier/row_id)
    """

    incorrectly_labelled = []

    for identifier in gold_labels.keys():

        truth = gold_labels[identifier]
        pred = preds[identifier]

        # if wrong prediction
        if truth != pred:
            row = (truth, pred, identifier)
            incorrectly_labelled.append(row)
    
    wrong_labels_df = pd.DataFrame(incorrectly_labelled, columns = ['gold', 'predicted', 'identifier'])

    # export to csv file
    data_name = datacsv[:-4]
    wrong_labels_name = data_name + '-wronglabels.csv'

    wrong_labels_path = os.path.join(eval_output_dir, wrong_labels_name)
    wrong_labels_df.to_csv(wrong_labels_path, index=False)
    
    print('Incorrectly Labelled Entities (truth, pred, row_id)')
    print(*incorrectly_labelled, sep="\n")




