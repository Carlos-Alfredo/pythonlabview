import json
import PySimpleGUI as sg
import serial
from Communication import Communication

layout = [	[sg.Text("Hello from PySimpleGUI")],
[sg.Text("Serial port")],[sg.InputText("COM5")],
[sg.Text("Baud Rate")],[sg.InputText("9600")],
[sg.Text("Timeout")],[sg.InputText("1")],
[sg.Text("Passo")],[sg.InputText("10")],
[sg.Text("Numero de degraus")],[sg.InputText("10")],
[sg.Text("Piso")],[sg.InputText("10")],
[sg.Button("OK")],[sg.Button("Cancel")]	]

# Create the window
window = sg.Window("Teste da Carga", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED or event == "Cancel":
        break
    error_log=[]
    serial_port=values[0]
    baud_rate=float(values[1])
    timeout=float(values[2])
    passo=int(values[3])
    n_degraus=int(values[4])
    piso=int(values[5])
    comm=Communication(serial_port,baud_rate,timeout)
    for i in range(0,n_degraus):
    	response=comm.send_message(6,0,piso+i*passo)
    	if response!=0:
    		error_log.append([i,response])
    n_erros=len(error_log)
    taxa_erros=n_erros/n_degraus
    error_report=[	
    				{
	    				"Passo":passo,
	    				"Numero de degraus":n_degraus,
	    				"Piso":piso,
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
    with open('error_log.json') as infile:
    	data=json.load(infile)
    data.append(error_report)
    with open('error_log.json','w') as outfile:
    	json.dump(data, outfile,indent=4)


window.close()

