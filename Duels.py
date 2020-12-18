###Duelist Class
###Nicole Chant
import random
import matplotlib.pyplot as plt

class Duelist():
    '''A duelist'''
    _allowed_key_values = ['health','dmg','std','crit','critdmg','arpen','miss','armor','rg']
    all_duelists = {}
    dead_duelists = {}
    alive_duelists = {}

    def __init__(self,name,health = 300 , **kwargs):
        self.name = name
        self.health = float(health)
        self.max_health = self.health
        print(kwargs)
        if len(kwargs)>=1:
            dropped_keys = {}
            for key in kwargs.keys():
                if key.strip() in Duelist._allowed_key_values:
                    try:
                        self.__setattr__(key.strip(),float(kwargs[key]))
                    except TypeError as er:
                        print(er)
                        print('Something went wrong...')
                else:
                    dropped_keys[key.strip()] = kwargs[key]
            if len(dropped_keys)>=1:
                print("Warning! The following arguments were not used in the item's creation: ")
                for key, values in dropped_keys.items():
                         print(f'{key.strip()} = {values}', end="\n")
        Duelist.all_duelists[self.name] = self
        Duelist.alive_duelists[self.name] = self
        self.items = []
        #self.alive = self.is_alive()

    def is_alive(self):
        '''Returns True if a unit is alive.'''
        return False if self.health<=0 else True

    def resurrect(self,pool):
        '''Resurrects a dead unit.'''
        if not self.is_alive():
            self.health = pool
            del Duelist.dead_duelists[self.name]
            Duelist.alive_duelists[self.name] = self
            print(f'{self.name} has been resurrected with health pool {self.health}.')
        else:
            print(f'Cannot resurrect a living unit. {self.name} is alive: \"{self.is_alive()}\".')

    def takes_pure_dmg(self):
        '''Returns True if a unit has armor.'''
        return True if 'armor' not in self.__dict__.keys() else False

    def is_wielding_weapon(self):
        '''Returns True if the Duelist has specified damage statistics (mean & standard deviation). Else returns False.'''
        return True if ('dmg' in self.__dict__.keys()) & ('std' in self.__dict__.keys()) else False

    def attack(self):
        '''Returns an amount of induced damage.'''
        if not self.is_alive(): return f"Unit unable to attack. Duelist {self.name} status: \"Dead\"."
        if not self.is_wielding_weapon(): return f"Duelist {self.name} cannot attack without a weapon."
        return random.gauss(self.__dict__['dmg'] , self.__dict__['std'])


    def attacked_by(self,other):
        '''Decreases the health of the duelist whenever receiving an enemy hit.'''
        if not self.is_alive(): return f"Cannot attack a dead unit. Duelist {self.name} status: \"Dead\"."
        if not self.takes_pure_dmg():
            try:
                damage = float((1 - Duelist.armor(self.__dict__['armor']))*other.attack())*self.miss_me()*(1+self.crit_me())
                self.health -= damage
                #if not self.is_alive():
                #    Duelist.dead_duelists[self.name] = self
                #    del Duelist.alive_duelists[self.name] #TODO
                return damage
            except ValueError as er:
                print(er)
                print(f"Duelist {other.name} cannot attack without a weapon.")
        else:
            damage = self.miss_me()*other.attack()*(self.crit_me()+1)
            self.health -= damage
            return damage

    def can_crit(self):
        '''Returns True if duelist can crit.'''
        expr = ('crit' in self.__dict__.keys()) & ('critdmg' in self.__dict__.keys())
        if expr:
            expr2 = ( self.__dict__['crit'] <=1) & (self.__dict__['crit']>=0) & (self.__dict__['critdmg']>=0) & (self.__dict__['critdmg']<=1)
            return True if expr2 else False
        return False

    def crit_me(self):
        '''critical strike!'''
        if self.can_crit(): return float(self.__dict__['critdmg']) if random.random()<=self.__dict__['crit'] else 0
        return 0

    def can_miss(self):
        '''Returns True if duelist can miss.'''
        return True if 'miss' in self.__dict__.keys() else False

    def miss_me(self):
        '''evasion'''
        if self.can_miss(): return 0 if random.random()<=float(self.__dict__['miss']) else 1
        return 1

    def score(self):
        pass            #TODO

    def death_risk(self):
        '''Risk of dying function evaluator. Perhaps should move to the Arena class...'''
        pass            #TODO

    @staticmethod
    def exists(name):
        return True if name in Duelist.all_duelists else False

    @staticmethod
    def show():
        print("Duelists: ")
        for duelist_name in sorted(Duelist.all_duelists):
            print(Duelist.all_duelists[duelist_name])

    @staticmethod
    def armor_pen(p,a=1,K=100):
         '''The armor penetration function.'''
         return (p**a)/(p**a+K)

    @staticmethod
    def armor(a,p=1,K=100):
        '''The armor function.'''
        return (a**p)/(a**p+K)

    @staticmethod
    def store_data():
        pass #TODO

    def __repr__(self):
        s = f'Duelist {self.name}\n'
        for key , value in self.__dict__.items():
            s += f'{key} : \t {value}\n'
        s += f'Is alive: {self.is_alive()}\n'
        return s

