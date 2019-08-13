from app import app

if __name__ == "__main__":
    from gevent import monkey
    monkey.patch_all()
    #hmm
    app.run()
    # app.run(host= '0.0.0.0') # batu - left it here for future use
    # app.run(use_reloader=True) # Uncomment this or run production mode if you want APScheduler to work properly
