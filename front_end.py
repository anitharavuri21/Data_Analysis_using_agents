# streamlit_app.py
import streamlit as st
import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt

from main import run_auto_analysis  # Make sure your script is properly modularized

# ================== STREAMLIT APP ==================

st.set_page_config(page_title="Auto Data Analyzer", layout="wide")

st.title("📊 Auto Data Analysis with Gemini + Autogen")
st.write("Upload a CSV file and automatically perform data cleaning, analysis, and visualization.")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    temp_input_path = os.path.join("temp_uploaded_file.csv")
    with open(temp_input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    if st.button("Run Auto Analysis 🚀"):
        with st.spinner('Running the full auto-analysis pipeline...'):
            # Clean up old outputs if exist
            if os.path.exists("analysis"):
                shutil.rmtree("analysis")
            os.makedirs("analysis", exist_ok=True)
            
            try:
                run_auto_analysis(temp_input_path)

                # Display cleaned data
                cleaned_path = "analysis/cleaned_data.csv"
                if os.path.exists(cleaned_path):
                    st.success("✅ Data cleaned successfully!")
                    cleaned_df = pd.read_csv(cleaned_path)
                    st.subheader("🔹 Cleaned Data Preview")
                    st.dataframe(cleaned_df.head())

                # Display analysis results
                analysis_folder = "analysis/analysis_results"
                if os.path.exists(analysis_folder):
                    st.success("✅ Analysis completed!")
                    analysis_files = [f for f in os.listdir(analysis_folder) if f.endswith('.csv') or f.endswith('.txt')]
                    for file in analysis_files:
                        st.subheader(f"📄 {file}")
                        file_path = os.path.join(analysis_folder, file)
                        if file.endswith(".csv"):
                            st.dataframe(pd.read_csv(file_path))
                        elif file.endswith(".txt"):
                            with open(file_path, 'r') as f:
                                st.text(f.read())

                # Show visualizations
                visuals_folder = "analysis/visuals"
                if os.path.exists(visuals_folder):
                    st.success("✅ Visualizations generated!")
                    image_files = [f for f in os.listdir(visuals_folder) if f.endswith(('.png', '.jpg'))]
                    for img_file in image_files:
                        st.subheader(f"🖼️ {img_file}")
                        img_path = os.path.join(visuals_folder, img_file)
                        st.image(img_path, use_column_width=True)

            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
            finally:
                # Optional: Clean up temp files
                if os.path.exists(temp_input_path):
                    os.remove(temp_input_path)
                    
    st.warning("Click 'Run Auto Analysis' after uploading your file.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit, AutoGen, and Gemini AI")

