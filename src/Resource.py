from EpsUtil import text_length_in_picture

class Resource(object):
    def __init__(self, data, label=None):
        self.data = data
        if label is None:
            self.label = self.data.n3()
        else:
            self.label = label

        self.len_x = text_length_in_picture(self.label)

    def __str__(self):
        return f"<Resouce label={self.label}>"
