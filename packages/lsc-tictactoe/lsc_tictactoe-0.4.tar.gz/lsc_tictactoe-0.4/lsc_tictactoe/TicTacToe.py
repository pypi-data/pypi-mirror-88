class TicTacToe:
    
    def __init__(self):
        self.board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.win_condition = ((1, 2, 3), (4, 5, 6), (7, 8, 9),
                              (1, 4, 7), (2, 5, 8), (3, 6, 9),
                              (1, 5, 9), (3, 5, 7))
        self.moves_count = 0
        
    def create_board(self):
        print()
        print(self.board[0], self.board[1], self.board[2])
        print(self.board[3], self.board[4], self.board[5])
        print(self.board[6], self.board[7], self.board[8])
        print()
        
    def p1(self):
        try:
            print("Player 'X'")
            position = int(input("Type the position where 'X' is placed. \n"))
            if self.board[position-1] != 'X' and self.board[position-1] != '0':
                self.board[position-1] = 'X'
                self.create_board()
                self.moves_count += 1
            else:
                print("The position is already taken, please select another cell.")
                self.p1()
            self.check_win()
        except ValueError:
            print("Write a number from 1 to 9")
            self.p1()
            
    def p2(self):
        try:
            print("Player '0'")
            position = int(input("Type the position where '0' is placed. \n"))
            if self.board[position-1] != 'X' and self.board[position-1] != '0':
                self.board[position-1] = '0'
                self.create_board()
                self.moves_count += 1
            else:
                print("The position is already taken, please select another cell.")
                self.p2()
            self.check_win()
        except ValueError:
            print("Write a number from 1 to 9")
            self.p2()
            
    def check_win(self):
        for win in self.win_condition:
            if self.board[win[0]-1] == self.board[win[1]-1] == self.board[win[2]-1] == 'X':
                print("Player 'X' wins.")
                self.play_again()
            elif self.board[win[0]-1] == self.board[win[1]-1] == self.board[win[2]-1] == '0':
                print("Player '0' wins.")
                self.play_again()
            elif self.moves_count == 9:
                print("A draw.")
                exit()
                
    def play(self):
        while True:
            self.p1()
            self.p2()
    
    def run(self):
        self.create_board()
        self.play()
        
    def play_again(self):
        import sys
        
        while True:
            question = input("Do you want to play again?\n Type y or n \n")
            if question == 'y':
                print("Good luck! Have fun!")
                self.moves_count = 0
                self.board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                self.run()
            elif question == 'n':
                print("See you next time!")
                sys.exit()
            else:
                print("That's not a valid answer.")
             
ttt = TicTacToe()
ttt.run()
   