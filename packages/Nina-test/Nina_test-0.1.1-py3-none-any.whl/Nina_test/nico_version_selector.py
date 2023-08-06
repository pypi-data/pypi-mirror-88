from .pd import *

def set_version(app,version):
    app+=f' {version}'
    return app

def create_versions(app,major,minor,micro_limit):
    version_list=[]
    version= [major,minor,0]
    version_text=f'{version[0]}.{version[1]}.{version[2]}'
    app2=app
    for i in range(micro_limit):
        version[2] = i
        version_text=f'{version[0]}.{version[1]}.{version[2]}'
        app2=app
        app2+=f' {version_text}'
        version_list.append(app2)
        print(app2)
    return version_list

def version_to_csv(vl,fl):
    create_csv(fl,vl,Frame=True)

