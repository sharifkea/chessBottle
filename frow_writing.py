import copy

def invalid_move(mc , trn, wm, bm):
    #print('Invalid move')
    #xt = input('Enter:')
    if trn=='W':
        wm.pop()
        #nt='Z'
    else:
        bm.pop()
        #nt = 'W'
    return mc-1, trn, wm, bm#,xt
def swipe(r, c, r1,c1,array):
    array[r][c] = array[r1][c1]
    array[r1][c1] = 0
    return array

def row_col(get_move):
    row = int(get_move[1]) - 1
    col = ord(get_move[0]) - 97
    return (row,col)
def cst_pos(trn):
    if trn == 'Z':
        return 2
    else:
        return 0

def find_value_location(matrix, target):
    for row_index, row in enumerate(matrix):
        for col_index, value in enumerate(row):
            if value == target:
                return row_index, col_index
    return None  # Value not found

def pawn_move(get_move, arr, turn, plus, capt, cst, is_capt, move_from):
    row, col = row_col(get_move)
    new_col=col
    ep=0

    if len(plus)==2:
        ext=1
        plus=plus[:-1]
    else:
        ext=0
    if turn == 'W':
        tap = 'WP'
        mul = -1
        row_com=3
        chk = 'ZK'
        max_row=7
        max=7
        min=2
    else:
        tap = 'ZP'
        mul = 1
        row_com = 4
        chk='WK'
        max_row=0
        max=5
        min=0
    kill=False
    
    #new_col = copy.deepcopy(arr)
    if min > row or row > max :
        return bool(False)
    if is_capt:
        from_col = ord(move_from) - 97
        if ((from_col==col-1)or(from_col==col+1))and str(arr[row][col])!='0' and str(arr[row][col])[:2]!=chk and str(arr[row][col])[1]!=turn and str(arr[row + (1*mul)][from_col])[:2] == tap:
           new_col= from_col
           kill=True
        else:
            return bool(False)
    elif arr[row][col] != 0:
        return bool(False)


    if str(arr[row + (1*mul)][new_col])[:2] == tap:
        newarr = copy.deepcopy(arr)
        if kill:
            capt.append(newarr[row][ col])
            newarr[row][ col]=0
            capt[0]+=1
        newarr = swipe(row, col, row + (1*mul), new_col, newarr)
        k_row, k_col = find_value_location(newarr, turn + 'K')
        if in_check(k_row, k_col, newarr, turn):
            return bool(False)

    elif row == row_com and arr[row + (1*mul)][col] == 0 and str(arr[row + (2*mul)][col])[:2] == tap:
        newarr = copy.deepcopy(arr)
        newarr = swipe(row, col, row + (2*mul), col, newarr)
        k_row, k_col = find_value_location(newarr, turn+'K')
        if in_check(k_row, k_col, newarr, turn):
            return bool(False)
        else:
            ep=1
    else:
        return bool(False)
    if newarr:
        ac = cst_pos(chk[0])
        k_row, k_col = find_value_location(newarr, chk)

        if plus == '0':
            if in_check(k_row, k_col, newarr, chk[0]):
                return bool(False)  
            else:
                return (newarr, capt, cst,ep)
        elif plus == ('+' or '#'):
            if in_check(k_row, k_col, newarr, chk[0]):
                cst[ac] = 1
                cst[ac + 1] = 1
                return (newarr, capt, cst,ep)
            else:
                return bool(False)
        else:
            if row != max_row or capt[0] == 0:
                return bool(False)
            else:
                for x in range(1, capt[0]+1):
                    if turn+plus in capt[x]:
                        flag = newarr[row][col]
                        newarr[row][col] = capt[x]
                        if_ch = in_check(k_row, k_col, newarr, chk[0])
                        if  (if_ch and not ext) or (not if_ch and ext):
                            return bool(False)
                        else:
                            capt.pop(x)
                            capt.append(flag)
                            return (newarr, capt, cst)
                return bool(False)
    else:
        return bool(False)

