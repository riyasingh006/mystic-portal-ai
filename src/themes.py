class Theme:

    def __init__(self):

        self.index = 0

        self.themes = [

            {
                "name": "Orange",
                "ring": (0, 170, 255),
                "particle": (0, 120, 255)
            },

            {
                "name": "Blue",
                "ring": (255, 180, 0),
                "particle": (255, 255, 0)
            },

            {
                "name": "Purple",
                "ring": (255, 0, 255),
                "particle": (255, 120, 255)
            },

            {
                "name": "Green",
                "ring": (0, 255, 120),
                "particle": (0, 255, 0)
            }

        ]

    def get(self):

        return self.themes[self.index]

    def next(self):

        self.index += 1

        if self.index >= len(self.themes):
            self.index = 0