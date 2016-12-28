# solve_sudoku should return None
ill_formed = [[5,3,4,6,7,8,9,1,2],
              [6,7,2,1,9,5,3,4,8],
              [1,9,8,3,4,2,5,6,7],
              [8,5,9,7,6,1,4,2,3],
              [4,2,6,8,5,3,7,9],  # <---
              [7,1,3,9,2,4,8,5,6],
              [9,6,1,5,3,7,2,8,4],
              [2,8,7,4,1,9,6,3,5],
              [3,4,5,2,8,6,1,7,9]]

# solve_sudoku should return valid unchanged
valid = [[5,3,4,6,7,8,9,1,2],
         [6,7,2,1,9,5,3,4,8],
         [1,9,8,3,4,2,5,6,7],
         [8,5,9,7,6,1,4,2,3],
         [4,2,6,8,5,3,7,9,1],
         [7,1,3,9,2,4,8,5,6],
         [9,6,1,5,3,7,2,8,4],
         [2,8,7,4,1,9,6,3,5],
         [3,4,5,2,8,6,1,7,9]]

# solve_sudoku should return False
invalid = [[5,3,4,6,7,8,9,1,2],
           [6,7,2,1,9,5,3,4,8],
           [1,9,8,3,8,2,5,6,7],
           [8,5,9,7,6,1,4,2,3],
           [4,2,6,8,5,3,7,9,1],
           [7,1,3,9,2,4,8,5,6],
           [9,6,1,5,3,7,2,8,4],
           [2,8,7,4,1,9,6,3,5],
           [3,4,5,2,8,6,1,7,9]]

# solve_sudoku should return a 
# sudoku grid which passes a 
# sudoku checker. There may be
# multiple correct grids which 
# can be made from this starting 
# grid.
easy = [[2,9,0,0,0,0,0,7,0],
        [3,0,6,0,0,8,4,0,0],
        [8,0,0,0,4,0,0,0,2],
        [0,2,0,0,3,1,0,0,7],
        [0,0,0,0,8,0,0,0,0],
        [1,0,0,9,5,0,0,6,0],
        [7,0,0,0,9,0,0,0,1],
        [0,0,1,2,0,0,3,0,6],
        [0,3,0,0,0,0,0,5,9]]

# Note: this may timeout 
# in the Udacity IDE! Try running 
# it locally if you'd like to test 
# your solution with it. 
hard = [[1,0,0,0,0,7,0,9,0],
        [0,3,0,0,2,0,0,0,8],
        [0,0,9,6,0,0,5,0,0],
        [0,0,5,3,0,0,9,0,0],
        [0,1,0,0,8,0,0,0,2],
        [6,0,0,0,0,4,0,0,0],
        [3,0,0,0,0,0,0,1,0],
        [0,4,0,0,0,0,0,0,7],
        [0,0,7,0,0,0,3,0,0]]

# I've added this puzzle to test
# the solver more rigorously
Null = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]

# This puzzle CANNOT be solved, even 
# though it appears to be a 'valid'
# puzzle (the middle cell is over-
# constrained with no possibilities).
# It is essential the solver can
# deal with this type of puzzle so
# Guessing works properly
Impossible=[[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,3,0,0,0,0],
            [0,0,0,0,9,0,0,0,0],
            [0,0,0,0,0,6,0,0,0],
            [1,0,5,0,0,0,0,2,7],
            [0,0,0,8,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,4,0,0,0,0]]


def check_sudoku(grid) :
    ### Sanity Checking ###
    if grid is None : return None
    if (len(grid) != 9) or (type(grid) is not list) : return None
    for row in grid :
        if (len(row) != 9) or (type(row) is not list) : return None
        for entry in row :
            if (type(entry) is not int) or (entry not in range(0,10)) : return None
    
    ### Valid grid checking ###
    # step 1: all rows valid
    for row in grid :
        available = list(range(0,10))
        for item in row : # row element
            if item in available : 
                if item != 0: available.remove(item) # only 1 of each number per row
                #else: pass # any number of 0's is valid
            else : return False
        
    # step 2: all columns valid
    for j in range(0,9) : # column
        available = list(range(0,10))
        for i in range(0,9) : # row
            item = grid[i][j] # column element
            if item in available:
                if item != 0: available.remove(item)
                #else: pass
            else : return False
        
    # step 3: all boxes valid 
    for m in range(0,3) : # row multiplier
        for n in range(0,3) : # column multiplier
            available = list(range(0,10)) # 'valid items'
            for i in range(1,4) : # row
                for j in range(1,4) : # column
                    item = grid[i-1+m*3][j-1+n*3]
                    if item in available:
                        if item != 0: available.remove(item)
                        else: pass
                    else : return False
    
    return True # if we made it this far, all checks have completed without failure


