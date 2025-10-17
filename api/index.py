import json
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def handler(request, context):
    """Vercel serverless function handler"""
    
    # Get request method and path
    method = request.get('httpMethod', 'GET')
    path = request.get('path', '/')
    
    # Handle CORS preflight
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': 'CORS preflight'})
        }
    
    # Handle health check
    if path == '/api/health' and method == 'GET':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'status': 'ok'})
        }
    
    # Handle extract endpoint
    if path == '/api/extract' and method == 'POST':
        try:
            # Import and use the actual extract functionality
            from routes.extract import extract
            from fastapi import UploadFile, Form
            from fastapi.responses import JSONResponse
            import tempfile
            import os
            
            # Parse the request body for multipart form data
            body = request.get('body', '')
            headers = request.get('headers', {})
            
            # For now, return a simple response indicating the endpoint is working
            # TODO: Implement proper multipart form parsing for file uploads
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'Extract endpoint is working - file upload parsing needs implementation',
                    'filename': 'test_extraction.xlsx'
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': str(e)})
            }
    
    # Handle download endpoint
    if path.startswith('/api/download/') and method == 'GET':
        try:
            # Extract filename from path
            filename = path.split('/api/download/')[-1]
            
            # For now, return a simple response
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'Download endpoint is working',
                    'filename': filename
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': str(e)})
            }
    
    # Default response
    return {
        'statusCode': 404,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'error': 'Not found', 'path': path, 'method': method})
    }
