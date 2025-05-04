import pickle

import numpy as np
import pandas as pd

loaded_model = pickle.load(open('project_variables/model.pkl', 'rb'))
le = pickle.load(open('project_variables/Labelencoder.pkl', 'rb'))
ohe = pickle.load(open('project_variables/one_hot_encoder.pkl', 'rb'))
df = pd.read_csv("project_variables/Crop and fertilizer dataset.csv")

"""
Inputs:
Nitrogen
Phosphorus
Soil Color
Crop
pH
Rainfall
Temperature
"""
"""
output = Fertilizer
"""
soil_color = df["Soil_color"].unique()
soil_color = [s.title() for s in soil_color]
crop = df["Crop"].unique()
crop = [c.title() for c in crop]
half = len(crop) // 2
line1 = ", ".join(crop[:half])
line2 = ", ".join(crop[half:])

half_soil = len(soil_color) // 2
line1_soil = ", ".join(soil_color[:half])
line2_soil = ", ".join(soil_color[half:])


"""
to seperate text in a list
data = [1, "test", 8, "two"]
strings_only = [item for item in data if isinstance(item, str)]
"""
def chatbot():
    while True:
        categorical = []
        ##User entering Crop Type
        print("Welcome")
        crop_input = input(f"""Enter Crop Type:\n({line1}\n{line2}):\n""")
        crop_input = crop_input.title()
        if crop_input == "Corn":
            crop_input = "Maize"
        while crop_input not in crop:
            crop_input = input(f"""Error {crop_input}: Enter the correct Crop Type:\n({line1}\n{line2}):\n""")
            crop_input = crop_input.title()
            if crop_input == "Corn":
                crop_input = "Maize"

        ##User Entering Soil Color
        soil_input = input(f"""Enter Soil Colorl:\n({line1_soil}\n{line2_soil}):\n""")
        soil_input = soil_input.title()
        if soil_input == "Brown":
            soil_input = input(f"Did you mean: Reddish Brown, Dark Brown, Light Brown, or Medium Brown:\n")
            while soil_input not in ['Reddish Brown','Light Brown','Reddish Brown', 'Dark Brown']:
                soil_input = input(f"Sorry Ektebha Sa77 >:( :\n")
        while soil_input not in soil_color:
            soil_input = input(f"""Error {soil_input}: Enter the correct Soil Color:\n({line1_soil}\n{line2_soil}):\n""")
            soil_input = soil_input.title()
            if soil_input == "Brown":
                soil_input = input(f"Did you mean: Reddish Brown, Dark Brown, Light Brown, or Medium Brown:\n")
                while soil_input not in ['Reddish Brown', 'Light Brown', 'Reddish Brown', 'Dark Brown']:
                    soil_input = input(f"Sorry Ektebha Sa77 >:( :\n")

        categorical.append([soil_input,crop_input])
        encoded_cat = ohe.transform(pd.DataFrame(categorical,columns=["Soil_color","Crop"]))
        print(encoded_cat[0])


        numerical= []
        #Numerical Nitrogen
        nitrogen = float(input("Please Enter Nitrogen Level> "))
        if nitrogen < np.min(df["Nitrogen"]):
            nitrogen = np.min(df["Nitrogen"])
        elif nitrogen > np.max(df["Nitrogen"]):
            nitrogen = np.max(df["Nitrogen"])


        # Temperature
        temperature = float(input("Please Enter Temperature> "))
        if temperature < np.min(df["Temperature"]):
            temperature = np.min(df["Temperature"])
        elif temperature > np.max(df["Temperature"]):
            temperature = np.max(df["Temperature"])

        # Phosphorus
        phosphorus = float(input("Please Enter Phosphorus Level> "))
        if phosphorus < np.min(df["Phosphorus"]):
            phosphorus = np.min(df["Phosphorus"])
        elif phosphorus > np.max(df["Phosphorus"]):
            phosphorus = np.max(df["Phosphorus"])

        # pH
        ph = float(input("Please Enter pH Level> "))
        if ph < np.min(df["pH"]):
            ph = np.min(df["pH"])
        elif ph > np.max(df["pH"]):
            ph = np.max(df["pH"])

        # Rainfall
        rainfall = float(input("Please Enter Rainfall (mm)> "))
        if rainfall < np.min(df["Rainfall"]):
            rainfall = np.min(df["Rainfall"])
        elif rainfall > np.max(df["Rainfall"]):
            rainfall = np.max(df["Rainfall"])

        # Potassium
        potassium = float(input("Please Enter Potassium Level> "))
        if potassium < np.min(df["Potassium"]):
            potassium = np.min(df["Potassium"])
        elif potassium > np.max(df["Potassium"]):
            potassium = np.max(df["Potassium"])


        numerical.append(nitrogen)
        numerical.append(phosphorus)
        numerical.append(potassium)
        numerical.append(ph)
        numerical.append(rainfall)
        numerical.append(temperature)

        # Convert numerical list to numpy array
        numerical_array = np.array(numerical).reshape(1, -1)

        # Convert sparse matrix to dense if necessary
        encoded_cat_dense = encoded_cat.toarray() if hasattr(encoded_cat, 'toarray') else encoded_cat

        # Combine numerical and categorical features horizontally
        combined_features = np.hstack((numerical_array, encoded_cat_dense))

        # Get original feature names used during training
        numerical_feature_names = ["Nitrogen", "Phosphorus", "Potassium", "pH", "Rainfall", "Temperature"]

        # Get categorical feature names (same as used during training)
        # This assumes your one-hot encoder has 'get_feature_names_out' method (scikit-learn ≥ 1.0)
        categorical_feature_names = ohe.get_feature_names_out(["Soil_color", "Crop"])

        # Combine all feature names
        all_feature_names = np.concatenate([numerical_feature_names, categorical_feature_names])

        # Create DataFrame with proper feature names
        input_df = pd.DataFrame(combined_features, columns=all_feature_names)

        # Now predict using the DataFrame with correct feature names
        prediction = loaded_model.predict(input_df)
        fertilizer = le.inverse_transform(prediction)[0]

        print(f"Recommended fertilizer: {fertilizer}")


"""Production Code"""
def preprocess_data(user_input):
    categorical = [item for item in user_input if isinstance(item, str)]
    numerical = [item for item in user_input if not isinstance(item,str)]

    encoded_cat = ohe.transform(pd.DataFrame([categorical], columns=["Soil_color", "Crop"]))
    # Convert numerical list to numpy array
    numerical_array = np.array(numerical).reshape(1, -1)

    # Convert sparse matrix to dense if necessary
    encoded_cat_dense = encoded_cat.toarray() if hasattr(encoded_cat, 'toarray') else encoded_cat

    # Combine numerical and categorical features horizontally
    combined_features = np.hstack((numerical_array, encoded_cat_dense))

    # Get original feature names used during training
    numerical_feature_names = ["Nitrogen", "Phosphorus", "Potassium", "pH", "Rainfall", "Temperature"]

    # Get categorical feature names (same as used during training)
    # This assumes your one-hot encoder has 'get_feature_names_out' method (scikit-learn ≥ 1.0)
    categorical_feature_names = ohe.get_feature_names_out(["Soil_color", "Crop"])

    # Combine all feature names
    all_feature_names = np.concatenate([numerical_feature_names, categorical_feature_names])

    # Create DataFrame with proper feature names
    input_df = pd.DataFrame(combined_features, columns=all_feature_names)

    return input_df

def predict(input_df):
    prediction = loaded_model.predict(input_df)
    fertilizer = le.inverse_transform(prediction)[0]
    return fertilizer

