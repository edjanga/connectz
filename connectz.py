"""
    Custom Errors used in the Game class
"""
class ColumnError(Exception):
    pass
class RowError(Exception):
    pass
class IllegalGameError(Exception):
    pass
class OutOfFrameError(Exception):
    pass

class Game:
    """
        Class attribute (shared across all Game instances)
    """
    counter_type_dd = {0:'X',1:'O'}

    def __init__(self,filename):
        """
            Series of tags used to check whether files are conform
        """
        self.valid_file = True
        self.valid_col = True
        self.valid_row = True
        self.legal_game = True
        """
            List used to store the sequence of moves.
        """
        sequence_move_ls = []
        with open(filename,'r') as f:
            for line in f:
                parse_line = line.rstrip()
                if len(parse_line)>2:
                    """
                        Handling files that contain non-integers values 
                    """
                    try:
                        description_ls = [int(info) for info in parse_line.split(' ')]#[1:]
                    except ValueError:
                        self.valid_file = False
                        break
                    else:
                        """
                            Storing game info in a tuple to make sure they cannot be altered
                        """
                        self.game_description = (description_ls[0],description_ls[1],description_ls[-1])
                        """
                            Check for illegal games, i.e. if target lines > col or target lines > row
                        """
                        try:
                            if (self.game_description[0]<self.game_description[-1])|\
                                (self.game_description[1]<self.game_description[-1]):
                                raise IllegalGameError
                        except:
                            self.legal_game = False
                            break
                else:
                    try:
                        """
                            Handling invalid columns in files.
                        """
                        if int(parse_line)>description_ls[1]:
                            raise ColumnError
                        sequence_move_ls.append(int(parse_line.replace(' ','')))
                    except ColumnError:
                        self.valid_col = False
                        break
                    except UnboundLocalError:
                        """
                            description_ls not defined as process does define if the file is invalid
                            self.valid_file --> False
                        """
                        self.valid_file = False
                        break
        """
            Add row to each move to locate each counter in the frame (row,col)
        """
        if self.valid_file&self.valid_col&self.legal_game:
            location_dd = {}
            location_ls = []
            for idx,move in enumerate(sequence_move_ls):
                if move not in location_dd.keys():
                    location_dd.setdefault(move,1)
                else:
                    location_dd[move] += 1
                location_ls.append((location_dd[move],move))
            """
                If any column (key) has a value greater than the row given in the game description,
                this means that particular column is full but a player has tried to drop a counter in that column.
                Invalid row if invalid_rows_dd is empty.
            """
            invalid_rows_dd = {col:number_of_rows for col,number_of_rows in location_dd.items() if number_of_rows\
                               > description_ls[0]}
            if invalid_rows_dd:
                self.valid_row = False
            if self.valid_row:
                self.moves_rows = [location[0] for location in location_ls]
                self.moves_cols = [location[-1] for location in location_ls]
                """
                    Dictionary as it allows to access any values in constant time O(1) using a key.
                    Key: column index
                    Value: list 
                """
                self.frame = {key:[] for key in range(0,self.game_description[0])}
                """
                    Tag to keep track of remaining moves to be played (used for handling illegal continue)
                    Initialise to len of moves and decreased each time a player drops a counter
                """
                self.remaining_counters = len(self.moves_cols)


    def player(self,idx):
        """
            Method returning 0 for Player1 or 1 for Player 2
        """
        return idx%2

    def vertical_check(self,player_idx,col):
        """
            Check whether one player has piled up target line counters.
        """
        count = 0
        reverse_col = self.frame[col-1][::]
        reverse_col.reverse()
        """
            Iterate through the current column.
            As soon as the counter is different from the player's counter --> break and return False
            As soon as the number of consecutive counters has reached target line number --> break and return True
        """
        for idx,counter in enumerate(reverse_col):
            if counter == Game.counter_type_dd[self.player(player_idx)]:
                count += 1
            else:
                break
            if count == self.game_description[-1]:
                return True
                break
        return False

    def horizontal_check(self,player_idx,row):
        """
            Check whether one player has lined up target line counters horizontally.
        """
        count = 0
        reverse_row = []
        for col,counters_ls in self.frame.items():
            """
                Error handling need as counters may not be adjacent to each other.
                Fill the gaps with None.
            """
            try:
                reverse_row.append(counters_ls[row-1])
            except IndexError:
                reverse_row.append(None)
        """
            Iterate through the current column.
            As soon as the counter is different from the player's counter --> break and return False
            As soon as the number of consecutive counters has reached target line number --> break and return True
        """
        for idx,counter in enumerate(reverse_row):
            if counter == Game.counter_type_dd[self.player(player_idx)]:
                count += 1
            if count == self.game_description[-1]:
                return True
                break
        return False

    def diagonal_check_1(self,player_idx,col_idx,row_idx):
        """
            Check whether one player has lined up target line counters from South West to North East.
        """
        diagonal_ls = []
        diagonal_tag = (col_idx-1)-(row_idx-1)
        for col,counters_ls in self.frame.items():
            try:
                if(col-diagonal_tag)<0:
                    raise OutOfFrameError
                diagonal_ls.append(counters_ls[col-diagonal_tag])
            except IndexError:
                diagonal_ls.append(None)
            except OutOfFrameError:
                diagonal_ls.append(None)
        """
            Iterate through the current column.
            As soon as the counter is different from the player's counter --> break and return False
            As soon as the number of consecutive counters has reached target line number --> break and return True
        """
        count = 0
        for counter in diagonal_ls:
            if counter == Game.counter_type_dd[self.player(player_idx)]:
                count += 1
            if count == self.game_description[-1]:
                return True
        return False

    def diagonal_check_2(self,player_idx,col_idx,row_idx):
        """
            Check whether one player has lined up target line counters from South East to North West.
        """
        diagonal_ls = []
        diagonal_tag = (col_idx-1)+(row_idx-1)
        # for col,counters_ls in self.frame.items():
        #     try:
        #         diagonal_ls.append(counters_ls[diagonal_tag-col])
        #     except IndexError:
        #         diagonal_ls.append(None)
        for col,counters_ls in self.frame.items():
            try:
                if(col-diagonal_tag)<0:
                    raise OutOfFrameError
                if diagonal_tag > self.game_description[1]:
                    raise OutOfFrameError
                diagonal_ls.append(counters_ls[diagonal_tag-col])
            except IndexError:
                diagonal_ls.append(None)
            except OutOfFrameError:
                diagonal_ls.append(None)

        """
            Iterate through the current column.
            As soon as the counter is different from the player's counter --> break and return False
            As soon as the number of consecutive counters has reached target line number --> break and return True
        """
        count = 0
        for counter in diagonal_ls:
            if counter == Game.counter_type_dd[self.player(player_idx)]:
                count += 1
            if count == self.game_description[-1]:
                return True
        return False

    def drop_counter(self,player_idx,col):
        """
            Player 1: X (even index)
            Player 2: O (odd index)
        """
        if player_idx==0:
            self.frame[col-1].append('X')
        else:
            self.frame[col-1].append('O')

    def is_full(self):
        """
            Check whether frame is full.
        """
        for key,col in self.frame.items():
            if len(col)!=self.game_description[1]:
                return False
                break
        return True

    def run_game(self):
        """
            Check if file is valid
        """
        if not self.valid_file:
            return 8

        if not self.valid_col:
            return 6

        if not self.valid_row:
            return 5

        if not self.legal_game:
            return 7
        """
            Tag needed to determine whether someone has won the game.
        """
        winner = False
        for idx,col in enumerate(self.moves_cols):
            """
                Player drops a counter iteratively in a given column.
            """
            #print(f'Player {self.player(idx)+1} drops a counter in {col}th column.')
            self.drop_counter(self.player(idx),col)
            self.remaining_counters -= 1
            """
                Check whether a player has lined up a target line amount of
                counters (vertically, horizontally or diagonally)
                Returns Player's id if no counters left otherwise an illegal continue has been caught
            """
            if self.horizontal_check(self.player(idx),self.moves_rows[idx]):
                winner = True
                if winner & (self.remaining_counters==0):
                    return self.player(idx)+1
                if winner & (self.remaining_counters!=0):
                    return 4
                break
            if self.vertical_check(self.player(idx),self.moves_cols[idx]):
                winner = True
                if winner & (self.remaining_counters == 0):
                    return self.player(idx) + 1
                if winner & (self.remaining_counters != 0):
                    return 4
                break
            if self.diagonal_check_1(self.player(idx),self.moves_cols[idx],self.moves_rows[idx]):
                winner = True
                if winner & (self.remaining_counters == 0):
                    return self.player(idx) + 1
                if winner & (self.remaining_counters != 0):
                    return 4
                break
            if self.diagonal_check_2(self.player(idx),self.moves_cols[idx],self.moves_rows[idx]):
                winner = True
                if winner & (self.remaining_counters == 0):
                    return self.player(idx) + 1
                if winner & (self.remaining_counters != 0):
                    return 4
                break

        """
            If frame is full and no one has won --> draw
        """
        if (self.is_full())&(not winner):
            return 0

        """
            If frame is not full and no one has won --> incomplete
        """
        if (not self.is_full()) & (not winner):
            return 3

    def print_frame(self):
        for key,column in self.frame.items():
            print(column)


if __name__ == '__main__':
    filename = 'test_case/test0.txt'
    game_obj = Game(filename)
    print(game_obj.run_game())