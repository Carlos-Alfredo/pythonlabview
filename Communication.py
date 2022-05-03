import serial

class Communication():

	def __init__(self,port,baudrate,timeout):
		self.ser=serial.Serial()
		self.ser.port=port
		self.ser.baudrate=baudrate
		self.ser.timeout=timeout
		self.ser.close()

	def protocol(self,id,command,subcommand,data1,data2,data3,data4):
		checksum=(id+command+subcommand+data1+data2+data3+data4)%256
		return ((id << 56)+ (command << 48) + (subcommand << 40) + (data1 << 32) + (data2 << 24) + (data3 << 16) + (data4 << 8) + checksum).to_bytes(8,'big')

	def send_message(self,command,subcommand,data):
		message=self.protocol(0,command,subcommand,(data >> 8), data%256,0,0)
		self.ser.open()
		self.ser.read(self.ser.in_waiting)
		self.ser.write(message)
		response=self.ser.read(8)
		resp_handler=self.response_handler(response)
		self.ser.close()
		return resp_handler

	def response_handler(self,response):
		vector=list(response)
		resp_handler=0
		if len(vector)!=8:
			resp_handler=-1 #Timeout error
		elif vector[1]==0:
			resp_handler=vector[2]
		return resp_handler

