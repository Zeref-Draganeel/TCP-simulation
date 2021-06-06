class State:
    state = None #abstract class
    CurrentContext = None
    def __init__(self, Context):
        self.CurrentContext = Context

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

from socket import socket
from time import sleep

class Transition:
    def passive_open(self):
        print ("Error!")
        return False
    def syn(self):
        print ("Error!")
        return False
    def ack(self):
        print ("Error!")
        return False
    def rst(self):
        print ("Error!")
        return False
    def syn_ack(self):
        print ("Error!")
        return False
    def close(self):
        print ("Error!")
        return False
    def fin(self):
        print ("Error!")
        return False
    def timeout(self):
        print ("Error!")
        return False
    def active_open(self):
        print ("Error!")
        return False

class TCPClient(StateContext, Transition):
    def __init__(self):
        self.sleep_time = 2 
        self.host = "localhost"
        self.port = 1234
        self.socket = None
        self.availableStates["Closed"] = Closed(self)
        self.availableStates["syn_sent"] = syn_sent(self)
        self.availableStates["established"] = established(self)
        self.availableStates["fin_wait_1"] = fin_wait_1(self)
        self.availableStates["fin_wait_2"] = fin_wait_2(self)
        self.availableStates["timed_wait"] = timed_wait(self)
        self.availableStates["reset"] = reset(self)

    def closed(self):
        return self.CurrentState.closed()
    def syn_sent(self):
        return self.CurrentState.syn_received()
    def established(self):
        return self.CurrentState.established()
    def fin_wait_1(self):
        return self.CurrentState.close_wait()
    def fin_wait_2(self):
        return self.CurrentState.last_ack()
    def reset(self):
        return self.CurrentState.reset()
 
 # this method initiates a listen socket
    def connect(self):
        self.socket = socket()
        try:
            self.socket.connect((self.host,self.port))
            return True
        except Exception as err:
            print (err)
            exit()

class SocketFunctions:
    def __init__(self):
        self.socket = ActiveTCPCon.socket
        
    def send_syn(self):
        print ('sending syn')
        self.socket.send(b'syn')

    def send_ack(self):
        print ('sending ack')
        self.socket.send(b'ack')

    def recv_syn_ack(self):
        print ('waiting for syn/ack from server...')
        msg = self.socket.recv(1024).decode()
        print ('recieved %s from server'%(msg))

    def recv_ack(self):
        print ('waiting for ack from server...')
        msg = self.socket.recv(1024).decode()
        print ('recieved %s from server'%(msg))
        
    def recv_fin(self):
        print ('waiting for fin from server...')
        msg = self.socket.recv(1024).decode()
        print ('recieved %s from server'%(msg))
        
    def send_fin(self):
        print ('sending fin')
        self.socket.send(b'fin')

class Closed(State, StateContext, Transition):
    def __init__(self, Context):
        State.__init__(self,Context)
    def next(self):
        print( "Transitioning to syn_sent")
        self.CurrentContext.setState("syn_sent")
        return True
    def trigger(self):
        sf.send_syn()

class syn_sent(State, Transition):
    def __init__ (self, Context):
         State.__init__(self,Context)
    def next(self):
        print( "Transitioning to established")
        self.CurrentContext.setState("established")
        return True
    def trigger(self):
        sf.recv_syn_ack()
        sf.send_ack()

class established(State, Transition):
    def __init__ (self, Context):
         State.__init__(self,Context)
    def next(self):
        print ("Transitioning to fin_wait_1")
        self.CurrentContext.setState("fin_wait_1")
        return True
    def trigger(self):
        sf.send_fin()
        print ('Connection established')

class fin_wait_1(State, Transition):
    def __init__ (self, Context):
         State.__init__(self,Context)
    def next(self):
        print ("Transitioning to fin_wait_2")
        self.CurrentContext.setState("fin_wait_2")
        return True
    def trigger(self):
        sf.recv_ack()

class fin_wait_2(State, Transition):
    def __init__ (self, Context):
         State.__init__(self,Context)
    def next(self):
        print ("Transitioning to timed_wait")
        self.CurrentContext.setState("timed_wait")
        return True
    def trigger(self):
        sf.recv_fin()
        sf.send_ack()

class timed_wait(State, Transition):
    def __init__ (self, Context):
         State.__init__(self,Context)
    def next(self):
        print ("Transitioning to closed")
        self.CurrentContext.setState("reset")
        return True
    def trigger(self):
        pass

class reset(State, Transition):
    def __init__(self,Context):
        State.__init__(self,Context)
    def trigger(self):
        ActiveTCPCon.socket.close()
    def next(self):
        pass

# Entry point
if __name__ == '__main__':
    ActiveTCPCon = TCPClient()
    ActiveTCPCon.connect()
    sf = SocketFunctions()
    print ("Transitioning to closed")
    a = StateContext()
    a.setState("Closed")
