import numpy as np
import re
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.impute import SimpleImputer

def scaling(dataframe):
    try:
        print(f"scaling reached...") #
        numeric_indices = list(range(15, 24))
        scaler = StandardScaler()
        prep_data = scaler.fit_transform(dataframe.iloc[:, numeric_indices])
        print(f"scaling done...{prep_data}") #
        return prep_data, scaler
    except Exception as e:
        print(f"Error in scaling function: {e}")
        return None, None

def nn_predictor(prep_data):
    try:
        print(f"nn_predictor reached...")

        # Impute missing values in prep_data
        imputer = SimpleImputer(strategy='mean')  # Impute missing values with mean
        prep_data_imputed = imputer.fit_transform(prep_data)

        # Fit NearestNeighbors
        neigh = NearestNeighbors(metric='cosine', algorithm='brute')
        neigh.fit(prep_data_imputed)

        return neigh
    except Exception as e:
        print(f"Error in nn_predictor function: {e}")
        return None

def build_pipeline(neigh, scaler, params):
    try:
        print(f"build_pipeline function reached...") #
        transformer = FunctionTransformer(neigh.kneighbors, kw_args=params)
        print(f"build_pipeline function transformer value...{transformer}") #
        pipeline = Pipeline([('std_scaler', scaler), ('NN', transformer)])
        print(f"build_pipeline function pipeline value...{pipeline}") #
        return pipeline
    except Exception as e:
        print(f"Error in build_pipeline function: {e}")
        return None

def extract_data(dataframe, ingredients):
    try:
        print(f"data extraction in extract_data...") #
        extracted_data = dataframe.copy()
        extracted_data = extract_ingredient_filtered_data(extracted_data, ingredients)

        # Convert non-numeric values to NaN
        # extracted_data.iloc[:, 6:15] = pd.to_numeric(extracted_data.iloc[:, 6:15], errors='coerce')

        print(f"extracted_data in extract_data: {extracted_data}") #
        return extracted_data
    except Exception as e:
        print(f"Error in extract_data function: {e}")
        return None

def filter_diabetic_friendly(dataframe, is_diabetic=False):
    try:
        print(f"filter_diabetic_friendly reached...")

        if is_diabetic:
            nutritional_columns = dataframe.columns[15:24]

            max_sugar = 5.0
            max_carbs = 20.0

            filtered_data = dataframe[
                (dataframe[nutritional_columns].astype(float)['SugarContent'] <= max_sugar) &
                (dataframe[nutritional_columns].astype(float)['CarbohydrateContent'] <= max_carbs)
            ]
        else:
            filtered_data = dataframe.copy()

        print(f"filtered_data in filter_diabetic_friendly: {filtered_data}")
        return filtered_data
    except Exception as e:
        print(f"Error in filter_diabetic_friendly function: {e}")
        return dataframe

def extract_ingredient_filtered_data(dataframe, ingredients):
    try:
        print(f"extract_ingredient_filtered_data function reached...") #
        extracted_data = dataframe.copy()
        regex_string=''.join(map(lambda x:f'(?=.*{x})',ingredients))
        extracted_data = extracted_data[extracted_data['RecipeIngredientParts'].str.contains(regex_string, regex=True, flags=re.IGNORECASE)]
        print(f"extract_ingredient_filtered_data in extracted_data: {extracted_data}") #
        return extracted_data
    except Exception as e:
        print(f"Error in extract_ingredient_filtered_data function: {e}")
        return None

def apply_pipeline(pipeline, _input, extracted_data):
    try:
        _input=np.array(_input).reshape(1,-1)
        return extracted_data.iloc[pipeline.transform(_input)[0]]

    except Exception as e:
        print(f"Error in apply_pipeline function: {e}")
        return None

def recommend(dataframe, _input, ingredients=[], params={'n_neighbors': 5, 'return_distance': False}, is_diabetic=False):
    try:
        print(f"recommend function called...") #
        extracted_data = extract_data(dataframe, ingredients)
        print(f"extracted_data: {extracted_data}") #
        # print("Column Names:") #
        # for col in extracted_data.columns: #
        #     print(col) #

        if is_diabetic:
            extracted_data = filter_diabetic_friendly(extracted_data, is_diabetic)

        if extracted_data is not None and not extracted_data.empty and extracted_data.shape[0] >= params['n_neighbors']:
            prep_data, scaler = scaling(extracted_data)
            neigh = nn_predictor(prep_data)
            pipeline = build_pipeline(neigh, scaler, params)
            return apply_pipeline(pipeline, _input, extracted_data)
        else:
            return None
    except Exception as e:
        print(f"Error in recommend function: {e}")
        return None

def extract_quoted_strings(s):
    try:
        print(f"extract_quoted_strings reached...") #
        # Find all the strings inside double quotes
        strings = re.findall(r'"([^"]*)"', s)
        # Join the strings with 'and'
        return strings
    except Exception as e:
        print(f"Error in extract_quoted_strings function: {e}")
        return []

def output_recommended_recipes(dataframe):
    try:
        print(f"output_recommended_recipes reached...") #
        if dataframe is not None:
            output = dataframe.copy()
            print(f"output-before-to-api: {output}") #
            output = output.to_dict("records")
            print(f"output-after-to-api: {output}") #
            for recipe in output:
                recipe['RecipeIngredientParts'] = extract_quoted_strings(recipe['RecipeIngredientParts'])
                recipe['RecipeInstructions'] = extract_quoted_strings(recipe['RecipeInstructions'])
        else:
            output = None
        return output
    except Exception as e:
        print(f"Error in output_recommended_recipes function: {e}")
        return None
