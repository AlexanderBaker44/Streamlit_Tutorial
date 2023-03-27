import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.utils_functions import read_data


def sep_cols(df):
    '''
    Let's start by dividing the columns into:
    categorical and nominal columns and
    numerical columns
    '''
    #empty cat list
    cat_cols = []
    #empty numerical col list
    num_cols = []
    #iterate through columns to sort
    for i in df.columns:
        #get the first value
        value = df[i][0]
        #get the type of the value
        col_type = type(value)
        #check if nominal or categorical variable, if the value is less than 10, in this case, it is certain to be nominal
        if col_type.__name__ =='str' or value < 10:
            cat_cols.append(i)
        else:
            num_cols.append(i)
    return cat_cols,num_cols


def create_bar_charts(selected_cols):
    '''
    This fucntion takes the selected columns and
    will group the data by the selected columns
    will plot these histograms to a subplot chart
    displays it on streamlit
    '''
    #get empty figure
    fig_b, ax_b = plt.subplots(figsize = (14, 4))
    #iterate through the input col
    for j,i in enumerate(selected_cols):
        #group the data by the chosen column
        grouped_df = df.groupby(i).count()['price']
        #put the plot in the subplot
        plt.subplot(1,len(selected_cols),j+1)
        #plot the data
        grouped_df.plot(kind='bar')
    #plot the matplotlib plot on a streamlit dash
    st.pyplot(fig_b)


def stacked_bar_chart(selected_pair):
    '''
    This plot gets a pair of categorical values
    groups them based on these two indices
    unstacks the indices and
    plots them on a stacked bar chart
    displays it on a streamlit dash
    this function also checks to ensure that only a pair of values is chosen
    '''
    #we are using a try except statement to handle inputs that aren't pairs
    try:
        #unpack the pair
        selected_col_1,selected_col_2 = selected_pair
        #groupby the two categories and unstack the indices
        df_double_grouped = df.groupby([selected_col_1,selected_col_2]).count()['price'].unstack()
        #get an empty figure
        fig_sb, ax_sb = plt.subplots(figsize = (14, 4))
        #plot the data on the figure
        df_double_grouped.plot(kind = 'bar', stacked = True,ax=ax_sb)
        #plot on streamlit
        st.pyplot(fig_sb)
    except:
        #check to make sure the error is what we think it is
        if len(selected_pair) < 2:
            #display the error on streamlit
            st.error('Please enter another column')
        else:
            #otherwise output the misc message
            st.error('unknown error')


def colored_scatter_plot(selected_col):
    '''
    takes in a selected categorical column
    Creates the scatter plot between area and price
    It will then color the scatterplot based on the chosen column
    '''
    #get empty plot
    fig_s, ax_s = plt.subplots(figsize = (14, 4))
    #write the sns plot for colored scatter plots
    sns.scatterplot(data = df, x = 'area', y = 'price', hue = selected_col, palette="plasma", ax = ax_s)
    #plot the scatterplot to streamlit
    st.pyplot(fig_s)

#read in the data
df = read_data('data/Housing.csv')
#write the header
st.header('Data Analysis')
#write the subheader
st.subheader('A Sample from the Data')
#display a sample of the data
st.table(df.head())
#create tabs on the dash
tab1, tab2 = st.tabs(["Categorical","Numerical"])
#lets make the first categorical analysis tab
with tab1:
    #write the intro  subheader
    st.subheader('Analyze categorical and nominal columns')
    #seperate the numerical and categorical cols
    cat_cols,num_cols = sep_cols(df)
    #create the multiselect widget
    selected_cols = st.multiselect(label = 'Select columns to compare', options = cat_cols, default = 'stories')
    #write the expanding bar chart
    create_bar_charts(selected_cols)
    #create the pair multiselect
    selected_pair =  st.multiselect(label = 'Select columns to compare', options = cat_cols, default = ['bedrooms','bathrooms'], max_selections = 2)
    #plot the stacked bar chart
    stacked_bar_chart(selected_pair)
#let's create the numerical tab
with tab2:
    #write the intro subheader
    st.subheader('Analyze numerical columns')
    #create the single select box widget
    selected_col = st.selectbox(label = 'Select a categorical column', options = cat_cols)
    #plot the colored scatter plot based on the input
    colored_scatter_plot(selected_col)
