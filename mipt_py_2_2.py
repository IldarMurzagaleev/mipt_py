from pathlib import Path
import tempfile


class File:
    def __init__(self, path_to_file):
        self.path = path_to_file
        path = Path(self.path)
        path.touch(exist_ok=True)

    def __str__(self):
        return self.path

    def __iter__(self):
        with open(self.path) as f:
            self.lines = f.readlines()
            return iter(self.lines)

    def __next__(self):
        return next(self.lines)

    def read(self):
        with open(self.path) as f:
            lines = f.readlines()
        return ''.join(lines)

    def write(self, text):
        with open(self.path, 'w') as f:
            f.write(text)

    def __add__(self, second_file):
        tmp = tempfile.gettempdir()
        name = self.path.split('/')[-1].split('.')[0] + '_' + second_file.path.split('/')[-1].split('.')[0]
        new = File(tmp + '/' + name)
        new.write(self.read() + second_file.read())
        return new
