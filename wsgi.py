from app import create_app

# Create the app instance
app = create_app()

# Gunicorn will look for this app instance to run
if __name__ == "__main__":
    app.run()