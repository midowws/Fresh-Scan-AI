import os

class Config:
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    MODEL_PATH = os.environ.get('MODEL_PATH', '../model/saved_model/freshscan.h5')