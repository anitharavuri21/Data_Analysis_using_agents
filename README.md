# Data_Analysis_using_agents
Overview
This project automates the end-to-end data analysis workflow using AI agents powered by the AutoGen framework and Google Gemini API.

It breaks down the workflow into three specialized agents:

Data Engineer 🛠️ — Cleans and prepares the data

Data Analyst 📈 — Analyzes the cleaned data and extracts actionable insights

Visualizer 🎨 — Creates meaningful visualizations

The agents collaborate to automatically clean, analyze, and visualize your datasets with minimal manual intervention!

Features
---------
Automated data cleaning:
-----------------------

Handle missing values

Remove duplicates

Correct data types

Descriptive data analysis:
-------------------------

Statistical summaries

Correlation analysis

Pattern and anomaly detection

High-quality visualizations:
---------------------------

Histograms, heatmaps, scatter plots, time series, and more

Organized outputs:
------------------

Cleaned data saved to analysis/cleaned_data.csv

Analytical reports saved to analysis/analysis_results/

Visualizations saved to analysis/visuals/

Project Structure
-----------------

Data_Analysis_Using_Autogen/
│
├── analysis/
│   ├── cleaned_data.csv
│   ├── analysis_results/
│   ├── visuals/
│
├── sales_data.csv          # Sample dataset (you can replace this with your own)
├── main.py                 # Main script to run the backend AutoGen agents
├── front_end.py            # Front-end or UI to interact with the project
├── .env                    # Contains your GOOGLE_API_KEY
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
