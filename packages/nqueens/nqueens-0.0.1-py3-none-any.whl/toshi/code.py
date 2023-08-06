import sys
import subprocess
import ast
from collections import namedtuple

def find_modules(path):
    
    Import = namedtuple("Import", ["module", "name", "alias"])
    with open(path) as fh:        
       root = ast.parse(fh.read(), path)

    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):  
            module = node.module.split('.')
        else:
            continue

        for n in node.names:
            print(Import(module, n.name.split('.'), n.asname))

def list_packages():
    # process output with an API in the subprocess module:
    reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

    i =1
    print("----------", "Installed Packages are : ", "----------")
    for package in installed_packages:
        print(i,".", package)
        i = i +1
    print("-----------------------------------------------")
    
    return installed_packages

def install(package_name):
    
    reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    
    if package_name in installed_packages:
        print("----------", package_name, "- Package already installed", "----------")
    else:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
        print("----------", package_name, "-Installed by toshi", "----------")
        
def add(package_name):
    
    reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    
    if package_name in installed_packages:
        print("----------", package_name, "- Package already installed", "----------")
    else:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
        print("----------", package_name, "-Installed by toshi", "----------")
    
def install_packages(package_list):
    
    reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    
    for package_name in package_list:
        if package_name in installed_packages:
            print("----------", package_name, "- Package already installed", "----------")
        else:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
            print("----------", package_name, "- Installed by toshi", "----------")
            
def add_packages(package_list):
    
    reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    
    for package_name in package_list:
        if package_name in installed_packages:
            print("----------", package_name, "- Package already installed", "----------")
        else:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
            print("----------", package_name, "- Installed by toshi", "----------")
        
def check(package_name):
    
    reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    
    if package_name in installed_packages:
        print("----------", package_name, "- Package already installed", "----------")
    
    
def remove(package_name):
    reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    
    if package_name not in installed_packages:
        print("----------", package_name, "- Package not installed", "----------")
    else:
        subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall','-y', package_name])
        print("----------", package_name, "- Unistalled by toshi", "----------")
        
def remove_packages(package_list):
    reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    
    for package_name in package_list:
        if package_name not in installed_packages:
            print("----------", package_name, "- Package not installed", "----------")
        else:
            subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall','-y', package_name])
            print("----------", package_name, "- Unistalled by toshi", "----------")
        
def uninstall(package_name):
    reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    
    if package_name not in installed_packages:
        print("----------", package_name, "- Package not installed", "----------")
    else:
        subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall','-y', package_name])
        print("----------", package_name, "- Unistalled by toshi", "----------")
        
def uninstall_packages(package_list):
    reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    
    for package_name in package_list:
        if package_name not in installed_packages:
            print("----------", package_name, "- Package not installed","----------")
        else:
            subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall','-y', package_name])
            print("----------", package_name, "- Unistalled by toshi", "----------")
    
# install('numpy')
# check('numpy')

# packages= ['simplejson']
# install_packages(packages)

# remove('simplejson')
# uninstall_packages(packages)

# list_packages()

# find_modules("E:\Machine_learning\ML_001_Heart_faliure\Prediction_algorithms\Decision_tree\decision_tree.py")
