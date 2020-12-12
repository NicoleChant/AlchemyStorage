####This is a Heroine Project    v.0
import random

class Item():
    '''A shiny item.'''
    _allowed_keys_list = ['health','armor','dmg','speed','crit'
        ,'crit_dmg','rg','arpen','agility','intelligence'
        ,'strength','mana','mana_rg','cost','miss','description']

    all_items = {}
    db = 'Created_Items_db.txt'

    def __init__(self,name,**kwargs):
        self.name = name
        if len(kwargs)>=1:
            dropped_arg = {}
            for key in kwargs.keys():
                if key.strip() in Item._allowed_keys_list:
                    self.__setattr__(key.strip(),kwargs[key])
                else:
                    dropped_arg[key.strip()] = kwargs[key]
            if len(dropped_arg)>=1:
                print("Warning! The following arguments were not used in the item's creation: ")
                for key,values in dropped_arg.items():
                    print(f'{key.strip()} = {values}',end="\n")
        Item.all_items[self.name] = self

    @staticmethod
    def show_items():
        for item in sorted(Item.all_items):
            print(Item.all_items[item])

    @staticmethod
    def store_data():
        headers = 'items_name'+','
        for key in sorted(Item._allowed_keys_list):
            headers += key + ','
        headers = headers[:-1]
        with open(Item.db,'w') as file:
              file.write(headers+'\n')
              for item_name in Item.all_items:
                  data = f'{item_name}' + ','
                  for key in sorted(Item._allowed_keys_list):
                      if key in Item.all_items[item_name].__dict__.keys():
                           data += str(Item.all_items[item_name].__dict__[key])
                      else:
                           data += '0'
                      data += ','
                  data = data[:-1] + '\n'
                  file.write(data)

    @staticmethod
    def retrieve_data():
        pass


    def __repr__(self):
        s = f'{self.name}\n'
        for key,value in self.__dict__.items():
               s += f'{key} : \t {value} \n'
        return s[:-1]

class Unit(Item):
    '''This is a unit class.'''
    all_units = {}

    def __init__(self,name,health,armor,damage,critical):
        self.name = name
        self.health = float(health)
        self.armor = float(armor)
        self.damage = float(damage)
        self.stats = {'Name':self.name,
                      'Health':self.health,
                      'Armor':self.armor,
                      'Damage':self.damage,
                      'Critical':self.critical}
        self.items = []
        Unit.all_units[self.name] = self

    def acquire_item(self,new_item):
            if type(new_item)==Item:
                self.items.append(new_item)
            else:
                return 'Cannot pick this item.'
            for attr in Item._allowed_keys_list:
                pass

    def __repr__(self):
        return self.name

class Hero(Unit):
    '''Hero Class'''
    max_level = 25
    all_heroines = {}

    def __init__(self,unit,agility,strength,intelligence):
        self.unit = unit
        self.agility = int(agility)
        self.strength = int(strength)
        self.intelligence = int(intelligence)
        self.level = 1
        Hero.all_heroines[self.name] = self

    def level_up(self,n=1):
          if self.level+n<=Hero.max_level:
              self.level += n
              return f'{self.name} levels up to {self.level}!'
          else:
              if self.max_level(): return f'{self.name} is already at maximum level!'
              return f'{self.name} cannot level up {n} times.'

    def max_level(self):
        return True if self.level == Hero.max_level else False


class Main():
    '''Main Program.'''

    @staticmethod
    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def __init__(self):
            s = 'Enter item name & stats: name = , health = , armor = , dmg = ...'
            #_attributes = {key : None for key in Item._allowed_keys_list}
            while True:
                user_input = input("""Number of Items {:d}. Press: 
                (+) to enter an item
                (-) to delete an item
                (?) to overview existing items
                (??) to search (by name) if a specified item exists
                (enter)to exit the program.""".format(len(Item.all_items))).strip()

                if user_input == '+':
                    item_stats = input(s).strip()
                    if ',' in item_stats:
                        item_stats = item_stats.split(',')
                        all_stats = dict()
                        name = item_stats[0].split('=')[1].strip()
                        for stat in item_stats[1:]:
                            if stat.count('=') == 1:
                                print(Main.isfloat(stat.split('=')[1].strip()))
                                if Main.isfloat(stat.split('=')[1].strip()):
                                    all_stats.update({stat.split('=')[0].strip() : stat.split('=')[1].strip()})
                            print(all_stats)
                        try:
                            Item(name,**all_stats)
                        except IndexError:
                            print('Incorrect data.')
                    else:
                        try:
                            Item(item_stats.split('=')[1].strip())
                        except IndexError:
                            print('Incorrect data.')
                elif user_input == '-':
                    item_name = input('Enter the name of the item: ').strip()
                    try:
                        del Item.all_items[item_name]
                    except KeyError:
                        print(f"Item deletion was unsuccesful.\n The given name \"{item_name}\" doesn\'t exist.")
                elif user_input == "?":
                    Item.show_items()
                elif user_input == "??":
                    item_name = input('Enter the name of the item: ').strip()
                    if item_name in Item.all_items:
                        print(Item.all_items[item_name])
                    else:
                        print(f'Search results: Item {item_name} not found.')
                elif user_input == "": break
                else:
                    print('Please enter a valid command.')
                    continue
            Item.store_data()

if __name__ == "__main__": Main()