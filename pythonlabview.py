import serial

from Communication import Communication

serial_port='COM5'
baud_rate=9600
timeout=0.5
passo=10
n_degraus=20
piso=100
error_log=[]

comm=Communication(serial_port,baud_rate,timeout)

for i in range(0,n_degraus):
	response=comm.send_message(6,0,piso+i*passo)
	if response!=0:
		error_log.append([i,response])

print(error_log)
