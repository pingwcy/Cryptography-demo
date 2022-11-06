def getfilesalt(filename):
    try:
        realfilename = filename+'.SafeSloth'
        file = open(realfilename, 'rb')
        salt = file.read(32)
        file.close()
    except:
        realfilename = filename+'.Cha.SafeSloth'
        file = open(realfilename, 'rb')
        salt = file.read(32)
        file.close()
    return salt
    
