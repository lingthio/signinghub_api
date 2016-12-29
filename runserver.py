import os
from example_app.example_app import app

# Start a Flask development server with SSL support
if __name__ == "__main__":
    # Let Werkzeug create the SSL server
    ssl_context = (app.root_path+'/server.crt', app.root_path+'/server.key')

    print()
    print("Point your browser to https://localhost:5443")
    print("Notice the 's' in 'https' and the 5443 port instead of the usual 5000")
    print()

    app.run(host='127.0.0.1',port=5443,
            debug = True, ssl_context=ssl_context)

