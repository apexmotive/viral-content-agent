"""Streamlit UI for Viral Content Agent Team."""

import streamlit as st
import time
from datetime import datetime
import config
from workflow.graph import run_workflow

# Page configuration
st.set_page_config(
    page_title="Viral Content Agent Team",
    page_icon=None,
    layout="wide"
)

# Custom CSS for clean, modern styling
st.markdown("""
<style>
    /* Main Header */
    .main-header {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    
    /* Cards */
    .metric-card {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #3B82F6;
    }
    .metric-label {
        font-size: 0.875rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }
    
    /* Content Box */
    .content-box {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.5rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px;
        color: #64748B;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #3B82F6;
        border-bottom: 2px solid #3B82F6;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">Viral Content Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Autonomous multi-agent team for social media content creation</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### Settings")
        
        # Model Selection
        selected_model = st.selectbox(
            "Model",
            options=[
                "meta-llama/llama-4-scout-17b-16e-instruct",
                "meta-llama/llama-4-maverick-17b-128e-instruct",
                "openai/gpt-oss-120b"
            ],
            index=0
        )
        
        # Update config with selected model
        config.GROQ_MODEL = selected_model
        
        # Max Iterations
        max_iterations = st.number_input(
            "Max Iterations",
            min_value=1,
            max_value=5,
            value=config.MAX_ITERATIONS
        )
        config.MAX_ITERATIONS = max_iterations
        
        # Virality Threshold
        virality_threshold = st.slider(
            "Virality Threshold",
            min_value=50,
            max_value=100,
            value=config.VIRALITY_THRESHOLD
        )
        config.VIRALITY_THRESHOLD = virality_threshold
        
        st.divider()
        
        st.markdown("### Active Agents")
        st.markdown("**Trend Scout** (Researcher)")
        st.markdown("**Ghostwriter** (Creator)")
        st.markdown("**Chief Editor** (Reviewer)")
    
    # Input Section
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            topic = st.text_input(
                "Topic",
                placeholder="Enter a topic (e.g., Database Normalization)",
                label_visibility="collapsed"
            )
            
        with col2:
            platform = st.selectbox(
                "Platform",
                options=["Twitter", "LinkedIn"],
                label_visibility="collapsed"
            )
            
        with col3:
            generate_button = st.button(
                "Generate Content",
                type="primary",
                use_container_width=True
            )

    # Results Section
    if generate_button:
        if not topic:
            st.warning("Please enter a topic first.")
            return
            
        # Progress Container
        progress_container = st.empty()
        with progress_container.container():
            st.info("Initializing agents...")
            progress_bar = st.progress(0)
            
        try:
            start_time = time.time()
            
            # Research Phase
            with progress_container.container():
                st.info("Trend Scout is researching angles...")
                progress_bar.progress(25)
            
            # Run Workflow
            final_state = run_workflow(topic, platform.lower())
            
            # Complete
            progress_bar.progress(100)
            time.sleep(0.5)
            progress_container.empty()
            
            # Store in session state
            st.session_state['results'] = {
                'final_state': final_state,
                'elapsed_time': time.time() - start_time,
                'platform': platform
            }
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            with st.expander("Error Details"):
                st.code(str(e))

    # Display Results from Session State
    if 'results' in st.session_state:
        results = st.session_state['results']
        final_state = results['final_state']
        elapsed_time = results['elapsed_time']
        platform = results['platform']
        
        virality_score = final_state.get('virality_score', 0)
        iterations = final_state.get('iteration_count', 0)
        
        # Display Metrics Row
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{virality_score}/100</div>
                <div class="metric-label">Virality Score</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{elapsed_time:.1f}s</div>
                <div class="metric-label">Generation Time</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{iterations}</div>
                <div class="metric-label">Iterations</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Tabbed Results
        tab_content, tab_research, tab_feedback = st.tabs([
            "Agent: Ghostwriter (Content)", 
            "Agent: Trend Scout (Research)", 
            "Agent: Chief Editor (Feedback)"
        ])
        
        # 1. Generated Content Tab
        with tab_content:
            final_content = final_state.get('final_content', '') or final_state.get('draft_content', '')
            if final_content:
                st.markdown(final_content)
                st.download_button(
                    "Download Text",
                    data=final_content,
                    file_name=f"viral_{platform.lower()}_{int(time.time())}.txt",
                    mime="text/plain"
                )
            else:
                st.error("No content generated.")
        
        # 2. Research Angles Tab
        with tab_research:
            angles = final_state.get('research_angles', [])
            if angles:
                st.markdown("### 🕵️ Trend Scout's Findings")
                for i, angle in enumerate(angles, 1):
                    with st.expander(f"Angle {i}: {angle.get('title', 'Untitled')}", expanded=True):
                        st.markdown(f"**Why Viral:** {angle.get('why_viral', 'N/A')}")
                        st.markdown(f"**Summary:** {angle.get('summary', 'N/A')}")
                        if angle.get('sources'):
                            st.markdown("**Sources:**")
                            for source in angle['sources']:
                                st.markdown(f"- [{source}]({source})")
            else:
                st.info("No research angles found.")
        
        # 3. Editor Feedback Tab
        with tab_feedback:
            feedback = final_state.get('editor_feedback', '')
            if feedback:
                st.markdown("### ⚖️ Chief Editor's Report")
                st.info(feedback)
                
                if final_state.get('virality_score', 0) >= config.VIRALITY_THRESHOLD:
                    st.success("✨ Active Editor: Applied final polish based on this feedback.")
            else:
                st.info("No feedback provided.")


if __name__ == "__main__":
    main()
