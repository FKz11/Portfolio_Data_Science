"""
Tic-tac-toe game.
"""
import random


def enter(line):
    data = input(line)
    if line == "Choose difficulty easy/medium/hard or e/m/h\n>>>:":
        if data == "e" or data == "easy" or data == "легко":
            return "easy"
        if data == "m" or data == "medium" or data == "средне":
            return "medium"
        if data == "h" or data == "hard" or data == "сложно":
            return "hard"
    if line == "Enter who goes first bot/player or b/p\n>>>:":
        if data == "p" or data == "player" or data == "игрок":
            return True
        if data == "b" or data == "bot" or data == "бот":
            return False
    if line == "Who do you play x/o\n>>>:":
        if data == "X" or data == "x" or data == "х" or data == "Х":
            return True
        if data == "O" or data == "o" or data == "0" or data == "О" or data == "о":
            return False
    print("Invalid input!!!")
    return enter(line)


class Xo:
    dictionary = {'a': 0, 'b': 1, 'c': 2, '1': 2, '2': 1, '3': 0}

    def __init__(self, level, name, first_move, x_or_o):
        self.level = level
        self.name = name
        self.first_move = first_move
        if x_or_o:
            self.x_or_o_player = 'X'
            self.x_or_o_bot = 'O'
        if not x_or_o:
            self.x_or_o_player = 'O'
            self.x_or_o_bot = 'X'
        self.array = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.free = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']
        self.count_move = 0
        self.win = ''

    def __str__(self):
        result = f'  |-----|-----|-----|\n'
        result += f'3 |  {self.array[0][0]}  |  {self.array[0][1]}  |  {self.array[0][2]}  |\n'
        result += f'  |-----|-----|-----|\n'
        result += f'2 |  {self.array[1][0]}  |  {self.array[1][1]}  |  {self.array[1][2]}  |\n'
        result += f'  |-----|-----|-----|\n'
        result += f'1 |  {self.array[2][0]}  |  {self.array[2][1]}  |  {self.array[2][2]}  |\n'
        result += f'  |-----|-----|-----|\n'
        result += f'     a     b     c'
        return result

    def enter_cell(self):
        result = input("Enter the cell in the format b1\n>>>:")
        if result in self.free:
            return result
        print("The input is incorrect or the cell is already occupied!!!")
        return self.enter_cell()

    def delete_free(self):
        if self.array[0][0] != ' ' and 'a3' in self.free:
            self.free.remove('a3')
        elif self.array[0][1] != ' ' and 'b3' in self.free:
            self.free.remove('b3')
        elif self.array[0][2] != ' ' and 'c3' in self.free:
            self.free.remove('c3')
        elif self.array[1][0] != ' ' and 'a2' in self.free:
            self.free.remove('a2')
        elif self.array[1][1] != ' ' and 'b2' in self.free:
            self.free.remove('b2')
        elif self.array[1][2] != ' ' and 'c2' in self.free:
            self.free.remove('c2')
        elif self.array[2][0] != ' ' and 'a1' in self.free:
            self.free.remove('a1')
        elif self.array[2][1] != ' ' and 'b1' in self.free:
            self.free.remove('b1')
        elif self.array[2][2] != ' ' and 'c1' in self.free:
            self.free.remove('c1')

    def move_player(self):
        cell = self.enter_cell()
        if cell in self.free:
            self.array[self.dictionary[cell[1]]][self.dictionary[cell[0]]] = self.x_or_o_player
            self.free.remove(cell)
        else:
            return self.move_player()

    def move_bot_easy(self):
        cell = random.choice(self.free)
        self.array[self.dictionary[cell[1]]][self.dictionary[cell[0]]] = self.x_or_o_bot
        self.free.remove(cell)

    def move_bot_medium(self):
        flag = True
        i = 0
        x_or_o = self.x_or_o_bot
        while flag and i < 2:
            if self.array[1][0] == ' ' and self.array[1][1] == x_or_o and self.array[1][2] == x_or_o:
                self.array[1][0] = self.x_or_o_bot
                flag = False
            elif self.array[1][0] == x_or_o and self.array[1][1] == ' ' and self.array[1][2] == x_or_o:
                self.array[1][1] = self.x_or_o_bot
                flag = False
            elif self.array[1][0] == x_or_o and self.array[1][1] == x_or_o and self.array[1][2] == ' ':
                self.array[1][2] = self.x_or_o_bot
                flag = False
            elif self.array[0][1] == ' ' and self.array[1][1] == x_or_o and self.array[2][1] == x_or_o:
                self.array[0][1] = self.x_or_o_bot
                flag = False
            elif self.array[0][1] == x_or_o and self.array[1][1] == ' ' and self.array[2][1] == x_or_o:
                self.array[1][1] = self.x_or_o_bot
                flag = False
            elif self.array[0][1] == x_or_o and self.array[1][1] == x_or_o and self.array[2][1] == ' ':
                self.array[2][1] = self.x_or_o_bot
                flag = False
            elif self.array[0][0] == ' ' and self.array[1][1] == x_or_o and self.array[2][2] == x_or_o:
                self.array[0][0] = self.x_or_o_bot
                flag = False
            elif self.array[0][0] == x_or_o and self.array[1][1] == ' ' and self.array[2][2] == x_or_o:
                self.array[1][1] = self.x_or_o_bot
                flag = False
            elif self.array[0][0] == x_or_o and self.array[1][1] == x_or_o and self.array[2][2] == ' ':
                self.array[2][2] = self.x_or_o_bot
                flag = False
            elif self.array[0][2] == ' ' and self.array[1][1] == x_or_o and self.array[2][0] == x_or_o:
                self.array[0][2] = self.x_or_o_bot
                flag = False
            elif self.array[0][2] == x_or_o and self.array[1][1] == ' ' and self.array[2][0] == x_or_o:
                self.array[1][1] = self.x_or_o_bot
                flag = False
            elif self.array[0][2] == x_or_o and self.array[1][1] == x_or_o and self.array[2][0] == ' ':
                self.array[2][0] = self.x_or_o_bot
                flag = False
            elif self.array[0][0] == ' ' and self.array[0][1] == x_or_o and self.array[0][2] == x_or_o:
                self.array[0][0] = self.x_or_o_bot
                flag = False
            elif self.array[0][0] == x_or_o and self.array[0][1] == ' ' and self.array[0][2] == x_or_o:
                self.array[0][1] = self.x_or_o_bot
                flag = False
            elif self.array[0][0] == x_or_o and self.array[0][1] == x_or_o and self.array[0][2] == ' ':
                self.array[0][2] = self.x_or_o_bot
                flag = False
            elif self.array[0][2] == ' ' and self.array[1][2] == x_or_o and self.array[2][2] == x_or_o:
                self.array[0][2] = self.x_or_o_bot
                flag = False
            elif self.array[0][2] == x_or_o and self.array[1][2] == ' ' and self.array[2][2] == x_or_o:
                self.array[1][2] = self.x_or_o_bot
                flag = False
            elif self.array[0][2] == x_or_o and self.array[1][2] == x_or_o and self.array[2][2] == ' ':
                self.array[2][2] = self.x_or_o_bot
                flag = False
            elif self.array[2][0] == ' ' and self.array[2][1] == x_or_o and self.array[2][2] == x_or_o:
                self.array[2][0] = self.x_or_o_bot
                flag = False
            elif self.array[2][0] == x_or_o and self.array[2][1] == ' ' and self.array[2][2] == x_or_o:
                self.array[2][1] = self.x_or_o_bot
                flag = False
            elif self.array[2][0] == x_or_o and self.array[2][1] == x_or_o and self.array[2][2] == ' ':
                self.array[2][2] = self.x_or_o_bot
                flag = False
            elif self.array[0][0] == ' ' and self.array[1][0] == x_or_o and self.array[2][0] == x_or_o:
                self.array[0][0] = self.x_or_o_bot
                flag = False
            elif self.array[0][0] == x_or_o and self.array[1][0] == ' ' and self.array[2][0] == x_or_o:
                self.array[1][0] = self.x_or_o_bot
                flag = False
            elif self.array[0][0] == x_or_o and self.array[1][0] == x_or_o and self.array[2][0] == ' ':
                self.array[2][0] = self.x_or_o_bot
                flag = False
            i += 1
            x_or_o = self.x_or_o_player
        if not flag:
            self.delete_free()
        else:
            self.move_bot_easy()

    def move_bot_hard(self):
        flag = True
        if self.count_move == 0:
            self.array[1][1] = self.x_or_o_bot
            flag = False
        elif self.count_move == 2:
            if self.array[0][1] == self.x_or_o_player or self.array[1][2] == self.x_or_o_player:
                self.array[2][0] = self.x_or_o_bot
                flag = False
            elif self.array[1][0] == self.x_or_o_player or self.array[2][1] == self.x_or_o_player:
                self.array[0][2] = self.x_or_o_bot
                flag = False
            elif self.array[0][0] == self.x_or_o_player:
                self.array[2][2] = self.x_or_o_bot
                flag = False
            elif self.array[0][2] == self.x_or_o_player:
                self.array[2][0] = self.x_or_o_bot
                flag = False
            elif self.array[2][0] == self.x_or_o_player:
                self.array[0][2] = self.x_or_o_bot
                flag = False
            elif self.array[2][2] == self.x_or_o_player:
                self.array[0][0] = self.x_or_o_bot
                flag = False
        elif self.count_move == 4:
            if (self.array[0][0] == self.x_or_o_player and self.array[2][1] == self.x_or_o_player) or (
                    self.array[2][2] == self.x_or_o_player and self.array[1][0] == self.x_or_o_player):
                self.array[0][2] = self.x_or_o_bot
                flag = False
            elif (self.array[0][0] == self.x_or_o_player and self.array[1][2] == self.x_or_o_player) or (
                    self.array[2][2] == self.x_or_o_player and self.array[0][1] == self.x_or_o_player):
                self.array[2][0] = self.x_or_o_bot
                flag = False
            elif (self.array[2][0] == self.x_or_o_player and self.array[0][1] == self.x_or_o_player) or (
                    self.array[0][2] == self.x_or_o_player and self.array[1][0] == self.x_or_o_player):
                self.array[2][2] = self.x_or_o_bot
                flag = False
            elif (self.array[2][0] == self.x_or_o_player and self.array[1][2] == self.x_or_o_player) or (
                    self.array[0][2] == self.x_or_o_player and self.array[2][1] == self.x_or_o_player):
                self.array[0][0] = self.x_or_o_bot
                flag = False
        elif self.count_move == 1:
            if self.array[1][1] == self.x_or_o_player:
                self.array[0][2] = self.x_or_o_bot
                flag = False
            else:
                self.array[1][1] = self.x_or_o_bot
                flag = False
        elif self.count_move == 3:
            if self.array[1][1] == self.x_or_o_player and self.array[2][0] == self.x_or_o_player:
                self.array[0][0] = self.x_or_o_bot
                flag = False
            elif (self.array[0][0] == self.x_or_o_player and self.array[2][2] == self.x_or_o_player) or (
                    self.array[0][2] == self.x_or_o_player and self.array[2][0] == self.x_or_o_player):
                self.array[0][1] = self.x_or_o_bot
                flag = False
            elif (self.array[0][0] == self.x_or_o_player and self.array[2][1] == self.x_or_o_player) or (
                    self.array[2][2] == self.x_or_o_player and self.array[1][0] == self.x_or_o_player) or (
                    self.array[2][1] == self.x_or_o_player and self.array[1][0] == self.x_or_o_player):
                self.array[2][0] = self.x_or_o_bot
                flag = False
            elif (self.array[0][0] == self.x_or_o_player and self.array[1][2] == self.x_or_o_player) or (
                    self.array[2][2] == self.x_or_o_player and self.array[0][1] == self.x_or_o_player) or (
                    self.array[0][1] == self.x_or_o_player and self.array[1][2] == self.x_or_o_player):
                self.array[0][2] = self.x_or_o_bot
                flag = False
            elif (self.array[0][2] == self.x_or_o_player and self.array[2][1] == self.x_or_o_player) or (
                    self.array[2][0] == self.x_or_o_player and self.array[1][2] == self.x_or_o_player) or (
                    self.array[2][1] == self.x_or_o_player and self.array[1][2] == self.x_or_o_player):
                self.array[2][2] = self.x_or_o_bot
                flag = False
            elif (self.array[0][2] == self.x_or_o_player and self.array[1][0] == self.x_or_o_player) or (
                    self.array[2][0] == self.x_or_o_player and self.array[0][1] == self.x_or_o_player) or (
                    self.array[0][1] == self.x_or_o_player and self.array[1][0] == self.x_or_o_player) or (
                    self.array[0][1] == self.x_or_o_player and self.array[2][1] == self.x_or_o_player) or (
                    self.array[1][0] == self.x_or_o_player and self.array[1][2] == self.x_or_o_player):
                self.array[0][0] = self.x_or_o_bot
                flag = False
        if not flag:
            self.delete_free()
        else:
            self.move_bot_medium()

    def win_lose(self):
        if (self.array[0][0] == self.array[0][1] == self.array[0][2] == self.x_or_o_player) or (
                self.array[1][0] == self.array[1][1] == self.array[1][2] == self.x_or_o_player) or (
                self.array[2][0] == self.array[2][1] == self.array[2][2] == self.x_or_o_player) or (
                self.array[0][0] == self.array[1][0] == self.array[2][0] == self.x_or_o_player) or (
                self.array[0][1] == self.array[1][1] == self.array[2][1] == self.x_or_o_player) or (
                self.array[0][2] == self.array[1][2] == self.array[2][2] == self.x_or_o_player) or (
                self.array[0][0] == self.array[1][1] == self.array[2][2] == self.x_or_o_player) or (
                self.array[2][0] == self.array[1][1] == self.array[0][2] == self.x_or_o_player):
            self.win = self.name
            return True
        if (self.array[0][0] == self.array[0][1] == self.array[0][2] == self.x_or_o_bot) or (
                self.array[1][0] == self.array[1][1] == self.array[1][2] == self.x_or_o_bot) or (
                self.array[2][0] == self.array[2][1] == self.array[2][2] == self.x_or_o_bot) or (
                self.array[0][0] == self.array[1][0] == self.array[2][0] == self.x_or_o_bot) or (
                self.array[0][1] == self.array[1][1] == self.array[2][1] == self.x_or_o_bot) or (
                self.array[0][2] == self.array[1][2] == self.array[2][2] == self.x_or_o_bot) or (
                self.array[0][0] == self.array[1][1] == self.array[2][2] == self.x_or_o_bot) or (
                self.array[2][0] == self.array[1][1] == self.array[0][2] == self.x_or_o_bot):
            self.win = 'Bot'
            return True
        return False

    def play(self):
        move_bot = self.move_bot_easy
        if self.level == "easy":
            move_bot = self.move_bot_easy
        if self.level == "medium":
            move_bot = self.move_bot_medium
        if self.level == "hard":
            move_bot = self.move_bot_hard
        print(f"---------{self.name} vs bot----move {self.count_move}---------")
        print(self.__str__())
        print("----------------------------------------")
        if not self.first_move:
            move_bot()
            self.count_move += 1
            print(f"---------{self.name} vs bot----move {self.count_move}---------")
            print(self.__str__())
            print("----------------------------------------")
        while True:
            self.move_player()
            self.count_move += 1
            print(f"---------{self.name} vs bot----move {self.count_move}---------")
            print(self.__str__())
            print("----------------------------------------")
            if self.win_lose() or self.count_move == 9:
                break
            move_bot()
            self.count_move += 1
            print(f"---------{self.name} vs bot----move {self.count_move}---------")
            print(self.__str__())
            print("----------------------------------------")
            if self.win_lose() or self.count_move == 9:
                break
        if self.win == '':
            print("Draw!!!")
        else:
            print(f'{self.win} won!!!')
        return True


q = 0
games = []
while True:
    origin_level = enter("Choose difficulty easy/medium/hard or e/m/h\n>>>:")
    origin_name = input("Enter a name\n>>>:")
    origin_first_move = enter("Enter who goes first bot/player or b/p\n>>>:")
    origin_x_or_o = enter("Who do you play x/o\n>>>:")
    games.append(Xo(origin_level, origin_name, origin_first_move, origin_x_or_o))
    games[q].play()
    q += 1
