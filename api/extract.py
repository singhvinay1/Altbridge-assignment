def handler(request, context):
    """Extract endpoint"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': '{"message": "Extract endpoint is working", "filename": "test_extraction.xlsx"}'
    }
