# ABS Chatbot - Enhanced AI Assistant

A powerful document-based chatbot system built with Streamlit, FastAPI, and Google's Gemini AI. This enhanced version provides a modern, user-friendly interface for intelligent document querying.

## 🚀 Features

### Enhanced UI/UX
- **Modern Design**: Beautiful gradient backgrounds and professional styling
- **Responsive Layout**: Optimized for different screen sizes
- **Animated Elements**: Smooth transitions and loading animations
- **Brand Colors**: Custom ABS color scheme throughout

### Advanced Functionality
- **Real-time Chat Interface**: Streamlit chat components with avatars
- **API Health Monitoring**: Connection status indicators
- **Performance Metrics**: Response time tracking and session statistics
- **Chat Export**: Download conversation history as JSON
- **Quick Actions**: Pre-defined common questions
- **Error Handling**: Comprehensive error messages and recovery

### Technical Improvements
- **FastAPI Backend**: Robust API architecture with proper error handling
- **Session Management**: Persistent chat history and user preferences
- **Logo Support**: Automatic logo detection and display
- **Modular Code**: Clean, maintainable code structure

## 📋 Prerequisites

- Python 3.8+
- Google API Key for Gemini AI
- PDF documents for processing

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Add your logo (optional):**
   Place your logo file as `abs-logo-Blue.png` in the project root

## 🚀 Usage

### Step 1: Process Documents (First Time Setup)
1. Run the document processor:
   ```bash
   streamlit run main.py
   ```
2. Upload your PDF files using the sidebar
3. Click "Submit & Process" to create the document database
4. Wait for processing to complete

### Step 2: Start the API Server
```bash
python backend_api.py
```
The API will start on `http://localhost:8001`

### Step 3: Launch the Enhanced Chatbot
```bash
streamlit run chatbot_app.py
```
The chatbot interface will open in your browser

## 📱 Using the Chatbot

### Main Interface
- **Chat Input**: Type questions in the bottom input field
- **Quick Actions**: Click preset question buttons for common queries
- **Response Tracking**: View response times and session statistics

### Sidebar Features
- **Clear Chat**: Reset conversation history
- **Export Chat**: Download conversations as JSON
- **Connection Status**: Monitor API connectivity
- **Help Guide**: Built-in usage instructions

### Status Indicators
- 🟢 **Online**: API connection is healthy
- 🔴 **Offline**: API connection failed
- ⚡ **Response Time**: Performance metrics displayed

## 🎨 Customization

### Branding
- Replace `abs-logo-Blue.png` with your logo
- Modify CSS variables in `chatbot_app.py` for custom colors
- Update the title and subtitle in the header section

### API Endpoints
The backend provides several endpoints:
- `GET /health`: API health check
- `POST /ask`: Submit questions
- `GET /stats`: System statistics
- `GET /docs`: API documentation

## 🔧 Configuration

### Environment Variables
```env
GOOGLE_API_KEY=your_api_key           # Required: Google Gemini API key
```

### API Settings
Modify `backend_api.py` to adjust:
- Model temperature (creativity level)
- Search result count
- Response timeout settings
- Logging levels

### UI Settings
Customize `chatbot_app.py` for:
- Color schemes
- Layout preferences
- Animation settings
- Quick action questions

## 📊 Features Overview

### Chat Interface
- **Real-time messaging** with typing indicators
- **Message history** preserved during session
- **Error recovery** with helpful error messages
- **Mobile-responsive** design

### Performance Monitoring
- **Response time tracking** for each query
- **Session duration** and message count
- **API connectivity** status monitoring
- **System health** indicators

### Data Management
- **Chat export** in JSON format
- **Session persistence** during browser session
- **Conversation cleanup** tools
- **Metadata tracking** for responses

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Ensure `backend_api.py` is running on port 8001
   - Check if documents have been processed
   - Verify Google API key is valid

2. **Logo Not Displaying**
   - Ensure `abs-logo-Blue.png` exists in project root
   - Check file permissions and format

3. **Slow Responses**
   - Check internet connection
   - Verify Google API quota
   - Monitor system resources

### Error Messages
- **"No document database found"**: Run document processing first
- **"Connection Error"**: Start the backend API server
- **"Request timed out"**: Check network connectivity

## 🔒 Security Notes

- Keep your Google API key secure and never commit it to version control
- The system uses `allow_dangerous_deserialization=True` for FAISS - only use with trusted data
- API runs on localhost by default - configure appropriately for production use

## 📈 Performance Tips

- **Document Processing**: Larger documents take more time to process
- **Response Speed**: Depends on document size and query complexity
- **Memory Usage**: Monitor RAM usage with large document collections

## 🤝 Contributing

To improve the chatbot:
1. Follow the modular code structure
2. Test both frontend and backend changes
3. Update documentation for new features
4. Maintain the existing design patterns

## 📄 License

This project is for ABS internal use. Please follow your organization's guidelines for code usage and distribution.

---

**Made with ❤️ using Streamlit, FastAPI, and Google Gemini AI**
