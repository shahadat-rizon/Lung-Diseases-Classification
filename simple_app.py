"""
Simple Flask-like web application for Lung Disease Classification
This version works without external dependencies for demonstration purposes.
"""

import os
import json
import base64
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import cgi
import io
import tempfile
import shutil
from simple_model import load_simple_model, SimpleLungDiseaseModel

# Global model instance
model = None

def get_model():
    global model
    if model is None:
        model = load_simple_model()
    return model

class LungDiseaseHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/' or path == '/index.html':
            self.serve_index()
        elif path == '/health':
            self.serve_health()
        else:
            self.send_error(404, "Page not found")
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/upload':
            self.handle_upload()
        elif path == '/api/predict':
            self.handle_api_predict()
        else:
            self.send_error(404, "Endpoint not found")
    
    def serve_index(self):
        """Serve the main upload page"""
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lung Disease Classification</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }
        .header {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #007bff;
            margin-bottom: 10px;
        }
        .upload-area {
            border: 3px dashed #007bff;
            border-radius: 10px;
            padding: 40px 20px;
            text-align: center;
            background: #f8f9ff;
            margin: 20px 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .upload-area:hover {
            border-color: #0056b3;
            background: #e6f3ff;
        }
        .upload-icon {
            font-size: 48px;
            color: #007bff;
            margin-bottom: 15px;
        }
        .btn {
            background: linear-gradient(45deg, #007bff, #0056b3);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 123, 255, 0.4);
        }
        .info-section {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
        }
        .conditions {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }
        .condition {
            text-align: center;
            flex: 1;
        }
        .condition-icon {
            font-size: 36px;
            margin-bottom: 10px;
        }
        .normal { color: #28a745; }
        .opacity { color: #ffc107; }
        .pneumonia { color: #dc3545; }
        .file-info {
            display: none;
            background: #e9ecef;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
        }
        .footer {
            text-align: center;
            color: #6c757d;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #dee2e6;
        }
        input[type="file"] {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🫁 Lung Disease Classification</h1>
            <p>Upload an X-ray image to detect lung diseases using AI</p>
        </div>

        <form method="POST" action="/upload" enctype="multipart/form-data" id="uploadForm">
            <div class="upload-area" onclick="document.getElementById('fileInput').click();">
                <div class="upload-icon">📁</div>
                <h3>Drop your X-ray image here</h3>
                <p>or click to browse files</p>
                <input type="file" name="file" id="fileInput" accept="image/*" required>
                <button type="button" class="btn" onclick="document.getElementById('fileInput').click();">
                    Choose File
                </button>
            </div>
            
            <div id="fileInfo" class="file-info">
                <h4>📋 Selected File:</h4>
                <p id="fileName"></p>
                <button type="submit" class="btn">🧠 Analyze Image</button>
                <button type="button" class="btn" onclick="clearFile()" style="background: #6c757d;">Clear</button>
            </div>
        </form>

        <div class="info-section">
            <h4>🔍 Supported Conditions:</h4>
            <div class="conditions">
                <div class="condition">
                    <div class="condition-icon normal">✅</div>
                    <strong>Normal</strong>
                    <p>Healthy lung condition</p>
                </div>
                <div class="condition">
                    <div class="condition-icon opacity">⚠️</div>
                    <strong>Lung Opacity</strong>
                    <p>Lung abnormalities</p>
                </div>
                <div class="condition">
                    <div class="condition-icon pneumonia">🦠</div>
                    <strong>Viral Pneumonia</strong>
                    <p>Viral infection</p>
                </div>
            </div>
        </div>

        <div class="footer">
            <small>
                ⚠️ This is a demonstration app. For medical diagnosis, please consult healthcare professionals.
            </small>
        </div>
    </div>

    <script>
        const fileInput = document.getElementById('fileInput');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');

        fileInput.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                const file = e.target.files[0];
                fileName.textContent = file.name + ' (' + formatFileSize(file.size) + ')';
                fileInfo.style.display = 'block';
            }
        });

        function clearFile() {
            fileInput.value = '';
            fileInfo.style.display = 'none';
        }

        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        // Form submission with loading state
        document.getElementById('uploadForm').addEventListener('submit', function() {
            const submitBtn = document.querySelector('button[type="submit"]');
            submitBtn.innerHTML = '⏳ Analyzing...';
            submitBtn.disabled = true;
        });
    </script>
</body>
</html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_upload(self):
        """Handle file upload and prediction"""
        try:
            # Parse multipart form data
            content_type = self.headers['content-type']
            if not content_type or not content_type.startswith('multipart/form-data'):
                self.send_error(400, "Bad request")
                return
            
            # Get boundary
            boundary = content_type.split('boundary=')[1]
            
            # Read the data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse multipart data
            form = cgi.FieldStorage(
                fp=io.BytesIO(post_data),
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            
            if 'file' not in form:
                self.send_error(400, "No file uploaded")
                return
            
            file_item = form['file']
            if not file_item.filename:
                self.send_error(400, "No file selected")
                return
            
            # Save uploaded file temporarily
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, file_item.filename)
            
            with open(file_path, 'wb') as f:
                f.write(file_item.file.read())
            
            try:
                # Get model and make prediction
                model = get_model()
                result = model.predict(file_path)
                
                # Read image for display
                with open(file_path, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode()
                
                # Serve result page
                self.serve_result(result, img_data, file_item.filename)
                
            finally:
                # Clean up
                shutil.rmtree(temp_dir)
                
        except Exception as e:
            self.send_error(500, f"Error processing image: {str(e)}")
    
    def serve_result(self, result, image_data, filename):
        """Serve the results page"""
        # Determine alert class and icon based on prediction
        prediction = result['class']
        if prediction == 'Normal':
            alert_class = 'normal'
            icon = '✅'
        elif prediction == 'Lung Opacity':
            alert_class = 'opacity'
            icon = '⚠️'
        else:  # Viral Pneumonia
            alert_class = 'pneumonia'
            icon = '🦠'
        
        # Create progress bars for all predictions
        progress_bars = ""
        for class_name, probability in result['all_predictions'].items():
            class_icon = '✅' if class_name == 'Normal' else ('⚠️' if class_name == 'Lung Opacity' else '🦠')
            color = 'normal' if class_name == 'Normal' else ('opacity' if class_name == 'Lung Opacity' else 'pneumonia')
            progress_bars += f"""
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <span>{class_icon} {class_name}</span>
                    <strong>{probability * 100:.1f}%</strong>
                </div>
                <div style="background: #e9ecef; height: 8px; border-radius: 4px;">
                    <div class="{color}" style="height: 100%; width: {probability * 100}%; border-radius: 4px; 
                         background: {'#28a745' if color == 'normal' else ('#ffc107' if color == 'opacity' else '#dc3545')};"></div>
                </div>
            </div>
            """
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analysis Result - Lung Disease Classification</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
        }}
        .results-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }}
        .card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .card h3 {{
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }}
        .uploaded-image {{
            max-width: 100%;
            max-height: 400px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        .prediction-result {{
            text-align: center;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 18px;
        }}
        .normal {{ background: #d4edda; color: #155724; }}
        .opacity {{ background: #fff3cd; color: #856404; }}
        .pneumonia {{ background: #f8d7da; color: #721c24; }}
        .btn {{
            display: inline-block;
            background: linear-gradient(45deg, #007bff, #0056b3);
            color: white;
            text-decoration: none;
            padding: 12px 24px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
            margin: 5px;
        }}
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 123, 255, 0.4);
        }}
        .info-section {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }}
        .disclaimer {{
            background: #cce5ff;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            color: #004085;
        }}
        @media (max-width: 768px) {{
            .results-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🫁 Analysis Results</h1>
        </div>

        <div class="results-grid">
            <div class="card">
                <h3>📸 Uploaded X-ray Image</h3>
                <div style="text-align: center;">
                    <img src="data:image/jpeg;base64,{image_data}" class="uploaded-image" alt="Uploaded X-ray">
                    <p style="color: #6c757d; margin-top: 10px;"><small>{filename}</small></p>
                </div>
            </div>
            
            <div class="card">
                <h3>📊 Analysis Results</h3>
                
                <div class="prediction-result {alert_class}">
                    <h2>{icon} {prediction}</h2>
                    <p><strong>Confidence: {result['confidence'] * 100:.1f}%</strong></p>
                </div>

                <h4>📈 Detailed Analysis:</h4>
                {progress_bars}

                <div style="margin-top: 20px;">
                    <a href="/" class="btn">➕ Analyze Another Image</a>
                </div>
            </div>
        </div>

        <div class="disclaimer">
            <strong>⚠️ Disclaimer:</strong> This AI analysis is for educational purposes only. 
            Please consult with healthcare professionals for medical diagnosis and treatment.
        </div>

        <div class="info-section">
            <h4>💡 Understanding the Results</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
                <div>
                    <h5 style="color: #28a745;">✅ Normal</h5>
                    <p>Indicates healthy lung tissue with no visible abnormalities in the X-ray image.</p>
                </div>
                <div>
                    <h5 style="color: #ffc107;">⚠️ Lung Opacity</h5>
                    <p>Suggests presence of abnormal areas in the lungs that may require medical attention.</p>
                </div>
                <div>
                    <h5 style="color: #dc3545;">🦠 Viral Pneumonia</h5>
                    <p>Indicates patterns consistent with viral pneumonia infection.</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_api_predict(self):
        """Handle API prediction requests"""
        try:
            # Similar to handle_upload but return JSON
            content_type = self.headers['content-type']
            if not content_type or not content_type.startswith('multipart/form-data'):
                self.send_json_error(400, "Bad request")
                return
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            form = cgi.FieldStorage(
                fp=io.BytesIO(post_data),
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            
            if 'file' not in form:
                self.send_json_error(400, "No file uploaded")
                return
            
            file_item = form['file']
            if not file_item.filename:
                self.send_json_error(400, "No file selected")
                return
            
            # Save and process file
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, file_item.filename)
            
            with open(file_path, 'wb') as f:
                f.write(file_item.file.read())
            
            try:
                model = get_model()
                result = model.predict(file_path)
                self.send_json_response(result)
            finally:
                shutil.rmtree(temp_dir)
                
        except Exception as e:
            self.send_json_error(500, str(e))
    
    def serve_health(self):
        """Health check endpoint"""
        model = get_model()
        health_data = {
            'status': 'healthy',
            'model_loaded': model.is_loaded()
        }
        self.send_json_response(health_data)
    
    def send_json_response(self, data):
        """Send JSON response"""
        response = json.dumps(data).encode()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)
    
    def send_json_error(self, status_code, message):
        """Send JSON error response"""
        error_data = {'error': message}
        response = json.dumps(error_data).encode()
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)

def run_server(port=5000):
    """Run the web server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, LungDiseaseHandler)
    print(f"🚀 Starting Lung Disease Classification Server on port {port}")
    print(f"📱 Open your browser and go to: http://localhost:{port}")
    print("⚠️  Note: This is a demonstration server using mock predictions")
    print("🔄 Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    run_server()