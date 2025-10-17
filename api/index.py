import json

def handler(request, context):
    """Minimal Vercel serverless function handler"""
    
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
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Extract endpoint is working',
                'filename': 'test_extraction.xlsx'
            })
        }
    
    # Handle download endpoint
    if path.startswith('/api/download/') and method == 'GET':
        filename = path.split('/api/download/')[-1]
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
    
    # Default response
    return {
        'statusCode': 404,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'error': 'Not found', 'path': path, 'method': method})
    }
