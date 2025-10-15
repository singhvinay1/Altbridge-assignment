# PDF Data Extraction Tool

A full-stack application for extracting structured data from PDF documents using AI/LLM technology. The tool supports multiple extraction templates and generates Excel files with the extracted data.

## 🚀 Features

- **PDF Text Extraction**: Extract text content from PDF files using multiple extraction methods
- **AI-Powered Data Extraction**: Use Google's Generative AI to extract structured data from unstructured text
- **Template-Based Extraction**: Support for multiple extraction templates (Template 1 & Template 2)
- **Excel Output**: Generate formatted Excel files with extracted data
- **Modern Web Interface**: React-based frontend with drag-and-drop file upload
- **RESTful API**: FastAPI backend with comprehensive endpoints

## 📁 Project Structure

```
Altbridge-assignment/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── lib/            # API utilities
│   │   └── styles.css      # Global styles
│   ├── index.html
│   └── package.json
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── main.py         # FastAPI app entry point
│   │   └── settings.py     # Configuration
│   └── requirements.txt
├── templates/              # Extraction templates
│   ├── template1.json     # Template 1 configuration
│   └── template2.json     # Template 2 configuration
├── examples/              # Sample files and outputs
│   ├── sample_pdfs/       # Sample PDF files for testing
│   └── output/           # Example extracted Excel files
└── README.md
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+ 
- Node.js 16+
- npm or yarn
- Google AI API key (for data extraction)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the backend directory:
   ```env
   GOOGLE_API_KEY=your_google_ai_api_key_here
   FRONTEND_ORIGIN=http://localhost:5173
   ```

5. **Run the backend server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🏃‍♂️ How to Run Locally

### Quick Start

1. **Start the backend:**
   ```bash
   cd backend
   source .venv/bin/activate
   uvicorn app.main:app --reload
   ```

2. **Start the frontend (in a new terminal):**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open your browser:**
   Navigate to http://localhost:5173

### Using the Application

1. **Upload PDFs**: Drag and drop PDF files or click to select
2. **Choose Template**: Select between Template 1 or Template 2
3. **Extract Data**: Click "Extract Data" to process the files
4. **Download Results**: Download the generated Excel file

## 📡 API Endpoints

### Health Check
- **GET** `/health` - Check API health status

### Data Extraction
- **POST** `/extract` - Extract data from uploaded PDFs
  - **Parameters:**
    - `files`: List of PDF files (multipart/form-data)
    - `template_id`: Template identifier ("template1" or "template2")
  - **Response:**
    ```json
    {
      "filename": "extracted_data_template1_20250115_120000.xlsx"
    }
    ```

### File Download
- **GET** `/download/{filename}` - Download generated Excel file
  - **Parameters:**
    - `filename`: Name of the Excel file to download
  - **Response:** Excel file download

### API Documentation
- **GET** `/docs` - Interactive API documentation (Swagger UI)
- **GET** `/redoc` - Alternative API documentation

## 🔄 How to Switch Between Templates

### Template Selection

The application supports two extraction templates:

1. **Template 1** (`template1.json`):
   - Designed for Private Equity Funds data extraction
   - Extracts: Number, Tab, Description fields

2. **Template 2** (`template2.json`):
   - Alternative template for Private Equity Funds
   - Same field structure as Template 1

### Switching Templates

**Via Frontend:**
1. Use the template selector dropdown in the UI
2. Choose between "Template 1" and "Template 2"
3. Upload files and extract data

**Via API:**
```bash
curl -X POST "http://localhost:8000/extract" \
  -F "files=@sample.pdf" \
  -F "template_id=template1"
```

### Adding New Templates

1. Create a new JSON file in `/templates/` directory
2. Define the template structure:
   ```json
   {
     "templateId": "template3",
     "description": "Your template description",
     "fields": [
       { "key": "field1", "header": "Field 1" },
       { "key": "field2", "header": "Field 2" }
     ]
   }
   ```
3. Update the backend validation in `extract.py` to include the new template

## 🧪 Testing with Sample Files

The project includes sample PDFs for testing:

- `examples/sample_pdfs/Horizon Capital.pdf`
- `examples/sample_pdfs/Linolex Fund LP.pdf`

Example outputs are available in `examples/output/` showing the expected Excel format.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google AI API key for data extraction | Required |
| `FRONTEND_ORIGIN` | Frontend URL for CORS | `http://localhost:5173` |

### Template Configuration

Templates are defined in JSON format with the following structure:
- `templateId`: Unique identifier
- `description`: Human-readable description
- `fields`: Array of field definitions with `key` and `header`

## 🚀 Deployment

### Backend Deployment

1. **Build for production:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run with production server:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### Frontend Deployment

1. **Build the application:**
   ```bash
   npm run build
   ```

2. **Serve the built files:**
   ```bash
   npm run preview
   ```

## 📋 Dependencies

### Backend Dependencies
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **pdfplumber**: PDF text extraction
- **PyMuPDF**: Alternative PDF processing
- **openpyxl**: Excel file generation
- **google-generativeai**: AI data extraction
- **pandas**: Data manipulation
- **python-multipart**: File upload handling

### Frontend Dependencies
- **React**: UI framework
- **Vite**: Build tool
- **Axios**: HTTP client

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of the Altbridge assignment.

## 🆘 Troubleshooting

### Common Issues

1. **Google API Key Error:**
   - Ensure your Google AI API key is valid and has proper permissions
   - Check the `.env` file is in the backend directory

2. **CORS Issues:**
   - Verify `FRONTEND_ORIGIN` matches your frontend URL
   - Check that both frontend and backend are running

3. **PDF Processing Errors:**
   - Ensure PDF files are not password-protected
   - Check file size limits (default: 10MB per file)

4. **Port Conflicts:**
   - Backend runs on port 8000 by default
   - Frontend runs on port 5173 by default
   - Change ports if conflicts occur

### Getting Help

- Check the API documentation at `/docs`
- Review the example files in `/examples/`
- Ensure all dependencies are properly installed