import os
def findjobdir(jobpath, metatag):
    for dir in os.listdir(jobpath):
        dirpath = jobpath+dir
        if os.path.isdir(dirpath):
            for file in os.listdir(dirpath):
                if file.startswith("METADATA"):
                    with open(os.path.join(dirpath, file),'r') as fp:
                        lines = fp.readlines()
                        for line in lines:
                            try:
                                line.index(metatag)
                                return dir
                            except:
                                pass
    return None


jobpath = "/storage/work/y/yuw3/dfttk/ytests/"
metatag = '343f9bb2-640d-4312-9039-05516d5925f3'
dir=findjobdir(jobpath, metatag)
if dir!=None: print(dir)
