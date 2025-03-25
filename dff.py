import pickle
import pandas as pd

# Load the saved model
# with open("/content/drive/MyDrive/MDS/model.pkl", "rb") as model_file:
#     model = pickle.load(model_file)

# Define test data (replace with actual test samples)
test_data = pd.DataFrame({
    'event1_cat1': [10, 5],
    'event1_cat2': [2, 8],
    'event1_cat4': [3, 1],
    'event1_cat5': [7, 4],
    'event1_cat6': [1, 2],
    'event1_cat7': [5, 9],
    'event1_cat8': [2, 3],
    'event1_cat9': [8, 6],
    'event1_cat10': [4, 7],
    'event1_cat11': [9, 1],
    'event2_cat1': [6, 2],
    'event2_cat2': [3, 5],
    'event2_cat3': [1, 8],
    'event2_cat4': [7, 4],
    'event2_cat5': [4, 1],
    'event2_cat6': [2, 7],
    'event2_cat7': [9, 3],
    'event2_cat8': [5, 6],
    'event2_cat9': [1, 9],
    'event2_cat10': [8, 2],
    'Total_Order': [5, 10],
    'Recency': [15, 30],
    'Total_Revenue': [100, 250],
    'cat1_freq': [0.2, 0.1],
    'cat2_freq': [0.3, 0.4],
    'cat3_freq': [0.1, 0.2],
    'cat4_freq': [0.4, 0.3],
    'cat5_freq': [0.0, 0.0],
    'cat7_freq': [0.0, 0.0],
    'cat1_brow': [1,2],  
    'cat2_brow': [3,4],  
    'cat3_brow': [2,1]  
})

# Ensure test data matches model features
expected_features = model.feature_names_in_
test_data = test_data[expected_features]  # Keep only required columns

test_data.to_csv('test.csv', index=False)

# Assuming 'results' should contain probabilities, use predict_proba
# results = model.predict_proba(test_data)  
# cno = 1
# # Create DataFrame with probabilities for each class
# df = pd.DataFrame({'custno': cno ,  # Replace with actual custno if available
#                    'procat1_1': [p[1] for p in results[0]],  # Access probabilities for class 1
#                    'procat1_2': [p[1] for p in results[1]],  # Access probabilities for class 2
#                    'procat1_3': [p[1] for p in results[2]],  # Access probabilities for class 3
#                    'procat1_4': [p[1] for p in results[3]],  # Access probabilities for class 4
#                    'procat1_5': [p[1] for p in results[4]],  # Access probabilities for class 5
#                    'procat1_7': [p[1] for p in results[5]]})  # Access probabilities for class 7

# df.head()

# print(df)