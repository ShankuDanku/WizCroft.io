primary = '#2c2f33'
secondary = '#23272a'
content = '#acacad'
accent = '#4884ff'
inactive = 'grey'

# standard block text font
std_font = ('Uni Sans-Trial', 20, 'normal')


class Font:
    def __init__(self, family, size, style='normal'):
        self.family = family
        self.size = size
        self.style = style

    def getFont(self):
        return self.family, self.size, self.style
