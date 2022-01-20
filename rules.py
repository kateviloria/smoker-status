# Rules as functions to classify patients
    # Functions ordered in order they should be called.


# are imports needed in every .py file?
import pandas as pd
import nltk 
from nltk import tokenize
# from nltk.corpus import stopwords

# ------------------------------

# CREATE BASELINE
smoke_words = ['smoke', 
               'smoker', 
               'smoking', 'Smoking',
               'smokes',
               'smoked', 'Smoked', 
               'ppd', 
               'nonsmoker', 'Nonsmoker',
               'tob', 'tobacco', 'cigarettes']

def baseline(all_sents):
    """
    Texts that do not have any smoke-related words will be labelled as Unknown.

    Args:
        - all_sents - list of lists where each inner list is a row text that is tokenized by word
            eg. [ ['a', 'sentence'], ['another', sentence], ...]

    Returns:
        - list of integers [2, 3, 46, 56]
        - each integer is the index of what should be labelled as Unknown in entire dataset
    """
    
    to_label_unknown = []
    
    for every_sentence_idx in range(len(all_sents)):
        
        word_list = all_sents[every_sentence_idx]
        
        # check if any of the smoke_words appear in each row text
        if any([every_smoke_word in word_list for every_smoke_word in smoke_words]) == False:
            
            to_label_unknown.append(every_sentence_idx)
    
    return to_label_unknown


# classify as UNKNOWN 
def smoker_in_household(all_sents):
    """
    Classifies patient texts with phrase 'smoker in the household' as Unknown.

    Args:
        - all_sents - list of lists where each inner list is a row text that is tokenized by word
            eg. [ ['a', 'sentence'], ['another', sentence], ...]

    Returns:
        - list of integers [2, 3, 46, 56]
        - each integer is the index of what should be labelled as Unknown in entire dataset
    """

    to_label_unknown = []
    
    for every_sentence_idx in range(len(all_sents)):
        
        word_list = all_sents[every_sentence_idx]
        
        # check if 'smoker in the household' is in sentence
            # relies on text only having 'smoker' appear once
            # no other chances of 'smoke-related' info to be mentioned
        if word_list.count('smoker') == 1:

            smoker_idx = word_list.index('smoker')
            in_idx = smoker_idx + 1
            the_idx = smoker_idx + 2
            household_idx = smoker_idx + 3

            # 'smoker', 'in', 'the', 'household' must appear in exact order in word list
            if word_list[in_idx] == 'in' and word_list[the_idx] == 'the' and word_list[household_idx] == 'household':
                to_label_unknown.append(every_sentence_idx)

        
    return to_label_unknown


# classify as NONSMOKER
def find_nonsmokers(all_sents):
    """
    Classifies patient texts as Nonsmoker:
        - if 'nonsmoker' or 'Nonsmoker' appears in text
        - 'no h/o of smoking'
        - 'does not smoke'

    Args:
        - all_sents - list of lists where each inner list is a row text that is tokenized by word
            eg. [ ['a', 'sentence'], ['another', sentence], ...]

    Returns:
        - list of integers [2, 3, 46, 56]
        - each integer is the index of what should be labelled as Unknown in entire dataset
    """
    
    nonsmoker_words = ['nonsmoker', 'Nonsmoker']
    
    to_label_nonsmoker = []
    
    for every_sentence_idx in range(len(all_sents)):
        
        word_list = all_sents[every_sentence_idx]
        
        # check if any of nonsmoker_words appear in each sentence
            # medical notes typically refer to patient
            # doesn't seem like it would be significant that a doctor mentions someone other than the patient is a nonsmoker
        if any([every_word in word_list for every_word in nonsmoker_words]) == True:
            
            to_label_nonsmoker.append(every_sentence_idx)
        
        # check if text includes 'does not drink, smoke, or do any drugs'
            # NO RULE 
            
        # check for 'no h/o smoking'
        if word_list.count('smoking') == 1:

            smoking_idx = word_list.index('smoking')
            ho_idx = smoking_idx - 1
            no_idx = smoking_idx - 2

            # 'no', 'h/o', 'smoking' must appear in exact order in word list
            if word_list[ho_idx] == 'h/o' and word_list[no_idx] == 'no':

                to_label_nonsmoker.append(every_sentence_idx)
        
        # 'does not smoke'
        if word_list.count('smoke') == 1:
            
            #if 'smoke' in word_list:
            smoke_idx = word_list.index('smoke')
            not_idx = smoke_idx - 1 
            does_idx = smoke_idx - 2

            if word_list[not_idx] == 'not' and word_list[does_idx] == 'does':

                to_label_nonsmoker.append(every_sentence_idx)

    # make sure there are no double indices   
    unique_labels_nonsmoker = list(set(to_label_nonsmoker))

    return unique_labels_nonsmoker


# classify as FORMER SMOKER

# indicator words for Former Smoker Labels
act_of_smoking = ['smoking', 'cigarettes', 'tobacco', 'tob']
smoked_NN = ['cigarette', 'cigarettes', 'cigs', 'tobacco', 'tob', 'packs', 'pack'] # unsure if packs should be included
temporal_words = ['years', 'yrs', 'months', 'weeks', 'wks', 'days'] # maybe change to time units (there are other temporal words)
approximate_words = ['under', 'over', 'around', 'approx', 'approximately','about']


