import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page configuration as the first Streamlit command
st.set_page_config(page_title="Student Dropout Dashboard", page_icon="📊", layout="wide")

# Load your data from GitHub raw URL
url = 'https://raw.githubusercontent.com/Davis-hub24/Student-Dropout-Prediction/main/3Signet_David_cleaned_data_1%20(1).csv'

try:
    df = pd.read_csv(url)
    st.write("Data loaded successfully!")
    st.write(df.head())  # Display the first few rows of the dataframe
except Exception as e:
    st.error(f"Failed to load data: {e}")

# Rest of your Streamlit code
st.title("Student Dropout Prediction Dashboard")
st.write("Explore the factors influencing student dropout rates.")

# Sidebar filters
st.sidebar.header("Filters")
age = st.sidebar.slider("Select Age at Enrollment", 18, 60, 25)
nationality = st.sidebar.selectbox("Select Nationality", ['All'] + list(df['Nationality'].unique()))
unemployment_rate = st.sidebar.slider("Unemployment Rate", float(df['Unemployment rate'].min()), float(df['Unemployment rate'].max()), float(df['Unemployment rate'].mean()))
gdp = st.sidebar.slider("GDP", float(df['GDP'].min()), float(df['GDP'].max()), float(df['GDP'].mean()))



# Filter data based on user input
filtered_df = df[(df['Age at enrollment'] >= age) &
                 (df['Unemployment rate'] >= unemployment_rate) &
                 (df['GDP'] >= gdp)]


st.sidebar.markdown("Use these filters to analyze the data more deeply.")

# Sidebar filters
st.sidebar.header("Filters")

# Filter by 'Target'
target = st.sidebar.selectbox("Select Target:", options=['All', 'Graduate', 'Dropout', 'Enrolled'], key="target_select")

# Other filters
age = st.sidebar.slider("Select Age at Enrollment", 18, 60, 25, key="age_slider")
nationality = st.sidebar.selectbox("Select Nationality", ['All'] + list(df['Nationality'].unique()), key="nationality_select")
unemployment_rate = st.sidebar.slider("Unemployment Rate", float(df['Unemployment rate'].min()), float(df['Unemployment rate'].max()), float(df['Unemployment rate'].mean()), key="unemployment_slider")
gdp = st.sidebar.slider("GDP", float(df['GDP'].min()), float(df['GDP'].max()), float(df['GDP'].mean()), key="gdp_slider")

# Key Metrics
total_enrollments = df.shape[0]
dropout_count = df[df['Target'] == 'Dropout'].shape[0]
graduate_count = df[df['Target'] == 'Graduate'].shape[0]
retention_rate = (graduate_count / total_enrollments) * 100
overall_dropout_rate = (dropout_count / total_enrollments) * 100

st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Enrollments", total_enrollments)
col2.metric("Dropout Count", dropout_count)
col3.metric("Graduate Count", graduate_count)
col4.metric("Overall Dropout Rate (%)", round(overall_dropout_rate, 2))
col4.metric("Retention Rate (%)", round(retention_rate, 2))

# Count the occurrences of each category in the 'Target' column
target_counts = df['Target'].value_counts()

