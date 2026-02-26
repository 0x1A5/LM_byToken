from os import system
import json

class Launch:
    def __init__(self, dir, version, acc_token, username, uuid):

        self.versiondir = dir["versionDir"]
        self.assetsdir = dir["assetsDir"]
        self.javadir = dir["javaDir"]
        self.version = version
        self.acc_token = acc_token
        self.username = username
        self.uuid = uuid
        
        self.bat = f"cd /D \"{self.versiondir}/{self.version}/\" \n\"{self.javadir}/java.exe\" "
    def launchMinecraft(self):
        self.libraries = open(f"{self.versiondir}/{self.version}/{self.version}.json", "r")
        self.libraries_data = json.load(self.libraries)
        self.libraries.close()

        self.libraries_list = self.libraries_data["libraries"]

        self.libraries_java_cp = ""
        for i in self.libraries_list:
            path0 = i["name"]
            path1 = path0.split(":")
            path2 = path1[0]
            path2_1 = path2.split(".")
            path2_2 = "/".join(path2_1)
            path1_1 = path1[1:]
            path2_2 += f"/{path1_1[0]}/{path1_1[1]}/{'-'.join(path1_1)}.jar"
            self.libraries_java_cp += f"{self.assetsdir}/libraries/{path2_2};"
            

        self.libraries_java_cp += f"{self.versiondir}/{self.version}/{self.version}.jar"
        self.bat += f"-cp \"{self.libraries_java_cp}\" "

        self.bat += f"{self.libraries_data['mainClass']} "
        self.bat += f"--gameDir \"{self.versiondir}/{self.version}\" "
        self.bat += f"--assetsDir \"{self.assetsdir}/assets\" "
        
        self.assetindex = self.libraries_data["assetIndex"]["id"]
        self.bat += f"--assetIndex {self.assetindex} "

        self.bat += f"--version \"{self.version}\" "

        self.bat += f"--username {self.username} "
        self.bat += f"--uuid {self.uuid} "
        self.bat += f"--accessToken {self.acc_token} "
        self.bat += "--userType msa "

        self.bat_file = open(".\Launch\launch.bat", "w")
        self.bat_file.write(self.bat)
        self.bat_file.close()

        system(".\Launch\launch.bat")

        
        