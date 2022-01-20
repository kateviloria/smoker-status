# smoker-status

__How To Run:__  
```bash
python smokerstatus.py smoker_status.csv
python smokerstatus.py [DATA CSV FILENAME]
```  

### Rules Summary
###### in order of implementation, further explanations and cases possibly missed or mislabelled commented in functions in `rules.py`
- **Unknown**
    - baseline - any texts with no "smoke-related" words
    - 'smoker in the household'
- **Non Smoker**
    - if 'nonsmoker' or 'Nonsmoker' appears in text
    - 'no h/o of smoking'
    - 'does not smoke'
- **Former Smoker**
    - 'quit ACT_OF_SMOKING_WORD A_NUMBER TEMPORAL_WORD ago'
    - 'quit smoking APPROXIMATE_WORD A_NUMBER TEMPORAL_WORD ago' 
    - 'quit A_NUMBER TEMPORAL_WORD ago'
    - 'former smoker' or 'Former smoker'
    - 'smoked SMOKED_NN for A_NUMBER TEMPORAL_WORD' 
    - 'smoked' and 'quit' must appear
- **Smoker**
    - 'CURRENT_WORD smoker'
    - 'CURRENT_WORD smoking'
    - 'due to smoking'
    - 'SMOKING_PRESENT A_NUMBER ppd'
    - 'A_NUMNBER-PPD' (eg. 2PPD)
    
#### Indicator Words
```
smoke_words = ['smoke', 'smoker', 'smoking', 'Smoking', 'smokes', 'smoked', 'Smoked', 
'ppd', 'nonsmoker', 'Nonsmoker','tob', 'tobacco', 'cigarettes']

act_of_smoking = ['smoking', 'cigarettes', 'tobacco', 'tob']
smoked_NN = ['cigarette', 'cigarettes', 'cigs', 'tobacco', 'tob', 'packs', 'pack'] 
temporal_words = ['years', 'yrs', 'months', 'weeks', 'wks', 'days'] 
approximate_words = ['under', 'over', 'around', 'approx', 'approximately','about']

current_words = ['current', 'Current', 'currently', 'Currently', 'active', 'Active', 'actively', 
'Actively', 'still', 'Still', 'reports', 'Reports']
smoking_present = ['smoking', 'smokes', 'smoke']
```

