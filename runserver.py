import os
from example_app.example_app import app

# Start a Flask development server with SSL support
if __name__ == "__main__":
    # Optional HTTPS Server
    # ssl_context = (app.root_path+'/server.crt', app.root_path+'/server.key')
    # print("Point your browser to https://localhost:5443")
    # print("Notice the 's' in 'https' and the 5443 port instead of the usual 5000")
    # app.run(host='127.0.0.1', port=5443, debug=True, ssl_context=ssl_context)
    # Optional HTTPS Server

    # Normal HTTP Server
    app.run(host='127.0.0.1',port=5000, debug=True)

