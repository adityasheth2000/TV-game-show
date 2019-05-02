import socket 
import select 
import sys 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

IP_address = '172.16.144.247' 
Port = 8888
server.connect((IP_address, Port)) 

while True: 
	message=server.recv(2048)
	if("quit" in message):
		if("No winner" in message):
			print("NO WINNERS")
		else:
			print("Winnner is player: "+message[5])
		server.close()
		sys.exit()
	if('Question' in message):
		print(message)
		list_input=[server,sys.stdin]
		read_sockets,write_socket, error_socket = select.select(list_input,[],[])		
		if(read_sockets[0]==server):
			stop_taking_input=server.recv(2048)
			print(stop_taking_input)
			sys.stdout.flush()
			continue
		else:
			buzzer=raw_input() 
			server.send(buzzer)
			take_answer=server.recv(2048)
			print(take_answer)
			answer=raw_input()  
			server.send(answer)
			right_or_wrong=server.recv(2048)
			print(right_or_wrong)
			#sys.stdout.flush()
			continue

	
server.close()