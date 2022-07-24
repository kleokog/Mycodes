import logging

def cm_to_meters(height_cm:float):
    return height_cm/100

def estimate_bmi(user_id:int, height_cm:float, weight:float):
    try:
        float(height_cm)
    except:
        logging.error(f"The height of user: {user_id} is not float")
    try:
        float(weight)
    except:
        logging.error(f"The weight of {user_id} is not float")
    height_m = cm_to_meters(height_cm)
    bmi = weight/(height_m**2)
    return bmi

# Put these 2 functions into 1
def estimate_BMI_category(bmi:float):
    try:
        float(bmi)
    except ValueError:
        print(f"The input -- {bmi} -- is not a number")
    else:
        if bmi <=18.4:
            return 'Underweight'
        elif( bmi >18.4) & (bmi<=24.9):
            return 'Normal weight'
        elif( bmi >24.9) & (bmi<=29.9):
            return 'Overweight'
        elif( bmi >29.9) & (bmi<=34.9):
            return 'Moderately obese'
        elif( bmi >34.9) & (bmi<=39.9):
            return 'Severely obese'
        else:
            return "Very severely obese"

def estimate_Health_risk(bmi:float):
    try:
        float(bmi)
    except ValueError:
        print(f"The input -- {bmi} -- is not a number")
    else:
        if bmi <=18.4:
            return 'Malnutrition risk'
        elif( bmi >18.4) & (bmi<=24.9):
            return 'Low risk'
        elif( bmi >24.9) & (bmi<=29.9):
            return 'Enhanced risk'
        elif( bmi >29.9) & (bmi<=34.9):
            return 'Medium risk'
        elif( bmi >34.9) & (bmi<=39.9):
            return 'High risk'
        else:
            return "Very high risk"