-----
### Overall Evaluation
![Classifier Confusion Matrix](https://github.com/kateviloria/smoker-status/blob/main/eval-output/smoker_status-cm.png)
- aimed for a higher precision, in a healthcare domain, I thought it would be more useful to end up with an 'Unknown' if unsure to flag someone that it must be double checked (of course in a larger scale, it also presents a different kind of risk)
- although in this case, it's not ideal since there is a significant amount of 'Unknown' labels (40/70, more than half)
----

### Design Decisions
- **split text into sentences immediately**
    - would be useful, but majority of texts are not full sentences (medical notes format), some would end up with one long sentence and the rest which are in sentence format are only one sentence (in a bigger dataset, this might just take up computational time and energy)
- **tokenizer**
    - great way to filter texts that have no information regarding smoker status (label as unknown immediately)
    - splitting texts in words, very useful for labels/smoker-statuses that have a key word that directly indicates what the patient's smoker status is (unknown and nonsmoker)
- **stop words**
    - since texts being used are medical notes, stop words provide a lot of meaning for shorter sentences (eg. pronouns, 'is' and its other conjugations, 'have' and its other conjugations, approximate words, words regarding time)  
- **dependency parsing**
    - not that great for medical notes format
    - mostly thought it would be useful for texts with negation
    - 'Does not drink, smoke, or do any drugs.' (row_id 26743) - with spaCy's dependency parser, the negation's head is only drink, difficult to pick up that both 'smoke' and 'do any drugs' are included in negation ([Image Below](https://explosion.ai/demos/displacy?text=Does%20not%20drink%2C%20smoke%2C%20or%20do%20any%20drugs.&model=en_core_web_sm&cpu=1&cph=1))
![SpaCy Dependency Parsing](https://github.com/kateviloria/smoker-status/blob/main/images/dep-labels.png)
- **constituency parsing**
    - looks more promising compared to dependencies
    - 'Does not drink, smoke, or do any drugs.' (row_id 26743) - CoreNLP/Stanza parses it where mother node is sister to 'does not' in tree, captures negation of 'drink', 'smoke', *and* 'do any drugs', need to figure out how to implement this! ([Image Below](https://corenlp.run/))
![CoreNLP Constituency Parsing](https://github.com/kateviloria/smoker-status/blob/main/images/constituency-labels.png)

- **rules and processing order**
    - baseline - any texts that have no "smoke-related" rules are immediately labelled as Unknown (17708 labelled as Former Smoker but no information indicating so, at least for a program)
    - started with more definitive rules with clearer patterns (eg. Non Smoker labels)
    - started differentiating Former Smoker and Smoker (where I found Former Smoker to have clearer/"easier" patterns to handle")
    - specific phrases to search for typically considered if it would appear in a larger dataset (is it a common saying? is it something that will be regularly used/said by doctors?)

- **most difficult label: smoker**
    - considered implementing a rule that if it didn't have a label yet and it includes 'smoking', 'smoker', 'smoke' (more "present" words) to label as Smoker, but opted against it to preserve precision

----
### Edge Cases
- any time a text speaks about smoking another substance
- 34464 - have both 'current smoker' and 'married current smoker'
- ppd rule won't work with the ** around numbers, if corrected should work
- Former Smoker: 'quit A_NUMBER TEMPORAL_WORD ago' - might have quit another drug

----
### Concerns & Things To Refine
- smoke-related word as an indicator of smoke status only appearing once
    - some rules rely on a smoke-related word appearing only once (thought it would be okay for now since medical notes are meant to be concise and terse), especially the code/rules that find exact phrases 
    - Unknown rule relies on finding "smoker in the household" where "smoker" is only used once
- merging ppd and PPD rules
- building an FST pipeline based on rules written to have an elimination process of labels by states instead of double checking labels for doubles at the end
- negation
    - Nonsmoker: 'does not smoke' (in a manner that isn't hard-coded), 'no h/o smoking', 'does not drink, smoke, or do any drugs'
- how are words which are wrapped in asterisks ** handled, if they are around information that's needed for analysis, should it be ignored (on non-existent dates I understand that it's probably treated as incorrect/not viable)
- identifying the recommendation to quit smoking as Smoker 
    - "do not start smoking again" as Former Smoker

### Future Ideas
- how to separate medical notes based on headings
    - anything before ':' is a category and anything after is its contents?
- **negation** (especially when used in a list)
    - [this method](https://medium.com/@MansiKukreja/clinical-text-negation-handling-using-negspacy-and-scispacy-233ce69ab2ac) looks promising, leaning towards something to implement especially for larger datasets, did not implement due to time restrictions and prioritised as an edge case for dataset given
    - however, it is definitely a case that will appear again with a larger dataset
- SVM classifier implementation
- using word vectors and vector calculations
- explore using 'Social History' in medical notes as indicator for smoke status

#### Texts That are Incorrectly Labelled
- 5377, Smoker: We recommend that you work closely with your doctor to quit smoking to help preserve your lung function and reduce your risk for further COPD exacerbation.
- 46361, Smoker: He restarted smoke 3 weeks ago.
- 12798, Smoker: 30pk-yr smoking, current. Drinks 2-3 per night.
- 10377, Smoker: Admission Date:  **2116-2-6**              Discharge Date:   **2116-2-12**  Date of Birth:  **2076-11-17**             Sex:   M  Service: MEDICINE  Allergies: Penicillins  Attending:**First Name3 (LF) 1253** Chief Complaint: shortness of Breath  Major Surgical or Invasive Procedure: none  History of Present Illness: 39 M smoker, no PMH p/w several days of fever, cough, sore throat, found to have bilateral pneumonia and hypoxia.
- 34014, Smoker: She smoked up until current admission.
- 14238, Smoker: Past Medical History: post-traumatic vertigo depression End stage liver disease secondary to alcohol cirrhosis w/ ascites onset **4-/2166** elevated ferritin level umbilical hernia hepatic encephalopathy hepatic coma DT GI bleeding lung mass followed on lung CT chronic tob abusedisorder chronic pancreatitis   Social History: lives alone, no drink since **4-13**, smoke **2-11** ppd   Family History: father died of cirrhosis  Physical Exam: On admission to MICU: PE:  T 97.4, HR 67, BP 95/47 in dopamine 5mcg/kg/m, RR 14, O2 sat 99% 3L/m  Gen: jaundiced man lying flat in bed, speaking in full sentences in NAD  HEENT: icteric, EOMI w/ lateral nystagmus B, PERRL, OP clear w/ dry MM, JVP 8cm  CV: reg s1/s2, no s3/s4/m/r  Pulm: crackles at bases B, no wheezes  Abd: +BS, soft, NT, moderately distended, no fluid wave  Ext: cool feet, 2+ DP B, 1+ pitting edema to ankles B  Neuro: a/o x 3, CN 2-12 intact, no asterixis, strength 5/5 throghout UE/LE B, sensation to fine touch intact throughout except decreased over L ant tibia  Pertinent Results: **2176-12-18** 05:52PM   LACTATE-2.9*
- 17708, Former Smoker: #NAME?
- 20403, Smoker: The patient had been smoking crack for three days prior to admission.
- 7256, Former Smoker: Former pipe and cigar smoker.
- 46701, Former Smoker: Quit smoking '**82** (smoked for 20 years)  Family History: Father: MI **47**'s, sister had CABG  Physical Exam: Vitals T 97.8  HR 60  BP 120/76 sO2 95% RA  RR 18  FSBS 102 i/o: 190/500(shift) General: NAD HEENT: mmm; no icterus Neck: no bruits over carotids; no LAD; no JVD, supple Cor: S1, S2, regular, no murmurs Pulm: CTA bilaterally Abd: soft, nt, nd, nl bs Extr: no edema, warm  Neurological exam: Mental status: awake, alert, oriented to person, time and place.
- 49089, Smoker: Smoking causes narrowing of your blood vessels which in turn decreases circulation.
- 24790, Smoker: At the present time, she says she smokes about five cigarettes per day.
- 33349, Former Smoker: Pt quit smoking **2147-5-29**, was smoking 1/3ppd.
- 50867, Former Smoker: Past Medical History: 1)Hypertension 2)COPD on 2L at home 3)Bronchiectasis 4)MRSA pneumonia 5)Myofascial pain syndrome 6)GERD 7)s/p hiatal hernia repair 8)s/p TAH 9)Right angioplasty and stenting of Right popliteal and superfical femoral artery **4-16** 10)Osteoarthritis 11)Sciatica 12)Peripheral vascular disease 13)Hysterectomy 14)Colonic adenoma found in **2136** 15)Cystogram for hematuria - **2124**  Social History: - + Smoking: smoked for approx. seven years during her 20s about **12-12** pack/day.
- 52244, Former Smoker: + tob: cigar/pipe smoking, daily x20-25 years w/cessation 20yrs prior - EtOH - Illicit/Recreational drug use   Family History: Daughter with MI in mid-40s, had Type 1 DM, deceased 56y/o Brother w/heart disease, ?MI.
- 15564, Former Smoker: He does have a history of alcohol abuse and is a former cigarette smoker.
- 12663, Smoker: She has smoked one pack per day for 15 years and drinks approximately two drinks per night of alcohol.
- 26743, Non Smoker: Does not drink, smoke, or do any drugs.
- 50129, Smoker: SOCIAL HISTORY:  The patient smokes one pack per day and has a prior history of alcohol abuse.  LABORATORY DATA:  Chest x-ray showed stable cardiomegaly with increased congestive heart failure and increased left effusion; ill-defined lucency along the left upper mediastinum, possibly representing air in distended esophagus, however, mediastinal air collection could not be ruled out; recommend follow-up study.
- 35305, Former Smoker: He has less than 10-pack-year smoking history; however, he did smoke a pipe on a daily basis up until **2145**.
- 20173, Smoker: SOCIAL HISTORY:   The patient smokes half to one pack per day.
- 45881, Smoker: # Diastolic CHF, EF **2204** 55% # Hypertension # Hyperlipidemia # Hypothyroidism secondary to RAI for **Doctor Last Name 933** Disease # Depression with psychosis/ bipolar disorder # Discoid Lupus # PTSD # Carcinoid s/p resection in **2173** # COPD w/ admissions for acute exacerbations (**8-1** PFTs FEV1 51%pred, FVC 51%pred, DSB(Hb) 56%pred) # s/p TAH and b/l BOS # Hemolytic Anemia # Migraine # T9/T10 Disc Herniation # Right hip arthritis # obstructive sleep apnea (not on CPAP)   Social History: Per notes, smokes a pack per day, no alcohol or ilicit drug use.
- 23216, Smoker: The patient is a smoker- has smoked for 55 years 1 **11-23** ppd, now down to 1/2 ppd.
- 20796, Former Smoker: >60pk yr smoking quit ~25 yrs ago.
- 58482, Former Smoker: - **2145-1-22** cycle 2 IVAC   Social History: Smoked 1ppd x five years around age 30, does not drink or use drugs, lives with wife and 2 grown children live nearby, worked as a limo driver   Family History: Sister with **Name2 (NI) ** cancer, sister with bilateral breast cancer, brother with unspecified cancer, heart disease in father.
- 29654, Smoker: Admission Date:  **2127-1-13**              Discharge Date:   **2127-1-16**  Date of Birth:  **2070-1-31**             Sex:   M  Service: MEDICINE  Allergies: Iodine  Attending:**First Name3 (LF) 1145** Chief Complaint: Chest pain  Major Surgical or Invasive Procedure: cardiac catheterization s/p RCA cypher stent   History of Present Illness: 56yo M with GERD, smoker and pos alcohol p/w chest pain at 1:30 AM.
- 47290, Former Smoker: Quit smoking in **2098-7-22**.
- 43336, Smoker: Admission Date:  **2104-3-15**       Discharge Date:  **2104-3-20**  Date of Birth:   **2057-6-30**       Sex:  M  Service:  HISTORY OF PRESENT ILLNESS:  Mr. **Known lastname 46763** is a 46-year-old smoker with positive family history of coronary artery disease who presented to **Hospital ** Hospital complaining of 18 hours of chest pain intermittent accompanied by nausea and shortness of breath.
- 19217, Smoker: He smokes occasionally, **1-9** cigarettes a month, but has a 20 year history of smoking **1-9** ppd.
- 37035, Smoker: Patient being discharged on maximal COPD regimen including advair inhaler, combivent QID and advise to quit smoking.
- 13777, Former Smoker: It is crucial for your breathing and your heart that you do not start smoking again.