def rest_move(move_to, move_of, arr, turn, plus, cap, cst, is_capt, move_from ):
    print('in rest_move')
    row, col = row_col(move_to)
    tap = turn + move_of
    if turn == 'W':
        opn = 'Z'
        ac = 0
    else:
        opn = 'W'
        ac = 2
    from_col = -1
    from_row = -1
    if is_capt:
        if('a' <= move_from <= 'h'):
            from_col = ord(move_from) - 97
            for x in range(0,8):
                if str(arr[x][from_col])[:2]==tap:
                    from_row=x
            if from_row<0:
                return bool(False)
        elif('1' <= move_from <= '8'):
            
            from_row =int(move_from)-1
            for x in range(0,8):
                if str(arr[from_row][x])[:2]==tap:
                    from_col=x
            if from_col<0:
                return bool(False)
        elif move_from=='0':
            pass
        else:
            return bool(False)
        if str(arr[row][col])[:1]==opn:
            newarr=copy.deepcopy(arr)
            cap.append(newarr[row][ col])
            newarr[row][ col]=0
            cap[0]+=1
        else:
            return bool(False)
    elif arr[row][col]:
        return bool(False)
    else:
        newarr=copy.deepcopy(arr)
    if move_of == 'K':
        if ret := move_K(row, col, tap, newarr):
            cst[ac] = 1
            cst[ac+1] = 1
    elif move_of == 'Q':
        ret = move_Q(row, col, tap, newarr)
    
    elif move_of == 'R':
        if ret := move_R(row, col, tap, newarr, from_row, from_col):
            ret, r_num = ret
            cst[ac + r_num] = 1
    elif move_of == 'N':
        ret = move_N(row, col, tap, newarr, from_row, from_col)
    elif move_of == 'B':
        ret = move_B(row, col, tap, newarr)
    else:
        return bool(False)
    if ret:
        ac = cst_pos(opn)
        k_row, k_col = find_value_location(ret, opn+'K')
        if plus == '0':
            if in_check(k_row, k_col, ret, opn):
                return bool(False)  
            else:
                return (ret, cap, cst)
        elif plus == ('+' or '#'):
            if in_check(k_row, k_col, ret, opn):
                cst[ac] = 1
                cst[ac + 1] = 1
                return (ret, cap, cst)
            else:
                return bool(False)
        else:
            return bool(False)

def move_K(row, col, tap, newarr):
    if str(newarr[row][col]) == '0' and (row_col := in_check_king(row, col, newarr, tap)) and not (in_check(row, col, newarr, tap[0])):
        oldrow,oldcol = row_col
        newarr = swipe(row, col, oldrow, oldcol, newarr)

        return newarr
    else:
        return bool(False)
def move_N(row, col, tap, newarr, from_row, from_col):
    if str(newarr[row][col]) == '0' and (ret_row_col := in_check_knight(row, col, newarr, tap, from_row, from_col)):
        oldrow, oldcol = ret_row_col
        newarr = swipe(row, col, oldrow, oldcol, newarr)
        k_row, k_col = find_value_location(newarr, tap[0] + 'K')
        if in_check(k_row, k_col, newarr, tap[0]):
            return bool(False)
        else:
            return newarr
    else:
        return bool(False)


def move_R(row, col, tap, newarr, from_row, from_col):
    rn = 0
    if str(newarr[row][col]) == '0' and (ret_row_col := in_check_rq(row, col, newarr, tap, from_row, from_col)):
        oldrow, oldcol = ret_row_col
        newarr = swipe(row, col, oldrow, oldcol, newarr)
        k_row, k_col = find_value_location(newarr, tap[0] + 'K')
        if in_check(k_row, k_col, newarr, tap[0]):
            return bool(False)
        else:
            if newarr[row][col][2] == '1':
                bn = 1
            return newarr, rn
    else:
        return bool(False)

def move_B(row, col, tap, newarr):

    if str(newarr[row][col]) == '0' and (ret_row_col := in_check_bq(row, col, newarr, tap)):
        oldrow, oldcol = ret_row_col
        newarr = swipe(row, col, oldrow, oldcol, newarr)
        k_row, k_col = find_value_location(newarr, tap[0] + 'K')
        if in_check(k_row, k_col, newarr, tap[0]):
            return bool(False)
        else:
            return newarr
    else:
        return bool(False)


