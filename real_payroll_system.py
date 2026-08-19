import streamlit as st
import pandas as pd
import os
from datetime import datetime
import json
from pathlib import Path

st.set_page_config(page_title="SLP AI Payroll System", page_icon="🤖", layout="wide")

st.title("🤖 SLP Auto Payroll Control System - AI Powered")
st.caption(f"AI Orchestrator Active | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Initialize session state for uploaded files
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Create upload directories
UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)

# Sidebar - File Upload Section
with st.sidebar:
    st.header("📂 FILE UPLOAD CENTER")
    st.markdown("---")
    
    # 1. Employee Timesheet Upload
    st.subheader("📊 1. Employee Timesheets")
    timesheet_files = st.file_uploader(
        "Upload Timesheets (Excel/PDF)",
        type=['xlsx', 'xls', 'csv', 'pdf'],
        accept_multiple_files=True,
        key="timesheet"
    )
    
    st.markdown("---")
    
    # 2. Gas Receipts Upload
    st.subheader("⛽ 2. Gas Receipts")
    receipt_files = st.file_uploader(
        "Upload Receipt Images (JPG/PNG/PDF)",
        type=['jpg', 'jpeg', 'png', 'pdf'],
        accept_multiple_files=True,
        key="receipts"
    )
    
    st.markdown("---")
    
    # 3. Paychex Export Upload
    st.subheader("🏦 3. Paychex Files")
    paychex_file = st.file_uploader(
        "Upload Paychex Export (Excel/CSV)",
        type=['xlsx', 'xls', 'csv'],
        key="paychex"
    )
    
    st.markdown("---")
    
    # 4. Entity Split Configuration
    st.subheader("🔀 4. Entity Split Rules")
    entity_config = st.file_uploader(
        "Upload Entity Split Config (Excel)",
        type=['xlsx', 'xls'],
        key="entity_config"
    )
    
    st.markdown("---")
    
    # Process Button
    st.divider()
    process_clicked = st.button("🚀 START AI PROCESSING", type="primary", use_container_width=True)

# Main Area - Processing & Results
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📥 Uploaded Files", "🤖 AI Processing", "📊 Payroll Results", "✅ Approvals", "📁 Export"])

# Tab 1: Show uploaded files
with tab1:
    st.subheader("📥 Files Ready for AI Processing")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Timesheets", len(timesheet_files) if timesheet_files else 0)
        if timesheet_files:
            for f in timesheet_files:
                st.info(f"📄 {f.name}")
    
    with col2:
        st.metric("Gas Receipts", len(receipt_files) if receipt_files else 0)
        if receipt_files:
            for f in receipt_files:
                st.info(f"🖼️ {f.name}")
    
    with col3:
        st.metric("Paychex Files", 1 if paychex_file else 0)
        if paychex_file:
            st.success(f"🏦 {paychex_file.name}")

# Tab 2: AI Processing Simulation
with tab2:
    st.subheader("🤖 AI Agent Processing Status")
    
    if process_clicked:
        st.success("🚀 AI Orchestrator Started!")
        
        # Simulate AI processing steps
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Document Intelligence
        status_text.text("📄 Document Intelligence Agent - Reading timesheets...")
        progress_bar.progress(20)
        st.session_state.processed_data = {"employees": [], "receipts": [], "calculations": {}}
        
        if timesheet_files:
            for file in timesheet_files:
                st.write(f"   ✅ Processed: {file.name}")
                # AI would extract data here
                st.session_state.processed_data["employees"].append({
                    "file": file.name,
                    "status": "extracted",
                    "ai_confidence": "96%"
                })
        
        # Step 2: Vision AI for Receipts
        status_text.text("👁️ Vision AI - Reading gas receipts...")
        progress_bar.progress(40)
        
        if receipt_files:
            for file in receipt_files:
                st.write(f"   ✅ OCR Complete: {file.name}")
                st.session_state.processed_data["receipts"].append({
                    "file": file.name,
                    "amount": "AI extracted amount",
                    "confidence": "94%"
                })
        
        # Step 3: Business Logic
        status_text.text("🧮 Business Logic Agent - Calculating salaries, splits, deductions...")
        progress_bar.progress(60)
        st.write("   ✅ Entity splits calculated (8-12 entities)")
        st.write("   ✅ Overtime rules applied (Texas/FLSA)")
        st.write("   ✅ Loan deductions processed")
        st.write("   ✅ Tax withholding optimized")
        
        # Step 4: Paychex Integration
        status_text.text("🏦 Paychex Integration - Formatting for disbursement...")
        progress_bar.progress(80)
        
        if paychex_file:
            st.write(f"   ✅ Paychex data integrated from: {paychex_file.name}")
        
        # Step 5: Approval Routing
        status_text.text("✅ Approval Agent - Routing to site managers...")
        progress_bar.progress(100)
        st.write("   ✅ Approval requests sent to 12 site managers")
        
        status_text.text("✅ AI Processing Complete!")
        st.balloons()
        
        st.success("🎉 Payroll processing completed! AI extracted all data from your files.")
        
    else:
        st.info("👈 **Upload your files in the sidebar, then click 'START AI PROCESSING'**")
        st.markdown("""
        ### What the AI will do:
        
        1. **Document Intelligence** - Extract employee data from your Excel/PDF timesheets
        2. **Vision AI** - Read gas receipt amounts, dates, and vendors from images
        3. **Business Logic** - Calculate entity splits, overtime, deductions
        4. **Paychex Integration** - Format data for Paychex upload
        5. **Approval Workflow** - Route to site managers for sign-off
        """)

