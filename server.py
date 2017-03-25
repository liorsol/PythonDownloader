
import socket
import sys
import json

###
# server receiving json messages on port 6736
###
class Server():

    PORT = 6736

    def __init__(self, port=6736):
        self.PORT = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.create_socket()

    def create_socket(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the port
        server_address = ('localhost', self.PORT)
        print >> sys.stdout, 'starting up on %s port %s' % server_address
        self.sock.bind(server_address)

    def start_listen(self):
        # Listen for incoming connections
        self.sock.listen(1)

        while True:
            # Wait for a connection
            print >> sys.stderr, 'waiting for a connection'
            connection, client_address = self.sock.accept()
            data = ""
            try:
                print >> sys.stdout, 'connection from', client_address
                retmsg = ""
                while True:
                    datatmp = connection.recv(100)
                    if not datatmp:
                        break
                    data += datatmp
                retmsg = self.handle_command(json.loads(data))

                # self.sock.sendall(retmsg)


            finally:
                # Clean up the connection
                print >> sys.stderr, "closing connection"
                connection.close()

    def handle_command(self, msg):
        print >> sys.stdout, 'received "%s"' % json.dumps(msg)
        return "Unknown command"