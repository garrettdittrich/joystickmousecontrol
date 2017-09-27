import SimpleHTTPServer
import SocketServer

PORT = 8001

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("192.168.1.6", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
