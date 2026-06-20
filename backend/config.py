import os

class Config:
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    BASE_DIR = os.getcwd()
    MODEL_PATH = os.environ.get('MODEL_PATH', os.path.join(BASE_DIR, 'model', 'saved_model', 'freshscan.h5'))
