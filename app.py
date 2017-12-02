#!flask/bin/python
from app import createApp 

app = createApp('development')

if __name__ == '__main__':
    app.run(host='0.0.0.0')