def solve_sudoku(grid) :

    ### object definitions
    class Node :
        # all coordinates (box, col, row) are numbered 0 through 8
        def __init__(self, row, col, val=0) :
            self.col = col
            self.row = row
            self.box = 3*int(row/3) + int(col/3) # MUST NOT ROUND UP
            self.cell = row*9+col+1 # we don't make use of this
            self.val = val
            if val != 0 :
                self.cannot = list(range(0,10))
                self.possible = []
            else :
                self.possible = list(range(1,10))
                self.cannot = [0]
        
        def __str__(self) : 
            return "(%d, %d) = %d" % (self.row, self.col, self.val)
        
        def coord(self) :  
            """Return a string of the current node's coordinates"""
            return "(%d, %d)" % (self.row, self.col)
        
        def not_possible(self, val) :
            ret_val = False
            
            if val in self.possible :
                self.possible.remove(val)
                ret_val = True
            
            if val not in self.cannot :
                self.cannot.append(val)
                self.cannot.sort()
            
            total = self.cannot + self.possible
            total.sort()
            assert total == list(range(0,10))
            
            return ret_val
        
        def set(self, val) :
            assert val in range(1,10)
            assert val in self.possible
            assert val not in self.cannot
            assert self.val == 0
            
            self.val = val
            self.cannot = list(range(0,10))
            self.possible = []
            print (self)
        
    
    class Sudoku_Matrix :
        def __init__(self, input_grid=[[0]*9]*9) :
            if check_sudoku(input_grid) is not True : 
                print( "Fix your sudoku!" )
                print( str(check_sudoku(input_grid)) )
                return
            
            self.matrix = []
            for i in range(0,9) : 
                temp_row = []
                for j in range(0,9) :
                    temp_row.append( Node(i,j,input_grid[i][j]) )
                self.matrix.append(temp_row)
            
        def __str__(self) :
            ret_mat = []
            for i in range(0,9) : 
                temp_row = []
                for j in range(0,9) : 
                    temp_row.append( self.matrix[i][j].val )
                ret_mat.append(temp_row)
            return str(ret_mat)
        
        def print_game(self, string="") :
            """Print to console a human-readable version of the current game.
            Note: we MUST use sys.stdout.write(..) to properly format the
            matrix on the screen"""
            from sys import stdout
            stdout.write( str(string) + str(self).replace(r"[[" , r"[").replace(r"]]" , "]\n").replace(r"[" , "\n[").replace(r"]," , "]") )
        
        def output(self) :
            """returns simple 2D integer array of the current game. 
            This is the expected return format for this assignment"""
            ret_matrix = []
            for i in range(0,9) : 
                temp_row = []
                for j in range(0,9) :
                    temp_row.append(self.matrix[i][j].val )
                ret_matrix.append(temp_row)
            assert check_sudoku( ret_matrix ) is True
            return ret_matrix
        
        def sorted_possibilities(self) :
            """Return a list of nodes sorted by the amount of 
            possibilities they have remaining; node with least
            possibilities is at top of list (element 0)"""
            
            ret_list = []
            from copy import deepcopy
            game = deepcopy(self)
            
            for row in range(0,9) : 
                for col in range(0,9) : 
                    if game.matrix[row][col].val == 0 :
                        ret_list.append( game.matrix[row][col] )
                    else :
                        assert game.matrix[row][col].possible == []
                        assert game.matrix[row][col].cannot == list(range(0,10))
            
            ret_list.sort( key=lambda node: len(node.possible) )
            return ret_list
        
        
        # return nodes in each row, column, or box
        def getRowNodes(self, row) :
            assert row in range(0,9)
            ret_val = []
            for j in range(0,9) : ret_val.append( self.matrix[row][j] )
            return ret_val
        
        def getColNodes(self, col) :
            assert col in range(0,9)
            ret_val = []
            for i in range(0,9) : ret_val.append( self.matrix[i][col] )
            return ret_val
        
        def getBoxNodes(self, box) :
            assert box in range(0,9)
            ret_val = []
            for i in range(1,4) : # row
                for j in range(1,4) : # column
                    ret_val.append( self.matrix[i-1+3*int(box/3)][j-1+3*(box%3)] )
            return ret_val
        
        # return values in each row, column, or box
        def getRowVals(self, row) :
            assert row in range(0,9)
            ret_val = []
            for j in range(0,9) : ret_val.append( self.matrix[row][j].val )
            return ret_val
        
        def getColVals(self, col) :
            assert col in range(0,9)
            ret_val = []
            for i in range(0,9) : ret_val.append( self.matrix[i][col].val )
            return ret_val
        
        def getBoxVals(self, box) :
            assert box in range(0,9)
            ret_val = []
            for i in range(1,4) : # row
                for j in range(1,4) : # column
                    ret_val.append( self.matrix[i-1+3*int(box/3)][j-1+3*(box%3)].val )
            return ret_val
        
        # determine if this puzzle is complete
        def Done(self) :
            for i in range(0,9) : 
                if (0 in self.getBoxVals(i)) or (0 in self.getColVals(i)) or (0 in self.getRowVals(i)) : 
                    return False
            
            # run some assertions on our supposedly complete game before returning
            for i in range(0,9) :
                for j in range(0,9) :
                    assert self.matrix[i][j].cannot == list(range(0,10))
                    assert self.matrix[i][j].possible == []
            assert check_sudoku( self.output() ) is True
            return True
        
        def DoneRow(self, row) : return 0 not in self.getRowVals(row)
        def DoneCol(self, col) : return 0 not in self.getColVals(col)
        def DoneBox(self, box) : return 0 not in self.getBoxVals(box)
        
        # reduce 'possible' and increase 'cannot' values for each node in a row
        def reduceRow(self, row) :
            row_vals = self.getRowVals(row)
            for j in range(0,9) : 
                for val in row_vals :
                    self.matrix[row][j].not_possible(val) 
                for val in self.getColVals( self.matrix[row][j].col ) :
                    self.matrix[row][j].not_possible(val) 
                # only need to calculate box vals for every 3 nodes
                if j % 3 == 0 : box_vals = self.getBoxVals( self.matrix[row][j].box )
                assert box_vals is not None
                assert len(box_vals) == 9
                #print ( "box vals for elm %d = %s" % (j, str(box_vals) ) )
                for val in box_vals : 
                    self.matrix[row][j].not_possible(val) 
                
        # reduce 'possible' and increase 'cannot' values for each node in a col
        def reduceCol(self, col) :
            col_vals = self.getColVals(col)
            for i in range(0,9) : 
                for val in col_vals :
                    self.matrix[i][col].not_possible(val) 
                for val in self.getRowVals( self.matrix[i][col].row ) :
                    self.matrix[i][col].not_possible(val)
                
                # only need to calculate box vals for every 3 nodes
                if i % 3 == 0 : 
                    box_vals = self.getBoxVals( self.matrix[i][col].box )
                
                assert box_vals is not None
                assert len(box_vals) == 9
                
                #print ( "box vals for elm %d = %s" % (j, str(box_vals) ) )
                for val in box_vals : 
                    self.matrix[i][col].not_possible(val) 
                
        # reduce 'possible' and increase 'cannot' values for each node in a box
        def reduceBox(self, box) :
            box_vals = self.getBoxVals(box)
            
            for i in range(1,4) : # row
                x = i-1+3*int(box/3)
                row_vals = self.getRowVals( x )
                for j in range(1,4) : # column
                    y = j-1+3*(box%3)
                    for val in box_vals :
                        self.matrix[x][y].not_possible(val) 
                    for val in row_vals :
                        self.matrix[x][y].not_possible(val) 
                    for val in self.getColVals( y ) :
                        self.matrix[x][y].not_possible(val) 
                
        # reduce 'possible' and increase 'cannot' values for a given node address
        def reduce_Node(self, row, col) :
            for val in self.getRowVals(row) :
                self.matrix[row][col].not_possible(val) 
            for val in self.getColVals( self.matrix[row][col].col ) :
                self.matrix[row][col].not_possible(val) 
            for val in self.getBoxVals( self.matrix[row][col].box ) : 
                self.matrix[row][col].not_possible(val) 
            
        # reduce 'possible' and increase 'cannot' values for every node
        def reduce_Matrix(self) :
            row_vals = []
            col_vals = []
            box_vals = []
            
            # for speed pre-compute these arrays (more memory intensive!)
            # TODO: benchmark with / without this 
            for x in range(0,9) : 
                row_vals.append( self.getRowVals(x) )
                col_vals.append( self.getColVals(x) )
                box_vals.append( self.getBoxVals(x) )
            
            for i in range(0,9) : 
                for j in range(0,9) :
                    for val in row_vals[i] :
                        self.matrix[i][j].not_possible(val) 
                    for val in col_vals[j] :
                        self.matrix[i][j].not_possible(val) 
                    for val in box_vals[ self.matrix[i][j].box ] :
                        self.matrix[i][j].not_possible(val) 
                    
                    if self.matrix[i][j].val == 0 and len(self.matrix[i][j].possible) == 0 :
                        print ("FOUND AN IMPOSSIBLE GAME !!")
                        return False
       
    
    ### sudoku reduction and solving functions
    def solve_game(game, loop=0) :
        
        if game.Done() :
            """Except for the case that we start off with
            a finished game, this should never get triggered"""
            assert loop == 0
            game.print_game("Game already done !")
            return game
        
        
        def node_analysis(node) :
            if (node.val == 0) and len(node.possible) == 0 : 
                assert node.cannot == list(range(0,10))
                print ("Found an impossible game (node with 0 possibilities) : " + str(node.coord()) )
                return -1
            
            if len(node.possible) == 1 : # only 1 possible answer!
                assert node.val == 0
                assert node.val != node.possible[0]
                node.set ( node.possible[0] )
                
                # re-calculate possibilities
                game.reduceRow(node.row)
                game.reduceCol(node.col)
                game.reduceBox(node.box)
                
                return True
            
            #'else' implied by returning
            assert ( node.val != 0 ) or ( len(node.cannot) < 9 )
            return False
        
        
        def solve_Nodes(node_list, guess) :
            """Given a collection of nodes, see if the
            integer 'guess' can be solved for within 
            these nodes. """
            
            assert len(node_list) == 9
            solved = False
            possibles = []
            ans = -1
            
            # get a full list of possibilities for these nodes
            for z in range(0,9) : 
                possibles += node_list[z].possible
            
            if possibles.count(guess) == 1 :
                # find the answer node
                for z in range(0,9) : 
                    if guess in node_list[z].possible : 
                        assert node_list[z].val == 0
                        node_list[z].set(guess)
                        
                        assert solved == False
                        solved = True
                        ans = z
                    
            
            if solved : 
                assert ans != -1
                game.reduceRow( node_list[ans].row )
                game.reduceCol( node_list[ans].col )
                game.reduceBox( node_list[ans].box )
            
            return solved
        
        
        def reduce_Dependancies( node_list ) :
            reduced = False # return value
            reduce_list = [] # to-reduce list
            check_list = []
            
            # get a list of all numbers that need completing
            possible_lists = [] # list of every node's possibilities
            for z in range(0,9) : 
                if node_list[z].val == 0 :
                    # append each element as a list, which means
                    # possible_lists is a list of lists
                    possible_lists.append(node_list[z].possible)
            
            for item in possible_lists : 
                if possible_lists.count( item ) > 1 : 
                    #assert len(item) >= possible_lists.count(item) # only valid with gussed games
                    if len(item) < possible_lists.count(item) :
                        print ("Found an impossible game (over-constrained set) :")
                        for node in node_list : print ( str(node) + str(node.possible) )
                        return -1
                        
                    if ( len(item) ==  possible_lists.count(item) )  and ( possible_lists.count(item) < len(possible_lists) ) :
                        reduce_list += [items for items in item if items not in reduce_list] # lol
                        if item not in check_list : check_list.append(item)
            
            for value in reduce_list :
                for node in node_list : 
                    if (node.val == 0) and (node.possible not in check_list) :
                        if node.not_possible(value) : 
                            reduced = True
                
            
            return reduced
        
        """ Body of solve_game """
        # check if any nodes have 0 possibilities
        answ = game.reduce_Matrix()
        if answ == False :
            print ("Goodbye")
            return False
        elif answ == -1 :
            print ("DEBUG !!!! ")
        game.print_game("Solving, loop %d" % loop)
        changed = False
        
        # check the properties of each individual
        # cell. this may solve certain nodes, or 
        # tell us our game is un-solvable
        for i in range(0,9) : # row
            for j in range(0,9) : # col
                result = node_analysis( game.matrix[i][j] )
                if result == True : 
                    changed = True
                elif result == -1 :
                    print("Goodbye")
                    return result
            
        
        # check if, for each possible value and set of 
        # cells, there is only 1 location it can go
        for y in range(0,9) : # for each row/col/box
            for x in range(1,10) : # for each possibile answer (solving for x)
                
                if x not in game.getBoxVals(y) : 
                    if solve_Nodes( game.getBoxNodes(y), x ) : 
                        changed = True
                
                if x not in game.getRowVals(y) : 
                    if solve_Nodes( game.getRowNodes(y), x ) : 
                        changed = True
                
                if x not in game.getColVals(y) : 
                    if solve_Nodes( game.getColNodes(y), x ) : 
                        changed = True
                
            
        # Go through selection of nodes and find
        # 'constrained cells' where the set of
        # possibilities is the same across multiple cells
        # This can also tell us if we have an invalid puzzle
        for y in range(0,9) : # each row/col/box
            if not game.DoneCol(y) : 
                res = reduce_Dependancies( game.getColNodes(y) )
                if res == True : 
                    changed = True # may not have changed values, but we did meaningful work
                elif res == -1 : 
                    return -1
            
            if not game.DoneRow(y) : 
                res = reduce_Dependancies( game.getRowNodes(y) )
                if res == True : 
                    changed = True
                elif res == -1 : 
                    return -1
            if not game.DoneBox(y) : 
                res = reduce_Dependancies( game.getBoxNodes(y) ) 
                if res == True : 
                    changed = True
                elif res == -1 : 
                    return -1
            
        
        # Recursion and Guessing control
        if changed and not game.Done() : 
            return solve_game(game, loop+1)
        
        elif game.Done() :
            game.print_game ( "\nSolved after %d iterations!" % loop )
            return game.output()
        
        else :
            print ( "Deadlocked after %d iterations!\n\n" % loop )
            
            # list of all possible places we can guess, 
            # in order of # of possibilities
            to_guess_list = game.sorted_possibilities()
            assert len(to_guess_list) > 0
            #print ("Current possibilities: ")
            #for node in to_guess_list : print ( node.coord() +" : "+ str(node.possible) ) 
            
            # Currently, we choose our "guessing" 
            # node by least-possibilities
            # TODO: other strategies, e.g. completing 
            # a row/col/box as highest priority, etc.
            node = to_guess_list[0]
            print ( "Guessing for node: "+str(node) )
            for possibility in node.possible :
                # take the current game output
                guess = game.output()
                assert guess[node.row][node.col] == 0
                
                # fill in our guess
                guess[node.row][node.col] = possibility
                assert check_sudoku(guess) is True
                print ( "Guess : (%d, %d) = %d" % (node.row, node.col, guess[node.row][node.col]) )
                
                # attempt to solve for this guess
                attempt = Sudoku_Matrix( guess )
                assert guess == attempt.output()
                answ = solve_game(attempt, loop+1)
                
                if (answ == -1) or (answ == False) : # TODO: sanity check when we return -1 and when we return False
                    print ("GUESS (%d, %d) = %d DIDN'T WORK\n\n" % (node.row, node.col, guess[node.row][node.col]) )
                else : 
                    #print ("guess "+str(answ)+" worked!")
                    return answ
            
            # we only choose 1 single node to 
            # iterate through all possibilities
            # and guess; if all possibilities
            # fail, this node cannot be solved!
            print ("NO NODES POSSIBLE FOR THIS GAME !!!")
            return False
            
    
    if check_sudoku(grid) is not True :
        return check_sudoku( grid )
    else :
        return solve_game( Sudoku_Matrix(grid) )


def test() :
    print ("Testing sudoku solver!")
    """
    # can't be done
    print ( solve_sudoku(ill_formed) )
    print ( solve_sudoku(invalid) )
    print ( solve_sudoku(Impossible) )
    assert str(valid) == str( solve_sudoku(valid) )
    
    # to-solve
    print ( solve_sudoku(easy) )
    print ( solve_sudoku(hard) )
    print ( solve_sudoku(Null) ) # all zeroes
    """
    Jeff=[[6,3,7,8,1,4,9,5,2],
          [8,0,0,0,0,0,6,4,1],
          [4,0,1,2,6,0,3,8,7],
          [7,0,5,0,0,0,1,0,0],
          [3,0,4,1,0,8,5,7,6],
          [1,0,0,0,0,0,4,0,0],
          [5,4,8,6,7,3,2,1,9],
          [9,0,6,0,0,0,0,3,5],
          [2,0,3,9,0,0,0,6,4]]
    print ( solve_sudoku(Jeff) )
test()
#raw_input ("\nPress 'Enter' to exit")
