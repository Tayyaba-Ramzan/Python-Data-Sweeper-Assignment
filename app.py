import streamlit as st
import pandas as pd
import os
from io import BytesIO

# ⚙️ Configure Streamlit Page
st.set_page_config(page_title="Data Sweeper | Smart File Converter", page_icon="🚀", layout="wide")

# 🏆 Application Title
st.title("📂 Data Sweeper: Convert, Clean & Visualize Your Data Effortlessly")
st.caption("A powerful tool for data professionals to transform CSV and Excel files with seamless cleaning and visualization. ⚡")
st.markdown("---")

# 📤 File Upload Section
st.subheader("📥 Upload Your Data Files")
uploaded_files = st.file_uploader("Drag & drop or browse files (CSV / Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # 📥 Read File Based on Type
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file, engine="openpyxl")
            else:
                st.error(f"❌ Unsupported file format: `{file_ext}`")
                continue
        except Exception as e:
            st.error(f"⚠️ Error reading file `{file.name}`: {e}")
            continue

        # 📄 File Details
        st.subheader(f"📝 File: `{file.name}`")
        st.write(f"📏 **Size:** `{round(file.size/1024, 2)} KB`")
        st.write(f"📌 **Format:** `{file_ext.upper()}`")
        st.markdown("---")

        # 🔍 Data Preview
        st.subheader("👀 Quick Data Preview")
        st.dataframe(df.head())

        # 🛠️ Data Cleaning Section
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"🔄 Enable Cleaning for `{file.name}`"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"🚫 Remove Duplicates from `{file.name}`"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates successfully removed!")
            
            with col2:
                if st.button(f"🔍 Fill Missing Values in `{file.name}`"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values replaced with column averages!")

        # 🎛️ Column Selection for Conversion
        st.subheader("🎯 Select Columns for Export")
        columns = st.multiselect(f"🔹 Choose relevant columns for `{file.name}`", df.columns, default=df.columns)
        df = df[columns] if columns else df

        # 📊 Data Visualization
        st.subheader("📊 Data Insights & Visualization")
        if st.checkbox(f"📈 Generate Insights for `{file.name}`"):
            numeric_df = df.select_dtypes(include='number')
            if not numeric_df.empty:
                st.bar_chart(numeric_df.iloc[:, :2])
            else:
                st.warning("⚠️ No numeric data available for visualization!")

        # 🔄 File Conversion
        st.subheader("🔄 Export & Download")
        conversion_types = st.radio(f"📂 Convert `{file.name}` to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"🚀 Convert `{file.name}` Now"):
            buffer = BytesIO()
            file_name, mime_type = "", ""

            try:
                if conversion_types == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_types == "Excel":
                    df.to_excel(buffer, index=False, engine="openpyxl")
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)

                # ⬇️ Download Button
                st.download_button(
                    label=f"⬇️ Download `{file.name}` as `{conversion_types}`",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type,
                )
                st.success(f"🎉 `{file.name}` successfully converted to `{conversion_types}`!")

            except Exception as e:
                st.error(f"⚠️ Error during conversion: {e}")

st.markdown("---")
st.success("🥳🎉 **All files processed successfully!** Ready for the next task?")
