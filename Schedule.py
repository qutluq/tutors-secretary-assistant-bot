from tabulate import tabulate
import pandas as pd

class Schedule:
    
    def __init__(self):
        
        self._df = pd.read_csv('data/schedule.csv', index_col = 'time', dtype=object)
        self._df.fillna(0, inplace=True)
        self._df = self._df.astype(int)
    
    def print(self):
        
        print(tabulate(self._df.replace(0,''), headers='keys', tablefmt='grid'))
    
    def get_schedule(self, numbers_str):
        ''' 
        Convert string of numbers to the list of hours from schedule.
        e.g. numbers_str = '3, 5'
        Returns tuple: (success->bool, schedule->str)
        '''
        df = self._df
        schedule = []
        success  = True
        numbers_str = numbers_str.strip(',')
        try:
            numbers = [int(n) for n in numbers_str.split(',')]
            for n in numbers:
                
                if df.eq(n).any().any():
                    # number exists in df
                    # r,c are chosen number's row and column in df
                    r, c = df.index[df.eq(n).any(1)].values[0], df.columns[df.eq(n).any(0)].values[0]
                    schedule.append((r, c))
                else:
                    print(f'Номера {n} нет в таблице.')
                    success = False
                    
        except Exception as e:
                
            if isinstance(e, ValueError):
                print('Неправильный формат.')
                
            success = False

        return success, str(schedule)