import posixpath
import os.path

SKIP_FILE = object()


class HeaderHandler(object):

    def __init__(self, include_paths):
        self.include_paths = list(include_paths)
        self.resolved = {}

    def _open(self, header_path):
        try:
            f = open(header_path)
        except IOError:
            return None
        else:
            return f

    def add_include_paths(self, include_paths):
        self.include_paths.extend(include_paths)

    def _resolve(self, anchor_file):
        if anchor_file is not None:
            if os.path.sep != posixpath.sep:
                anchor_file = anchor_file.replace(os.path.sep,
                                                  posixpath.sep)
            yield posixpath.dirname(anchor_file)
        for include_path in self.include_paths:
            yield include_path

    def open_header(self, include_header, skip_file, anchor_file):
        header_path = self.resolved.get(include_header)
        f = None
        if header_path is not None:
            if skip_file(header_path):
                return SKIP_FILE
            else:
                return self._open(header_path)
        for include_path in self._resolve(anchor_file):
            header_path = posixpath.join(include_path, include_header)
            f = self._open(posixpath.normpath(header_path))
            if f:
                self.resolved[include_header] = f.name
                break
        return f


class FakeFile(object):

    def __init__(self, name, contents):
        self.name = name
        self.contents = contents

    def __iter__(self):
        for line in self.contents:
            yield line

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class FakeHandler(HeaderHandler):

    def __init__(self, header_mapping, include_paths=()):
        self.header_mapping = header_mapping
        super(FakeHandler, self).__init__(list(include_paths))

    def _open(self, header_path):
        contents = self.header_mapping.get(header_path)
        if contents is not None:
            return FakeFile(header_path, contents)
        else:
            return None

    def parent_open(self, header_path):
        return super(FakeHandler, self)._open(header_path)
