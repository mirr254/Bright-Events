#!flask/bin/python
from app import createApp 

app = createApp('development')

if __name__ == '__main__':
    app.run(debug=True)