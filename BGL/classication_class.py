import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import precision_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split


class CustomClassifier:

    def __init__(self, model: str, X_train: pd.DataFrame = None, X_test: pd.DataFrame = None,
                 y_train: pd.DataFrame = None, y_test: pd.DataFrame = None):
        self.model = model
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.classifier = None
        self.accuracy = None
        self.precision = None
        self.y_pred = None
        self.number_of_classes = None
        self.labels_dict = None
        self.label_probability_df = None
        self.index_col = None
        self.significance_df = None
        self.f1_score_macro = None
        self.f1_score_weighted = None


    def split_to_train_and_test_set(self, X, y, test_size = 0.3):
        '''
        Parameters
        ----------
        X: the featues that are going to be used for training
        y: the labels
        test_size: percentage of submissions to be test set
        '''
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        return self

    def estimate_number_of_classes(self):
        labels_in_training_set = list(self.y_train.drop_duplicates())
        if self.y_test is None:
            self.number_of_classes = len(labels_in_training_set)
            return self.number_of_classes
        else:
            labels_in_test_set = list(self.y_test.drop_duplicates())
            test_set_new_labels = list(set(labels_in_test_set) - set(labels_in_training_set))
            if len(test_set_new_labels) == 0:
                self.number_of_classes = len(labels_in_training_set)
                return self.number_of_classes
            else:
                raise TypeError('Training set and Test set should have the same labels')

    def fit_model(self, **kwargs):
        # print(**kwargs)
        if self.model == 'LR':
            print(self.model)
            self.classifier = LogisticRegression(random_state=7, class_weight='balanced')
        elif self.model == 'RF':
            print(self.model)
            self.classifier = RandomForestClassifier(random_state=7, **kwargs)
        elif self.model == 'XGBoost':
            print(self.model)
            self.classifier = XGBClassifier()
        else:
            print("The classifier that you chose does not exist - setting default classifier Logistc Regression")
            self.classifier = LogisticRegression()
        self.classifier.fit(self.X_train, self.y_train)
        self.y_pred = self.classifier.predict(self.X_test)

        return self

    def estimate_accuracy(self):
        try:
            self.classifier.score(self.X_test, self.y_test)
        except:
            print("Check that the X_test and the y_test are estimated\n and also the classifier has been trained")
        self.accuracy = round(self.classifier.score(self.X_test, self.y_test), 4)
        print('Accuracy of {} classifier on test set: {:.4f}'.format(self.model, self.accuracy))
        return self.accuracy

    def estimate_precision(self):
        self.estimate_number_of_classes()
        if self.number_of_classes == 2:     # binary
            self.precision = precision_score(self.y_test, self.y_pred)
        else:
            self.precision = precision_score(self.y_test, self.y_pred, average='weighted')
        print('Precision of {} classifier on test set: {:.4f}'.format(self.model, self.precision))
        return self.precision

    def estimate_f1_score(self, **kwargs):
        self.f1_score_macro = f1_score(self.y_test, self.y_pred, average='macro')
        print('F1-score (unweighted) of {} classifier on test set: {:.4f}'.format(self.model, self.f1_score_macro))
        try:
            self.f1_score_weighted = f1_score(self.y_test, self.y_pred, average='weighted', sample_weight=kwargs['sample_weight'])
            print("The actual weights of the data is used to estmate the F1-score")
        except:
            self.f1_score_weighted = f1_score(self.y_test, self.y_pred, average='weighted')
        print('F1-score (weigthed) of {} classifier on test set: {:.4f}'.format(self.model, self.f1_score_weighted))



    def create_confusion_matrix(self):
        return confusion_matrix(self.y_test, self.y_pred)

    def estimate_label_probability(self, index_col:str = None):
        self.label_probability_df = (pd.DataFrame(self.classifier.predict_proba(self.X_test))
                                     .rename(columns=self.labels_dict))
        if index_col is not None:
            self.label_probability_df = (self.label_probability_df
                                         .join(self.X_test.reset_index()[[index_col]])
                                         .set_index(index_col))       # set submission id as index
        return self.label_probability_df

    def add_index_to_predictions(self, field_name):
        '''
        Parameters
        ----------
        field_name : column name of the y_pred

        Returns -  A big issue with the predictions is that we do not know the submission id that they belonng to in
        order to merge with other datasets. This function adds the submission id as index in the predictions
        -------
        '''
        index_col_name = self.X_test.index.name
        self.y_pred = pd.DataFrame(data = zip(list(self.X_test.reset_index()[index_col_name]), list(self.y_pred)),
                                   columns = [index_col_name, field_name]).set_index(index_col_name)
        return self.y_pred

    def estimate_feature_importance(self):
        if self.model == 'RF':
            self.significance_df = (pd.DataFrame(zip(list(self.X_train.columns), list(self.classifier.feature_importances_))).
                                    rename(columns= {0:'Feature', 1: 'Significance'}).
                                    sort_values('Significance', ascending = False))
        return self.significance_df


    def set_train_and_test_data(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        return self

    def set_labels_dict(self, labels_dict:dict):
        self.labels_dict = labels_dict
