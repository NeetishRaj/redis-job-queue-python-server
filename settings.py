
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None  # Change this if your Redis server requires authentication
CUSTOM_QUEUES = {
    'MEDIUM': {
        'default_timeout': 36000,  # Example timeout value in seconds (10 hour)
    }
}
RESULT_TTL_MEDIUM = 3600000  # Custom TTL for MEDIUM queue: 1000 hours