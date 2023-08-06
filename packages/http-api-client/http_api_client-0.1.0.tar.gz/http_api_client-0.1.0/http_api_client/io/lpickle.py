import pickle
import pathlib


class CachedObject():

    def __init__(self, path: pathlib.Path):
        self.path = path
        self.cached_object = None
        
    def get(self):
        return self.cached_object

    def set(self, o):
        self.cached_object = o

    def load(self):
        self.cached_object = load_pickle(self.path)
        return self.cached_object

    def save(self):
        save_pickle(self.path, self.cached_object)


def load_pickle(path: pathlib.Path, log=None) -> object:
    """
    Load a pickle file
    """
    if log:
        log.debug(f'Attempting to load python object from path: {path}')

    try:
        with open(path, 'rb') as handle:
            return pickle.load(handle)
        
    except Exception as e:

        msg = f'Error loading pickle file: {path} : {e!r}'
        
        if log:
            log.error(msg)

        else:
            print(msg)


def save_pickle(path: pathlib.Path, o: object, log=None) -> pathlib.Path:

    if log:
        log.debug(f'Attempting to save python object using pickle to path: {path}')

    try:
        with open(path, 'wb') as handle:
            pickle.dump(o, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
        return path
            
    except Exception as e:
        msg = f'Error saving object to path: {path} : {e!r}'
        if log:
            log.error(msg)
        else:
            print(msg)

