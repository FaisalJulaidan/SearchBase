try:
    import unzip_requirements
except ImportError:
    pass

from app import app

if __name__ == "__main__":
    app.run()
