#Abstract state class
class State:
    state = None 
    CurrentContext = None
    def __init__(self, Context):
        self.CurrentContext = Context

# Initial State 
class StateContext:
    stateIndex = 0;
    CurrentState = None
    availableStates = {}

    def setState(self, newstate):
        self.CurrentState = self.availableStates[newstate]
        self.stateIndex = newstate
        self.CurrentState.trigger()
        self.CurrentState.next()

    def getStateIndex(self):
        return self.stateIndex

# 'states: IDLE, Established, connect, opensent, openconfirmed, active, listen'

from socket import socket
from time import sleep


# Default State behaviour
class Transition:
    def closed(self):
        print ("Error! Cannot Transition to closed!")
        return False
    def listen(self):
        print ("Error! Cannot Transition to listen!")
        return False
    def syn_received(self):
        print ("Error! Cannot Transition to syn received!")
        return False
    def established(self):
        print ("Error! Cannot Transition to Established!")
        return False
    def close_wait(self):
        print ("Error! Cannot Transition to close wait!")
        return False
    def last_ack(self):
        print ("Error! Cannot Transition to last ack!")
        return False
    def reset(self):
        print ("Error! Cannot Reset!")
        return False

class SocketFunctions:
    def __init__(self):
        self.socket = ActiveTCPCon.connection
    def recv_syn(self):
        print ('waiting for syn from client...')
        msg = self.socket.recv(1024).decode()
        print ('received %s from client'%(msg))
    def send_syn_ack(self):
        print ('sending syn/ack')
        self.socket.send(b'syn/ack')
    def recv_ack(self):
        print ('waiting for ack from client...')
        msg = self.socket.recv(1024).decode()
        print ('received %s from client'%(msg))
    def send_ack(self):
        print ('sending ack')
        self.socket.send(b'ack')
    def send_fin(self):
        print ('sending fin')
        self.socket.send(b'fin')
    def recv_fin(self):
        print ('waiting for fin from client...')
        msg = self.socket.recv(1024).decode()
        print ('received %s from client'%(msg))

class Closed(State, StateContext, Transition):
    def __init__(self, Context):
        State.__init__(self,Context)
    def next(self):
        print ("Transitioning to listen")
        ActiveTCPCon.listen()
        return True
    def trigger(self):
        pass

class Listen(State, Transition):
    def __init__ (self, Context):
         State.__init__(self,Context)

# in Listen mode state can be closed or move to next state
    def trigger(self):
        sf.recv_syn()
        sf.send_syn_ack()
        return True

    def next(self):
        print ('transitioning to Syn Received')
        self.CurrentContext.setState('SynReceived')

class Syn_Received(State, Transition):
    def __init__ (self, Context):
         State.__init__(self,Context)
    def next(self):
        print ('conection established')
        print ("Transitioning to connection Established")
        self.CurrentContext.setState("Established")
        return True
    def trigger(self):
        sf.recv_ack()
               
class Established(State, Transition):
    def __init__ (self, Context):
         State.__init__(self,Context)
    def next(self):
        print ("Transitioning to Close wait")
        self.CurrentContext.setState("CloseWait")
        return True
    def trigger(self):
        sf.recv_fin()
        sf.send_ack()

class Close_Wait(State, Transition):
    def __init__ (self, Context):
         State.__init__(self,Context)
    def next(self):
        print ("Transitioning to last ack")
        self.CurrentContext.setState("LastAck")
        return True
    def trigger(self):
        sf.send_fin()

class Last_Ack(State, Transition):
    def __init__ (self, Context):
         State.__init__(self,Context)
    def next(self):
        print ("Transitioning to closed")
        self.CurrentContext.setState("reset")
        return True
    def trigger(self):
        sf.recv_ack()

class Reset(State, Transition):
    def __init__ (self, Context):
         State.__init__(self,Context)
    def trigger(self):
        ActiveTCPCon.connection.close()
    def next(self):
        pass

# Main TCP class implemenint all the server states
class TCPServer(StateContext, Transition):
    def __init__(self):
        self.sleep_time = 2 
        self.host = "localhost"
        self.port = 1234
        self.connection_address = 0
        self.socket = None
        self.availableStates["Listen"] = Listen(self)
        self.availableStates["Closed"] = Closed(self)
        self.availableStates["SynReceived"] = Syn_Received(self)
        self.availableStates["Established"] = Established(self)
        self.availableStates["CloseWait"] = Close_Wait(self)
        self.availableStates["LastAck"] = Last_Ack(self)
        self.availableStates["reset"] = Reset(self)
        print ("Transitioning to Listen!")

    def closed(self):
        return self.CurrentState.closed()
    def syn_recived(self):
        return self.CurrentState.syn_received()
    def established(self):
        return self.CurrentState.established()
    def close_wait(self):
        return self.CurrentState.close_wait()
    def last_Ack(self):
        return self.CurrentState.last_ack()
    def reset(self):
        return self.CurrentState.reset()
 
 # this method initiates a listen socket
    def listen(self):
        self.socket = socket()
        self.socket.bind((self.host,self.port))
        self.socket.listen(1)
        self.connection, self.connection_address = self.socket.accept() #connection acceptance
        return True

# Entry point
if __name__ == '__main__':
    ActiveTCPCon = TCPServer()
    ActiveTCPCon.listen()
    sf = SocketFunctions()
    a = StateContext()
    a.setState("Listen")