def move_Q(row, col, tap, newarr):
    if str(newarr[row][col]) == '0':
        if ret_row_col:=in_check_rq(row, col, newarr, tap, -1, -1):
            oldrow, oldcol = ret_row_col
        else:
            return bool(False)
        newarr = swipe(row, col, oldrow, oldcol, newarr)
        k_row, k_col = find_value_location(newarr, tap[0] + 'K')
        if in_check(k_row, k_col, newarr, tap[0]):
            return bool(False)
        else:
            return newarr
    else:
        return bool(False)

def castling(arr, turn, cast):
    ret = []
    row = 0
    if turn == 'Z':
        row = 7
    if cast == 0 and arr[row][5] == 0 and arr[row][6] == 0 and not in_check(row, 5, arr, turn) and not in_check(row, 6, arr, turn):
        arr=swipe(row,5,row,7,arr)
        arr = swipe(row, 6, row, 4, arr)
        return arr
    else:
        return bool(False)

def castlingQ(arr, turn, castQ):
    ret = []
    row = 0
    if turn == 'Z':
        row = 7
    if castQ == 0 and arr[row][3] == 0 and arr[row][2] == 0 and arr[row][1] == 0 and not in_check(row, 3, arr, turn) and not in_check(row, 2, arr, turn):
        arr = swipe(row, 3, row, 0, arr)
        arr = swipe(row, 2, row, 4, arr)
        return arr
    else:
        return bool(False)

def in_check_pon(row, col, arr, pon):

    if (0 <= row <= 7) and (0 <= col-1 <= 7) and str(arr[row][col - 1])[:2] == pon:
        return bool(True)
    if (0 <= row <= 7) and (0 <= col+1 <= 7) and str(arr[row][col + 1])[:2] == pon:
        return bool(True)
    return bool(False)

def in_check_knight(y, z, arr, kni, from_row, from_col):
    print(from_row, from_col)
    for x in range(-2, 3):  # N
        if x > 0:
            w = 3 - x
        else:
            w = 3 + x
        if (0 <= (y + x) <= 7) and (0 <= (z + w) <= 7) and x != 0:
            print([y + x],[z + w])
            if str(arr[y + x][z + w])[:2] == kni :
                if(from_col and from_row) != -1:
                    if y+x == from_row and z + w == from_col:
                        return y+x , z + w
                    else:
                        pass
                else:
                    return y + x, z + w
        if (0 <= (y - x) <= 7) and (0 <= (z - w) <= 7) and x != 0:
            print([y - x],[z - w])
            if str(arr[y - x][z - w])[:2] == kni :
                if(from_col and from_row) != -1:
                    if y - x == from_row and z - w == from_col:
                        return y - x , z - w
                    else:
                        pass
                else:
                    return y - x, z - w
    print('out')
    return bool(False)

def in_check_rq(y, z, arr, rq, from_row, from_col):
    for x in range(1, 8):
        if (y + x) <= 7: 
            if str(arr[y + x][z])[:2] == rq:
                if(from_col and from_row) != -1:
                    if y+x ==from_row and z ==from_col:
                        return y +x, z
                    else:
                        pass
                else:
                    return y + x, z
            elif str(arr[y + x][z])[:2] !='0':
                break
        else:
            break

    for x in range(1, 8):
        if (y - x) <= 7: 
            if str(arr[y - x][z])[:2] == rq:
                if(from_col and from_row) !=-1:
                    if y - x==from_row and z ==from_col:
                        return y - x, z 
                    else:
                        pass
                else:
                    return y - x, z
            elif str(arr[y - x][z])[:2] !='0':
                break
        else:
            break

    for x in range(1, 8):
        if (z + x) <= 7:
            if str(arr[y][z+x])[:2] == rq:
                if(from_col and from_row) != -1:
                    if y ==from_row and z + x==from_col:
                        return y , z + x
                    else:
                        pass
                else:
                    return y, z + x
            elif str(arr[y][z + x])[:2] !='0':
                break
        else:
            break
    for x in range(1, 8):
        if (z - x) >= 0:
            if str(arr[y][z-x])[:2] == rq:
                if(from_col and from_row) != -1:
                    if y ==from_row and z - x==from_col:
                        return y , z - x
                    else:
                        pass
                else:
                    return y, z - x
            elif str(arr[y][z - x])[:2] !='0':
                break
        else:
            break
    if rq[1]=='Q':
        return in_check_bq(y, z, arr, rq)
    return bool(False)

