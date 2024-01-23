'''
This module is the entry point of the Flask application. 

It creates an instance of the application and runs it. 
By default, the application will run in debug mode when run directly.
When deployed in a production environment, the WSGI server will use the `app` object.

Usage:
    python3 main.py
'''

from app import create_app #pylint: disable=import-error

app = create_app('development')
# Flask application instance.
# A call to create_app creates application instance from the app module.

if __name__ == '__main__':
    # The application instance will be run directly if this script is executed as the main script.
    # If this script is imported from another script, the application instance will not run.
    # Instead, the other script or the WSGI server can use the 'app' object.
    app.run(debug=True)