# Create a pie chart
fig, ax = plt.subplots()
ax.pie(target_counts, labels=target_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Title for the pie chart
plt.title('Distribution of Target Classes')

# Display the pie chart in Streamlit
st.subheader("Target Distribution")
st.pyplot(fig)
# Insights Based on Selected Filters
# Create age groups based on 'Age at enrollment'
bins = [18, 25, 30, 35, 40, 45, 50, 60]
labels = ['18-25', '26-30', '31-35', '36-40', '41-45', '46-50', '51-60']
df['Age_Group'] = pd.cut(df['Age at enrollment'], bins=bins, labels=labels, right=False)

# Filter based on user selections
# Assuming filtered_df is already created based on the sidebar filters
filtered_df = df[(df['Age at enrollment'] >= 18) & (df['Unemployment rate'] >= 0) & (df['GDP'] >= 0)]

# Insights Based on Selected Filters
st.header("Key Metrics Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Dropouts", value=len(filtered_df[filtered_df['Target'] == 'Dropout']))

with col2:
    st.metric(label="Average Age at Enrollment", value=filtered_df['Age at enrollment'].mean())

with col3:
    st.metric(label="Average Unemployment Rate", value=filtered_df['Unemployment rate'].mean())

# Plot Dropout Rate by Age Group
st.subheader("Dropout Rate by Age Group")
fig, ax = plt.subplots(figsize=(10, 6))
age_dropout = filtered_df.groupby('Age_Group')['Target'].apply(lambda x: (x == 'Dropout').mean() * 100).reset_index()
sns.barplot(data=age_dropout, x='Age_Group', y='Target', ax=ax)
ax.set_title('Dropout Rate by Age Group')
ax.set_xlabel('Age Group')
ax.set_ylabel('Dropout Rate (%)')
st.pyplot(fig)


# Define the semesters to compare
semesters_to_compare = ['Curricular units 1st sem (grade)', 'Curricular units 2nd sem (grade)']

# Reshape the DataFrame to compare grades from two semesters
df_long = df.melt(id_vars=['Target'], value_vars=semesters_to_compare, var_name='Semester', value_name='Grade')
df_long['Semester'] = df_long['Semester'].replace({
    'Curricular units 1st sem (grade)': '1st semester',
    'Curricular units 2nd sem (grade)': '2nd semester'
})

# Plot Grade Progression vs Dropout
st.subheader("Grade Progression vs Dropout")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=df_long, x='Semester', y='Grade', hue='Target', ax=ax)
ax.set_title('Grade Progression Over Two Semesters vs Dropout')
ax.set_xlabel('Semester')
ax.set_ylabel('Grade')
st.pyplot(fig)

# Plot Dropout Rates Over Semesters
dropout_trend = df_long.groupby('Semester')['Target'].apply(lambda x: (x == 'Dropout').mean()).reset_index()
st.subheader("Dropout Rates Over Semesters")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=dropout_trend, x='Semester', y='Target', ax=ax)
ax.set_title('Dropout Rates Over Two Semesters')
ax.set_xlabel('Semester')
ax.set_ylabel('Dropout Rate')
st.pyplot(fig)

# Dropout Rates by Gender
st.subheader("Dropout Rates by Gender")
gender_dropout = df.groupby('Gender')['Target'].apply(lambda x: (x == 'Dropout').mean()).reset_index()
sns.barplot(data=gender_dropout, x='Gender', y='Target', ax=plt.gca())
plt.title("Average Dropout Rate by Gender")
plt.ylabel("Dropout Rate")
st.pyplot(plt)
plt.clf()


# Grade Distribution by Dropout Status
st.subheader("Grade Distribution by Dropout Status")
sns.boxplot(data=df, x='Target', y='Curricular units 1st sem (grade)')
plt.title("Grade Distribution by Dropout Status")
st.pyplot(plt)
plt.clf()

# Scholarship holder vs Dropout
df['Dropout'] = df['Target'].apply(lambda x: 'Dropout' if x == 'Dropout' else 'Not Dropout')
st.subheader("Scholarship holder vs Dropout")
fig, ax = plt.subplots()
sns.countplot(data=df, x='Dropout', hue='Scholarship holder', ax=ax)
st.pyplot(fig)

# Daytime/Evening Attendance vs Dropout
st.subheader("Daytime/evening attendance vs Target")
fig, ax = plt.subplots()
sns.countplot(data=df, x='Dropout', hue='Daytime/evening attendance', ax=ax)
st.pyplot(fig)

# Filtered Data
gender_filter = st.selectbox("Select Gender:", options=df['Gender'].unique())
filtered_df = df[df['Gender'] == gender_filter]
st.subheader(f"Filtered Data for {gender_filter}")
st.dataframe(filtered_df)