#### Files Summary
- `data-exploration.ipynb` - manually looking at data, initial ideas and thoughts
- `scratch.ipynb` - small tests before plugging in to script
- `text-processing-and-rules.ipynb` - writing rules and function tests
- `smokerstatus.py` - main script
- `rules.py` - rules for classification and helper functions
- `eval.py` - evaluation (exports classification report, confusion matrix, and incorrectly labelled data)

#### Imports
- argparse
- pandas 
- os
- nltk
- sklearn.metrics
- matplotlib

#### References 
- on [Multi-label Model Evaluation](https://www.kaggle.com/kmkarakaya/multi-label-model-evaluation)
- on [Multi-Class Metrics](https://towardsdatascience.com/multi-class-metrics-made-simple-part-i-precision-and-recall-9250280bddc2), [PT.II](https://towardsdatascience.com/multi-class-metrics-made-simple-part-ii-the-f1-score-ebe8b2c2ca1)
- [sklearn Metrics and Scoring](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)
- Bae, Y. S., Kim, K. H., Kim, H. K., Choi, S. W., Ko, T., Seo, H. H., Lee, H.-Y., &amp; Jeon, H. (2021). [Keyword extraction algorithm for classifying smoking status from unstructured bilingual electronic health records based on Natural Language Processing](https://doi.org/10.3390/app11198812). Applied Sciences, 11(19), 8812. 
- Jonnagaddala, J., Dai, H.-J., Ray, P., &amp; Liaw, S.-T. (2015). [A preliminary study on automatic identification of patient smoking status in unstructured electronic health records](https://doi.org/10.18653/v1/w15-3818). Proceedings of BioNLP 15.
- Bui, D. D., &amp; Zeng-Treitler, Q. (2014). [Learning regular expressions for clinical text classification](https://doi.org/10.1136/amiajnl-2013-002411). Journal of the American Medical Informatics Association, 21(5), 850–857. 
- FST tutorials ([1](https://python-course.eu/applications-python/finite-state-machine.php), [2](https://martin-thoma.com/how-to-draw-a-finite-state-machine/))
- [SpaCY Dependency Parser and Visualizer](https://explosion.ai/demos/displacy?text=Does%20not%20drink%2C%20smoke%2C%20or%20do%20any%20drugs.&model=en_core_web_sm&cpu=1&cph=1)
- [CoreNLP Constituency Parser](https://corenlp.run/)
- [Penn Treebank POS-tags](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)
