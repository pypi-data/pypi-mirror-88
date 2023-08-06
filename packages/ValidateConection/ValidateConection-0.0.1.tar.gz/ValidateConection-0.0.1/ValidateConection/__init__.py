
import subprocess, platform
import os

def ping(host):
    #Returns True if host responds to a ping request  
    try:
        output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', host), shell=True)
        return True

    except Exception:
        return False



#print(ping("192.168.0.36"))
def ValidateRequest():
    i = 1
    while True:
        i = i + 1
        import time
        timeout = time.time() + 1   # 5 minutes from now
        while True:
            test = 0
            if test == 5 or time.time() > timeout:
                #print(ping("google.com"))
                if ping("www.google.com") == False:
                    print("Error de conexion en la Red")
                else:
                    print("Conexion de Red Exitosa")
                break
            test = test - 1
        if(i > 3):
            break

def ValidateDongleConection(STATUS_NUMBER):
    if(STATUS_NUMBER == 401):
        #print("Problema de conexion con Dongle")
        return "No se ha detectado Dongle"

    else:
        return "Conexion con Dongle exitosa"
        
def ShowExecutionNumber(EXECUTION_NUMBER):
    total_executions = str(EXECUTION_NUMBER)
    return "Tienes: " + total_executions + " Ejecuciones restantes"