class Arena(Duelist):
    '''A Duel Arena.'''
    def __init__(self,duelist1,duelist2):
        self.duelist1 = duelist1
        self.duelist2 = duelist2

    def sequential_duel(self,revive=True):
        if (not self.duelist1.is_alive()) | (not self.duelist2.is_alive()):
            return f"""Duelist {self.duelist1.name} status: {self.duelist1.is_alive()}. 
                     Duelist {self.duelist1.name} status: {self.duelist1.is_alive()}.
                     Dead duelists can\'t compete."""
        health1 = self.duelist1.health
        health2 = self.duelist2.health
        duelists = [(self.duelist1, health1), (self.duelist2, health2)]
        tod1 = {'0':health1}
        tod2 = {'0':health2}
        key = 0
        while True:
            duelists[(key+1)%2][0].attacked_by(duelists[key%2][0])
            key +=1
            tod1[str(key)] = self.duelist1.health
            tod2[str(key)] = self.duelist2.health
            if not duelists[key%2][0].is_alive():
                winner = duelists[(key+1)%2][0]
                break
        if revive:
            #self.duelists[key%2].resurrect(duelists[key%2][1])
            duelists[key%2][0].health = duelists[key%2][1]
            duelists[(key+1)%2][0].health = duelists[(key+1)%2][1]
        return {f"{self.duelist1.name}":tod1,f"{self.duelist2.name}":tod2}  #returns duel information (which round the duel ended)


    def simultaneous_duel(self):
        if (not self.duelist1.is_alive()) | (not self.duelist2.is_alive()): return f"""Duelist {self.duelist1.name} status: {self.duelist1.is_alive()}. 
                     Duelist {self.duelist1.name} status: {self.duelist1.is_alive()}.
                     Dead duelists can\'t compete."""
        health1 = self.duelist1.health
        health2 = self.duelist2.health
        key = 0
        #TODO

    def many_sequential(self,N):
        M = N
        records = dict()
        while M>0:
            results = self.sequential_duel()
            records.update({N-M+1:results})
            M -=1
        return records

    def many_simultaneous(self,N):
        pass #TODO

    def is_victorious(self):
        tod1 = list(list(self.sequential_duel().values())[0].values())[-1]
        if tod1<=0: return self.duelist2
        return self.duelist1

    def duel_stats(self):
        all = self.sequential_duel()
        keys = list(list(all.values())[0].keys())
        keys = list(map(lambda x: int(x),keys))
        print(keys)
        print(list(list(all.values())[0].values()))
        print(list(list(all.values())[1].values()))
        plt.plot(keys, list(list(all.values())[0].values()) , color='red')
        plt.plot(keys, list(list(all.values())[1].values()) , color='blue')
        plt.xlabel('rounds')
        plt.ylabel('healthpool')
        plt.xticks(keys)
        plt.title(f'sequential duel {self.duelist1.name} vs. {self.duelist2.name}')
        plt.legend([f'{self.duelist1.name}',f'{self.duelist2.name}'],loc=0)
        plt.tight_layout()
        plt.grid()
        plt.show()
        return all


    @staticmethod
    def store():
        pass     #TODO

    def __repr__(self):
        return f"An arena simulation with two duelists. Duelists: \n {self.duelist1} \n {self.duelist2}"

