import os, sys, configparser, datetime

now = datetime.datetime.now()
args = sys.argv

if (os.path.exists('log/')):
    logFile = open("log/"+now.strftime("%Y %m %d %H %M %S")+".log", "a")
else:
    os.mkdir('log')
    logFile = open("log/"+now.strftime("%Y %m %d %H %M %S")+".log", "a")

def die(error = False, message = "Unknown error!"):
    logFile.close()
    if error == True:
        sys.exit(message)

def log(message, level = 0):
    now = datetime.datetime.now()
    
    if (level == 0):
        logFile.write('['+now.strftime("%H:%M:%S")+'] '+config['LOGGING']['0']+': '+message+'\n')
        print('['+now.strftime("%H:%M:%S")+'] '+config['LOGGING']['0']+': '+message)
    elif (level == 1):
        logFile.write('['+now.strftime("%H:%M:%S")+'] '+config['LOGGING']['1']+': '+message+'\n')
        print('['+now.strftime("%H:%M:%S")+'] '+config['LOGGING']['1']+': '+message)
    elif (level == 2):
        logFile.write('['+now.strftime("%H:%M:%S")+'] '+config['LOGGING']['2']+': '+message+'\n')
        print('['+now.strftime("%H:%M:%S")+'] '+config['LOGGING']['2']+': '+message)
    elif (level == 3):
        logFile.write('['+now.strftime("%H:%M:%S")+'] '+config['LOGGING']['3']+': '+message+'\n')
        print('['+now.strftime("%H:%M:%S")+'] '+config['LOGGING']['3']+': '+message)
    elif (level == 4):
        logFile.write('['+now.strftime("%H:%M:%S")+'] '+config['LOGGING']['4']+': '+message+'\n')
        die(True, '['+now.strftime("%H:%M:%S")+'] '+config['LOGGING']['4']+': '+message)
    else:
        die(True, 'Invalid level!')

if (os.path.exists("config.ini")):
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
else:
    file = open("config.ini", "a")
    file.write("[LOGGING]\n")
    file.write("0=LOG\n")
    file.write("1=INFO\n")
    file.write("2=WARN\n")
    file.write("3=ERROR\n")
    file.write("4=FATAL ERROR\n\n")
    file.write("[VAULT]\n")
    file.write("location=\n")
    file.write("duplicate=yes\n")
    file.write("duplicates=3\n\n")
    file.close()
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    log('No config file found!', 2)

def TUI():
    print

if (len(args) == 3):
    print(str(args[1]))
    print(str(args[2]))

die()