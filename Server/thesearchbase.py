from app import app

if __name__ == "__main__":
    # app.run()
    app.run(use_reloader=False)  # Uncomment this or run production mode if you want APScheduler to work properly
