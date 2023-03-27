
import pandas as pd
import pickle as pkl
import numpy as np
import streamlit as st

@st.cache_data
def read_data(path):
    '''
    This function reads in the data, and outputs the information
    It is cached to improve performance
    '''
    #read in csv
    df = pd.read_csv(path)
    return df

@st.cache_resource
def load_models(file):
    """
    This function reads in the trained model and caches it
    This is mainly done to improve performance
    """
    #read in model
    model_file = open(f'model/{file}','rb')
    #load in the model using pickle
    model_import = pkl.load(model_file)
    #close the file
    model_file.close()
    return model_import

def get_encoded_input(cat_inputs):
    '''
    This function reads in the One Hot Encoding model
    Takes the encoding input, reshapes to be input into the ohe encoder
    It then condenses the transformation into a dense array
    The encoded values are then returned
    '''
    #load in the model
    ohe_model = load_models('ohe.pkl')
    #reshape the input
    cat_inputs = cat_inputs.reshape(-1,len(cat_inputs))
    #transform the input
    encoded = ohe_model.transform(cat_inputs)
    #condense the output
    encoded = encoded.toarray()[0]
    return encoded

def finalize_inputs(num_inputs,cat_inputs):
    '''
    Concatenates the inputs
    Reshapes the input to be a model input
    returns the array
    '''
    #concatenate the inputs
    full_array = np.concatenate([num_inputs,cat_inputs])
    #get the full input and reshape it for the model
    full_array = full_array.reshape(-1,len(full_array))
    return full_array

def get_predictions(full_inputs):
    '''
    This function reads in the model and returns the predictions
    '''
    #load in the rf model
    rfe_model = load_models('rf_model.pkl')
    #predict the price using the output
    prediction = rfe_model.predict(full_inputs)
    return prediction
