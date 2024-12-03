
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
@st.cache
def load_data():
    data = pd.read_csv('Police_Bulk_Data_2014_20241027.csv')
    columns_to_keep = [
        "offensedescription", "offenserace", "offensegender", "offenseage", 
        "offensezip", "offensestatus"
    ]
    cleaned_data = data[columns_to_keep].dropna()
    return cleaned_data

# Load data
data = load_data()

# Title and description
st.title("Interactive Crime Data Dashboard")
st.markdown("Explore crime data with interactive visualizations.")

# Sidebar filters
st.sidebar.header("Filters")
selected_offense = st.sidebar.selectbox(
    "Select Offense Category", options=data['offensedescription'].unique()
)
age_range = st.sidebar.slider("Select Age Range", 
                               min_value=int(data['offenseage'].min()),
                               max_value=int(data['offenseage'].max()),
                               value=(20, 50))

# Filter data
filtered_data = data[
    (data['offensedescription'] == selected_offense) &
    (data['offenseage'].astype(int).between(age_range[0], age_range[1]))
]

# Visualizations
st.header("Exploratory Visualizations")

# Bar plot: Offense Status
st.subheader("Offense Status Distribution")
status_counts = filtered_data['offensestatus'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=status_counts.index, y=status_counts.values, ax=ax)
ax.set_title("Offense Status Distribution")
ax.set_xlabel("Status")
ax.set_ylabel("Count")
st.pyplot(fig)

# Scatter plot: Age vs ZIP Code
st.subheader("Age vs ZIP Code")
fig, ax = plt.subplots()
sns.scatterplot(
    x=filtered_data['offensezip'], y=filtered_data['offenseage'].astype(int), hue=filtered_data['offenserace'], ax=ax
)
ax.set_title("Age vs ZIP Code")
ax.set_xlabel("ZIP Code")
ax.set_ylabel("Age")
st.pyplot(fig)

# Correlation heatmap
st.subheader("Correlation Heatmap")
numeric_data = filtered_data[['offensezip', 'offenseage']].astype(float)
corr_matrix = numeric_data.corr()
fig, ax = plt.subplots()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlation Heatmap")
st.pyplot(fig)

# Show filtered data
st.header("Filtered Data")
st.write(filtered_data)
