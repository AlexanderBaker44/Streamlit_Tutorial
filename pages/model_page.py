import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils.utils_functions import get_encoded_input, finalize_inputs, get_predictions, read_data



def get_inputs():
    '''
    This function shows the widgets, gets the inputs,
    and sorts the categorical and numerical one
    '''
    #establish the true false dict
    true_false_conversion_dict = {True:'yes',False:'no'}
    #introduce the input body
    st.subheader('Input Housing Attributes')
    #establish the columns for teh dashboard
    col1, col2, col3 = st.columns(3)
    #let's create the first column
    with col1:
        #get the airconditioning status using selectbox widget
        air_conditioning = st.selectbox(label = 'Air conditioning status', options = list(set(df['airconditioning'])))
        #get the furnishing status using radio buttons
        furnishing = st.radio(label = 'Firnishing status', options = list(set(df['furnishingstatus'])))
        #get the hot water heating status using check box
        hotwaterheating_tf = st.checkbox(label = 'Hot water heating status')
        #convert true false into what the check box expects
        hotwaterheating = true_false_conversion_dict[hotwaterheating_tf]
        #ge tthe preferred area status
        prefarea_tf = st.checkbox(label = 'Is the house in a preferred area')
        #convert the checkbox true false to actual value
        prefarea = true_false_conversion_dict[prefarea_tf]
    #let's create the second column
    with col2:
        #get the number of bathrooms using a select slider
        bathrooms = st.select_slider(label = 'Number of bathrooms', options = list(set(df['bathrooms'])))
        #get the number of bedrooms using the select slider
        bedrooms = st.select_slider(label = 'Number of bedrooms', options = list(set(df['bedrooms'])))
        #get the number of stories using the slider
        stories = st.slider(label = 'Select number of stories',min_value = min(df['stories']),max_value = max(df['stories']))
        #get the area using the number input
        area = st.number_input(label = 'Enter housing area', min_value = min(df['area']), max_value = max(df['area']))
        #divide the area by 1000
        area = area/(10**3)
    #let's create the third column
    with col3:
        #get the mainroad status using the select box
        mainroad = st.selectbox(label = 'Is the house on the mainroad',options = list(set(df['mainroad'])))
        #get the basement status using the radio buttons
        basement = st.radio(label = 'Does the house have a basement', options = list(set(df['basement'])))
        #get the guestroom status with text input
        guestroom = st.text_input(label = 'Does the house have a guestroom?',value = 'no')
        #get parking status using the select slider
        parking = st.select_slider(label = 'Number of parking spots', options = list(set(df['parking'])))

    #we need to catch the improper value for the text box
    if guestroom not in list(set(df['guestroom'])):
        st.error('Please enter yes or no')
    #these arrays are seperated for the ease of our encoder use later
    #make the numerical array
    input_nums = np.array([area,bedrooms,bathrooms,stories,parking])
    #make the categorical arry
    input_cats = np.array([mainroad,guestroom,basement,hotwaterheating,air_conditioning,prefarea,furnishing])
    return input_nums,input_cats


def get_predictions_dash(input_nums, input_cats):
    '''
    This encodes the cateogircal input
    Concatenates and reshapes the input
    Gets the predictions using the model
    '''
    #get encoded cat input
    encoded_inputs = get_encoded_input(input_cats)
    #combine the inputs
    full_inputs = finalize_inputs(input_nums,encoded_inputs)
    #get the prediction
    predictions = get_predictions(full_inputs)
    return predictions

def format_prediction(prediction_value):
    '''
    This function takes the prediction, and displays the number on the dash
    This also displays the output on a histogram for comparison
    '''
    #format the output to make it more readable
    formatted_output = prediction_value[0]*10**6
    #add the dollar value
    formatted_output_s = '$'+str(int(formatted_output))
    #introduce the section
    st.title('Predicted Housing Price')
    #write html code for streamlit to execute
    #we want to align the text to the center, and color it green
    html_sub = f"<h2 align=\"center\" style = color:green>{formatted_output_s}</h2>"
    #plot to the streamlit dash
    st.components.v1.html(html_sub, width=None, height=None, scrolling=False)
    #introduce the price distribution
    st.subheader('Price Distribution')
    #plot the price distribution
    fig, ax = plt.subplots(figsize = (14, 4))
    #establish the patches  and bins for the plot
    N, bins, patches = ax.hist(df['price'])
    #get the index of bucket the prediction lands in
    selected = np.digitize(formatted_output,bins)
    #make the select patch red while the others remain blue
    patches[selected].set_facecolor('r')
    #plot to the streamlit dash
    st.pyplot()

#read in the data
df = read_data('data/Housing.csv')
#create the intro header
st.header('Model Page')
#write the input section
input_nums, input_cats = get_inputs()
#check to ensure the input is proper
try:
    #get the predictions
    prediction = get_predictions_dash(input_nums, input_cats)
    #format and write the predictions to the dash
    format_prediction(prediction)
except:
    #output error if the error is improper
    st.error('Please enter a proper input')
