from bottle import run, get,view, post, request, Bottle, static_file
from frow_writing import move, castling, castlingQ, invalid_move
from chess_main import chess_move
import copy
import json

#app = Bottle()

@get('/')
def index():
    return static_file('index.html', root='./views')

@get('/static/js/<filename:path>')
def serve_static_js(filename):
    return static_file(filename, root='./static/js')

@get('/static/css/<filename:path>')
def serve_static_css(filename):
    return static_file(filename, root='./static/css')

@get('/static/img/<filename:path>')
def serve_static_css(filename):
    return static_file(filename, root='./static/img')

# Add more routes for other types of static files if needed


##############################


@get("/")
@view("index.html")
def do():
    company_name ="SUPER"
    return dict(company_name ="SUPER", user='Omar')
################################
@post('/first')
def do():
    req=request.json
    first = req.get("first")
    data = request.json.get("data")
    print(first, type(data))
    
    """arr,allcast,turn,get_move,move_count, white_moves, black_moves,captured,en_passant,ext=json.loads(data)
    token = req.get("data")
    print(token)
    """
    if first:
        rows, cols = (8, 8)
        arr = [[0 for _ in range(rows)] for _ in range(cols)]

        arr[0] = ['WR1', 'WN1', 'WB1', 'WQ', 'WK', 'WB2', 'WN2', 'WR2']
        arr[1] = ['WP1', 'WP2', 'WP3', 'WP4', 'WP5', 'WP6', 'WP7', 'WP8']
        arr[6] = ['ZP1', 'ZP2', 'ZP3', 'ZP4', 'ZP5', 'ZP6', 'ZP7', 'ZP8']
        arr[7] = ['ZR1', 'ZN1', 'ZB1', 'ZQ', 'ZK', 'ZB2', 'ZN2', 'ZR2']
        
        allcast = [0, 0, 0, 0] #cast will be 1 if the king or R2 moves[WR2,WR1,ZR2,ZR1]
        turn = 'W'
        get_move = ''
        move_count = 1
        black_moves = []
        white_moves = []
        captured = []
        en_passant=0
        ext=''
        valid=True
        captured.append(0)
    else:
        newdata=json.loads(data)
        if newdata:=chess_move(newdata):
            arr,allcast,turn,get_move,move_count, white_moves, black_moves,captured,en_passant,ext,valid=newdata

        
    ret=[]
    ret.append(arr)
    ret.append(allcast)
    ret.append(turn)
    ret.append(get_move)
    ret.append(move_count)
    ret.append(white_moves)
    ret.append(black_moves)
    ret.append(captured)
    ret.append(en_passant)
    ret.append(ext)
    ret.append(valid)

    print(ret)
    
    #response.status = 200
    #response.content_type = 'application/json; charset=UTF-8'
    
    return json.dumps(ret)

##############################





################################
run (host="127.0.0.1", port=5000, debug=True, reloader=True, server="paste")