from src import app


@app.route('/debug')
def debugPage():
    return 'Hello World!'
