import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List

def create_chart(data: List[float], chart_type: str):
    if not data:
        st.warning("No data provided for visualization.")
        return None

    fig, ax = plt.subplots()
    
    try:
        if chart_type == "Bar":
            sns.barplot(x=range(len(data)), y=data, ax=ax)
        elif chart_type == "Pie":
            ax.pie(data, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
        elif chart_type == "Histogram":
            sns.histplot(data=data, ax=ax)
        else:
            st.warning(f"Unsupported chart type: {chart_type}")
            return None
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None
    
    return fig
