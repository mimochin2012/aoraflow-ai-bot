# Agents/data_agent.py - إصدار مستقر مع PDF بالإنجليزية
import os
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import requests
import tempfile
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gpt-oss:120b-cloud"
REPORT_DIR = "Reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def call_ollama(prompt):
    try:
        payload = {"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.3, "num_predict": 800}}
        r = requests.post(OLLAMA_URL, json=payload, timeout=90)
        return r.json().get("response", "Unable to generate insights.")
    except:
        return "Error connecting to AI model."

def create_pdf(df, insights, file_name, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "AoraFlow AI - Data Analysis Report", ln=1, align="C")
    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 8, f"File: {file_name}", ln=1)
    pdf.cell(0, 8, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=1)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Basic Statistics:", ln=1)
    pdf.set_font("Helvetica", size=9)
    stats = df.describe().round(2)
    for col in list(stats.columns)[:6]:
        pdf.cell(0, 6, f"{col}: mean={stats[col]['mean']:.2f}, max={stats[col]['max']:.2f}", ln=1)
    
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "AI Insights:", ln=1)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, insights[:1800])
    pdf.output(output_path)

def data_agent(state):
    print("📊 Data Agent (PDF) يعمل...")
    file_path = state.get("file_path")
    file_name = state.get("file_name", "unknown.xlsx")
    
    if not file_path or not os.path.exists(file_path):
        state["messages"].append("📁 Please send a CSV or Excel file for analysis.")
        return state

    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        stats_text = df.describe().to_string()[:1000]
        insights = call_ollama(f"Analyze this business data and give 5 practical recommendations:\n{stats_text}")
        
        pdf_path = os.path.join(REPORT_DIR, f"Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        create_pdf(df, insights, file_name, pdf_path)
        
        state["messages"].append(f"✅ **Analysis complete!**\n\n📊 Rows: {len(df)}\n📋 Columns: {len(df.columns)}\n\n📄 PDF report attached.")
        state["pdf_to_send"] = pdf_path
        
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        state["messages"].append(f"❌ Error: {str(e)[:150]}")
    
    return state
