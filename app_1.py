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

# Rest of your Streamlit app code
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

# Filter by 'Target'
target = st.sidebar.selectbox("Select Target:", options=['All', 'Graduate', 'Dropout', 'Enrolled'], key="target_select")

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

# Create a pie chart for target distribution
target_counts = df['Target'].value_counts()
fig, ax = plt.subplots()
ax.pie(target_counts, labels=target_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
plt.title('Distribution of Target Classes')
st.subheader("Target Distribution")
st.pyplot(fig)

# Insights Based on Selected Filters
bins = [18, 25, 30, 35, 40, 45, 50, 60]
labels = ['18-25', '26-30', '31-35', '36-40', '41-45', '46-50', '51-60']
df['Age_Group'] = pd.cut(df['Age at enrollment'], bins=bins, labels=labels, right=False)

# Dropout Rate by Age Group
st.subheader("Dropout Rate by Age Group")
fig, ax = plt.subplots(figsize=(10, 6))
age_dropout = filtered_df.groupby('Age_Group')['Target'].apply(lambda x: (x == 'Dropout').mean() * 100).reset_index()
sns.barplot(data=age_dropout, x='Age_Group', y='Target', ax=ax)
ax.set_title('Dropout Rate by Age Group')
ax.set_xlabel('Age Group')
ax.set_ylabel('Dropout Rate (%)')
st.pyplot(fig)

# Grade Progression vs Dropout
semesters_to_compare = ['Curricular units 1st sem (grade)', 'Curricular units 2nd sem (grade)']
df_long = df.melt(id_vars=['Target'], value_vars=semesters_to_compare, var_name='Semester', value_name='Grade')
df_long['Semester'] = df_long['Semester'].replace({
    'Curricular units 1st sem (grade)': '1st semester',
    'Curricular units 2nd sem (grade)': '2nd semester'
})

st.subheader("Grade Progression vs Dropout")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=df_long, x='Semester', y='Grade', hue='Target', ax=ax)
ax.set_title('Grade Progression Over Two Semesters vs Dropout')
ax.set_xlabel('Semester')
ax.set_ylabel('Grade')
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