def find_former_smokers(all_sents):
    """
    Classifies patient texts as Former Smoker.
        - 'quit ACT_OF_SMOKING_WORD A_NUMBER TEMPORAL_WORD ago'
        - 'quit smoking APPROXIMATE_WORD A_NUMBER TEMPORAL_WORD ago' 
        - 'quit A_NUMBER TEMPORAL_WORD ago'
        - 'former smoker' or 'Former smoker'

    Args:
        - all_sents - list of lists where each inner list is a row text that is tokenized by word
            eg. [ ['a', 'sentence'], ['another', sentence], ...]

    Returns:
        - list of integers [2, 3, 46, 56]
        - each integer is the index of what should be labelled as Unknown in entire dataset
    """

    to_label_formersmoker = []
    
    for every_sentence_idx in range(len(all_sents)):
        
        word_list = all_sents[every_sentence_idx]

        pos_tagged = nltk.pos_tag(word_list)

        # should i be using elif?
        
        # check if 'quit' or 'Quit' is in text
        if word_list.count('quit') == 1 or word_list.count('Quit') == 1:
            
            # lowercase 'quit', easier to index both since they would follow the same patterns, just appear differently sometimes
            lowercase_quit = [every_word.lower() if every_word == 'Quit' else every_word for every_word in word_list]
            
            quit_idx = lowercase_quit.index('quit')
            after_quit_idx = quit_idx + 1

            # check if 'quit ACT_OF_SMOKING_WORD A_NUMBER TEMPORAL_WORD ago'
            if word_list[after_quit_idx] in act_of_smoking and pos_tagged[after_quit_idx + 1][1] == 'CD' and word_list[after_quit_idx + 2] in temporal_words and word_list[after_quit_idx + 3] == 'ago':

                to_label_formersmoker.append(every_sentence_idx)
            
            # takes into account 'quit smoking APPROXIMATE_WORD A_NUMBER TEMPORAL_WORD ago' 
            if word_list[after_quit_idx] == 'smoking' and word_list[after_quit_idx + 1] in approximate_words and pos_tagged[after_quit_idx + 2][1] == 'CD' and word_list[after_quit_idx + 3] in temporal_words and word_list[after_quit_idx + 4] == 'ago':

                to_label_formersmoker.append(every_sentence_idx)
                
            # check for 'quit A_NUMBER TEMPORAL_WORD ago'
                # might indicate that quit something other than smoking
            if pos_tagged[after_quit_idx][1] == 'CD' and word_list[after_quit_idx + 1] in temporal_words and word_list[after_quit_idx + 2] == 'ago':

                to_label_formersmoker.append(every_sentence_idx)
        
        # search 'former smoker'
        if word_list.count('smoker') == 1:
            smoker_idx = word_list.index('smoker')
            before_smoker_idx = smoker_idx - 1
            
            # allows 'former' and 'Former'
            if word_list[before_smoker_idx].lower() == 'former':
                
                # some texts have both 'quit smoking X years ago' AND 'former smoker'
                if every_sentence_idx not in to_label_formersmoker:
                    to_label_formersmoker.append(every_sentence_idx)

    # make sure there are no double indices   
    unique_labels_former_smoker = list(set(to_label_formersmoker))

    return unique_labels_former_smoker


def smoked_past(all_sents):
    """
    Classifies patient texts as Former Smoker.
        - 'smoked SMOKED_NN for A_NUMBER TEMPORAL_WORD' 
        - 'smoked' and 'quit' must appear

    Args:
        - all_sents - list of lists where each inner list is a row text that is tokenized by word
            eg. [ ['a', 'sentence'], ['another', sentence], ...]

    Returns:
        - list of integers [2, 3, 46, 56]
        - each integer is the index of what should be labelled as Unknown in entire dataset
    """

    to_label_formersmoker = []
    
    for every_sentence_idx in range(len(all_sents)):
        
        word_list = all_sents[every_sentence_idx]

        pos_tagged = nltk.pos_tag(word_list)
    
        # 'smoked X '
        if word_list.count('smoked') == 1 or word_list.count('Smoked') == 1:
            
            # lowercase 'smoked', easier to index both since they would follow the same patterns, just appear differently sometimes
            lowercase_smoked = [every_word.lower() if every_word == 'Smoked' else every_word for every_word in word_list]
            
            smoked_idx = lowercase_smoked.index('smoked')
            after_smoked_idx = smoked_idx + 1

            # check 'smoked SMOKED_NN for A_NUMBER TEMPORAL_WORD' 
            # (added for 60 years because 'smoked' can appear in (current) Smoker as well, establishes time has passed)
            if word_list[after_smoked_idx] in smoked_NN and word_list[after_smoked_idx + 1] == 'for' and pos_tagged[after_smoked_idx + 2][1] == 'CD'and word_list[after_smoked_idx + 3] in temporal_words:
                
                to_label_formersmoker.append(every_sentence_idx)
            
            # both smoked and quit have to be in text (can lead to false positives if multiple drugs are mentioned)
            if word_list.count('quit') == 1:
            
                to_label_formersmoker.append(every_sentence_idx)


    # make sure there are no double indices   
    unique_labels_former_smoker = list(set(to_label_formersmoker))

    return unique_labels_former_smoker 

