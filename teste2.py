import json
import PySimpleGUI as sg
import serial
from Communication import Communication
import random

layout = [	[sg.Text("Teste da Carga Eletrônica")],
[sg.Text("Serial port")],[sg.InputText("COM5")],
[sg.Text("Baud Rate")],[sg.InputText("9600")],
[sg.Text("Timeout")],[sg.InputText("0.1")],
[sg.Text("Limite superior")],[sg.InputText("1000")],
[sg.Text("Numero de tentativas")],[sg.InputText("1000")],
[sg.Text("Limite inferior")],[sg.InputText("100")],
[sg.Button("OK")],[sg.Button("Cancel")]	]

# Create the window
window = sg.Window("Teste da Carga", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the Cancel button
    if event == sg.WIN_CLOSED or event == "Cancel":
        break
    error_log=[]
    serial_port=values[0]
    baud_rate=float(values[1])
    timeout=float(values[2])
    superior=int(values[3])
    n_tentativas=int(values[4])
    inferior=int(values[5])
    comm=Communication(serial_port,baud_rate,timeout)
    for i in range(0,n_tentativas):
        corrente=random.randint(inferior,superior)
        response=comm.send_message(6,0,corrente)
        if response!=0:
            error_log.append([corrente,response])
    n_erros=len(error_log)
    taxa_erros=n_erros/n_tentativas
    error_report=[	
    				{
	    				"Limite Superior":superior,
	    				"Numero de tentativas":n_tentativas,
	    				"Limite Inferior":inferior,
                        "Numero de erros":n_erros,
	    				"Taxa de erros":taxa_erros,
	    				"Log de erros":error_log
    				}
    			]
    error_layout = [ [sg.Text("Numero de erros: "+str(n_erros))],[sg.Text("Taxa de erros: "+str(taxa_erros))] , [sg.Button("OK")] ]
    error_window = sg.Window("Error log",error_layout)
    while True:
    	event, values = error_window.read()
    	if event == sg.WIN_CLOSED or event == "OK":
    		break
    error_window.close()
    with open('error_log_random.json') as infile:
    	data=json.load(infile)
    data.append(error_report)
    with open('error_log_random.json','w') as outfile:
    	json.dump(data, outfile,indent=4)


window.close()

