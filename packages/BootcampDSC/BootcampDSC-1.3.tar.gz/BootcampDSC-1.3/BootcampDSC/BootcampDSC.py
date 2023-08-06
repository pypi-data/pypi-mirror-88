from PIL import Image
from urllib.request import urlopen

class BootcampDSC:
    def IntroOOPIllustration(self):
        self.gambar = Image.open(urlopen('https://i.ibb.co/mvvXrj5/oop.jpg'))
        return self.gambar

    def ClassIllustration(self):
        self.gambar = Image.open(urlopen('https://i.ibb.co/gzpHLc3/class.jpg'))
        return self.gambar

    def MethodIllustration(self):
        self.gambar = Image.open(urlopen('https://i.ibb.co/hcbd2hd/class-method-attribute.jpg'))
        return self.gambar
    
    def InheritanceIllustration(self):
        self.gambar = Image.open(urlopen('https://i.ibb.co/HYj0Bcr/inherit.jpg'))
        return self.gambar


