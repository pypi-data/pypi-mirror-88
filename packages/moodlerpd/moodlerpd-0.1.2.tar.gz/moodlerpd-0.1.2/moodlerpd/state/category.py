class Category:
    def __init__(self, _id: int, name: str, parent_id: int):
        self.id = _id
        self.name = name
        self.parent_id = parent_id

    def __str__(self):
        message = 'Category ('
        message += 'id: %s' % self.id
        message += ', name: "%s"' % self.name
        message += ', parent_id: "%s"' % self.parent_id
        message += ')'
        return message
