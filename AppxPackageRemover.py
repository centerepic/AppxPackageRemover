import os, colorama, ctypes
import subprocess
import sys

def IsAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

class Powershell:
    def Run(command : str, output : bool = True):
        match output:
            case True:
                p = subprocess.Popen(["powershell.exe", command], stdout=sys.stdout)
                p.communicate()
            case False:
                p = subprocess.Popen(["powershell.exe", command], stdout=subprocess.PIPE)
                return p.communicate()
            
if not IsAdmin():
    print(f"{colorama.Fore.RED}Please run this script as administrator!{colorama.Fore.RESET}")
    input("Press enter to exit...")
    exit()

while True:
    print("Packages:")

    result = Powershell.Run("Get-AppxPackage | Select-Object Name, PackageFullName", False)
    longest_package_name = 0

    for line in result[0].decode("utf-8").split("\r\n"):
        if line != "" and "." in line:
            packagename = line.split(" ")[0]
            if len(packagename) > longest_package_name:
                longest_package_name = len(packagename)

    for line in result[0].decode("utf-8").split("\r\n"):
        if line != "" and "." in line:
            packagename = line.split(" ")[0]
            packagefullname = '_'.join(line.split('_')[1:])
            print(f"{colorama.Fore.GREEN}{packagename}{colorama.Fore.RESET}{" " * (longest_package_name - len(packagename))} @ {colorama.Fore.YELLOW}{packagename + "_" + packagefullname}{colorama.Fore.RESET}")
    
    input_package = input("Package to remove (Enter package full name): ")

    if input_package == "":
        break

    Powershell.Run(f"Remove-AppxPackage {input_package}")
    print(f"{colorama.Fore.GREEN}Package {input_package} removed{colorama.Fore.RESET}")
    input("Press enter to continue...")