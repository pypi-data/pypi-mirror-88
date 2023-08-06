from weboa.libraries import Library

class FontAwesome(Library):
    def __init__(self):
        self.name = "Font Awesome"
        self.css = ["https://use.fontawesome.com/releases/v5.8.2/css/all.css"]

class Roboto(Library):
    def __init__(self):
        self.name = "Roboto"
        self.css = ["https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"]