import socket 
import select 
import sys 
from thread import *
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

'''if len(sys.argv) != 3: 
	print "Correct usage: script, IP address, port number"
	exit()''' 

IP_address = '' 

Port = 8888 

server.bind((IP_address, Port)) 

server.listen(100) 

list_of_clients = [] 

questions=["q"+str(i+1) for i in range(20)]  # all the questions are q1,q2,q3,.... q20.
answers=["a"+str(i+1) for i in range(20)]	# all the answers are a1,a2,a3,....a20
shuffle_intermediate=zip(questions,answers) 
random.shuffle(shuffle_intermediate) # shuffles all the questions and corresponding answers.
questions,answers=zip(*shuffle_intermediate)


points=[0 for i in range(20)]


any_winner=False
winner=False

def start_game():
	print("\n\nGame started")
	for i in range(len(questions)):
		print("\n\n\n")
		ask_question(i)
		print("Question "+str(i+1)+" asked")
		con=check_first_buzzer()
		
		stop_clients_from_taking_input(con)
		

		ans=get_answer(con)
		
		check=check_answer(con,ans,i)
		
		if(check==True):
			print("correct answer")
			add_points(con)
			check_winner()
		else:
			print("wrong answer")
		

		if(any_winner):
			break


def ask_question(index_no):
	for con in list_of_clients:
		con.send("Question "+str(index_no+1)+": "+questions[index_no]+"\nPress Buzzer to answer")


def check_first_buzzer(): #will return the index of connection that pressed the buzzer first
	socket_list=[con for con in list_of_clients]
	read_sockets,write_socket, error_socket = select.select(socket_list,[],[])
	#print(read_sockets)
	#print(str(read_sockets[0]))
	Player_no=-1
	for i in range(len(list_of_clients)):
		if(list_of_clients[i]==read_sockets[0]):
			Player_no=i+1
			break


	if(len(read_sockets)>0):
		buzzer_message=read_sockets[0].recv(2048)
		
		print("Buzzer pressed by: Player "+ str(Player_no))
		return read_sockets[0]
	else:
		return "NONE"
	#Else return something

def stop_clients_from_taking_input(con): # will stop client from taking input when any of the player pressed buzzer
	for co in list_of_clients:
		if(co!=con):
			co.send("Stop taking input")

def get_answer(con): # will get the answer from the client that pressed buzzer first
	con.send("Give answer:")
	ans=con.recv(2048)
	print("sent answer:"+str(ans))
	return ans


def check_answer(con,ans,index):#return whether the answer is true or false
	if(ans==answers[index]):
		con.send("Correct Answer")
		return True
	else:
		con.send("Wrong Answer")
		return False

	
def add_points(con): # adds points depending on whether the answer was right or wrong
	for i in range(len(list_of_clients)):
		if(list_of_clients[i]==con):
			points[i]=points[i]+1			
		print("Player "+str(i+1)+": "+str(points[i]))


def check_winner():# checks the winner depending on whether any of clients has total of 5 pts
	for i in range(len(points)):
		if(points[i]==5):
			any_winner=True
			declare_winner(i)
			sys.exit()


def declare_winner(winner): #Outputs the player which wins
	print("\n\nWinner is:"+str(winner+1))
	for con in list_of_clients:
		con.send("quit "+str(winner+1))
				 
 
def end_game(): #called in case no player is winner or the game is tie.
	print("\n\nNO WINNERS")
	for con in list_of_clients:
		con.send('quit No winner')


"""The following function simply removes the object 
from the list that was created at the beginning of 
the program"""

def broadcast(message, connection): 
	for clients in list_of_clients: 
		if clients!=connection: 
			try: 
				clients.send(message) 
			except: 
				clients.close() 

def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection)

for i in range(3):

	"""Accepts a connection request and stores two parameters, 
	conn which is a socket object for that user, and addr 
	which contains the IP address of the client that just 
	connected"""
	conn, addr = server.accept() 

	"""Maintains a list of clients for ease of broadcasting 
	a message to all available people in the chatroom"""
	list_of_clients.append(conn) 

	# prints the address of the user that just connected 
	print("Player "+str(i+1)+" connected")

	# creates and individual thread for every user 
	# that connects 
	#start_new_thread(clientthread,(conn,addr))	 



start_game()
end_game()
conn.close() 
server.close() 
sys.exit()