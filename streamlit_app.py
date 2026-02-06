"""
Streamlit UI for AI Operations Assistant.
Provides a web interface for the multi-agent system.
"""

import streamlit as st
from main import AIOpsAssistant


def display_plan(plan):
    """Display the execution plan."""
    st.subheader("📋 Execution Plan")
    with st.expander("View Plan Details", expanded=True):
        for i, step in enumerate(plan["steps"]):
            st.markdown(f"**Step {i + 1}**: {step['tool']}")
            st.text(f"Input: {step['input']}")
            st.divider()


def display_execution(results):
    """Display execution results."""
    st.subheader("⚙️ Execution Progress")
    
    for result in results:
        status_icon = "✅" if result["status"] == "success" else "❌"
        st.markdown(f"{status_icon} **Step {result['step']}**: {result['tool']}")
        
        with st.expander(f"View Details", expanded=False):
            st.text(f"Input: {result['input']}")
            
            if result["status"] == "success":
                st.json(result["result"])
            else:
                st.error(f"Error: {result['error']}")
        
        st.divider()


def display_verification(verification):
    """Display verification results."""
    st.subheader("✅ Verification")
    
    status_color = {
        "success": "green",
        "partial": "orange",
        "failed": "red"
    }
    
    st.markdown(f"**Status**: :{status_color.get(verification['status'], 'black')}[{verification['status'].upper()}]")
    
    st.markdown(f"**Summary**: {verification['summary']}")
    
    with st.expander("View Details", expanded=False):
        st.markdown(f"**Total Steps**: {verification['details']['total_steps']}")
        st.markdown(f"**Successful**: {verification['details']['successful_steps']}")
        st.markdown(f"**Failed**: {verification['details']['failed_steps']}")
        
        if verification['details']['findings']:
            st.markdown("**Key Findings**:")
            for finding in verification['details']['findings']:
                st.markdown(f"- {finding}")
        
        if verification.get('final_answer'):
            st.markdown("**Final Answer**:")
            st.json(verification['final_answer'])


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="AI Operations Assistant",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 AI Operations Assistant")
    st.markdown("""
    A multi-agent system that accepts natural language tasks, creates execution plans, 
    calls API tools, verifies results, and returns structured answers.
    """)
    
    st.divider()
    
    # Initialize assistant
    if 'assistant' not in st.session_state:
        with st.spinner("Initializing AI Operations Assistant..."):
            try:
                st.session_state.assistant = AIOpsAssistant()
                st.success("✅ Assistant initialized successfully!")
            except Exception as e:
                st.error(f"❌ Failed to initialize: {e}")
                st.stop()
    
    # Task input
    st.subheader("📝 Enter Your Task")
    task = st.text_area(
        "What would you like the assistant to do?",
        placeholder="e.g., Find top AI GitHub repo and current weather in Mumbai",
        height=100
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        run_button = st.button("🚀 Execute Task", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.session_state.results = None
        st.session_state.verification = None
        st.session_state.plan = None
        st.rerun()
    
    # Example tasks
    st.subheader("💡 Example Tasks")
    example_tasks = [
        "Find top AI GitHub repo and current weather in Mumbai",
        "Get latest news about AI technology",
        "Search for Python web frameworks on GitHub",
        "What's the weather like in New York?",
        "Find top AI GitHub repo, current weather in Mumbai, and latest news about technology"
    ]
    
    selected_example = st.selectbox("Or try an example task:", [""] + example_tasks)
    if selected_example:
        task = selected_example
    
    # Execute task
    if run_button and task:
        st.divider()
        st.subheader("🔄 Processing")
        
        try:
            # Planning phase
            with st.spinner("📋 Creating execution plan..."):
                plan = st.session_state.assistant.planner.create_plan(task)
                st.session_state.plan = plan
            
            display_plan(plan)
            
            # Execution phase
            with st.spinner("⚙️ Executing plan..."):
                results = st.session_state.assistant.executor.execute_plan(plan)
                st.session_state.results = results
            
            display_execution(results)
            
            # Verification phase
            with st.spinner("✅ Verifying results..."):
                verification = st.session_state.assistant.verifier.verify_results(results)
                st.session_state.verification = verification
            
            display_verification(verification)
            
            # Success message
            st.success("✅ Task completed successfully!")
            
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.exception(e)
    
    # Display previous results
    if 'results' in st.session_state and st.session_state.results:
        st.divider()
        st.subheader("📊 Previous Results")
        
        if 'plan' in st.session_state:
            display_plan(st.session_state.plan)
        
        display_execution(st.session_state.results)
        
        if 'verification' in st.session_state:
            display_verification(st.session_state.verification)
    
    # Sidebar with system info
    with st.sidebar:
        st.header("🔧 System Info")
        st.info(f"**Model**: {st.session_state.assistant.llm.model}")
        st.info(f"**Tools Available**: GitHub, Weather, News")
        
        st.header("📖 About")
        st.markdown("""
        This system uses a multi-agent architecture:
        
        - **Planner**: Creates execution plans
        - **Executor**: Executes API calls
        - **Verifier**: Validates results
        
        Powered by NVIDIA's LLM API.
        """)
        
        st.header("🔗 APIs")
        st.markdown("""
        - GitHub API
        - WeatherAPI
        - NewsAPI
        """)


if __name__ == "__main__":
    main()
