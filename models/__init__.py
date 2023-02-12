" Runs at initialization of the models module "

from .engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
