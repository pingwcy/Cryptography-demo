def getfilesalt(filename):
    realfilename = filename+'.SafeSloth'
    file = open(realfilename, 'rb')
    salt = file.read(32)
    file.close()
    return salt
    
