# Author: Stew Towle
# Date: 3/11/2021
# Description: Contains the definitions for the structure of a Janggi game.  If run as script
#           plays a janggi game in the text i/o. The script version will bring the game to
#        the verge of Checkmate, once the checkmate is made it will allow user to start
#  a new game. This file contains the class definition for GamePiece and JanggiGame.
#  GamePiece objects represent pieces on the JanggiBoard and should only be used by
#  JanggiGame objects. JanggiGame objects contain a janggi board representation and have
#  methods for playing a game. The methods for use outside the class are initializing
#  a game (sets to default starting game board), make_move (which allows you to attempt
#  to make a move and returns True if the move is valid and made, and false otherwise),
#  get_game_state (which returns the current state of the game, either 'UNFINISHED',
#   'RED_WON' or 'BLUE_WON), and is_in_check which takes a player color (either 'red'
#   or 'blue') and returns if that player is currently in check.



class GamePiece:
    """
    Defines objects to represent game pieces on Janggi board.  Each object has a name
    and a color, which must be passed when initializing. GamePieces are used by the
    JanggiGame class to represent the pieces on the board. Has get methods
    for name and color.
    """

    def __init__(self, name, color):
        """Initializes a given game piece with the given name (which is th pieces type:
        'GENERAL','GUARD','SOLDIER','CANNON','ELEPHANT','HORSE', or 'CHARIOT')
        and color ('red' or 'blue')"""
        self._piece_name = name
        self._color = color

    def __repr__(self):
        """REturns a stirng representation of the piece which is its name followed by color"""
        return self._piece_name + self._color

    def get_color(self):
        """Returns a string that is the color of the piece, either 'blue' or 'red'."""
        return self._color

    def get_name(self):
        """
        Returns the name (type) of the piece. Either 'GENERAL', 'SOLDIER', GUARD',
        'ELEPHANT', 'HORSE', 'CHARIOT' or 'CANNON'.
        """
        return self._piece_name


