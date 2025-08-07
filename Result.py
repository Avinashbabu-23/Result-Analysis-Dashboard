import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Set_page_config (title and icon in browser tab)

st.set_page_config(
page_title="Result Analyzer",
page_icon="📊",
layout="wide"
)

#Page title
st.title("Result_Analysis Dashboard")
#st.markdown("###please use the sidebar to upload the excel and begin analysis")

#Sidebar for file upload

st.sidebar.header("Input Panel")
uploaded_file = st.sidebar.file_uploader("C:\\Users\ppull\AppData\Roaming\Python\Python313\Scripts\Result.xlsx", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

# AAT Analysis  
    aat_columns = ['Roll Number', 'Name', 's1a1', 's1a2', 's2a1', 's2a2', 's3a1', 's3a2', 's4a1', 's4a2', 's5a1', 's5a2', 's6a1', 's6a2']  
    aat_data = df[aat_columns].copy()  
    aat_data.replace('A', pd.NA, inplace=True)  
    score_columns = [col for col in aat_columns if col not in ['Roll Number', 'Name']]  
    aat_data[score_columns] = aat_data[score_columns].apply(pd.to_numeric, errors='coerce')  
    aat_data.fillna(0, inplace=True)  

for i in range(1, 7):  
    aat_data[f'Subject {i} aatAverage'] = (aat_data[f's{i}a1'] + aat_data[f's{i}a2']) / 2  

result1 = aat_data[['Roll Number', 'Name'] + [f'Subject {i} aatAverage' for i in range(1, 7)]]  
  
# Mid Exam Analysis  
mid_columns = ['Roll Number', 'Name', 's1m1', 's1m2', 's2m1', 's2m2', 's3m1', 's3m2', 's4m1', 's4m2', 's5m1', 's5m2', 's6m1', 's6m2']  
mid_data = df[mid_columns].copy()  
mid_data.replace('A', pd.NA, inplace=True)  
mid_score_columns = [col for col in mid_columns if col not in ['Roll Number', 'Name']]  
mid_data[mid_score_columns] = mid_data[mid_score_columns].apply(pd.to_numeric, errors='coerce')  
mid_data.fillna(0, inplace=True)  

for i in range(1, 7):  
    max_marks = mid_data[[f's{i}m1', f's{i}m2']].max(axis=1)  
    min_marks = mid_data[[f's{i}m1', f's{i}m2']].min(axis=1)  
    mid_data[f'Subject {i} midAverage'] = ((max_marks * 0.75) + (min_marks * 0.25)) * 20 / 35  

result2 = mid_data[['Roll Number', 'Name'] + [f'Subject {i} midAverage' for i in range(1, 7)]]  

# Merge and compute internal  
merged_result = pd.merge(result1, result2, on=['Roll Number', 'Name'])  
for i in range(1, 7):  
    merged_result[f's{i}internal'] = np.ceil(  
        merged_result[f'Subject {i} aatAverage'] + merged_result[f'Subject {i} midAverage']  
    )  

final_result = merged_result[['Roll Number', 'Name'] + [f's{i}internal' for i in range(1, 7)]]  
# Status assignment  
for i in range(1, 7):  
    final_result[f's{i}status'] = np.where(final_result[f's{i}internal'] < 15, 'NQ', 'Q')  
  
# Calculate percentages for NQ students  
total_students = len(final_result)  
nq_counts = final_result[[f's{i}status' for i in range(1, 7)]].apply(lambda x: (x == 'NQ').sum())  
nq_percentages = (nq_counts / total_students) * 100  # Convert to percentage  
  
# Create tabs for separate sections  
tab1, tab2, tab3 = st.tabs(["📊 Box Plot Internal Marks", "📝 Final Internal Marks and Status", "🔢 Number of NQ Students per Subject"])  

with tab1:  
    st.subheader("Box Plot of Internal Marks")  
    fig, ax = plt.subplots(figsize=(10, 6))  
    ax.boxplot(final_result[[f's{i}internal' for i in range(1, 7)]].values, labels=[f'Subject {i}' for i in range(1, 7)])  
    ax.set_title('Box Plot of Internal Marks for Each Subject')  
    ax.set_xlabel('Subject')  
    ax.set_ylabel('Internal Marks')  
    st.pyplot(fig)  

with tab2:  
    st.subheader("Final Internal Marks and Status")  
    st.dataframe(final_result)  

with tab3:  
    st.subheader("Number of NQ Students per Subject")  
    fig, ax = plt.subplots(figsize=(10, 6))  
    ax.bar(nq_percentages.index,nq_percentages.values)  
    ax.set_title('percentage of NQ Statuses for Each Subject')  
    ax.set_xlabel('Subject')  
    ax.set_ylabel('NQ Percentage (%)')  
    ax.tick_params(axis='x', rotation=45)  
    st.pyplot(fig)  

# Download option placed in the sidebar  
st.sidebar.download_button("Download Final Result as CSV", final_result.to_csv(index=False), file_name='final_result.csv')  
# to run using this "python -m streamlit run new.py"


