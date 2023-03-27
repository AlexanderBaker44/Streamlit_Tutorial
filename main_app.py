import streamlit as st
import numpy as np
import cv2
from utils.utils_functions import read_data

st.set_option('deprecation.showPyplotGlobalUse', False)



def welcome_page():
    '''
    This function writes and formats text to the welcome page
    It also reads in the image form the images folder and displays it
    using the opencv library
    '''
    #display title on streamlit
    st.title('Welcome to Streamlit!')
    #read in image we want to display
    logo = cv2.imread('images/streamlit_logo.png')
    #display image on the page
    st.image(logo)
    #execute a simple streamlit write command, this will dispay text to your dash
    st.write('Streamlit is an incredible library that allows you to quickly make dashboards with python.')
    #let's display a markdown bulleted list
    st.markdown(
                    '''
                    Some really cool things you can do with streamlit include:
                    * Simple syntax
                    * Easy to format
                    * Excellent documentation
                    * Compatible with numerous plotting and styling methods
                    '''
                )

#execute the fucntion 
welcome_page()
