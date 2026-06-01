import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# TITLE 
#Setting the main title displayed at the very top of the webpage.
st.title('Sellers Performance Dashboard')

# DATA LOADING
# Reading the data file 
df = pd.read_excel('/Users/majochaviraguzman/Desktop/DAIA/streamlit/sellers.xlsx')

# Creating a new column 'FULL NAME' by combining the first name and last name.
# This makes it easier to display full names in dropdown lists later.
df['FULL NAME'] = df['NAME'] + " " + df['LASTNAME']


# REQUIREMENT 1: DISPLAY THE TABLE & FILTER BY REGION
# st.container() groups this entire section together visually.
with st.container():
    st.header('1. Filter Data Registry by Region')
    
    # Getting a list of all unique regions
    unique_regions = df['REGION'].unique()
    
    # Creating a selection dropdown box containing our unique regions to capture the specific region the user wants to see.
    selected_region = st.selectbox('Select a region:', unique_regions)
    
    # Filtering the data rows, keeping only rows that match the selected region.
    filtered_df = df[df['REGION'] == selected_region]
    
    # Displaying the filtered dataset in an interactive table format.
    st.dataframe(filtered_df)


# Creating a BUTTON FOR REGIONAL SUMMARIES to summarize totals per region
with st.container():
    st.header('2. Regional Revenue & Volume Summary')
    st.write(f"Click the button below to compute overall calculations for the **{selected_region}** region.")
    
    # Creating an interactive button element.
    if st.button('Calculate Totals for This Region'):
        
        # Summing up all values inside the 'SOLD UNITS' column for our filtered region.
        total_units = filtered_df['SOLD UNITS'].sum()
        
        # Summing up all values inside the 'TOTAL SALES' column for our filtered region.
        total_money = filtered_df['TOTAL SALES'].sum()
        
        # Using st.success to display the results in a nice green success box.
        st.success(f"**Results for {selected_region} Region:**")
        st.write(f"🔹 **Total Units Sold:** {total_units:,} units")
        st.write(f"🔹 **Total Financial Sales:** ${total_money:,}.00")


# REQUIREMENT 2: DISPLAY GRAPHS (Units Sold, Total Sales, and Average Sales) ---
# Grouping the chart visualizations inside another clean container.
with st.container():
    st.header('3. Regional Performance Charts')
    st.write(f"Showing visual analytics for the **{selected_region}** region:")
    
    # Graph A: Units Sold 
    st.subheader('Units Sold per Seller')
    # st.bar_chart builds a bar graph. We set the index to full names so names show on the bottom axis.
    st.bar_chart(filtered_df.set_index('FULL NAME')['SOLD UNITS'])
    
    # Graph B: Total Sales
    st.subheader('Total Financial Sales ($)')
    # st.line_chart builds a line graph tracking total revenue for each seller.
    st.line_chart(filtered_df.set_index('FULL NAME')['TOTAL SALES'])
    
    # Graph C: Average Sales
    st.subheader('Distribution of Sales Averages')
    # Creating a histogram to plot sales
    fig, ax = plt.subplots()
    ax.hist(filtered_df['SALES AVERAGE'], bins=10, color='lightgreen', edgecolor='black')
    ax.set_xlabel('Sales Average Score')
    ax.set_ylabel('Number of Sellers')
    
    # Passing our generated Matplotlib figure to Streamlit to display it.
    st.write(fig)


# REQUIREMENT 3: DISPLAY DATA FOR A SPECIFIC VENDOR 
with st.container():
    st.header('4. Specific Vendor Lookup')
    
    # Getting a unique list of all sellers from our original file.
    all_vendors = df['FULL NAME'].unique()
    
    # Creating a dropdown selector to pick exactly one employee.
    chosen_vendor = st.selectbox('Choose a vendor to view details:', all_vendors)
    
    # Creating an interactive click button for vendor search.
    if st.button('Search Vendor Profile'):
        
        # Filtering our original data down to just the single row for this person.
        vendor_row = df[df['FULL NAME'] == chosen_vendor]
        
        # Displaying their individual stats out in a small dashboard window.
        st.info(f"Displaying results for {chosen_vendor}:")
        st.dataframe(vendor_row)