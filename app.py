from website import create_app #can because website is the python package by init

app = create_app()

if __name__ == '__main__': #only run if we run this file => not import
    app.run(host='0.0.0.0', port=5000, debug=True)