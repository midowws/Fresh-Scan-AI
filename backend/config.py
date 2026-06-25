import os


class Config:
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    basedir = os.path.abspath(os.path.dirname(__file__))
    MODEL_PATH = os.path.join(basedir, '../model/saved_model/freshscan.h5')
