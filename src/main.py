import json
import logging
import os
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

def lambda_handler(event, context):
    """
    Main Lambda handler for Training Roster Automation
    Handles API Gateway requests and provides training roster functionality
    """
    try:
        # Log the incoming event for debugging
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Extract HTTP method and path from API Gateway event
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        
        # Route requests based on path and method
        if path == '/health':
            return handle_health_check()
        elif path == '/roster':
            if http_method == 'GET':
                return handle_get_roster()
            elif http_method == 'POST':
                return handle_create_roster(event)
            else:
                return create_response(405, {'error': 'Method not allowed'})
        else:
            return create_response(404, {'error': 'Endpoint not found'})
            
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return create_response(500, {'error': 'Internal server error'})

def handle_health_check():
    """Health check endpoint"""
    return create_response(200, {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'environment': os.environ.get('DEPLOY_ENVIRONMENT', 'unknown'),
        'service': 'Training Roster Automation'
    })

def handle_get_roster():
    """Get training roster information"""
    # TODO: Implement actual roster retrieval logic
    # This is a placeholder implementation
    roster_data = {
        'roster_id': 'ROSTER-001',
        'training_name': 'AWS Lambda Training',
        'participants': [
            {'name': 'John Doe', 'email': 'john.doe@company.com', 'status': 'registered'},
            {'name': 'Jane Smith', 'email': 'jane.smith@company.com', 'status': 'registered'}
        ],
        'schedule': {
            'start_date': '2024-01-15',
            'end_date': '2024-01-16',
            'location': 'Virtual'
        },
        'last_updated': datetime.utcnow().isoformat()
    }
    
    return create_response(200, roster_data)

def handle_create_roster(event):
    """Create a new training roster"""
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # TODO: Implement actual roster creation logic
        # This is a placeholder implementation
        roster_id = f"ROSTER-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        response_data = {
            'roster_id': roster_id,
            'message': 'Training roster created successfully',
            'training_name': body.get('training_name', 'Default Training'),
            'created_at': datetime.utcnow().isoformat()
        }
        
        return create_response(201, response_data)
        
    except json.JSONDecodeError:
        return create_response(400, {'error': 'Invalid JSON in request body'})
    except Exception as e:
        logger.error(f"Error creating roster: {str(e)}")
        return create_response(500, {'error': 'Failed to create roster'})

def create_response(status_code, body):
    """Create a standardized API Gateway response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
        },
        'body': json.dumps(body, default=str)
    }
