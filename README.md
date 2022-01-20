# smoker-status



#### Design Decisions
- **split text into sentences immediately**
    - would be useful, but majority of texts are not full sentences (medical notes format), some would end up with one long sentence and the rest which are in sentence format are only one sentence (in a bigger dataset, this might just take up computational time and energy)
- **tokenizer**
    - great way to filter texts that have no information regarding smoker status (label as unknown immediately)
    - splitting texts in words, very useful for labels/smoker-statuses that have a key word that directly indicates what the patient's smoker status is (unknown and nonsmoker)
- **stop words**
    - since texts being used are medical notes, stop words provide a lot of meaning for shorter sentences (eg. pronouns, 'is' and its other conjugations, 'have' and its other conjugations, temporal words,  
- **dependency parsing**
    - not that great for medical notes format
    - mostly thought it would be useful for texts with negation
    - 'Does not drink, smoke, or do any drugs.' (row_id 26743) - with spacy's dependency parser, the negation's head is only drink, difficult to pick up that both 'smoke' and 'do any drugs' are included in negation ([Image Below](https://explosion.ai/demos/displacy?text=Does%20not%20drink%2C%20smoke%2C%20or%20do%20any%20drugs.&model=en_core_web_sm&cpu=1&cph=1))
![dependencyscreenshot](screenshot.png)

- **constituency parsing**
    - 'Does not drink, smoke, or do any drugs.' (row_id 26743) - CoreNLP/Stanza parses it where mother node is sister to 'does not' in tree, captures negation 'drink', 'smoke', and 'do any drugs', need to figure out how to implement this!


#### Concerns & Future Ideas
- how to separate medical notes based on headings
    - anything before ':' is a category and anything after is its contents?
- **negation** (especially when used in a list)
    - [this method](https://medium.com/@MansiKukreja/clinical-text-negation-handling-using-negspacy-and-scispacy-233ce69ab2ac) looks promising, leaning towards something to implement especially for larger datasets, did not implement due to time restrictions and prioritised as an edge case for dataset given
    - however, it is definitely a case that will appear again with a larger dataset
- smoke-related word as an indicator of smoke status only appearing once
    - some rules rely on a smoke-related word appearing only once (thought it would be okay for now since medical notes are meant to be concise and terse), especially the code/rules that find exact phrases 

#### Files Summary
- `data-exploration.ipynb` - manually looking at data, initial ideas and thoughts
- `scratch.ipynb` - small tests before plugging in to script
- 

#### Environment


#### References 
- on [Multi-label Model Evaluation](https://www.kaggle.com/kmkarakaya/multi-label-model-evaluation)
- on [Multi-Class Metrics](https://towardsdatascience.com/multi-class-metrics-made-simple-part-i-precision-and-recall-9250280bddc2), [PT.II](https://towardsdatascience.com/multi-class-metrics-made-simple-part-ii-the-f1-score-ebe8b2c2ca1)
- [sklearn Metrics and Scoring](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)
- Bae, Y. S., Kim, K. H., Kim, H. K., Choi, S. W., Ko, T., Seo, H. H., Lee, H.-Y., &amp; Jeon, H. (2021). [Keyword extraction algorithm for classifying smoking status from unstructured bilingual electronic health records based on Natural Language Processing](https://doi.org/10.3390/app11198812). Applied Sciences, 11(19), 8812. 
- Jonnagaddala, J., Dai, H.-J., Ray, P., &amp; Liaw, S.-T. (2015). [A preliminary study on automatic identification of patient smoking status in unstructured electronic health records](https://doi.org/10.18653/v1/w15-3818). Proceedings of BioNLP 15.
- Bui, D. D., &amp; Zeng-Treitler, Q. (2014). [Learning regular expressions for clinical text classification](https://doi.org/10.1136/amiajnl-2013-002411). Journal of the American Medical Informatics Association, 21(5), 850–857. 
