# Evaluate accuracy, precision, recall, and F1 of smokerstatus.py
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
# from sklearn.metrics import classification_report TRY THIS LATER


# import functions
# from smokerstatus import get_gold

def evaluate_fst(gold_labels, preds, datacsv):
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

    # --- begin calculations ---

    # accuracy (normalize = True --> fraction of correctly classified samples, 
    #   vs False -->  number of correctly classified samples)
    accuracy = accuracy_score(gold_statuses, pred_statuses)

    # balanced accuracy score
        # average of recall obtained on each class
        # ** is this appropriate? think about this 
    # balanced_accuracy = balanced_accuracy_score(gold_statuses, pred_statuses)

    # confusion matrix
    cm = confusion_matrix(gold_statuses, pred_statuses)

    disp = ConfusionMatrixDisplay(confusion_matrix = cm, 
                    display_labels = ['Former', 'Non', 'Smoker', 'Unknown'])
    disp.plot() # necessary?

    data_name = datacsv[:-4]
    cm_path = data + '-cm.png'
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
    cr_path = data + '-classreport.csv'
    classreport_df.to_csv(cr_path, index=False)


    # precision
        # true positives / (true positives + false positives)
        # ability not to label as positive a sample that is negative
    # precision = precision_score(gold_statuses, pred_statuses, average=None)

    # recall

    # F1

# print on terminal statistics

# export statistics as text file
    # if possible, take all the incorrect instances and include in text file

    # txt file name as csvname-eval.txt

# print all wrong instances in .csv
    # gold, pred, identifier
