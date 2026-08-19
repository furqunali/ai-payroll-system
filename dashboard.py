import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="SLP Payroll Control System", page_icon="🏢", layout="wide")

st.title("🏢 SLP Auto Payroll Control System")
st.caption(f"HR Dashboard - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Sidebar
with st.sidebar:
    st.header("👤 HR User Panel")
    user_role = st.selectbox("Select Role", ["HR Manager", "Site Manager", "Finance Director", "Payroll Admin"])
    st.divider()
    st.header("📊 Filters")
    selected_entities = st.multiselect(
        "Select Entities", 
        ["Houston Operations", "Dallas Distribution", "Austin Retail", 
         "San Antonio Logistics", "Fort Worth Production", "El Paso Field Ops"]
    )
    st.divider()
    st.caption("🔒 Secure Access | All actions logged")

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📋 Pending Approvals", "12", delta="-3", delta_color="normal")
with col2:
    st.metric("✅ Completed Today", "47", delta="+12", delta_color="normal")
with col3:
    st.metric("⏱️ Avg Processing Time", "4.2 hrs", delta="-2.8 hrs", delta_color="inverse")
with col4:
    st.metric("🤖 AI Confidence Score", "96%", delta="+2%", delta_color="normal")

# Main Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📝 Pending Approvals", "📊 Payroll Summary", "👁️ Receipt Validation", "📈 Analytics"])

# Tab 1: Pending Approvals
with tab1:
    st.subheader("Awaiting Your Approval")
    
    approval_data = pd.DataFrame({
        "Employee ID": ["SLP-1001", "SLP-1002", "SLP-1003", "SLP-1004", "SLP-1005"],
        "Employee Name": ["John Smith", "Maria Garcia", "David Lee", "Sarah Johnson", "Michael Brown"],
        "Entity": ["Houston Ops", "Dallas Dist", "Austin Retail", "Houston Ops", "San Antonio Logistics"],
        "Gross Pay": ["$5,250", "$4,890", "$6,120", "$4,750", "$5,450"],
        "Net Pay": ["$4,125", "$3,890", "$4,980", "$3,750", "$4,325"],
        "Submitted Date": ["2026-04-14", "2026-04-14", "2026-04-13", "2026-04-13", "2026-04-12"],
        "Status": ["🟡 Pending", "🟡 Pending", "🔴 Review", "🟡 Pending", "🟢 Auto-Approved"]
    })
    st.dataframe(approval_data, use_container_width=True, hide_index=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("✅ Approve Selected", type="primary", use_container_width=True)
    with col2:
        st.button("❌ Request Changes", type="secondary", use_container_width=True)

# Tab 2: Payroll Summary
with tab2:
    st.subheader("Entity-Wise Payroll Summary")
    
    payroll_summary = pd.DataFrame({
        "Entity": ["Houston Operations", "Dallas Distribution", "Austin Retail", "San Antonio Logistics", 
                   "Fort Worth Production", "El Paso Field Ops", "Corpus Christi Marine", "Midland Energy"],
        "Total Payroll": ["$128,450", "$95,230", "$112,890", "$78,340", "$104,560", "$67,890", "$89,230", "$156,780"],
        "Employee Count": [28, 22, 25, 18, 24, 15, 20, 32],
        "Processing Status": ["✅ Completed", "🔄 Processing", "🔄 Processing", "⏳ Pending", 
                              "✅ Completed", "⏳ Pending", "🔄 Processing", "✅ Completed"],
        "AI Confidence": ["98%", "94%", "96%", "92%", "97%", "91%", "95%", "98%"]
    })
    st.dataframe(payroll_summary, use_container_width=True, hide_index=True)
    
    # Summary chart
    st.subheader("Payroll Distribution")
    chart_data = pd.DataFrame({
        "Entity": ["Houston", "Dallas", "Austin", "San Antonio", "Fort Worth", "Midland"],
        "Payroll Amount": [128450, 95230, 112890, 78340, 104560, 156780]
    })
    st.bar_chart(chart_data.set_index("Entity"))

# Tab 3: Receipt Validation
with tab3:
    st.subheader("Gas Receipt Validation Queue")
    st.info("📸 AI Vision System is processing receipts - 23 pending validation")
    
    receipt_data = pd.DataFrame({
        "Receipt ID": ["RCP-001", "RCP-002", "RCP-003", "RCP-004", "RCP-005"],
        "Employee": ["Robert Chen", "Lisa Wong", "Michael Brown", "Patricia Lee", "James Wilson"],
        "Amount": ["$45.67", "$78.32", "$112.50", "$34.89", "$67.23"],
        "Date": ["2026-04-14", "2026-04-13", "2026-04-12", "2026-04-14", "2026-04-11"],
        "AI Confidence": ["98%", "76%", "94%", "99%", "82%"],
        "Status": ["✅ Auto-Approve", "⚠️ Review Needed", "✅ Auto-Approve", "✅ Auto-Approve", "⚠️ Review Needed"]
    })
    st.dataframe(receipt_data, use_container_width=True, hide_index=True)
    
    # Highlight low confidence receipts
    st.warning("⚠️ 2 receipts need manual review (confidence below 85%)")

# Tab 4: Analytics
with tab4:
    st.subheader("Payroll Performance Metrics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Processing Time Saved", "40+ hours/cycle", "↓ from 5-7 days to 24hrs")
    with col2:
        st.metric("Error Rate Reduction", "99%", "Near-zero errors")
    
    st.subheader("12-Entity Processing Status")
    entity_status = pd.DataFrame({
        "Entity Group": ["Energy", "Retail", "Logistics", "Production", "Corporate"],
        "Completed": [5, 3, 4, 2, 1],
        "In Progress": [1, 1, 0, 1, 0],
        "Pending": [0, 0, 0, 1, 0]
    })
    st.dataframe(entity_status, use_container_width=True, hide_index=True)

st.divider()
st.caption("🔒 SLP Auto Payroll Control System v1.0 | AI Orchestrated | Texas Compliant | All transactions audited")