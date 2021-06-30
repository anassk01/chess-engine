 #!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import ast
import chess
import chess.engine
import requests

def runner3(PGNMoves):
        
    path="C:/xampp/htdocs"
    engine = chess.engine.SimpleEngine.popen_uci(path+'/'+'stockfish-10-64')
##    engine = chess.engine.SimpleEngine.popen_uci(path+'/'+'stockfish2.4')
    PGNMoves=PGNMoves.replace('D', 'Q')
    PGNMoves=PGNMoves.replace('C', 'N')
    PGNMoves=PGNMoves.replace('F', 'B')
    PGNMoves=PGNMoves.replace('T', 'R')
    print (PGNMoves)

    if PGNMoves[-1] == " ":
        PGNMoves=PGNMoves[0:-1]

    PGNMoves=PGNMoves.split(' ')

    board=chess.Board()
    for t in PGNMoves:
        board.push_san(t)

    loop="<h1>"
    for i in range(3):
        
        
        result = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
        finish=result.move
        if (i==0 or i==2):
            loop+="---"+str(finish)
    
    loop+="</h1>"

    return loop

    

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s", str(self.path))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
##        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
##                str(self.path), str(self.headers), post_data.decode('utf-8'))
        logging.info("%s",post_data.decode('utf-8'))
        

        self._set_response()
        self.wfile.write(" {}".format(self.path).encode('utf-8'))
        op=post_data.decode('utf-8')
        print (op)
        retsult=(runner3(op))
        retsult="{}<br>".format(str(retsult))
        f = open("d.html", "w")
        metadata="""  <meta http-equiv="refresh" content="1" /> \n"""
        f.write(metadata)
        f.write(retsult)
        f.close()
        print(retsult)

        retsult=str(retsult).encode('utf-8')
        self.wfile.write(retsult)
        

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':

    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