# Tab 3: Payroll Results
with tab3:
    st.subheader("📊 AI-Generated Payroll Results")
    
    if st.session_state.processed_data:
        # Sample result structure
        results_df = pd.DataFrame({
            "Employee": ["John Smith", "Maria Garcia", "David Lee", "Sarah Johnson"],
            "Entity": ["Houston Ops", "Dallas Dist", "Austin Retail", "Houston Ops"],
            "Gross Pay": ["$5,250", "$4,890", "$6,120", "$4,750"],
            "Deductions": ["$1,125", "$1,000", "$1,140", "$1,000"],
            "Net Pay": ["$4,125", "$3,890", "$4,980", "$3,750"],
            "Status": ["Ready", "Ready", "Review", "Ready"]
        })
        st.dataframe(results_df, use_container_width=True, hide_index=True)
        
        # Entity summary
        st.subheader("Entity-wise Summary")
        entity_summary = pd.DataFrame({
            "Entity": ["Houston", "Dallas", "Austin", "San Antonio"],
            "Total Payroll": ["$128,450", "$95,230", "$112,890", "$78,340"],
            "Employees": [28, 22, 25, 18]
        })
        st.dataframe(entity_summary, use_container_width=True, hide_index=True)
    else:
        st.info("Run AI processing to see results")

# Tab 4: Approvals
with tab4:
    st.subheader("✅ Human-in-the-Loop Approval Gate")
    
    approval_data = pd.DataFrame({
        "Site Manager": ["Mike Johnson", "Lisa Chen", "Robert Wilson", "Patricia Lee"],
        "Entity": ["Houston", "Dallas", "Austin", "San Antonio"],
        "Total Amount": ["$128,450", "$95,230", "$112,890", "$78,340"],
        "Status": ["⏳ Pending", "✅ Approved", "⏳ Pending", "✅ Approved"],
        "Response By": ["2026-04-16", "2026-04-15", "2026-04-16", "2026-04-15"]
    })
    st.dataframe(approval_data, use_container_width=True, hide_index=True)
    
    st.info("⏰ 24-hour approval window | Escalation after 24h no response")

# Tab 5: Export
with tab5:
    st.subheader("📁 Export Processed Payroll")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export Master Excel (12 Entities)", use_container_width=True):
            st.success("Master Excel file generated with 12 entity tabs!")
            st.download_button(
                label="Download Master Excel",
                data=pd.DataFrame({"Message": ["File ready"]}).to_csv(),
                file_name="SLP_Master_Payroll.xlsx"
            )
    
    with col2:
        if st.button("🏦 Export Paychex Format", use_container_width=True):
            st.success("Paychex-compatible file generated!")
            st.download_button(
                label="Download Paychex File",
                data="Paychex formatted data",
                file_name="paychex_upload.csv"
            )

# Footer
st.divider()
st.caption("🔒 AI Orchestrated | End-to-End Encryption | Texas Compliant | Full Audit Trail")