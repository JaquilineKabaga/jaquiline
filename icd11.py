import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Diagnosis Code Counter", layout="centered")

st.title("🩺 Diagnosis Code Range Counter")

# --- File Upload Section ---
uploaded_file = st.file_uploader("Upload a CSV, Excel, or TXT file", type=["csv", "xlsx", "xls", "txt"])

# --- Diagnosis Code Range Input ---
st.subheader("Enter ICD-11 Code Range")
col1, col2 = st.columns(2)
with col1:
    start_code = st.text_input("Start Code (e.g., 2A00)")
with col2:
    end_code = st.text_input("End Code (e.g., 2F9Z)")

# --- Function to extract ICD code from text ---
def extract_code(text):
    match = re.match(r"([A-Z0-9]+)", str(text))
    return match.group(1) if match else None

# --- Process uploaded file ---
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".txt"):
            df = pd.read_csv(uploaded_file, delimiter="\t")  # Assuming tab-delimited
        else:
            st.error("Unsupported file format.")
            st.stop()
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    st.success("File loaded successfully!")
    
    if "Diagnosis" not in df.columns:
        st.warning("No 'Diagnosis' column found in the file.")
    else:
        df["Code"] = df["Diagnosis"].apply(extract_code)

        if start_code and end_code:
            filtered_df = df[(df["Code"] >= start_code) & (df["Code"] <= end_code)]
            count = filtered_df.shape[0]

            st.subheader("Diagnosis Count in Range")
            st.info(f"🔍 Total diagnoses between `{start_code}` and `{end_code}`: **{count}**")

            with st.expander("Show Matching Diagnoses"):
                st.dataframe(filtered_df[["Diagnosis"]])
        else:
            st.info("Please enter both a start and end code.")
