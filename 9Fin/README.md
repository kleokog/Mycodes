# README

## Run the code
1. In a folder named 'Data' move the "db.sqlite3" database and the "titles.jsonl"
2. Run the 'Text Classification.ipynb' jupyter notebook. The only configuration that needs to be done is to define the path folder of 'Data' 

## Steps:
1. Read the 3 data sources (2 tables from database and the json file)
2. Basic data investigation and some visualisations
3. Bring 'URL' field in a textual format
4. Merge the 'URL' and 'title' column
5. Clean the 'URL and Title' column (remove stopwords, remove non-alphabetic tokens, remove non-English words)
6. Represent the clean text in a TF-IDF matrix
7. Feed the TF-IDF matrix in 3 classifiers (Logistic Regression, Random Forest and XGBoost)
8. Keep the classifier with the highest performance (XGBoost)
9. Evaluate performance with F1-score
10. Present the most important words of the classifier (Feature Importance)