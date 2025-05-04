import streamlit as st
import pandas as pd
from io import StringIO, BytesIO

st.set_page_config(page_title="Phone Cleaner", layout="centered")
st.title("📱 Attendee Phone Cleaner Tool")

st.markdown("Upload a **CSV or Excel file** with attendee data. This tool will:")
st.markdown("""
- Remove everything above the 'Attendee Details' section  
- Clean phone numbers (remove +91, 91, 0091, 0, single quotes)  
- Keep all other data intact  
- Give you back a cleaned Excel file (.xlsx)
""")

def clean_phone(phone):
    if pd.isna(phone):
        return phone
    phone = str(phone).strip().replace(" ", "").replace("'", "").replace('"', "")
    for prefix in ['+91', '0091', '91', '0']:
        if phone.startswith(prefix):
            phone = phone[len(prefix):]
            break
    return phone

def extract_attendee_df_from_csv(file):
    lines = file.read().decode('utf-8').splitlines()
    start_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith("First Name,Last Name,Email"):
            start_index = i
            break
    if start_index is None:
        return None
    csv_data = '\n'.join(lines[start_index:])
    return pd.read_csv(StringIO(csv_data))

uploaded_file = st.file_uploader("📤 Upload your file (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file is not None:
    file_name = uploaded_file.name
    try:
        if file_name.endswith(".csv"):
            df = extract_attendee_df_from_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        if df is None or "Phone" not in df.columns:
            st.error("❌ 'Phone' column ya attendee data section nahi mila.")
            st.stop()

        df["Phone"] = df["Phone"].apply(clean_phone)

        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        st.success("✅ Cleaning complete!")

        st.download_button(
            label="📥 Download Cleaned Excel File",
            data=output,
            file_name="cleaned_attendees.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
