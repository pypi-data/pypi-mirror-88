from PIL import Image
from weboa.utils import Processing
from weboa.utils import Printer
from weboa import os
from weboa import prepare

class General(Processing):
    def __init__(self, langs=("en","ru"), path = "../"):
        super().__init__(path=path)
        self.langs = langs

    def robots(self):
        self.copy(prepare.Package.stream + 'misc/robots.txt',"/robots.txt")

    def ico(self):
        img = Image.new('RGB', (64, 64))
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
        img.save(os.path.join(self.path, self.BUILDFOLDER)+'/favicon.ico', sizes=icon_sizes)

    def css(self):
        files = ("/css/styles.css", "/css/styles.min.css")
        for f in files:
            self.File_Create(f)

    def js(self):
        files = ("/js/script.js","/js/script.min.js")
        for f in files:
            self.File_Create(f)

    def img(self):
        img = Image.new('RGB', (128, 128))
        img.save(os.path.join(self.path, self.BUILDFOLDER) + '/img/favicon.png')
        img = Image.new('RGB', (1024, 500))
        img.save(os.path.join(self.path, self.BUILDFOLDER) + '/img/sn_share.png')

    def readme(self):
        self.copy(prepare.Package.stream + 'misc/README.md', "/README.md")

    def gitignore(self):
        self.copy(prepare.Package.stream + 'misc/gitignore',"/.gitignore")

    def ico_langs(self):
        for l in self.langs:
            self.copy(prepare.Package.stream + 'ico_langs/'+l+'.svg',"/img/"+l+".svg")

    def script(self, jscript):
        with open(self.path + self.BUILDFOLDER + "/php/modules/footer.phtml", "r") as f:
            scripts = f.read()
        scripts = scripts.split("\n")
        Printer.log("Loading " + jscript)
        for s in jscript.load_script():
            scripts.insert(-1, "<script src='" + s + "'></script>")
            with open(self.path + self.BUILDFOLDER + "/php/modules/footer.phtml", "w") as f:
                f.write("\n".join(scripts))

    def link(self, _link):
        with open(self.path+self.BUILDFOLDER+"/php/modules/header.phtml","r") as f:
            _links = f.read()
        _links = _links.split("\n")
        for s in _link.load_link():
            _links.insert(-1, "<link href='" + s + "' rel='stylesheet'/>")
            with open(self.path + self.BUILDFOLDER + "/php/modules/header.phtml", "w") as f:
                f.write("\n".join(_links))