# youtube-data-harvesting---project
This project elevates the retival of data fom particular social media or a domain
In this we have using youtube to obtain the data
Utilizing the YouTube API, the 'YouTube Data Harvesting' project collects information from YouTube. This is achieved through Python scripting to interact with the YouTube API. The gathered data is then stored in a MySQL database, where tables are created to organize the information effectively. The tables are later joined as needed to generate SQL query outputs. Finally, this data is presented in a Streamlit application for intuitive viewing and analysis using various visualization by some 10 insights.

#APPROACHES:
          Set up a Streamlit app,
          Connect to the YouTube API,
          Store and Clean data,
          Migrate data to a SQL data warehouse,
          Query the SQL data warehouse,
          Display data in the Streamlit app.


#SKILLS NEED FOR THIS PROJECT:
        Python scripting, 
        Data Collection, 
        Streamlit, 
        API integration, 
        Data Management using SQL.

#TECHNOLOGIES USED:
      Python 3.12.2
      MySQL(XAMPP)
      Pandas
      Streamlit
      API Integration

#INSTALLATION NEED:
      pip install google-api-python-client
      pip install mysql.connector
      pip install pandas
      pip install streamlit

      ( IMPORTANT: ALWAYS MUST USE USE THE PIP TO INSTALL ANY PACKAGES FOR PYTHON IN VS CODE)
      ( !pip or %pip)


  #LIBRARIES USED:
         Matplotlib -This library is the core plotting library in Python
         Seaborn -  Built on top of matplotlib, seaborn provides a higher-level interface for creating attractive and 
                    informative statistical visualizations.
          Numpy -       NumPy is a fundamental library for numerical computing in Python
          plotly.graph_objects as go- Plotly is an interactive plotting library that supports creating a wide variety 
                                     of visualizations,including graphs, charts, and maps
                                     

  #PACKAGES NEED TO IMPORT FOR THIS PROJECT:
        import streamlit as st
        import time
        import streamlit_option_menu
        from streamlit_option_menu import option_menu
        from googleapiclient.discovery import build
        import isodate
        import mysql.connector
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
        import plotly.graph_objects as go
        


