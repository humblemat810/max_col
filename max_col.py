import sys
from itertools import cycle
class Table():
    def __init__(self, n_col):
        self.width = 0
        self.reset(n_col)
        self.update()
        self.n_row = 0
        pass
    def reset(self, n_col):
        assert n_col > 0
        self.columns = [Column(self, False) for i in range(n_col-1)]
        self.columns.append(Column(self, True))
        
    def update(self):
        self.width = sum(i.get_width() for i in self.columns)
        
    def read(self, limit: int, ls_str)-> bool: # success or not
        i = 0
        while self.width < limit:
            for col in self.columns:
                if i == len(ls_str):
                    return True
            
                col.read_row(i, ls_str)
                i += 1
            self.n_row += 1
        return False
    def print_table(self, ls_words):
        col_iter = cycle(self.columns)
        cnt = 0
        for word, col in zip(ls_words, col_iter):
            col.print_word(word)
            
            cnt+=1
            if cnt == len(self.columns):
                cnt -= len(self.columns)
                print()

class Column():
    def __init__(self, table: Table, is_last_col: bool):
        self.__width = 0
        self.is_last_col = is_last_col
        self.table = table

    def read_row(self, i, ls_strings):
        l = len(ls_strings[i])
        if not self.is_last_col: 
            l += 1
        if l > self.__width:
            self.update(new_l = l)
        

    def update(self, new_l):
        self.__width = new_l
        self.table.update()
        

    def get_width(self): # space packed width (no pad for last col)
        if self.is_last_col:
            return(self.__width + 1)
        else: 
            return self.__width
    
    def print_word(self, word):
        print(word + ' '* (self.get_width() - len(word)), end= '')

def get_initial_guess(input_ls_str, limit):
    total = -1
    n_col_start_with = 0
    for word in input_ls_str:
        if total + 1 + len(word) <= limit:
            total+= 1 + len(word)
            n_col_start_with += 1
        else:
            break
    return n_col_start_with


if __name__ == "__main__":
    
    limit = int(sys.argv[1])
    input_ls_str = sys.argv[2:]
    trial_n_col  = get_initial_guess(input_ls_str, limit)

    while trial_n_col > 0:
        myTable =Table(n_col = trial_n_col)
        if myTable.read(ls_str = input_ls_str, limit = limit) is False:
        
            trial_n_col-=1
            
        else:
            print(f'answer is {trial_n_col}')
            myTable.print_table(input_ls_str)
            break
    else:
        print('no solution')
    
    