class Main():
    '''main class'''

    @staticmethod
    def is_float(num):
        try:
            float(num)
            return True
        except:
            return False

    def __init__(self):
         print("Allowed Duelist attributes: ")
         for key in Duelist._allowed_key_values:
                      print(key)
         print()
         while True:
                user_input = input("""Number of active Duelists: {:d}. Press: 
                                (+) to create a duelist,
                                (-) to delete a duelist,
                                (r) to resurrect a duelist,
                                (?) to overview duelists and their respective scores,
                                (??) to search if a duelist exists,
                                (a) enter arena mode,
                                (s) to show statistics,
                                (enter) to exit.""".format(len(Duelist.all_duelists))).strip()
                if user_input == '+':
                            duel_stats = input("""Enter duelist name and stats. Use expressions of the form: 
                                               \'name = Hermes, health = 250\' etc.""").strip()
                            if ',' in duel_stats:
                                      duel_stats = duel_stats.split(',')
                                      if duel_stats[0].count('=')==1:
                                              name = duel_stats[0].split('=')[1].strip()
                                      else:
                                              name = duel_stats[0].strip()
                                      all_stats = dict()
                                      for stat in duel_stats[1:]:
                                               if stat.count('=')==1:
                                                   if Main.is_float(stat.split("=")[1].strip()):
                                                         all_stats.update({stat.split('=')[0].strip() : stat.split('=')[1].strip()})
                                      try:
                                               Duelist(name,**all_stats)
                                      except IndexError:
                                               print("Incorrect data type.")
                            else:
                                      if duel_stats.count('=')==1:
                                             try:
                                                Duelist(duel_stats.split('=')[1].strip())
                                             except IndexError:
                                                print("Incorrect data type.")
                                      else:
                                             try:
                                                Duelist(duel_stats)
                                             except IndexError:
                                                 print("Incorrect data type.")
                elif user_input == "?":
                         Duelist.show()
                elif user_input == "??":
                         duelist_name = input("Enter the name of the duelist.").strip()
                         if duelist_name in Duelist.all_duelists[duelist_name]:
                                  print(Duelist.all_duelists[duelist_name])
                         else:
                                  print(f"Search: Item not found. There doesn\'t exist a duelist named \'{duelist_name}\'.")
                elif user_input == "-":
                            duelist_name = input("Enter the name of the duelist to be deleted.").strip()
                            try:
                                del Duelist.all_duelists[duelist_name]
                            except KeyError as er:
                                        print(er)
                                        print(f"Deletion unsuccesful. There doesn\'t exist a duelist named \"{duelist_name}\".")
                elif user_input == "a":
                            while True:
                                     single = input("""Enter: \n
                                                (S) for single player, \n
                                                (M) for multiplayer, \n
                                                (<) to return to start.""").strip()
                                     if single == 'S':
                                            name = input("Enter the name of the duelist.").replace(" ","")
                                            if Duelist.exists(name):
                                                duelist = Duelist.all_duelists[name]
                                                if not duelist.is_alive():
                                                    print(f'Duelist {duelist.name} is not alive. Try to resurrect this duelist before the duel.')
                                                    continue
                                                while True:
                                                    action = input("""Press: \n
                                                    (A) to produce an attack, \n
                                                    (<) to return back.""").strip()
                                                    if action == "A":
                                                        print(duelist.attack())
                                                    elif action =="<":
                                                        break
                                                    else: print("Invalid argument.")
                                     elif single == 'M':
                                             choice = input("Enter the name of two duelists: \nName1,Name2.").strip().split(',')
                                             name1 = choice[0].strip()
                                             name2 = choice[1].strip()
                                             if Duelist.exists(name1) & Duelist.exists(name2):
                                                 duelist1 = Duelist.all_duelists[name1]
                                                 duelist2 = Duelist.all_duelists[name2]
                                                 if not duelist1.is_alive():
                                                     print(f"Duelist status: {duelist1.is_alive()}.\n Try to resurrect a duelist before combat.")
                                                     continue
                                                 if not duelist2.is_alive():
                                                     print(f"Duelist status: {duelist2.is_alive()}.\n Try to resurrect a duelist before combat.")
                                                     continue
                                                 arena = Arena(duelist1, duelist2)
                                                 while True:
                                                     action = input("""Press:
                                                        (Seq) to initiate a sequential duel between the chosen duelists,
                                                        (MSeq) to initiate multiple sequential duels between the chosen duelists,
                                                        (Sim) to initiate a simultaneous duel between the chosen duelists,
                                                        (MSim) to initiate multiple simultaneous duels between the chosen duelists,
                                                         (<) to go back.""").replace(" ","")
                                                     if action == "Seq":
                                                              arena.duel_stats()
                                                     elif action == "MSeq":
                                                            N = int(input("Enter number of duels: ").strip())
                                                            for key, value in arena.many_sequential(N).items():
                                                                print(key)
                                                                for key2, value2 in value.items():
                                                                    print(key2)
                                                                    for val in value2:
                                                                        print(value2[val], end = " ")
                                                                    print()
                                                                print(value.items())
                                                     elif action == "Sim":
                                                              pass
                                                     elif action == "MSim":
                                                         pass
                                                     elif action == "<": break
                                                     else:
                                                         print("Invalid argument.")
                                     elif single == '<': break
                                     else:
                                         print("Invalid input.")
                elif user_input == "r":
                    name = input("Enter the name of the duelist you wish to resurrect.").split()
                    if Duelist.exists(name):
                        Duelist.all_duelists[name].resurrect(pool=300)
                    else: print(f"Duelist with name \"{name}\" doesn\'t exist.")
                elif user_input == "": break
                else: continue

if __name__ == "__main__": Main()