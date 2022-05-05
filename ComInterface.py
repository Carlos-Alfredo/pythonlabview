import serial.tools.list_ports
from Communication import Communication
import PySimpleGUI as sg
import random


comlist=serial.tools.list_ports.comports()
devicelist=[]
for element in comlist:
	devicelist.append(element.device)

layout = [	[sg.Text("Controlador da Carga Eletronica")],
[sg.Text("Serial Port")],[sg.Combo(values=devicelist)],
[sg.Text("Modo de Operacao")],[sg.Combo(values=["OFF","Corrente Continua","Potencia Continua","Resistencia Continua"])],
[sg.Text("Valor")],[sg.InputText("")],
[sg.Button("OK")],[sg.Button("Cancel")]	]

# Create the window
window = sg.Window("Controlador da Carga", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the Cancel button
    if event == sg.WIN_CLOSED or event == "Cancel":
        break
    serial_port=values[0]
    baud_rate=9600
    timeout=0.1
    if values[1]=="OFF":
    	modo_operacao=0
    elif values[1]=="Corrente Continua":
    	modo_operacao=1
    elif values[1]=="Potencia Continua":
    	modo_operacao=2
    elif values[1]=="Resistencia Continua":
    	modo_operacao=3
    valor=int(values[2])
    comm=Communication(serial_port,baud_rate,timeout)
    response=comm.send_message(6,modo_operacao,valor)
    error_log=0
    if response!=0:
    	error_layout = [ [sg.Text("Erro Codigo "+str(response))], [sg.Button("OK")] ]
    	error_window = sg.Window("Error log",error_layout)
    	while True:
    		event, values = error_window.read()
    		if event == sg.WIN_CLOSED or event == "OK":
    			break
    	error_window.close()
window.close()

