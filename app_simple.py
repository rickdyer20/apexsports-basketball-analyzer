import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time

# Set page config
st.set_page_config(
    page_title="Basketball Shot Analyzer - ApexSports",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #FF6B35 0%, #F7931E 100%);
    color: white;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #FF6B35;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏀 Basketball Shot Analyzer</h1>
        <h3>AI-Powered Shooting Form Analysis</h3>
        <p>Transform your shooting with professional AI coaching feedback</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/FF6B35/FFFFFF?text=ApexSports", width=200)
        st.markdown("### 🎯 Upload Your Shot")
        
        uploaded_file = st.file_uploader(
            "Choose a basketball shot video...",
            type=['mp4', 'mov', 'avi'],
            help="Upload a video of your basketball shot for AI analysis"
        )
        
        if uploaded_file:
            st.success("✅ Video uploaded successfully!")
            
        st.markdown("---")
        st.markdown("### 📊 Analysis Features")
        st.markdown("""
        - **Shot Mechanics Analysis**
        - **Form Correction Tips**
        - **60-Day Improvement Plan**
        - **Progress Tracking**
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🎬 Video Analysis")
        
        if uploaded_file:
            st.video(uploaded_file)
            
            # Simulate analysis
            if st.button("🔍 Analyze Shot", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(100):
                    progress_bar.progress(i + 1)
                    if i < 30:
                        status_text.text('🔍 Processing video frames...')
                    elif i < 60:
                        status_text.text('🤖 AI analyzing shot mechanics...')
                    elif i < 90:
                        status_text.text('📊 Generating coaching insights...')
                    else:
                        status_text.text('✅ Analysis complete!')
                    time.sleep(0.05)
                
                # Show results
                st.success("🎉 Analysis Complete!")
                
                # Sample metrics
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Shot Accuracy", "72%", "+8%")
                with col_b:
                    st.metric("Release Angle", "45°", "+2°")
                with col_c:
                    st.metric("Form Score", "B+", "+1 Grade")
                
                # Coaching feedback
                st.markdown("### 🏀 Coaching Feedback")
                st.markdown("""
                <div class="metric-card">
                <h4>🎯 Primary Focus Areas</h4>
                <ul>
                <li><strong>Elbow Alignment:</strong> Keep your shooting elbow directly under the ball</li>
                <li><strong>Follow Through:</strong> Snap your wrist down after release</li>
                <li><strong>Balance:</strong> Land in the same spot you shot from</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
                
        else:
            st.info("👆 Upload a basketball shot video to get started!")
            
            # Demo section
            st.markdown("### 🎥 Demo Analysis")
            st.markdown("See how our AI analyzes basketball shots:")
            
            demo_data = {
                'Metric': ['Release Angle', 'Arc Height', 'Follow Through', 'Balance', 'Consistency'],
                'Score': [85, 78, 92, 67, 74],
                'Target': [90, 85, 95, 80, 85]
            }
            
            df = pd.DataFrame(demo_data)
            st.bar_chart(df.set_index('Metric'))
    
    with col2:
        st.markdown("## 📈 Your Progress")
        
        # Sample progress data
        dates = pd.date_range('2024-01-01', periods=30, freq='D')
        progress_data = pd.DataFrame({
            'Date': dates,
            'Accuracy': 60 + np.cumsum(np.random.randn(30) * 0.5),
            'Form Score': 65 + np.cumsum(np.random.randn(30) * 0.3)
        })
        
        st.line_chart(progress_data.set_index('Date'))
        
        st.markdown("### 🏆 Achievements")
        st.markdown("""
        - 🎯 **Accuracy Improved** +15%
        - 📈 **Consistency Rating** A-
        - 🔥 **7-Day Streak** Active
        - 📊 **Form Analysis** Complete
        """)
        
        st.markdown("### 📋 60-Day Plan")
        st.markdown("""
        **Week 1-2:** Foundation
        - Focus on stance and balance
        - Practice proper grip
        
        **Week 3-4:** Mechanics
        - Shooting motion refinement
        - Elbow alignment drills
        
        **Week 5-8:** Consistency
        - Repetition and muscle memory
        - Game situation practice
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🏀 <strong>ApexSports Basketball Shot Analyzer</strong> | Powered by AI | www.apexsports-llc.com</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