# classify as SMOKER

# indicator words for Smoker Labels
current_words = ['current', 'Current', 'currently', 'Currently', 'active', 'Active', 'actively', 'Actively', 'still', 'Still', 'reports', 'Reports']
smoking_present = ['smoking', 'smokes', 'smoke']

def find_current_smokers(all_sents):
    """
    Classifies patient texts as Smoker.
        - 'CURRENT_WORD smoker'
        - 'CURRENT_WORD smoking'
        - 'due to smoking'
        - 'SMOKING_PRESENT A_NUMBER ppd'
        - A_NUMNBER-PPD (eg. 2PPD)

    Args:
        - all_sents - list of lists where each inner list is a row text that is tokenized by word
            eg. [ ['a', 'sentence'], ['another', sentence], ...]

    Returns:
        - list of integers [2, 3, 46, 56]
        - each integer is the index of what should be labelled as Unknown in entire dataset
    """

    to_label_smoker = []
    
    for every_sentence_idx in range(len(all_sents)):
        
        word_list = all_sents[every_sentence_idx]

        pos_tagged = nltk.pos_tag(word_list)
        
        # 'CURRENT_WORD smoker'
        if 'smoker' in word_list or 'Smoker' in word_list:

            lowercase_smoker = [every_word.lower() if every_word == 'Smoker' else every_word for every_word in word_list]

            smoker_idx = lowercase_smoker.index('smoker')
                
            smoker_idx = word_list.index('smoker')
            before_smoker_idx = smoker_idx - 1
            
            if word_list[before_smoker_idx] in current_words:
                to_label_smoker.append(every_sentence_idx)
        
        # 'CURRENT_WORD smoking'
        if 'smoking' in word_list:
            smoking_idx = word_list.index('smoking')
            
            before_smoking_idx = smoking_idx - 1
            
            if word_list[before_smoking_idx] in current_words:
                to_label_smoker.append(every_sentence_idx)
                
            # 'due to smoking'
            if word_list[before_smoking_idx] == 'to' and word_list[before_smoking_idx - 1] == 'due':
                to_label_smoker.append(every_sentence_idx)
            
        # 'smokes/smoking X ppd'
            # would capture 14238 and 19217 if no asterisks wrapped around numbers
        if 'ppd' in word_list:
            ppd_idx = word_list.index('ppd')
            before_ppd_idx = ppd_idx - 1 
            
            if pos_tagged[before_ppd_idx][1] == 'CD' and word_list[before_ppd_idx - 1] in smoking_present:
                
                to_label_smoker.append(every_sentence_idx)
                
        # find A_NUMBER-PPD
            # will not find any cases in dataset, but thought would be useful
            # if PPD have other meanings, would also need to check for SMOKE_RELATED words 
        if [True for every_word in word_list if every_word.endswith("PPD")] == [True]:
            
            # check if split its CD and NN
            word_PPD = [every_word for every_word in word_list if every_word.endswith('PPD')]

            ppd_idx = word_list.index(word_PPD[0])
            ppd_original = word_list[ppd_idx]
            
            # slicing string to make sure it's not just a word ending in PPD 
            ppd = ppd_original[-3:] # PPD in string
            before_ppd = ppd_original[:-3] # whatever comes before PPD
            
            new_ppd = [before_ppd, ppd] # list of strings to pos-tag
            postagged_new_ppd = nltk.pos_tag(new_ppd) # list of tuples [(word, POS), (word, POS)]
            
            # check if POS-tags are correct
            if postagged_new_ppd[0][1] == 'CD' and postagged_new_ppd[1][1] == 'NN':
                
                if word_list[ppd_idx - 1] in smoking_present:
                    to_label_smoker.append(every_sentence_idx)
            
                
    # make sure there are no double indices   
    unique_labels_smoker = list(set(to_label_smoker))

    return unique_labels_smoker
    
# HELPER FUNCTION TO PREVENT DOUBLE LABELS
def no_doubles(first_list, second_list): 
    
    """
    If a text is given two labels, the label that was given first is what is kept.

    Args:
        - first_list - list of indices
        - second_list - list of indices

    Returns:
        - tuple with two lists (doubles removed from the second list)
    """
    
    intersection = [every_index for every_index in first_list if every_index in second_list]
    
    # if there are doubles
    if len(intersection) > 0:
        
        # accounts for if there are more than one
        for every_double in intersection: 
            
            # remove from second list, keep in the first
            second_list.remove(every_double)
            
    return first_list, second_list

# HELPER FUNCTION TO REPLACE LABELS INITIALISED
def make_final_labels(init_list, index_list, str_label):
    
    for every_index in index_list:
        init_list[every_index] = str_label
    
    return init_list
