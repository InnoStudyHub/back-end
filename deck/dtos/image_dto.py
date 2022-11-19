class Image:
    def __init__(self, filename, content, content_type):
        self.name = filename
        self.content = content
        self.content_type = content_type

    def read(self):
        return self.content