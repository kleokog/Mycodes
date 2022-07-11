import json
import pandas as pd
from bmi_functions import *


# Logging
import logging

logging.basicConfig(filename = 'file.log',
                    level = logging.DEBUG,
                    format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.debug("---------------------------------------------------")
print("Logger is set")

# Read from json file
f = open('input.json')
json_input = json.load(f)
f.close()
print("Read json file successfully")

# Dataframe Initialisation
input_df = pd.DataFrame(json_input, columns = ['Gender', 'HeightCm', 'WeightKg'])  # column names could automatically been given
input_df = input_df.reset_index().rename(columns = {'index' : 'user_id'})  # so that the index can become the user_id

# Task 1 - Estimate all the bmi-related indicators
try:
    input_df
except:
    print("The dataframe is missing, BMI, BMI category and Health Risk can not be estimated")
    logging.error("The dataframe is missing, BMI, BMI category and Health Risk can not be estimated")
else:
    input_df['BMI'] = input_df.apply(lambda row : estimate_bmi(row['user_id'], row['HeightCm'], row['WeightKg']), axis = 1)
    logging.info("BMI is estimated for all users")
    input_df['BMICategory'] = input_df['BMI'].apply(lambda x : estimate_BMI_category(x))
    logging.info("BMI category is estimated for all users")
    input_df['HealthRisk'] = input_df['BMI'].apply(lambda x: estimate_Health_risk(x))
    output_file = "BMI_indicators.csv"
    input_df.to_csv(output_file)
    logging.info("Health Risk level is estimated for all users")
    print(f"Task 1 is done and the output can be found on {output_file}")

# Task 2 - Estimate the number of people who are overweight
overweighted_people = input_df[input_df["BMICategory"].str.lower() == 'overweight'].shape[0]
print(f"The number of overweighted people are {overweighted_people}")


print("End of script")