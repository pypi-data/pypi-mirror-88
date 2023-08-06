from weboa.project import *
from weboa import json
from weboa import __VERSION__

class PHP(General):
    def __init__(self, langs=("en","ru"), path = "../"):
        super().__init__(langs=langs,path=path)
        Printer.log("Start PHP Project")
        Printer.info(f"Your system is {self.os}")
        Printer.info(f"Weboa version is {__VERSION__}")

    def FS(self):
        # Creating folders for php project
        folders = ("","/css","/js","/img","/php","/php/api","/php/configs","/php/controller","/php/lib","/php/modules")
        for f in folders:
            self.Folder_Create(f)
        self.File_Create("/.weboa", json.dumps(Processing.Weboa_Create()))

    def index(self):
        self.copy(prepare.Package.stream + 'phpfs/_index.php',"/index.php")

    def language(self):
        # Language system
        self.copy(prepare.Package.stream + 'phpfs/language',"/php/controller/language.php")
        for l in self.langs:
            self.copy(prepare.Package.stream + 'phpfs/l', f"/php/configs/{l}.php")

    def controller(self):
        files = ("controller.php","index.php","router.php")
        for f in files:
            self.copy(prepare.Package.stream + 'phpfs/'+f,"/php/controller/"+f)

        # .htaccess
        self.copy(prepare.Package.stream + 'phpfs/.htaccess',"/.htaccess")

    def project(self):
        self.copy(prepare.Package.stream + 'phpfs/db',"/php/db.php")                     # DATABASE
        self.copy(prepare.Package.stream + 'phpfs/test',"/php/api/test.php")             # API
        self.copy(prepare.Package.stream + 'phpfs/consts',"/php/configs/consts.php")     # CONSTS
        self.copy(prepare.Package.stream + 'phpfs/header', "/php/modules/header.phtml")  # META
        self.copy(prepare.Package.stream + 'phpfs/footer', "/php/modules/footer.phtml")  # SCRIPTS

    def libs(self):
        self.copy(prepare.Package.stream + 'phpfs/autoload.php', "/php/lib/autoload.php")
        _path = os.path.join(self.path,prepare.Package.stream + 'phplib/')

        with open(_path+'libs.json') as json_file:
            data = json.load(json_file)
            data = json.dumps(data,indent=2)

        Printer.info("Libs versions:\n"+data)
        for f in os.listdir(_path):
            if(os.path.isdir(_path+f)):
                self.copytree(prepare.Package.stream + 'phplib/'+f,"/php/lib/"+f)
            else:
                self.copy(prepare.Package.stream + 'phplib/' + f, "/php/lib/" + f)