def in_check_bq(y,z,arr,bq):
    for x in range(1, 8):  # B Q
        if (z - x) >= 0 and (y + x) <= 7:
            if str(arr[y + x][z - x])[:2] == bq:
                return y + x, z - x
            elif str(arr[y + x][z - x])[:2] !='0':
                break
        else:
            break
    for x in range(1, 8):
        if (z + x) <= 7 and (y + x) <= 7:
            if str(arr[y + x][z + x])[:2] == bq:
                return y + x, z + x
            elif str(arr[y + x][z + x])[:2] != '0':
                break
        else:
            break
    for x in range(1, 8):
        if (z - x) >= 0 and (y - x) >= 0:
            if str(arr[y - x][z - x])[:2] == bq:
                return y - x, z - x
            elif str(arr[y - x][z - x])[:2] != '0':
                break
        else:
            break
    for x in range(1, 8):
        if (z + x) <= 7 and (y - x) >= 0:
            if str(arr[y - x][z + x])[:2] == bq:
                return y - x, z + x
            elif str(arr[y - x][z + x])[:2] != '0':
                break
        else:
            break
    return bool(False)

def in_check_king(y, z, arr, kng):
    for x in range(-1, 2):
        for w in range(-1, 2):
            if 0 <= (y + x) <= 7 and 0 <= (z + w) <= 7 and (x != 0 or w != 0) and str(arr[y + x][z + w])[:2] == kng:
                return y + x, z + w
    return bool(False)

def in_check(row, col, arr, turn):
    if turn == 'W':
        opn = 'Z'
        rowp = row+1
    else:
        opn = 'W'
        rowp = row-1
    if in_check_pon(rowp, col, arr, opn+'P'):
        return bool(True)
    if in_check_king(row, col, arr, opn+'K'):
        return bool(True)
    if in_check_knight(row, col, arr, opn+'N', -1, -1):
        return bool(True)
    if in_check_rq(row, col, arr, opn+'R', -1, -1):
        return bool(True)
    if in_check_bq(row, col, arr, opn+'B'):
        return bool(True)
    if in_check_rq(row, col, arr, opn+'Q', -1, -1):
        return bool(True)

    return bool(False)

def move(get_move,arr,turn, cast, captured):
    ret =[]
    plus ='0'
    is_capt=0
    move_from='0'
    if get_move[-1]=='+':
        plus='+'
        get_move= get_move[:-1]
    elif get_move[-1]=='#':
        plus='#'
        get_move= get_move[:-1]
    if 'x' in get_move:
        move_a,move_b = get_move.split("x")
        is_capt=1
        print('in x')
        if len(move_a)==1 and (move_a[0] in [ 'K' , 'B' , 'R' , 'Q' , 'N']):
            get_move=move_a+move_b
        elif len(move_a)==1 and ('a' <= move_a <= 'h'):
            print(move_a)
            move_from=move_a
            get_move=move_b
        elif len(move_a)==2 and (('a' <= move_a[1] <= 'h') or ('1' <= move_a[1] <= '8')) and move_a[0] in [  'R'  , 'N']:
            get_move=move_a[0]+move_b
            move_from=move_a[1]
        else:
            print('out from x')
            return bool(False)

    
    
    if len(get_move) == 3 and (get_move[2] in [ 'B' , 'R' , 'Q' , 'N']):
        print(get_move,is_capt,move_from)
        if plus!='0':
            plus = get_move[2]+plus
        else:
            plus = get_move[2]
        get_move= get_move[:-1]

    if len(get_move) == 2:
        if 'a' <= get_move[0] <= 'h' and '1' <= get_move[1] <= '8':
            ret= pawn_move(get_move, arr, turn, plus, captured, cast,is_capt,move_from)
        else:
            return bool(False)
        
    elif len(get_move) == 3:           
        if (get_move[0] in [ 'K' , 'B' , 'R' , 'Q' , 'N']) and ('a' <= get_move[1] <= 'h') and ('1' <= get_move[2] <= '8'):
            print(plus, is_capt,move_from)
            ret= rest_move(get_move[-2:], get_move[0], arr, turn, plus, captured, cast, is_capt,move_from)
#move_from=getmove[0] when Qxf4, if not Nexc4

        else:
            return bool(False)
    
    else:
        return bool(False)
    if ret:
        return ret
    else:
        return bool(False)