class JanggiGame:
    """
    Defines instances of a game of Janggi. All actions in the game should be performed
    by calling JanggiGame's methods. JanggiGame contains instances of GamePiece.
    JanggiGame is responsible for maintaining the games state and storing the board.
    It's methods allow for making moves, seeing if a player is in check, and
    getting the game's current state.
    """

    def __init__(self):
        """
        Initializes an instance of the JanggiGame with the default board setup
        and a number of private data members for storing and updating the game.
        Game begins with it being 'blue' player's turn and ends when a player
        puts another in check_mate.  Does not allow for elephant-horse swapping.
        """
        self._game_state = "UNFINISHED"
        self._board = self._construct_board()
        self._temp_board = list()
        self._current_turn = 'blue'
        self._color_dict = {'blue':'red','red':'blue'}
        self._col_conversion = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h', 8:'i',
                                'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8}
        self._col_label = self._col_label_gen(14)


    def _construct_board(self):
        """
        Creates and returns a two dimensional list to represent a Janggi Board. Populates empty verticies
        with None and the correct starting location with GamePiece objects of each piece
        and the appropriate color to have red on top and blue on bottom.
        """

        board_source = [[None for counter in range(9)] for count in range(10)]
        for row_num, row in enumerate(board_source):
            for col_num, col in enumerate(row):
                if row_num == 0 or row_num == 9:
                    #end rows
                    if col_num == 0 or col_num == 8:
                        board_source[row_num][col_num] = GamePiece("CHARIOT", ('blue' if row_num == 9 else 'red'))
                    if col_num == 1 or col_num == 6:
                        board_source[row_num][col_num] = GamePiece("ELEPHANT", ('blue' if row_num == 9 else 'red'))
                    if col_num == 2 or col_num == 7:
                        board_source[row_num][col_num] = GamePiece("HORSE", ('blue' if row_num == 9 else 'red'))
                    if col_num == 3 or col_num == 5:
                        board_source[row_num][col_num] = GamePiece("GUARD", ('blue' if row_num == 9 else 'red'))
                if row_num == 1 or row_num == 8:
                    #second rows
                    if col_num == 4:
                        board_source[row_num][col_num] = GamePiece("GENERAL", ('blue' if row_num == 8 else 'red'))
                if row_num == 2 or row_num == 7:
                    #third rows
                    if col_num == 1 or col_num == 7:
                        board_source[row_num][col_num] = GamePiece("CANNON", ('blue' if row_num == 7 else 'red'))
                if row_num == 3 or row_num == 6:
                    #Fourth rows
                    if col_num == 0 or col_num == 8 or col_num == 2 or col_num == 4 or col_num == 6:
                        board_source[row_num][col_num] = GamePiece("SOLDIER", ('blue' if row_num == 6 else 'red'))

        return board_source


    def print_board(self):
        """
        Prints out the board to output in a basic fashion which includes the board pieces and labelled
        collums and rows as well as the current state of the game and the player whose turn it is.
        """
        print(self.__repr__())

    def _col_label_gen(self, spacing):
        """
        Single use helper function to generate the label string that is used in
        __repr__ to make a printable depiction of the board. It creates a single line
        string of collumn labels given the number of spaces of text each collum on the
        actual board takes up.
        """
        label_string = "    "
        for index in range(len(self._board[0])):
            label_string += self._col_conversion[index]
            label_string += (" " * (spacing - 1))
        return label_string + '\n'

    def __repr__(self):
        """
        Creates a string representation of the board, with imbedded new_line character
        so board can be displayed by calling print on a JanggiBoard object. Includes
        the board with its pieces and None for empty verticies, as well as collum
        and row labels and a message on the bottom saying whose turn it is and
        the current game state.
        """
        board_string = self._col_label
        for row in range(len(self._board)):
            if row < 9:
                board_string += str(row + 1) + "  "
            else:
                board_string += str(row + 1) + " "
            for vertex in self._board[row]:
                board_string += str(vertex)
                for space_count in range((14 - len(str(vertex)))):
                    board_string += " "
            board_string += "\n"
        board_string += "It is " + self._current_turn + " player's turn. The game state is " \
                        + self._game_state + ". \n"
        return board_string


    def _set_vertex(self, location, value):
        """
        Takes a vertex location on the board and sets the value
        at the location to the value given. Should only be given None
        or a GamePiece as value.  Location in col-letter/row-num string format.
        """
        col_num = self._col_conversion[location[0]]
        row_num = int(location[1:]) - 1
        self._board[row_num][col_num] = value

    def get_game_state(self):
        """Returns whether the game is 'UNFINISHED', 'RED_WON', or 'BLUE_WON'"""
        return self._game_state

    def _find_general(self, player_color):
        """Returns the location of the given player's general in col-letter/row-num string format"""
        if player_color == 'blue':
            for row_index in range(7,10):
                for col_index in range(3,6):
                    if str(self._board[row_index][col_index]) == ("GENERAL" + player_color):
                        return self._col_conversion[col_index] + str(row_index + 1)
        else:
            for row_index in range(0,3):
                for col_index in range(3,6):
                    if str(self._board[row_index][col_index]) == ("GENERAL" + player_color):
                        return self._col_conversion[col_index] + str(row_index + 1)


    def _convert_to_string_location(self, row, col):
        """
        Given a row and collum of a vertix in the 2D board list returns the
        col-letter/row-num string representation of that location.
        """
        return self._col_conversion[col] + str(row + 1)

    def is_in_check(self, player):
        """
        Takes as a parameter either 'red' or 'blue' and returns True
        if that player is in check, but returns False otherwise.
        """
        general_location = self._find_general(player)
        for row_index in range(len(self._board)):
            for col_index in range(len(self._board[row_index])):
                current_piece = self._board[row_index][col_index]
                if current_piece is not None:
                    if current_piece.get_color() != player:
                        #At this point we have found a piece that belongs to the opponent
                        #so we check if the general's location is in that pieces move_list, and if so it is in check
                        if general_location in self._list_moves(self._convert_to_string_location(row_index, col_index)):
                            return True
        return False

    def _is_in_checkmate(self, player_color):
        """
        Takes as a parameter either 'red' or 'blue' and assumes that the given
        player is in check (should only be called when a player is in check)
        and returns True if there are no legal moves that would result in the player
        not being in check, False otherwise.
        """
        checkmate_bool = True

        #We begin by iterating through every vertex on the board, looking for piece's the current player contorls
        for row_index in range(len(self._board)):
            for col_index in range(len(self._board[0])):
                current_piece = self._board[row_index][col_index]
                if current_piece is not None and current_piece.get_color() == player_color:

                    #if we find one of current player's pieces then we see if any of its moves
                    # result in being not in check.
                    current_position = self._convert_to_string_location(row_index, col_index)
                    potential_moves = self._list_moves(current_position)
                    for move_to_try in potential_moves:
                        self._try_move(current_position, move_to_try)
                        checkmate_bool = self.is_in_check(player_color)
                        self._restore_board()
                        if not checkmate_bool:
                            break
                if not checkmate_bool:
                    break
            if not checkmate_bool:
                break
        return checkmate_bool

    def make_move(self, piece_origin, piece_destination):
        """
        Takes a location of a piece to be moved, and the destination to attempt to move it to.
        If the move is legal it makes the move and returns True, if the move is not
        a legal move, or the piece trying to be moved doesn't belong to the player
        whose turn it is, or if the game is already won returns False
        and does not alter the board state.
        Giving the same value for origin and destination is interpretted as an attempt to pass turn.
        Positions must be on the board, but dont need to be the current player's piece (or a piece at all)
        Unless attempting to pass turn while the current player is in check will return True
        and switch whose turn it is. If pass attempted while current player is in check returns False.
        """

        if self._game_state != 'UNFINISHED':
            return False
        try:
            #catching invalid inputs
            validate_col = self._col_conversion[piece_origin[0]]
            validate_row = int(piece_origin[1:])
            if validate_col < 0 or validate_col > 8 or validate_row < 1 or validate_row > 10:
                return False
        except:
            return False

        #per a note from Piazza I have made it so any input of the same location for origin and destination
        # will result in a pass-turn legal move unless, of course, the game is already won.

        piece_to_move = self._get_piece(piece_origin)
        if piece_origin != piece_destination:
            if piece_to_move is None:
                return False
            if piece_to_move.get_color() != self._current_turn:
                return False
            potential_moves = self._list_moves(piece_origin)
            if piece_destination not in potential_moves:
                return False
            self._try_move(piece_origin, piece_destination)

            #We check if making the given move is self-check, if so restore the board and return False
            if self.is_in_check(self._current_turn):
                self._restore_board()
                return False
        else:
            #Here we are in a situation where a player is trying to pass. This is a valid move unless that player
            # is currently in check.
            if self.is_in_check(self._current_turn):
                return False

        self._current_turn = self._color_dict[self._current_turn]

        #Check if the player whose turn it is becoming is in checkmate
        if self.is_in_check(self._current_turn):
            if self._is_in_checkmate(self._current_turn):
                if self._current_turn == 'blue':
                    self._game_state = 'RED_WON'
                else:
                    self._game_state = 'BLUE_WON'
                self._current_turn = self._color_dict[self._current_turn]

        return True


    def _try_move(self, piece_origin, piece_destination):
        """
        Stores a temporary board state before attempting to move a piece.
        Then (without checking if it is their turn or if the game has ended
        or if the piece can actually move in that way)
        it makes the move. _restore_board should always be called
        after _try_move unless the move has been certified as legal by make_move
        """
        self._temp_board = self._copy_2d_list(self._board)
        piece_moving = self._get_piece(piece_origin)
        if piece_moving is None:
            return
        if piece_origin == piece_destination:
            return
        self._set_vertex(piece_destination, piece_moving)
        self._set_vertex(piece_origin, None)


    def _copy_2d_list(self, list_to_copy):
        """
        Special helper function used for storing and restoring the locations
        of all the pieces on the board without mutating the original or the copy.
        Given a two dimensional list of standard dimensions (every row has the same
        number of collums) returns a copy of that list that is a separate instance.
        """
        copy = [list() for counter in range(len(list_to_copy))]
        for row in range(len(list_to_copy)):
            for col in range(len(list_to_copy[0])):
                copy[row].append(list_to_copy[row][col])
        return copy


    def _restore_board(self):
        """
        Only to be called after _try_move, restores the board to the state
        it was in before try_move
        """
        self._board = self._copy_2d_list(self._temp_board)

    def _get_piece(self, piece_location):
        """
        This function is used to get the piece (or None) at a given location.
        Takes as parameter a vertex location that is a string of form
        '[collumn letter][row number]' (ie 'a1' or 'i10') and returns the piece
        at that location (or None if no piece there or if the location is off the board).'
        """
        if piece_location[0] not in self._col_conversion or 10 < int(piece_location[1:]) < 0:
            return None
        col = self._col_conversion[piece_location[0]]
        row = int(piece_location[1:]) - 1
        return self._board[row][col]

    def _list_moves(self, piece_location):
        """
        Takes as parameter a vertex location, in the form '[collumn letter][row number]'
        and returns a list of all possible location the piece might move to
        based on how that piece moves and its color. Does not consider if the moves
        would put the moving player in check. Returns an empty list if there is
        no piece at the location or if the piece_location is off the board.
        """
        piece_to_check = self._get_piece(piece_location)
        if piece_to_check is None:
            return list()
        if piece_to_check.get_name() == "GENERAL":
            #General moves identical to guard, so removed earlier redundant method
            # for general_moves.
            return self._guard_moves(piece_location, piece_to_check.get_color())
        if piece_to_check.get_name() == "GUARD":
            return self._guard_moves(piece_location, piece_to_check.get_color())
        if piece_to_check.get_name() == "SOLDIER":
            return self._soldier_moves(piece_location, piece_to_check.get_color())
        if piece_to_check.get_name() == "CHARIOT":
            return self._chariot_moves(piece_location, piece_to_check.get_color())
        if piece_to_check.get_name() == "HORSE":
            return self._horse_moves(piece_location, piece_to_check.get_color())
        if piece_to_check.get_name() == "ELEPHANT":
            return self._ele_moves(piece_location, piece_to_check.get_color())
        if piece_to_check.get_name() == "CANNON":
            return self._cannon_moves(piece_location, piece_to_check.get_color())
        return list()


    def _cannon_moves(self, piece_location, piece_color):
        """
        Takes as a parameter a vertex location in form '[col letter][row num]'
        and a player color and returns a list of string locations of the same form
        of all valid moves for a cannon of the given color at the given location.
        Checks that any move includes a single piece jump over something
        that is not a cannon and does not arrive on
        a friendly piece or an opponents cannon.  Does not consider check.
        """
        move_list = list()
        move_list.append(piece_location)
        current_row = int(piece_location[1:]) - 1
        current_col = self._col_conversion[piece_location[0]]
        slide_move_counter = 1

        # integer values that counts the number of pieces encountered
        # along that direction. Notable become 1 once we jumped over a non-cannon piece,
        # and becomes 2 or greater when movement in that direction invalid.
        # Becomes 2 if we hit edge of board
        left_piece_count = 0
        right_piece_count = 0
        up_piece_count = 0
        down_piece_count = 0
        left_down_piece_count = 0
        right_down_piece_count = 0
        left_up_piece_count = 0
        right_up_piece_count = 0

        while left_piece_count < 2 or right_piece_count < 2 or up_piece_count < 2 or \
                down_piece_count < 2 or left_down_piece_count < 2 or right_down_piece_count < 2 or \
                left_up_piece_count < 2 or right_up_piece_count < 2:
            if current_row - slide_move_counter < 0:
                up_piece_count = 2
            if current_row + slide_move_counter >= len(self._board):
                down_piece_count = 2
            if current_col + slide_move_counter >= len(self._board[0]):
                right_piece_count = 2
            if current_col - slide_move_counter < 0:
                left_piece_count = 2

            # moving left
            # Once we have passed one piece each move is valid until we hit another pieces
            # (scenarios of this in connected if and elif's)
            if left_piece_count == 1 and self._board[current_row][current_col - slide_move_counter] is None:
                move_list.append(self._convert_to_string_location(current_row, current_col - slide_move_counter))
            elif left_piece_count == 1 and self._board[current_row][current_col - slide_move_counter].get_color() != piece_color:
                if self._board[current_row][current_col - slide_move_counter].get_name() != 'CANNON':
                    move_list.append(self._convert_to_string_location(current_row, current_col - slide_move_counter))
                left_piece_count += 1
            elif left_piece_count == 1:
                left_piece_count += 1

            #If we have not hit a piece yet checks if we hit a piece
            if left_piece_count == 0 and self._board[current_row][current_col - slide_move_counter] is not None:

                #if the piece we hit is a cannon set direction invalid, otherwise set pieces jumped to 1
                if self._board[current_row][current_col - slide_move_counter].get_name() == 'CANNON':
                    left_piece_count = 2
                else:
                    left_piece_count += 1

            # movin right, see moving left comments for specific check breakdowns
            if right_piece_count == 1 and self._board[current_row][current_col + slide_move_counter] is None:
                move_list.append(self._convert_to_string_location(current_row, current_col + slide_move_counter))
            elif right_piece_count == 1 and self._board[current_row][current_col + slide_move_counter].get_color() != piece_color:
                if self._board[current_row][current_col + slide_move_counter].get_name() == "CANNON":
                    right_piece_count += 2
                else:
                    move_list.append(self._convert_to_string_location(current_row, current_col + slide_move_counter))
                    right_piece_count += 1
            elif right_piece_count == 1:
                right_piece_count += 1

            if right_piece_count == 0 and self._board[current_row][current_col + slide_move_counter] is not None:
                if self._board[current_row][current_col + slide_move_counter].get_name() == "CANNON":
                    right_piece_count += 2
                else:
                    right_piece_count += 1

            # moving up, see moving left comments for specific check breakdowns
            if up_piece_count == 1 and self._board[current_row - slide_move_counter][current_col] is None:
                move_list.append(self._convert_to_string_location(current_row - slide_move_counter, current_col))
            elif up_piece_count == 1 and self._board[current_row - slide_move_counter][current_col].get_color() != piece_color:
                if self._board[current_row - slide_move_counter][current_col].get_name() == 'CANNON':
                    up_piece_count = 2
                else:
                    move_list.append(self._convert_to_string_location(current_row - slide_move_counter, current_col))
                    up_piece_count += 1
            elif up_piece_count == 1:
                up_piece_count += 1

            if up_piece_count == 0 and self._board[current_row - slide_move_counter][current_col] is not None:
                if self._board[current_row - slide_move_counter][current_col].get_name() == 'CANNON':
                    up_piece_count += 2
                else:
                    up_piece_count += 1


            # moving down, see moving left for specific check breakdowns
            if down_piece_count == 1 and self._board[current_row + slide_move_counter][current_col] is None:
                move_list.append(self._convert_to_string_location(current_row + slide_move_counter, current_col))
            elif down_piece_count == 1 and self._board[current_row + slide_move_counter][current_col].get_color() != piece_color:
                if self._board[current_row + slide_move_counter][current_col].get_name() != 'CANNON':
                    move_list.append(self._convert_to_string_location(current_row + slide_move_counter, current_col))
                down_piece_count += 1
            elif down_piece_count == 1:
                down_piece_count += 1

            if down_piece_count == 0 and self._board[current_row + slide_move_counter][current_col] is not None:
                if self._board[current_row + slide_move_counter][current_col].get_name() == "CANNON":
                    down_piece_count = 2
                else:
                    down_piece_count += 1

            #Now for the rare Diagonal scenarios
            if slide_move_counter == 3:
                left_up_piece_count = 2
                left_down_piece_count = 2
                right_up_piece_count = 2
                right_down_piece_count = 2

            # diagonal left down, first we check if we are on a square in the palace we could move diagonally
            #  left and down from.
            if not self._diag_left(piece_location, 1):
                left_down_piece_count = 2

            #if we have one intervining piece and could move down-left then check if it is a valid place to move
            if left_down_piece_count == 1 and self._diag_left(piece_location, 1):
                if slide_move_counter + current_row >= len(self._board) or \
                        current_col - slide_move_counter < 0:
                    left_down_piece_count = 2
                elif self._board[current_row + slide_move_counter][current_col - slide_move_counter] is None:
                    move_list.append(self._convert_to_string_location(current_row + slide_move_counter,
                                                                      current_col - slide_move_counter))
                    left_down_piece_count = 2
                elif self._board[current_row + slide_move_counter][current_col - slide_move_counter].get_color() != piece_color:
                    if self._board[current_row + slide_move_counter][current_col - slide_move_counter].get_name() != 'CANNON':
                        move_list.append(self._convert_to_string_location(current_row + slide_move_counter,
                                                                      current_col - slide_move_counter))
                    left_down_piece_count = 2
                else:
                    left_down_piece_count = 2

            #if we have not encountered a piece and can move diagonally down, check if there is a valid piece to jump
            if left_down_piece_count == 0 and \
                    self._board[current_row + slide_move_counter][current_col - slide_move_counter] is not None:
                if self._board[current_row + slide_move_counter][current_col - slide_move_counter].get_name() != 'CANNON':
                    left_down_piece_count += 1
                else:
                    left_down_piece_count += 2

            #If we dont find a valid jump on the first pass then there will never be a valid move, so set
            # piece count for left-down to 2
            elif left_down_piece_count == 0:
                left_down_piece_count = 2


            # diagonal left up, see diag left-down for logical breakdwon of parts
            if not self._diag_left(piece_location, -1):
                left_up_piece_count = 2

            if left_up_piece_count == 1 and self._diag_left(piece_location, -1):
                if current_row - slide_move_counter < 0 or \
                        current_col - slide_move_counter < 0:
                    left_up_piece_count = 2
                elif self._board[current_row - slide_move_counter][current_col - slide_move_counter] is None:
                    move_list.append(self._convert_to_string_location(current_row - slide_move_counter,
                                                                      current_col - slide_move_counter))
                    left_up_piece_count = 2
                elif self._board[current_row - slide_move_counter][current_col - slide_move_counter].get_color() != piece_color:
                    if self._board[current_row - slide_move_counter][current_col - slide_move_counter].get_name() != 'CANNON':
                        move_list.append(self._convert_to_string_location(current_row - slide_move_counter,
                                                                      current_col - slide_move_counter))
                    left_up_piece_count = 2
                else:
                    left_up_piece_count = 2

            if left_up_piece_count == 0 and \
                    self._board[current_row - slide_move_counter][current_col - slide_move_counter] is not None:
                if self._board[current_row - slide_move_counter][current_col - slide_move_counter].get_name() != 'CANNON':
                    left_up_piece_count = 1
                else:
                    left_up_piece_count = 2
            elif left_up_piece_count == 0:
                left_up_piece_count = 2

            # diagonal right up, see diag left-down for logical breakdwon of parts
            if not self._diag_right(piece_location, -1):
                right_up_piece_count = 2

            if right_up_piece_count == 1:
                if current_row - slide_move_counter < 0 or \
                        current_col + slide_move_counter >= len(self._board[0]):
                    right_up_piece_count = 2
                elif self._board[current_row - slide_move_counter][current_col + slide_move_counter] is None:
                    move_list.append(self._convert_to_string_location(current_row - slide_move_counter,
                                                                      current_col + slide_move_counter))
                    right_up_piece_count += 1
                elif self._board[current_row - slide_move_counter][current_col + slide_move_counter].get_color() != piece_color:
                    if self._board[current_row - slide_move_counter][current_col + slide_move_counter].get_name() != 'CANNON':
                        move_list.append(self._convert_to_string_location(current_row - slide_move_counter,
                                                                            current_col + slide_move_counter))
                    right_up_piece_count = 2
                else:
                    right_up_piece_count = 2

            if right_up_piece_count == 0:
                if self._board[current_row - slide_move_counter][current_col + slide_move_counter] is not None:
                    if self._board[current_row - slide_move_counter][current_col + slide_move_counter].get_name() != 'CANNON':
                        right_up_piece_count += 1
                    else:
                        right_up_piece_count = 2
                else:
                    right_up_piece_count = 2

            # diagonal right down, see diag left-down for logical breakdwon of parts
            if not self._diag_right(piece_location, 1):
                right_down_piece_count = 2

            if right_down_piece_count == 1:
                if current_row + slide_move_counter >= len(self._board) or \
                        current_col + slide_move_counter >= len(self._board[0]):
                    right_down_piece_count = 2
                elif self._board[current_row + slide_move_counter][current_col + slide_move_counter] is None:
                    move_list.append(self._convert_to_string_location(current_row + slide_move_counter,
                                                                      current_col + slide_move_counter))
                    right_down_piece_count += 1
                elif self._board[current_row + slide_move_counter][current_col + slide_move_counter].get_color() != piece_color:
                    if self._board[current_row + slide_move_counter][current_col + slide_move_counter].get_name() != 'CANNON':
                        move_list.append(self._convert_to_string_location(current_row + slide_move_counter,
                                                                      current_col + slide_move_counter))
                    right_down_piece_count = 2
                else:
                    right_down_piece_count = 2

            if right_down_piece_count == 0:
                if self._board[current_row + slide_move_counter][current_col + slide_move_counter] is not None:
                    if self._board[current_row + slide_move_counter][current_col + slide_move_counter].get_name() != 'CANNON':
                        right_down_piece_count += 1
                    else:
                        right_down_piece_count = 2
                else:
                    right_down_piece_count = 2

            slide_move_counter += 1

        return move_list

    def _horse_moves(self, piece_location, piece_color):
        """
        Takes as a parameter a vertex location in form '[col letter][row num]'
        and a player color and returns a list of possible moves for a horse
        at the given location of the given color. Considers to make sure
        it does not require moving through a piece illegally or arrive
        on a friendly piece when making the list of moves. Does not consider check.
        Moves returned in same string location form as locations are inputted.
        """
        move_list = list()
        move_list.append(piece_location)
        current_row = int(piece_location[1:]) - 1
        current_col = self._col_conversion[piece_location[0]]

        #check upward motion
        if current_row - 2 >= 0:
            if self._board[current_row - 1][current_col] is None:
                if current_col - 1 >= 0:
                    if self._board[current_row - 2][current_col - 1] is None or \
                            self._board[current_row - 2][current_col - 1].get_color() != piece_color:
                        move_list.append(self._convert_to_string_location(current_row - 2, current_col - 1))
                if current_col + 1 < len(self._board[0]):
                    if self._board[current_row - 2][current_col + 1] is None or \
                            self._board[current_row - 2][current_col + 1].get_color() != piece_color:
                        move_list.append(self._convert_to_string_location(current_row - 2, current_col + 1))

        #check downward motion
        if current_row + 2 < len(self._board):
            if self._board[current_row + 1][current_col] is None:
                if current_col - 1 >= 0:
                    if self._board[current_row + 2][current_col - 1] is None or \
                            self._board[current_row + 2][current_col - 1].get_color() != piece_color:
                        move_list.append(self._convert_to_string_location(current_row + 2, current_col - 1))
                if current_col + 1 < len(self._board[0]):
                    if self._board[current_row + 2][current_col + 1] is None or \
                            self._board[current_row + 2][current_col + 1].get_color() != piece_color:
                        move_list.append(self._convert_to_string_location(current_row + 2, current_col + 1))

        #check rightward motion
        if current_col + 2 < len(self._board[0]):
            if self._board[current_row][current_col + 1] is None:
                if current_row - 1 >= 0:
                    if self._board[current_row - 1][current_col + 2] is None or \
                        self._board[current_row - 1][current_col + 2].get_color() != piece_color:
                        move_list.append(self._convert_to_string_location(current_row - 1, current_col + 2))
                if current_row + 1 < len(self._board):
                    if self._board[current_row + 1][current_col + 2] is None or \
                            self._board[current_row + 1][current_col + 2].get_color() != piece_color:
                        move_list.append(self._convert_to_string_location(current_row + 1, current_col + 2))

        #check leftward motion
        if current_col - 2 >= 0:
            if self._board[current_row][current_col - 1] is None:
                if current_row - 1 >= 0:
                    if self._board[current_row - 1][current_col - 2] is None or \
                            self._board[current_row - 1][current_col - 2].get_color() != piece_color:
                        move_list.append(self._convert_to_string_location(current_row - 1, current_col - 2))
                if current_row + 1 < len(self._board):
                    if self._board[current_row + 1][current_col - 2] is None or \
                            self._board[current_row + 1][current_col - 2].get_color() != piece_color:
                        move_list.append(self._convert_to_string_location(current_row + 1, current_col - 2))

        return move_list

    def _ele_moves(self, piece_location, piece_color):
        """
        Takes as a parameter a vertex location in form '[col letter][row num]'
        and a player color and returns a list of possible moves for a elephant
        at the given location of the given color. Considers to make sure
        it does not require moving through a piece illegally or arrive
        on a friendly piece when making the list of moves. Does not consider check.
        Moves returned in same string location form as locations are inputted.
        """
        move_list = list()
        move_list.append(piece_location)
        current_row = int(piece_location[1:]) - 1
        current_col = self._col_conversion[piece_location[0]]

        # check upward motion
        if current_row - 3 >= 0:
            if self._board[current_row - 1][current_col] is None:
                if current_col - 2 >= 0:
                    if self._board[current_row - 2][current_col - 1] is None:
                        if self._board[current_row - 3][current_col - 2] is None or \
                                self._board[current_row - 3][current_col - 2].get_color() != piece_color:
                            move_list.append(self._convert_to_string_location(current_row - 3, current_col - 2))
                if current_col + 2 < len(self._board[0]):
                    if self._board[current_row - 2][current_col + 1] is None:
                        if self._board[current_row - 3][current_col + 2] is None or \
                                self._board[current_row - 3][current_col + 2].get_color() != piece_color:
                            move_list.append(self._convert_to_string_location(current_row - 3, current_col + 2))

        # check downward motion
        if current_row + 3 < len(self._board):
            if self._board[current_row + 1][current_col] is None:
                if current_col - 2 >= 0:
                    if self._board[current_row + 2][current_col - 1] is None:
                        if self._board[current_row + 3][current_col - 2] is None or \
                                self._board[current_row + 3][current_col - 2].get_color() != piece_color:
                            move_list.append(self._convert_to_string_location(current_row + 3, current_col - 2))
                if current_col + 2 < len(self._board[0]):
                    if self._board[current_row + 2][current_col + 1] is None:
                        if self._board[current_row + 3][current_col + 2] is None or \
                                self._board[current_row + 3][current_col + 2].get_color() != piece_color:
                            move_list.append(self._convert_to_string_location(current_row + 3, current_col + 2))

        # check rightward motion
        if current_col + 3 < len(self._board[0]):
            if self._board[current_row][current_col + 1] is None:
                if current_row - 2 >= 0:
                    if self._board[current_row - 1][current_col + 2] is None:
                        if self._board[current_row - 2][current_col + 3] is None or \
                                self._board[current_row - 2][current_col + 3].get_color() != piece_color:
                            move_list.append(self._convert_to_string_location(current_row - 2, current_col + 3))
                if current_row + 2 < len(self._board):
                    if self._board[current_row + 1][current_col + 2] is None:
                        if self._board[current_row + 2][current_col + 3] is None or \
                                self._board[current_row + 2][current_col + 3].get_color() != piece_color:
                            move_list.append(self._convert_to_string_location(current_row + 2, current_col + 3))

        # check leftward motion
        if current_col - 3 >= 0:
            if self._board[current_row][current_col - 1] is None:
                if current_row - 2 >= 0:
                    if self._board[current_row - 1][current_col - 2] is None:
                        if self._board[current_row - 2][current_col - 3] is None or \
                                self._board[current_row - 2][current_col - 3].get_color() != piece_color:
                            move_list.append(self._convert_to_string_location(current_row - 2, current_col - 3))
                if current_row + 2 < len(self._board):
                    if self._board[current_row + 1][current_col - 2] is None:
                        if self._board[current_row + 2][current_col - 3] is None or \
                                self._board[current_row + 2][current_col - 3].get_color() != piece_color:
                            move_list.append(self._convert_to_string_location(current_row + 2, current_col - 3))

        return move_list

    def _chariot_moves(self, piece_location, piece_color):
        """
        Takes as a parameter a vertex location in form '[col letter][row num]'
        and a player color and returns a list of possible moves for a chariot
        at the given location of the given color. Considers to make sure
        it does not require moving through a piece illegally or arrive
        on a friendly piece when making the list of moves. Does not consider check.
        Moves returned in same string location form as locations are inputted.
        """
        move_list = list()
        move_list.append(piece_location)
        current_row = int(piece_location[1:]) - 1
        current_col = self._col_conversion[piece_location[0]]
        slide_move_counter = 1

        #Boolean value that remain true until we hit a piece or board edge along
        #that direction (or in the case of diagonal if we arent in the palace)
        left_bool = True
        right_bool = True
        up_bool = True
        down_bool = True
        left_down_bool = True
        right_down_bool = True
        left_up_bool = True
        right_up_bool = True

        #Loop through while there are valid moves in any direction, increasing distanced moved
        # by 1 each time until we generate all the possible moves
        while left_bool or right_bool or up_bool or down_bool or left_down_bool or \
                        right_down_bool or left_up_bool or right_up_bool:
            if current_row - slide_move_counter < 0:
                up_bool = False
            if current_row + slide_move_counter >= len(self._board):
                down_bool = False
            if current_col + slide_move_counter >= len(self._board[0]):
                right_bool = False
            if current_col - slide_move_counter < 0:
                left_bool = False

            #Orthogonal moves check (if their direction bool is not False) if at the current slide distance
            # there is an empty vertex or an opponents piece, if so they add that vertex to move list.
            # If there is any piece at the vertex current distance along that direction then the direction
            # bool sets to False since the piece can't move past that position along that direction.

            #moving left
            if left_bool and (self._board[current_row][current_col - slide_move_counter] is None or \
                            self._board[current_row][current_col - slide_move_counter].get_color() != piece_color):
                move_list.append(self._convert_to_string_location(current_row, current_col - slide_move_counter))
            if left_bool and self._board[current_row][current_col - slide_move_counter] is not None:
                    left_bool = False

            #movin right
            if right_bool and (self._board[current_row][current_col + slide_move_counter] is None or \
                            self._board[current_row][current_col + slide_move_counter].get_color() != piece_color):
                move_list.append(self._convert_to_string_location(current_row, current_col + slide_move_counter))
            if right_bool and self._board[current_row][current_col + slide_move_counter] is not None:
                    right_bool = False

            #moving up
            if up_bool and (self._board[current_row - slide_move_counter][current_col] is None or \
                            self._board[current_row - slide_move_counter][current_col].get_color() != piece_color):
                move_list.append(self._convert_to_string_location(current_row - slide_move_counter, current_col))
            if up_bool and self._board[current_row - slide_move_counter][current_col] is not None:
                    up_bool = False

            #moving down
            if down_bool and (self._board[current_row + slide_move_counter][current_col] is None or \
                            self._board[current_row + slide_move_counter][current_col].get_color() != piece_color):
                move_list.append(self._convert_to_string_location(current_row + slide_move_counter, current_col))
            if down_bool and self._board[current_row + slide_move_counter][current_col] is not None:
                    down_bool = False

            #If we hit third iteration, stop checking diagonals, no diagonal move of more than 2 is possible.
            if slide_move_counter == 3:
                left_up_bool = False
                left_down_bool = False
                right_up_bool = False
                right_down_bool = False

            #For each diagonal direction we check if the bool is still true and if a piece at origin location
            #   Would be able to move diagonally that direction (ie in the palace along that sort of diagonal)
            #   If we hit a piece or move out of the palace given slide distance then the directio bool become False
            #   If bool is still true and we hit an empty spot or the opponents piece along the direction then we add
            #   that location to the move list.

            #diagonal left down
            if left_down_bool and self._diag_left(piece_location, 1):
                if slide_move_counter + current_row >= len(self._board) or \
                        current_col - slide_move_counter < 0:
                    left_down_bool = False
                elif 2 < current_row + slide_move_counter < 7:
                    left_down_bool = False
                elif not 2 < current_col - slide_move_counter < 6:
                    left_down_bool = False
                elif self._board[current_row + slide_move_counter][current_col - slide_move_counter] is None:
                    move_list.append(self._convert_to_string_location(current_row + slide_move_counter, current_col - slide_move_counter))
                elif self._board[current_row + slide_move_counter][current_col - slide_move_counter].get_color() != piece_color:
                    move_list.append(self._convert_to_string_location(current_row + slide_move_counter,
                                                                      current_col - slide_move_counter))
                    left_down_bool = False
                else:
                    left_down_bool = False
            else:
                left_down_bool = False

            # diagonal left up
            if left_up_bool and self._diag_left(piece_location, -1):
                if current_row - slide_move_counter < 0 or \
                        current_col - slide_move_counter < 0:
                    left_up_bool = False
                elif 2 < current_row - slide_move_counter < 7:
                    left_up_bool = False
                elif not 2 < current_col - slide_move_counter < 6:
                    left_up_bool = False
                elif self._board[current_row - slide_move_counter][current_col - slide_move_counter] is None:
                    move_list.append(self._convert_to_string_location(current_row - slide_move_counter,
                                                                      current_col - slide_move_counter))
                elif self._board[current_row - slide_move_counter][current_col - slide_move_counter].get_color() != piece_color:
                    move_list.append(self._convert_to_string_location(current_row - slide_move_counter,
                                                                      current_col - slide_move_counter))
                    left_up_bool = False
                else:
                    left_up_bool = False
            else:
                left_up_bool = False

            # diagonal right up
            if right_up_bool and self._diag_right(piece_location, -1):
                if current_row - slide_move_counter < 0 or \
                        current_col + slide_move_counter >= len(self._board[0]):
                    right_up_bool = False
                elif 2 < current_row - slide_move_counter < 7:
                    right_up_bool = False
                elif not 2 < current_col + slide_move_counter < 6:
                    right_up_bool = False
                elif self._board[current_row - slide_move_counter][current_col + slide_move_counter] is None:
                    move_list.append(self._convert_to_string_location(current_row - slide_move_counter,
                                                                      current_col + slide_move_counter))
                elif self._board[current_row - slide_move_counter][current_col + slide_move_counter].get_color() != piece_color:
                    move_list.append(self._convert_to_string_location(current_row - slide_move_counter,
                                                                      current_col + slide_move_counter))
                    right_up_bool = False
                else:
                    right_up_bool = False
            else:
                right_up_bool = False

            # diagonal right down
            if right_down_bool and self._diag_right(piece_location, 1):
                if current_row + slide_move_counter >= len(self._board) or \
                        current_col + slide_move_counter >= len(self._board[0]):
                    right_down_bool = False
                elif 2 < current_row + slide_move_counter < 7:
                    right_down_bool = False
                elif not 2 < current_col + slide_move_counter < 6:
                    right_down_bool = False
                elif self._board[current_row + slide_move_counter][current_col + slide_move_counter] is None:
                    move_list.append(self._convert_to_string_location(current_row + slide_move_counter,
                                                                      current_col + slide_move_counter))
                elif self._board[current_row + slide_move_counter][current_col + slide_move_counter].get_color() != piece_color:
                    move_list.append(self._convert_to_string_location(current_row + slide_move_counter,
                                                                      current_col + slide_move_counter))
                    right_down_bool = False
                else:
                    right_down_bool = False
            else:
                right_down_bool = False


            slide_move_counter += 1

        return move_list




    def _diag_left(self, vertex_location, vertical_direction):
        """
        Helper function to determine if a Solider/Chariot/Cannon at the given location
        and with the given vertical_direction (-1 for up, 1 for down) that it moves
        could move diagonally left (along palace diagonal).
        Returns True if so, False otherwise.  Really just checks if there is a line
        diagonally that direction from the given location.
        """
        if vertical_direction > 0:
            if vertex_location in ['f8','e9', 'f1','e2']:
                return True
            return False
        if vertical_direction < 0:
            if vertex_location in ['f3','e2','f10','e9']:
                return True
            return False
        return False

    def _diag_right(self, vertex_location, vertical_direction):
        """
        Helper function to determine if a Solider/Chariot/Cannon at the given location
        and with the given vertical_direction (-1 for up, 1 for down) that it moves
        could move diagonally right (along palace diagonal) in that direction.
        Returns True if so, False otherwise.
        """
        if vertical_direction > 0:
            if vertex_location in ['d8', 'e9','d1','e2']:
                return True
            return False
        if vertical_direction < 0:
            if vertex_location in ['d3', 'e2','d10','e9']:
                return True
            return False
        return False


    def _soldier_moves(self, piece_location, piece_color):
        """
        Takes as a parameter a vertex location in form '[col letter][row num]'
        and a player color and returns a list of possible moves for a soldier
        at the given location of the given color. Considers to make sure
        it does not arrive on a friendly piece when making the list of moves.
        Does not consider check.
        Moves returned in same string location form as locations are inputted.
        """
        move_list = list()
        move_list.append(piece_location)
        #vertical_move used to determine if piece moves up or down the board
        # -1 for up, 1 for down.
        if piece_color == 'blue':
            vertical_move = -1
        else:
            vertical_move = 1
        current_row = int(piece_location[1:]) - 1
        current_col = self._col_conversion[piece_location[0]]
        left_col = current_col - 1
        right_col = current_col + 1
        next_row = current_row + vertical_move

        #move left
        if current_col > 0:
            if self._board[current_row][left_col] is None or \
                self._board[current_row][left_col].get_color() != piece_color:
                    move_list.append(self._convert_to_string_location(current_row, left_col))

        #move right
        if current_col < 8:
            if self._board[current_row][right_col] is None or \
                self._board[current_row][right_col].get_color() != piece_color:
                    move_list.append(self._convert_to_string_location(current_row, right_col))

        #move up
        if vertical_move < 0:
            if current_row > 0:
                if self._board[next_row][current_col] is None or \
                    self._board[next_row][current_col].get_color() != piece_color:
                    move_list.append(self._convert_to_string_location(next_row, current_col))

        #move down
        if vertical_move > 0:
            if current_row < 9:
                if self._board[next_row][current_col] is None or \
                    self._board[next_row][current_col].get_color() != piece_color:
                    move_list.append(self._convert_to_string_location(next_row, current_col))

        #diagonal left
        if self._diag_left(piece_location, vertical_move):
            if self._board[next_row][left_col] is None or \
                    self._board[next_row][left_col].get_color() != piece_color:
                    move_list.append(self._convert_to_string_location(next_row, left_col))

        #diagonal right
        if self._diag_right(piece_location, vertical_move):
            if self._board[next_row][right_col] is None or \
                    self._board[next_row][right_col].get_color() != piece_color:
                    move_list.append(self._convert_to_string_location(next_row, right_col))

        return move_list

    def _guard_moves(self, piece_location, piece_color):
        """
        Takes as a parameter a vertex location in form '[col letter][row num]'
        and a player color and returns a list of possible moves for a guard or general
        at the given location of the given color. Considers to make sure
        it does not arrive on a friendly piece when making the list of moves,
        and that the move would not take it out of the palace.
        Does not consider check.
        Moves returned in same string location form as locations are inputted.
        """
        move_list = list()
        move_list.append(piece_location)
        current_row = int(piece_location[1:]) - 1
        current_col = self._col_conversion[piece_location[0]]

        #For blue guards checks for moves within the blue palace
        if piece_color == 'blue':

            #Iterates through each square in the palace looking to see if moving there
            # would be a valid move
            for row_index in range(7, 10):
                for col_index in range(3, 6):
                    row_dist = abs(row_index - current_row)
                    col_dist = abs(col_index - current_col)
                    if row_dist > 1 or col_dist > 1:
                        continue

                    #Checks each of the non-existent diagonal conditions
                    # and skips this iteration if it would be a move from
                    #  one of the non-diagonal connected squares in a diagonal direction
                    if current_col == 3 and current_row == 8:
                        if row_dist == 1 and col_dist == 1:
                            continue
                    if current_col == 5 and current_row == 8:
                        if row_dist == 1 and col_dist == 1:
                            continue
                    if current_col == 4 and current_row == 7:
                        if row_dist == 1 and col_dist == 1:
                            continue
                    if current_col == 4 and current_row == 9:
                        if row_dist == 1 and col_dist == 1:
                            continue

                    if self._board[row_index][col_index] is None or \
                            self._board[row_index][col_index].get_color() == 'red':
                        move_list.append(self._col_conversion[col_index] + str(row_index + 1))

        # If not blue then it is red and we do the parrallel comparisons within the red palace.
        else:
            for row_index in range(0, 3):
                for col_index in range(3, 6):
                    row_dist = abs(row_index - current_row)
                    col_dist = abs(col_index - current_col)
                    if row_dist > 1 or col_dist > 1:
                        continue
                    if current_col == 3 and current_row == 1:
                        if row_dist == 1 and col_dist == 1:
                            continue
                    if current_col == 5 and current_row == 1:
                        if row_dist == 1 and col_dist == 1:
                            continue
                    if current_col == 4 and current_row == 0:
                        if row_dist == 1 and col_dist == 1:
                            continue
                    if current_col == 4 and current_row == 2:
                        if row_dist == 1 and col_dist == 1:
                            continue
                    if self._board[row_index][col_index] is None or \
                            self._board[row_index][col_index].get_color() == 'blue':
                        move_list.append(self._col_conversion[col_index] + str(row_index + 1))
        return move_list







