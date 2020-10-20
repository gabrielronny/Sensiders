import psutil, time, sys, os
from crawlerOHM import gerarTemperatura

def getCPU():
    valCPU = psutil.cpu_percent() # percentual de CPU
    return valCPU

def getRAM():
    valRAM = psutil.virtual_memory()[2] # percentual de RAM
    return valRAM

def getHD():
    valHD = psutil.disk_usage('/')[3] # percentual de ocupação HD na raiz
    return valHD

def getDownloadAndUpload():
    oldDownload = psutil.net_io_counters()[1] # pega os dados de download antes de 1s
    oldUpload = psutil.net_io_counters()[0]
    time.sleep(1) # espera 1s para o calculo KiB/s
    newDownload = psutil.net_io_counters()[1] # pega os dados de download depois de 1s
    newUpload = psutil.net_io_counters()[0]

    # assim realiza o calculo do novo - antigo para saber o uso durante o 1s
    valDownload = round((newDownload - oldDownload) / (2**10)) # KiB/s Download
    valUpload = round((newUpload - oldUpload) / (2**10)) # KiB/s Upload

    return (valDownload, valUpload)

def getTemp():
    if sys.platform == 'linux': # se o OS for linux
        if not "Microsoft" in os.uname(): # se NAO for WSL
            dadosTemp = psutil.sensors_temperatures(fahrenheit=False)
            if bool(dadosTemp): # se estiver em linux nativo
                tempCPU = dadosTemp.get('coretemp')[0][1] # temperatura CPU (celsius)
            else: # se estiver em linux VM (ex: virtualBox)
                tempCPU = 0 # (TODO: deixamos como 0 enquanto OHM não conseguir pegar pela VM)
        else: # se for WSL
            tempCPU = gerarTemperatura()
    elif sys.platform == 'win32': # se OS for Windows
        tempCPU = gerarTemperatura()

    return tempCPU

def getSWAP():
    valSWAP = psutil.swap_memory()[3] # percentual de SWAP
    return valSWAP

def getTASKS():
    valTASKS = len(psutil.pids()) # quantidade de tarefas/processos em execução
    return valTASKS


""" CODIGO ANTIGO (BACKUP)

def dadosHardware():
    valNET = getDownloadAndUpload()

    valDownload = valNET[0]
    valUpload = valNET[1]
    valCPU = getCPU()
    valRAM = getRAM()
    valHD = getHD()
    tempCPU = getTemp()
    valSWAP = getSWAP()
    valTASKS = getTASKS()

    maquina = 1

    t = time.localtime()
    valTEMPO = ('{}-{}-{} {}:{}:{}'.format(t[0], t[1], t[2], t[3], t[4], t[5]))

    hardware = {
    'cpu': valCPU,
    'memory': valRAM,
    'disk': valHD,
    'download': valDownload,
    'upload': valUpload,
    'temp': tempCPU,
    'swap': valSWAP,
    'tasks': valTASKS,
    'maquina': maquina
    }
    print(hardware)

    dadosHW = (valCPU, valRAM, valHD, valDownload, valUpload, tempCPU, valSWAP, valTASKS, maquina, valTEMPO)
    return [dadosHW, hardware]
"""
