# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from frow_writing import move, castling, castlingQ, invalid_move
#from to_open_ai import to_ai
import copy 


# Press the green button in the gutter to run the script.
def chess_move(data):
    arr,allcast,turn,get_move,move_count, white_moves, black_moves,captured,en_passant,ext,valid=data
    
    print(get_move)
    copy_allcst=allcast
    save_cap_num=captured[0]
    move_count = move_count + 1
    mc, r = divmod(move_count, 2)
    if turn == 'Z':
        ac = 2
        #get_move = input('Black: Enter move number ' + str(mc) + ': ')
        #get_move = to_ai(str(white_moves),str(black_moves))
        #print('Black: Enter move number ' + str(mc) + ': '+get_move)
        black_moves.append(get_move)
    else:
        turn = 'W'
        #ac = 0
        #get_move = input('White: Enter move number ' + str(mc) + ': ')
        white_moves.append(get_move)

    if get_move.lower() == 'exit':
        print('Exiting the game')
    
    elif (len(get_move)==8) and ('(ep)' == get_move[-4:]) and ('a' <= get_move[0] <= 'h'):
        ep_row = 4
        new_ep_row=5
        if en_passant and (turn=='W') and(black_moves[-1]==get_move[2]+'5') :
            ep_array=copy.deepcopy(arr)
            ep_row = 4
            new_ep_row=5
        elif en_passant and (turn=='Z') and(white_moves[-1]==get_move[2]+'4') :
            ep_row = 3
            new_ep_row=2

        ep_array=copy.deepcopy(arr)
        ep_col = ord(get_move[2]) - 97
        ep_flag=ep_array[ep_row][ep_col]
        ep_array[ep_row][ep_col]=0
        ep_array[new_ep_row][ep_col]=ep_flag
    
        if ret := move(get_move[:-4], ep_array, turn, allcast, captured):   
            if len(ret)==3:
                arr, captured, allcast = ret
                en_passant=0
            else:
                arr, captured, allcast, en_passant = ret
        else:
            if save_cap_num!=captured[0]:
                captured[0]=save_cap_num
                allcast=copy_allcst
                captured.pop()
            move_count, turn, white_moves, black_moves = invalid_move(move_count, turn, white_moves, black_moves)
            valid=False
            ext = 'The move or En Passant not valid.'
    elif get_move == '0-0':
        if ret := castling(arr, turn, allcast[ac]):
            arr = ret
            allcast[ac] = 1
            allcast[ac+1] = 1
        else:
            move_count, turn, white_moves, black_moves = invalid_move(move_count, turn, white_moves, black_moves)
            valid=False
            ext = 'King Side Castling not valid.'
    elif get_move == '0-0-0':
        if ret := castlingQ(arr, turn, allcast[ac+1]):
            arr = ret
            allcast = 1
            allcast[ac + 1] = 1
        else:
            move_count, turn, white_moves, black_moves = invalid_move(move_count, turn, white_moves, black_moves)
            valid=False
            ext = 'Queen Side Catsling not valid.'
    elif len(get_move)>1:
        if ret := move(get_move, arr, turn, allcast, captured):
            if len(ret)==3:
                arr, captured, allcast = ret
                en_passant=0
            else:
                arr, captured, allcast, en_passant = ret
        else:
            if save_cap_num!=captured[0]:
                captured[0]=save_cap_num
                allcast=copy_allcst
                captured.pop()
            move_count, turn, white_moves, black_moves = invalid_move(move_count, turn, white_moves, black_moves)
            valid=False
            ext = 'The move is not valid.'
    else:
            move_count, turn, white_moves, black_moves = invalid_move(move_count, turn, white_moves, black_moves)
            valid=False
            ext = 'The Input is not a valid move.'
    for row in range(7, -1, -1):
        for col in range(0, 8):
            if len(str(arr[row][col]))==1:
                print(arr[row][col],end='    ')
            elif len(str(arr[row][col]))==2:
                print(arr[row][col],end='   ')
            else: 
                print(arr[row][col],end='  ')
        print('')
    print(captured)
    print(allcast)
    print('White move:',white_moves)
    print('Black move:',black_moves)
    print(en_passant)
    if ext.lower()=='exit':
        get_move='exit'
    if valid:
        if turn=='Z':
            turn='W'
        else:
            turn='Z'
    print(arr,allcast,turn,get_move,move_count, white_moves, black_moves,captured,en_passant,ext,valid)
    return(arr,allcast,turn,get_move,move_count, white_moves, black_moves,captured,en_passant,ext,valid)




    #print(in_check(0, 4, arr, turn))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