def main():
    """
    Runs some basic tests and then starts a fresh game which it plays to checkmate.
    Lets you start a new game after you attempt to run make_move again (which is left
    in so that I can check that make_move is not allowing moves to be made once the game
    is finished.
    """

    game = JanggiGame()
    move_result = game.make_move('c1', 'e3')  # should be False because it's not Red's turn
    print(move_result, "should be", False)
    move_result = game.make_move('a7','b7') #should return True
    print(move_result, "should be", True)
    blue_in_check = game.is_in_check('blue')  # should return False
    print(blue_in_check, "should be", False)
    game.make_move('a4', 'a5')  # should return True
    state = game.get_game_state()  # should return UNFINISHED
    print(state, "should be", "UNFINISHED")
    print(game.make_move('b7', 'b6'), True)  # should return True
    print(game.make_move('b3', 'b6'), False)  # should return False because it's an invalid move
    print(game.make_move('a1', 'a4'), True)  # should return True
    print(game.make_move('c7', 'd7'), True)  # should return True
    print(game.make_move('a4', 'a4'), True)  # this will pass the Red's turn and return True
    keep_playing = True
    game = JanggiGame()
    #moving some pieces around
    game.make_move('e9','e8')
    game.make_move('e2','e3')
    game.make_move('f10','e10')
    game.make_move('d1','e1')
    game.make_move('a10','a9')
    game.make_move('a1','a2')
    game.make_move('a9','f9')
    game.make_move('a2','f2')
    #setting up a checkmate
    game.make_move('f9','f2')
    game.make_move('e3','d3')
    game.make_move('f2','f1')
    game.make_move('d3','d2')
    game.make_move('i7','h7')
    game.make_move('i4','h4')
    game.make_move('i10','i2')
    game.make_move('d2','d1')
    game.make_move('h8','d8')
    game.make_move('a4','a5')
    game.make_move('f1','f2')
    game.make_move('e1','f1')
    game.make_move('e7', 'd7')
    game.make_move('c1', 'd3')
    game.make_move('d8', 'i8')
    game.make_move('i1', 'i2')
    game.make_move('f2', 'f4')
    game.make_move('e4', 'f4')
    game.make_move('i8', 'i1')
    game.make_move('h3', 'h7')
    game.make_move('c7', 'c6')
    game.make_move('h7', 'e7')
    game.make_move('c6', 'c5')
    game.make_move('i2', 'i9')
    game.make_move('c5', 'c4')
    game.make_move('e7', 'e10')
    game.make_move('c4', 'c3')
    game.make_move('e10', 'h10')
    game.make_move('c3', 'c2')
    game.make_move('d3', 'e5')
    game.make_move('c2', 'b2')
    game.make_move('e5', 'f7')
    with open('move_save.txt', 'w') as save_file:
        while keep_playing:
            print(game)
            to_move = input("which piece would you like to move? ")
            move_to = input("where would you like to move it to? ")
            if not game.make_move(to_move, move_to):
                print("That is an invalid move. Please select again.")
            else:
                save_file.write("game.make_move('" + to_move + "','" + move_to + "')\n")
            if game.get_game_state() != 'UNFINISHED':
                print("The game is over, with the result:", game.get_game_state())
                play_again = input("Would you like to play again? Anything but 'no' is interpretted as yes:")
                if play_again == 'no':
                    keep_playing = False
                else:
                    game = JanggiGame()
                    print("Let's start a new game, weeeeeee!")


if __name__ == "__main__":
    main()