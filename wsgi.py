import os
from app import createApp

app = createApp( os.getenv('APP_SETTINGS'))

if __name__ == "__main__":
    app.run()