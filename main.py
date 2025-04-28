import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import autogen
from dotenv import load_dotenv
from google.generativeai import configure

# ================== ENV SETUP ==================
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")
configure(api_key=GEMINI_API_KEY)

# ================== GEMINI CONFIG ==================
gemini_llm_config = {
    "config_list": [
        {
            "model": "gemini-2.0-flash-exp",
            "api_key": GEMINI_API_KEY,
            "api_type": "google",
            "base_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        }
    ],
    "timeout": 120,
    "temperature": 0.3,
}

# ================== AGENTS ==================
data_engineer = autogen.AssistantAgent(
    name="Data_Engineer",
    system_message="""You are a data cleaning expert. Your tasks:
    1. Load data from the dataframe that is passed to you in the context
    2. Fill missing numeric values with median, categorical with mode
    3. Remove duplicates
    4. Convert dtypes appropriately
    5. IMPORTANT: You MUST execute your code to actually clean the data
    6. IMPORTANT: You should only do data cleaning process only.. not the data analysis and visualizations..
    8. Print shape changes, head(3), and a summary of the changes you made
    9. save the summary of changes you have made in a folder with name 'data_cleaning'. you can give the descriptive filenames
    
    ```""",
    llm_config=gemini_llm_config
)

data_analyst = autogen.AssistantAgent(
    name="Data_Analyst",
    system_message="""You are a senior data analyst. Tasks:
    1. Take the cleaned dataframe provided in your context
    2. Generate descriptive statistics
    3. Calculate correlations between numeric columns
    4. Identify patterns and anomalies
    5. IMPORTANT: You MUST execute your code to perform the analysis
    6. IMPORTANT: You should only do the analysis part and find the key insights and patterns
    6. Output: Clear summary with 3 key insights, table summaries, and any issue highlights
    ```""",
    llm_config=gemini_llm_config
)

visualizer = autogen.AssistantAgent(
    name="Visualizer",
    system_message="""You create visualizations:
    1. Use the cleaned dataframe provided in your context
    2. Create the following plots:
       - Histograms/KDE for numeric columns
       - Correlation heatmap
       - Scatter plots for correlated features
       - Time series plots if date columns are present
       - Bar plots for comparision
    3. IMPORTANT: You MUST execute your code to generate the visualizations
    4. IMPORTANT: Save all plots as PNG files in the visuals folder created in current working directory
    5. Use seaborn and matplotlib with clear labels, titles, and appropriate color schemes
    6. Return a list of the saved filenames
    
    ```""",
    llm_config=gemini_llm_config
)

# Using NEVER instead of TERMINATE ensures the code execution happens
user_proxy = autogen.UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",  # Changed from TERMINATE
    max_consecutive_auto_reply=6,
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    code_execution_config={
        "work_dir": "analysis",
        "use_docker": False
    },
    default_auto_reply=None
)

# ================== SAMPLE DATA ==================

# ================== AUTO ANALYSIS ==================
def run_auto_analysis(file_path):
    print("=== STEP 1: Loading Data ===")
    working_dir='analysis'
    os.makedirs(working_dir,exist_ok=True)
    copied_path=os.path.join(working_dir,file_path)
    df=pd.read_csv(file_path)
    df.to_csv(copied_path, index=False)
    
    print("\n=== STEP 2: Data Cleaning ===")
    # Pass the dataframe directly in the message for more reliable handling
    cleaning_message = f"""
    Please clean the dataframe loaded from {file_path}. 
    
    Apply your data cleaning procedures and return the cleaned dataframe.
    save the cleaned dataframe to current directory as 'cleaned_data.csv'
    """
    
    # Use a one-to-one chat for more reliable data transfer
    user_proxy.initiate_chat(data_engineer, message=cleaning_message)

    print("\n=== STEP 3: Data Analysis ===")
    cleaned_data_path='cleaned_data.csv'
    analysis_message = f"""
    Please analyze the cleaned data in cleaned_data.csv in current working directory and extract insights.
    Perform your analysis and summarize the key findings about the features that you found interesting.
    example:
    if you are having an ecommerce data, find interesting facts like which item is having more sales. why an item is becoming popular, what item will get more sales in future etc.. 
    you need to give that type of information for eact dataset you are working on. 
    you need to give the useful and interesting information to the user from your analysis of the dataset.
    please create a folder 'analysis_results' and save your analysis results in to that folder in working directory
    """
    
    # Use a one-to-one chat for more reliable data transfer
    user_proxy.initiate_chat(data_analyst, message=analysis_message)

    print("\n=== STEP 4: Visualization ===")
    viz_message = f"""
    Please generate visualizations for the cleaned_data.csv in current working directory.  
    Generate and save the following visualizations:
    create a folder 'visuals' and Save all plots to that folder in working directory with descriptive filenames.
    """
    
    # Use a one-to-one chat for more reliable data transfer
    user_proxy.initiate_chat(visualizer, message=viz_message)
    
    # List the generated visualization files
    print("\n ANALYSIS COMPLETE")
    viz_files = [f for f in os.listdir("analysis/visuals") if f.endswith(('.png', '.jpg'))]
    print(f"Generated {len(viz_files)} visualization files:")
    for viz in viz_files:
        print(f"   - {viz}")
    print(f"Files saved in: {os.path.abspath('analysis/visuals')}")

# ================== MAIN ==================
if __name__ == "__main__":
    os.makedirs("analysis", exist_ok=True)
    try:
        run_auto_analysis('sales_data.csv')
    except Exception as e:
        print(f"Analysis failed: {str(e)}")
    finally:
        print("Cleaning up...")
        plt.close('all')