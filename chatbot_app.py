import streamlit as st
import requests
from PIL import Image
import time
import json
from datetime import datetime
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="ABS Chatbot - AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS Styles ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Inter', sans-serif;
        }
        
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 800px;
        }
        
        /* Header styling */
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #003057 0%, #004080 100%);
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0, 48, 87, 0.3);
        }
        
        .main-title {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .main-subtitle {
            color: #e6f0fa;
            font-size: 1.1rem;
            margin-top: 0.5rem;
            font-weight: 400;
        }
        
        /* Chat input styling */
        .stChatInput > div > div > input {
            border: 2px solid #003057;
            border-radius: 25px;
            padding: 12px 20px;
            font-size: 1rem;
            background-color: white;
            box-shadow: 0 4px 15px rgba(0, 48, 87, 0.1);
            transition: all 0.3s ease;
        }
        
        .stChatInput > div > div > input:focus {
            border-color: #0066cc;
            box-shadow: 0 4px 20px rgba(0, 102, 204, 0.2);
            outline: none;
        }
        
        /* Chat message styling */
        .stChatMessage {
            border-radius: 15px;
            margin: 1rem 0;
            padding: 1rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            animation: fadeIn 0.5s ease-in;
        }
        
        .stChatMessage.user {
            background: linear-gradient(135deg, #e6f0fa 0%, #cce7ff 100%);
            border-left: 4px solid #003057;
        }
        
        .stChatMessage.assistant {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-left: 4px solid #0066cc;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #003057 0%, #004080 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 48, 87, 0.2);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #004080 0%, #0066cc 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 48, 87, 0.3);
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Status indicators */
        .status-indicator {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin: 0.5rem 0;
        }
        
        .status-online {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status-offline {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        /* Sidebar styling */
        .sidebar-content {
            background-color: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        /* Loading spinner custom */
        .custom-spinner {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 1rem;
        }
        
        /* Chat statistics */
        .chat-stats {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .stat-item {
            display: inline-block;
            margin: 0 1rem;
            text-align: center;
        }
        
        .stat-number {
            font-size: 1.5rem;
            font-weight: 700;
            color: #003057;
            display: block;
        }
        
        .stat-label {
            font-size: 0.8rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Logo and Header ---
def render_header():
    """Render the application header with logo and title"""
    try:
        if os.path.exists("abs-logo-Blue.png"):
            logo = Image.open("abs-logo-Blue.png")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(logo, width=200)
        else:
            st.info("Logo file 'abs-logo-Blue.png' not found. Add your logo to display it here.")
    except Exception as e:
        st.warning(f"Could not load logo: {e}")
    
    st.markdown("""
        <div class="main-header">
            <h1 class="main-title">🤖 ABS Chatbot</h1>
            <p class="main-subtitle">Your intelligent document-based AI assistant</p>
        </div>
    """, unsafe_allow_html=True)

# --- Session State Initialization ---
def initialize_session_state():
    """Initialize all session state variables"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "message_count" not in st.session_state:
        st.session_state.message_count = 0
    
    if "session_start_time" not in st.session_state:
        st.session_state.session_start_time = datetime.now()
    
    if "api_status" not in st.session_state:
        st.session_state.api_status = "unknown"
    
    if "last_response_time" not in st.session_state:
        st.session_state.last_response_time = None

# --- API Health Check ---
def check_api_health():
    """Check if the backend API is accessible"""
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            st.session_state.api_status = "online"
            return True
        else:
            st.session_state.api_status = "offline"
            return False
    except:
        st.session_state.api_status = "offline"
        return False

# --- API Request Function ---
def send_question_to_api(question):
    """Send question to API and handle response"""
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:8001/ask",
            json={"question": question},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        response_time = time.time() - start_time
        st.session_state.last_response_time = response_time
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "No answer received from the server.")
            
            # Check for additional metadata
            metadata = {
                "response_time": response_time,
                "confidence": data.get("confidence"),
                "sources": data.get("sources"),
                "timestamp": datetime.now().isoformat()
            }
            
            return answer, metadata, True
        else:
            error_msg = f"❌ Server Error {response.status_code}: {response.text}"
            return error_msg, {"response_time": response_time}, False
            
    except requests.exceptions.Timeout:
        return "⏱️ Request timed out. The server is taking too long to respond.", {"response_time": None}, False
    except requests.exceptions.ConnectionError:
        return "🚨 Connection Error: Cannot connect to the chatbot server. Please ensure it's running on localhost:8001.", {"response_time": None}, False
    except Exception as e:
        return f"🚨 Unexpected Error: {str(e)}", {"response_time": None}, False

# --- Chat Statistics Display ---
def display_chat_stats():
    """Display chat session statistics"""
    session_duration = datetime.now() - st.session_state.session_start_time
    duration_minutes = int(session_duration.total_seconds() / 60)
    
    status_class = "status-online" if st.session_state.api_status == "online" else "status-offline"
    status_text = "🟢 Online" if st.session_state.api_status == "online" else "🔴 Offline"
    
    st.markdown(f"""
        <div class="chat-stats">
            <div class="stat-item">
                <span class="stat-number">{len(st.session_state.chat_history)}</span>
                <span class="stat-label">Messages</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{duration_minutes}m</span>
                <span class="stat-label">Session Time</span>
            </div>
            <div class="stat-item">
                <span class="status-indicator {status_class}">{status_text}</span>
            </div>
            {f'<div class="stat-item"><span class="stat-number">{st.session_state.last_response_time:.1f}s</span><span class="stat-label">Last Response</span></div>' if st.session_state.last_response_time else ''}
        </div>
    """, unsafe_allow_html=True)

# --- Sidebar Functions ---
def render_sidebar():
    """Render sidebar with additional features"""
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        st.markdown("### 🛠️ Chat Controls")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", type="secondary"):
            st.session_state.chat_history = []
            st.session_state.message_count = 0
            st.rerun()
        
        # Export chat button
        if len(st.session_state.chat_history) > 0:
            if st.button("📥 Export Chat", type="secondary"):
                chat_data = {
                    "session_start": st.session_state.session_start_time.isoformat(),
                    "message_count": len(st.session_state.chat_history),
                    "chat_history": [
                        {"question": q, "answer": a, "index": i} 
                        for i, (q, a) in enumerate(st.session_state.chat_history)
                    ]
                }
                st.download_button(
                    label="Download Chat JSON",
                    data=json.dumps(chat_data, indent=2),
                    file_name=f"abs_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        st.markdown("---")
        
        # API Status
        st.markdown("### 📡 Connection Status")
        if st.button("🔄 Check Connection"):
            with st.spinner("Checking API..."):
                check_api_health()
        
        status_color = "🟢" if st.session_state.api_status == "online" else "🔴"
        st.markdown(f"**Status:** {status_color} {st.session_state.api_status.title()}")
        
        st.markdown("---")
        
        # Help section
        st.markdown("### ❓ How to Use")
        st.markdown("""
        1. Type your question in the chat input
        2. Press Enter or click Send
        3. Wait for the AI to process your request
        4. View the response with relevant sources
        
        **Tips:**
        - Be specific in your questions
        - Ask follow-up questions for clarification
        - Use the export feature to save important conversations
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- Main Chat Interface ---
def render_chat_interface():
    """Render the main chat interface"""
    
    # Display chat history
    for i, (question, answer) in enumerate(st.session_state.chat_history):
        # User message
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"**You:** {question}")
        
        # Assistant message
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(f"**ABS Assistant:** {answer}")
    
    # Chat input
    user_input = st.chat_input("💬 Ask me anything about your documents...")
    
    # Handle new user input
    if user_input:
        # Display user message immediately
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"**You:** {user_input}")
        
        # Display assistant response with loading
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🧠 Processing your question..."):
                answer, metadata, success = send_question_to_api(user_input)
            
            # Display response with formatting
            if success:
                st.markdown(f"**ABS Assistant:** {answer}")
                
                # Show response time if available
                if metadata.get("response_time"):
                    st.caption(f"⚡ Response time: {metadata['response_time']:.2f}s")
            else:
                st.error(answer)
        
        # Add to chat history
        st.session_state.chat_history.append((user_input, answer))
        st.session_state.message_count += 1
        
        # Auto-rerun to update display
        st.rerun()

# --- Quick Action Buttons ---
def render_quick_actions():
    """Render quick action buttons for common questions"""
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    quick_questions = [
        "What is this document about?",
        "Can you summarize the key points?",
        "What are the main conclusions?"
    ]
    
    cols = [col1, col2, col3]
    
    for i, (col, question) in enumerate(zip(cols, quick_questions)):
        with col:
            if st.button(f"💡 {question[:20]}...", key=f"quick_{i}"):
                # Simulate user input
                st.session_state.temp_question = question
                st.rerun()
    
    # Handle quick question
    if hasattr(st.session_state, 'temp_question'):
        question = st.session_state.temp_question
        del st.session_state.temp_question
        
        # Add to chat and process
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"**You:** {question}")
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🧠 Processing your question..."):
                answer, metadata, success = send_question_to_api(question)
            
            if success:
                st.markdown(f"**ABS Assistant:** {answer}")
                if metadata.get("response_time"):
                    st.caption(f"⚡ Response time: {metadata['response_time']:.2f}s")
            else:
                st.error(answer)
        
        st.session_state.chat_history.append((question, answer))
        st.session_state.message_count += 1

# --- Main Application ---
def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Check API health on startup
    if st.session_state.api_status == "unknown":
        check_api_health()
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Display chat statistics
    display_chat_stats()
    
    # Show quick actions if no chat history
    if len(st.session_state.chat_history) == 0:
        render_quick_actions()
        st.markdown("---")
    
    # Render main chat interface
    render_chat_interface()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.8rem;'>"
        "Powered by ABS AI Technology 🚀 | Built with Streamlit"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()