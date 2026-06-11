import  streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import re

# Page configuration
st.set_page_config(
    page_title="Ramah Operations Dashboard",
    page_icon="🏗️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stAlert {
        padding: 10px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .overdue-text {
        color: #ff4444;
        font-weight: bold;
    }
    .due-soon-text {
        color: #ff9800;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🏗️ RAMAH General Contracting Operations Dashboard")
st.markdown("**Transport LLC - Project Management & Tracking**")

# File upload section
st.sidebar.header("📁 Data Source")
uploaded_file = st.sidebar.file_uploader(
    "Upload Operations Spreadsheet",
    type=['xlsx', 'xls', 'csv']
)

# Alternatively, allow file path input
file_path = st.sidebar.text_input("Or enter file path:")

# Function to load and clean data
@st.cache_data
def load_data(file_source):
    try:
        if isinstance(file_source, str):
            # Loading from file path
            if file_source.endswith('.csv'):
                df = pd.read_csv(file_source)
            else:
                df = pd.read_excel(file_source)
        else:
            # Loading from uploaded file
            if file_source.name.endswith('.csv'):
                df = pd.read_csv(file_source)
            else:
                df = pd.read_excel(file_source)
        
        # Convert date columns to datetime - handle multiple date formats
        date_columns = ['EDD at Site', 'Requested Date', 'ECD', 'ECD of PDI', 'EDD at Site.1']
        for col in date_columns:
            if col in df.columns:
                # Try multiple date formats
                df[col] = pd.to_datetime(df[col], format='%d-%b-%Y', errors='coerce')
                if df[col].isna().all():  # If first format didn't work
                    df[col] = pd.to_datetime(df[col], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

# Function to categorize tasks
def categorize_task(task_description, module_name, remarks):
    """Categorize tasks into Logistics, Payments, Transport, etc."""
    if pd.isna(task_description):
        task_description = ""
    if pd.isna(module_name):
        module_name = ""
    if pd.isna(remarks):
        remarks = ""
    
    text = f"{task_description} {module_name} {remarks}".lower()
    
    # Define keywords for each category
    if any(word in text for word in ['transport', 'vehicle', 'truck', 'driver', 'fleet', 'delivery']):
        return 'Transport'
    elif any(word in text for word in ['payment', 'invoice', 'billing', 'payable', 'receivable', 'financial', 'salary', 'expense']):
        return 'Payments'
    elif any(word in text for word in ['logistics', 'warehouse', 'inventory', 'stock', 'equipment', 'asset', 'supply', 'hire purchase']):
        return 'Logistics'
    elif any(word in text for word in ['purchase', 'procurement', 'supplier', 'vendor', 'order']):
        return 'Procurement'
    elif any(word in text for word in ['hr', 'employee', 'staff', 'user master', 'payroll', 'attendance']):
        return 'HR & Admin'
    elif any(word in text for word in ['project', 'contract', 'site', 'construction']):
        return 'Project Management'
    elif any(word in text for word in ['database', 'migration', 'configuration', 'system', 'software', 'module', 'installation', 'menu setting']):
        return 'IT & Systems'
    elif any(word in text for word in ['account', 'finance', 'opening data', 'financial transaction']):
        return 'Finance & Accounts'
    else:
        return 'General'

# Function to get date status
def get_date_status(due_date, status):
    """Determine if task is overdue, due soon, or on track"""
    if pd.isna(due_date):
        return 'no_date'
    
    today = pd.Timestamp(datetime.now().date())
    due_date = pd.Timestamp(due_date.date())
    
    # If task is done, it's not overdue
    if status == 'Done':
        return 'completed'
    
    # Calculate days difference
    days_diff = (due_date - today).days
    
    if days_diff < 0:
        return 'overdue'
    elif days_diff <= 7:
        return 'due_soon'
    else:
        return 'on_track'

# Load data
df = None
if uploaded_file is not None:
    df = load_data(uploaded_file)
elif file_path:
    df = load_data(file_path)

# Main dashboard
if df is not None:
    st.success("✅ Data loaded successfully!")
    
    # Show data info
    with st.expander("ℹ️ Data Information"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Total Rows:** {len(df)}")
        with col2:
            st.write(f"**Total Columns:** {len(df.columns)}")
        with col3:
            date_col_exists = 'EDD at Site' in df.columns
            st.write(f"**Due Date Column:** {'✅ Found' if date_col_exists else '❌ Not Found'}")
    
    # Add category column
    df['Category'] = df.apply(
        lambda row: categorize_task(
            row['Work Breakdown Structure Task Description'],
            row.get('Module Name', ''),
            row.get('Remarks', '')
        ),
        axis=1
    )
    
    # Fill empty status with "Pending" (tasks with no status are pending)
    if 'Current Status' in df.columns:
        df['Current Status'] = df['Current Status'].replace('', 'Pending')
        df['Current Status'] = df['Current Status'].fillna('Pending')
        df['Current Status'] = df['Current Status'].astype(str)
        df['Current Status'] = df['Current Status'].replace('nan', 'Pending')
    
    # Add date status column
    if 'EDD at Site' in df.columns:
        df['Date Status'] = df.apply(
            lambda row: get_date_status(row['EDD at Site'], row.get('Current Status', '')),
            axis=1
        )
    
    # Show raw data option
    with st.expander("📋 View Raw Data"):
        st.dataframe(df, use_container_width=True)
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Category filter
    categories = ['All'] + sorted(df['Category'].unique().tolist())
    selected_category = st.sidebar.selectbox("Category", categories)
    
    if selected_category != 'All':
        df_filtered = df[df['Category'] == selected_category].copy()
    else:
        df_filtered = df.copy()
    
    # Status filter
    status_options = ['All']
    if 'Current Status' in df.columns:
        status_options += sorted(df['Current Status'].dropna().unique().tolist())
    selected_status = st.sidebar.selectbox("Status", status_options)
    
    if selected_status != 'All':
        df_filtered = df_filtered[df_filtered['Current Status'] == selected_status]
    
    # Date-based filters
    st.sidebar.subheader("📅 Due Date Filters")
    
    date_filter_option = st.sidebar.radio(
        "Show tasks:",
        ["All Tasks", "With Due Dates Only", "Overdue Only", "Due This Week", "No Due Date"]
    )
    
    if 'EDD at Site' in df_filtered.columns:
        if date_filter_option == "With Due Dates Only":
            df_filtered = df_filtered[df_filtered['EDD at Site'].notna()]
        elif date_filter_option == "Overdue Only":
            df_filtered = df_filtered[df_filtered['Date Status'] == 'overdue']
        elif date_filter_option == "Due This Week":
            df_filtered = df_filtered[df_filtered['Date Status'].isin(['due_soon', 'overdue'])]
        elif date_filter_option == "No Due Date":
            df_filtered = df_filtered[df_filtered['EDD at Site'].isna()]
    
    # Search functionality
    search_term = st.sidebar.text_input("🔎 Search tasks:", "")
    if search_term:
        df_filtered = df_filtered[
            df_filtered['Work Breakdown Structure Task Description'].str.contains(search_term, case=False, na=False) |
            df_filtered['Remarks'].astype(str).str.contains(search_term, case=False, na=False)
        ]
    
    # Key Metrics
    st.header("📈 Key Metrics")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        total_tasks = len(df_filtered)
        st.metric("Total Tasks", total_tasks)
    
    with col2:
        completed = len(df_filtered[df_filtered['Current Status'] == 'Done'])
        completion_rate = (completed / total_tasks * 100) if total_tasks > 0 else 0
        st.metric("Completed", completed, f"{completion_rate:.1f}%")
    
    with col3:
        pending = len(df_filtered[df_filtered['Current Status'] == 'Pending'])
        st.metric("Pending", pending)
    
    with col4:
        in_progress = len(df_filtered[
            (df_filtered['Current Status'] != 'Done') & 
            (df_filtered['Current Status'] != 'Pending')
        ])
        st.metric("In Progress", in_progress)
    
    with col5:
        if 'EDD at Site' in df_filtered.columns:
            overdue = len(df_filtered[df_filtered['Date Status'] == 'overdue'])
            st.metric("🚨 Overdue", overdue, delta=f"-{overdue}" if overdue > 0 else "0", delta_color="inverse")
        else:
            st.metric("Overdue", "N/A")
    
    with col6:
        if 'EDD at Site' in df_filtered.columns:
            no_date = len(df_filtered[df_filtered['EDD at Site'].isna()])
            st.metric("No Due Date", no_date)
        else:
            st.metric("No Due Date", total_tasks)
    
    # Progress bar
    if total_tasks > 0:
        progress = completed / total_tasks
        st.progress(progress)
        st.caption(f"Overall Progress: {progress*100:.1f}% ({completed} of {total_tasks} tasks completed)")
    
    # Date Summary Section
    if 'EDD at Site' in df_filtered.columns:
        st.header("📅 Due Date Summary")
        
        date_col1, date_col2, date_col3, date_col4 = st.columns(4)
        
        with date_col1:
            with_dates = len(df_filtered[df_filtered['EDD at Site'].notna()])
            st.metric("Tasks with Due Dates", with_dates)
        
        with date_col2:
            overdue_count = len(df_filtered[df_filtered['Date Status'] == 'overdue'])
            st.metric("🔴 Overdue", overdue_count)
        
        with date_col3:
            due_soon_count = len(df_filtered[df_filtered['Date Status'] == 'due_soon'])
            st.metric("🟡 Due This Week", due_soon_count)
        
        with date_col4:
            on_track_count = len(df_filtered[df_filtered['Date Status'] == 'on_track'])
            st.metric("🟢 On Track", on_track_count)
    
    # Visualizations
    st.header("📊 Analytics")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        # Category distribution
        st.subheader("Tasks by Category")
        category_counts = df_filtered['Category'].value_counts()
        fig_category = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title="Distribution by Category",
            hole=0.4
        )
        fig_category.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_category, use_container_width=True)
    
    with viz_col2:
        # Status distribution
        st.subheader("Tasks by Status")
        status_counts = df_filtered['Current Status'].value_counts()
        
        colors = {
            'Done': '#28a745',
            'Pending': '#ffc107',
            'In Progress': '#17a2b8'
        }
        color_list = [colors.get(status, '#6c757d') for status in status_counts.index]
        
        fig_status = px.bar(
            x=status_counts.index,
            y=status_counts.values,
            title="Status Overview",
            labels={'x': 'Status', 'y': 'Count'},
            color=status_counts.index,
            color_discrete_sequence=color_list
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    # Date Status Distribution (if dates exist)
    if 'EDD at Site' in df_filtered.columns and df_filtered['Date Status'].notna().any():
        st.subheader("📅 Due Date Status Distribution")
        
        date_status_counts = df_filtered['Date Status'].value_counts()
        
        date_status_labels = {
            'overdue': '🔴 Overdue',
            'due_soon': '🟡 Due This Week',
            'on_track': '🟢 On Track',
            'completed': '✅ Completed',
            'no_date': '⚪ No Date'
        }
        
        date_status_colors = {
            'overdue': '#ff4444',
            'due_soon': '#ff9800',
            'on_track': '#4caf50',
            'completed': '#2196f3',
            'no_date': '#9e9e9e'
        }
        
        labels = [date_status_labels.get(status, status) for status in date_status_counts.index]
        colors_list = [date_status_colors.get(status, '#6c757d') for status in date_status_counts.index]
        
        fig_date_status = px.pie(
            values=date_status_counts.values,
            names=labels,
            title="Tasks by Due Date Status",
            color=date_status_counts.index,
            color_discrete_sequence=colors_list
        )
        st.plotly_chart(fig_date_status, use_container_width=True)
    
    # Timeline chart
    if 'EDD at Site' in df_filtered.columns and df_filtered['EDD at Site'].notna().any():
        st.subheader("📅 Task Timeline")
        
        timeline_df = df_filtered[df_filtered['EDD at Site'].notna()].copy()
        timeline_df = timeline_df.sort_values('EDD at Site')
        
        # Add color based on date status
        color_map = {
            'overdue': 'red',
            'due_soon': 'orange',
            'on_track': 'green',
            'completed': 'blue',
            'no_date': 'gray'
        }
        
        fig_timeline = px.scatter(
            timeline_df,
            x='EDD at Site',
            y='WBS Sr#',
            color='Date Status',
            color_discrete_map=color_map,
            hover_data=['Work Breakdown Structure Task Description', 'Current Status'],
            title="Tasks Timeline by Due Date (EDD at Site)",
            labels={'EDD at Site': 'Due Date', 'WBS Sr#': 'WBS Number'}
        )
        
        # Add vertical line for today
        today = datetime.now()
        fig_timeline.add_vline(x=today, line_dash="dash", line_color="red", 
                               annotation_text="Today", annotation_position="top")
        
        fig_timeline.update_layout(height=500)
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Tasks by Category - Detailed View
    st.header("📋 Detailed Tasks by Category")
    
    categories_list = sorted(df_filtered['Category'].unique())
    
    for category in categories_list:
        category_df = df_filtered[df_filtered['Category'] == category].copy()
        
        with st.expander(f"**{category}** ({len(category_df)} tasks)", expanded=(selected_category == category)):
            # Category statistics
            cat_col1, cat_col2, cat_col3, cat_col4, cat_col5 = st.columns(5)
            with cat_col1:
                st.write(f"**Total:** {len(category_df)}")
            with cat_col2:
                completed_cat = len(category_df[category_df['Current Status'] == 'Done'])
                st.write(f"**Completed:** {completed_cat}")
            with cat_col3:
                pending_cat = len(category_df[category_df['Current Status'] == 'Pending'])
                st.write(f"**Pending:** {pending_cat}")
            with cat_col4:
                if 'Date Status' in category_df.columns:
                    overdue_cat = len(category_df[category_df['Date Status'] == 'overdue'])
                    st.write(f"**Overdue:** {overdue_cat}")
            with cat_col5:
                if 'EDD at Site' in category_df.columns:
                    no_date_cat = len(category_df[category_df['EDD at Site'].isna()])
                    st.write(f"**No Date:** {no_date_cat}")
            
            st.divider()
            
            # Display tasks
            for idx, row in category_df.iterrows():
                cols = st.columns([0.5, 3, 1.5, 1.2, 1])
                
                # WBS Number
                with cols[0]:
                    st.write(f"**{row['WBS Sr#']}**")
                
                # Task description
                with cols[1]:
                    task_text = str(row['Work Breakdown Structure Task Description'])
                    
                    # Strikethrough for completed tasks
                    if row['Current Status'] == 'Done':
                        st.markdown(f"~~{task_text}~~")
                    else:
                        st.write(task_text)
                    
                    # Show remarks if available
                    if pd.notna(row['Remarks']) and str(row['Remarks']).strip():
                        st.caption(f"💬 {row['Remarks']}")
                
                # Status
                with cols[2]:
                    status_value = str(row['Current Status'])
                    
                    if status_value == 'Done':
                        st.success(f"✅ {status_value}")
                    elif status_value == 'Pending':
                        st.warning(f"⏳ {status_value}")
                    else:
                        st.info(f"🔄 {status_value}")
                
                # Due date (EDD at Site)
                with cols[3]:
                    if 'EDD at Site' in row.index and pd.notna(row['EDD at Site']):
                        due_date = pd.to_datetime(row['EDD at Site'])
                        today = pd.Timestamp(datetime.now().date())
                        days_diff = (due_date.date() - today.date()).days
                        
                        # Color code based on status
                        if row['Current Status'] == 'Done':
                            st.success(f"📅 {due_date.strftime('%d-%b-%Y')}")
                        elif days_diff < 0:
                            st.error(f"🚨 {due_date.strftime('%d-%b-%Y')}")
                            st.caption(f"⏰ {abs(days_diff)} days overdue")
                        elif days_diff <= 7:
                            st.warning(f"⚠️ {due_date.strftime('%d-%b-%Y')}")
                            st.caption(f"⏰ Due in {days_diff} days")
                        else:
                            st.info(f"📅 {due_date.strftime('%d-%b-%Y')}")
                            st.caption(f"⏰ {days_diff} days left")
                    else:
                        st.write("📅 No due date")
                
                # Requested date
                with cols[4]:
                    if 'Requested Date' in row.index and pd.notna(row['Requested Date']):
                        req_date = pd.to_datetime(row['Requested Date'])
                        st.caption(f"📥 Requested:")
                        st.caption(f"{req_date.strftime('%d-%b-%Y')}")
                    else:
                        st.caption("📥 Not specified")
                
                st.divider()
    
    # Upcoming Deadlines Section
    if 'EDD at Site' in df_filtered.columns:
        st.header("⏰ Upcoming Deadlines (Next 30 Days)")
        
        today = pd.Timestamp(datetime.now().date())
        future_30_days = today + timedelta(days=30)
        
        upcoming_df = df_filtered[
            (df_filtered['EDD at Site'].notna()) &
            (df_filtered['EDD at Site'] >= today) &
            (df_filtered['EDD at Site'] <= future_30_days) &
            (df_filtered['Current Status'] != 'Done')
        ].sort_values('EDD at Site')
        
        if len(upcoming_df) > 0:
            for idx, row in upcoming_df.iterrows():
                due_date = pd.to_datetime(row['EDD at Site'])
                days_until = (due_date.date() - today.date()).days
                
                col1, col2, col3, col4 = st.columns([0.5, 3, 1.5, 1])
                
                with col1:
                    st.write(f"**{row['WBS Sr#']}**")
                
                with col2:
                    st.write(row['Work Breakdown Structure Task Description'])
                
                with col3:
                    if days_until <= 3:
                        st.error(f"🚨 {due_date.strftime('%d-%b-%Y')} ({days_until} days)")
                    elif days_until <= 7:
                        st.warning(f"⚠️ {due_date.strftime('%d-%b-%Y')} ({days_until} days)")
                    else:
                        st.info(f"📅 {due_date.strftime('%d-%b-%Y')} ({days_until} days)")
                
                with col4:
                    st.write(f"**{row['Category']}**")
        else:
            st.info("✅ No upcoming deadlines in the next 30 days!")
    
    # Export functionality
    st.header("💾 Export Data")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export filtered data as CSV
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name=f"ramah_operations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Export overdue tasks
        if 'Date Status' in df_filtered.columns:
            overdue_df = df_filtered[df_filtered['Date Status'] == 'overdue']
            csv_overdue = overdue_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="🚨 Download Overdue Tasks (CSV)",
                data=csv_overdue,
                file_name=f"ramah_overdue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col3:
        # Export summary report
        summary_data = {
            'Category': [],
            'Total Tasks': [],
            'Completed': [],
            'Pending': [],
            'Overdue': [],
            'No Due Date': []
        }
        
        for cat in df_filtered['Category'].unique():
            cat_df = df_filtered[df_filtered['Category'] == cat]
            summary_data['Category'].append(cat)
            summary_data['Total Tasks'].append(len(cat_df))
            summary_data['Completed'].append(len(cat_df[cat_df['Current Status'] == 'Done']))
            summary_data['Pending'].append(len(cat_df[cat_df['Current Status'] == 'Pending']))
            
            if 'Date Status' in cat_df.columns:
                summary_data['Overdue'].append(len(cat_df[cat_df['Date Status'] == 'overdue']))
            else:
                summary_data['Overdue'].append(0)
            
            if 'EDD at Site' in cat_df.columns:
                summary_data['No Due Date'].append(len(cat_df[cat_df['EDD at Site'].isna()]))
            else:
                summary_data['No Due Date'].append(len(cat_df))
        
        summary_df = pd.DataFrame(summary_data)
        csv_summary = summary_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Download Summary Report (CSV)",
            data=csv_summary,
            file_name=f"ramah_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

else:
    # Instructions when no data is loaded
    st.info("👆 Please upload your operations spreadsheet or enter the file path in the sidebar")
    
    st.subheader("📝 How to Use This Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Getting Started
        1. **Upload your file** using the sidebar file uploader
        2. Or **enter the file path** directly
        3. The dashboard will automatically categorize tasks into:
           - 🚛 Transport
           - 💰 Payments
           - 📦 Logistics
           - 🛒 Procurement
           - 👥 HR & Admin
           - 🏗️ Project Management
           - 💻 IT & Systems
           - 📊 Finance & Accounts
        """)
    
    with col2:
        st.markdown("""
        ### Features
        - ✅ Track completed vs pending operations
        - 📅 Monitor due dates with **EDD at Site** column
        - 🚨 Automatic overdue detection with countdown
        - 🔍 Filter by category, status, or due date
        - 📊 Visual analytics and timeline charts
        - 💾 Export filtered data and reports
        - ⏰ Upcoming deadlines view
        """)
    
    st.subheader("📋 Expected Data Format")
    st.write("Your spreadsheet should contain these columns:")
    st.code("""
    - WBS Sr# (Work Breakdown Structure Number)
    - Work Breakdown Structure Task Description
    - Current Status (Done, Pending, In Progress, etc.)
    - EDD at Site (Expected Delivery Date - Format: DD-MMM-YYYY)
    - Remarks (Optional notes)
    - Requested Date (Optional)
    """)
    
    st.info("💡 **Important:** EDD at Site is used as the due date column. Format: 25-Dec-2025")

# Footer
st.markdown("---")
st.caption("🏗️ Ramah General Contracting & Transport LLC - Operations Management Dashboard | Powered by Streamlit")
