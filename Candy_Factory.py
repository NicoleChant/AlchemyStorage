#THE WIDGET PROBLEM FROM JAYNES
import random
import time
import numpy as np
import logging
import math
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

plt.style.use("seaborn")

class CandyFactory():
    candies = list()
    colors = list()

    @staticmethod
    def generate_colors():
        return ["b", "g","m", "y", "k"]

    @staticmethod
    def generate_candies():
        return ["chocolate","blue violet","marshmallow","ice cream"
            ,"lollipop","dark cholocate","white chocolate","vanilla"]

    @staticmethod
    def choose_colors(num):
        colors_gen = []
        for _ in range(num):
            chosen_color = random.choice(CandyFactory.colors)
            colors_gen.append(chosen_color)
            CandyFactory.colors.remove(chosen_color)
        return colors_gen

    @staticmethod
    def choose_candy():
        a_candy = random.choice(CandyFactory.candies)
        CandyFactory.candies.remove(a_candy)
        return a_candy

    #constructor
    def __init__(self,gold,discounter,name="Alice's Candy Factory"):
        CandyFactory.candies = CandyFactory.generate_candies()
        CandyFactory.colors = CandyFactory.generate_colors()
        self.initial_gold = float(gold)
        self.current_gold = float(gold)
        self.initial_stock = dict()
        self.current_storage = dict()
        self.onlyints = True
        self.stock_initialized = False
        self.candy_types = list()
        self.costs = list()
        self.candy_num = len(self.candy_types)
        self.discounter = float(discounter)
        self.name = name.strip()
        self.total_loss = 0 ##unmet demand
        self.candy_loss = dict()
        self.colors = list()

    def initialize_stock(self,*quantities):
        '''initializing storage facility'''
        for quantity in quantities:
            if isinstance(quantity,float) | isinstance(quantity,int):
                if quantity>=0:
                    if self.onlyints:
                        self.current_storage.update({CandyFactory.choose_candy():int(quantity)})
                    else:
                        self.current_storage.update({CandyFactory.choose_candy():float(quantity)})
        self.initial_stock = self.current_storage.copy()
        self.candy_types = list(self.current_storage.keys())
        for candy in self.candy_types:
            self.candy_loss.update({candy:0})
        self.candy_num = len(self.candy_types)
        self.colors = CandyFactory.choose_colors(self.candy_num)
        self.stock_initialized = True
        print("Stock was initialized!")

    def use_floats(self):
        self.onlyints = False

    def action_scheme(self):
        def build_widgets(self):
            pass #TODO

    def restore_sim(self):
        self.total_loss = 0
        self.current_gold = self.initial_gold
        self.current_storage = self.initial_stock.copy()

    def add_costs(self,*cost_prices):
        if len(cost_prices)==self.candy_num:
            self.costs = cost_prices
        else:
            raise ValueError

    def invest_gold(self):
        pass #TODO

    def loss_function(self,type,order_size):
        '''step loss function returns the difference between product demand and its availability in units'''
        if order_size<=self.current_storage[type]: return 0
        return order_size-self.current_storage[type]

    def cdloss_per_candy(self):
        '''calculates commulative loss'''
        pass #TODO cummulative loss

    def calc_total_loss(self,orders):
        '''returns the total induced loss for each candy which didn't meet the market demands criteria'''
        total_loss = 0
        for i in range(len(orders)):
            total_loss += self.loss_function(self.candy_types[i],orders[i])
        return total_loss

    def apply_discount(self,x):
        if self.onlyints:
            return math.floor(x*(1-self.discounter))
        else:
            return x*(1-self.discounter)

    def apply_daily_leftovers(self):
        '''After each day remaining candies diminish by a certain percentage;the percentange (or discounter) may be 0'''
        if self.discounter>0:
            for candies, quantities in self.current_storage.items():
                if quantities>0:
                    self.current_storage[candies] = self.apply_discount(self.current_storage[candies])

    def apply_daily_orders(self,*orders):
        if self.stock_initialized:
            indiv_daily_losses = list()
            for i in range(len(orders)):
                 indiv_daily_losses.append(self.loss_function(self.candy_types[i],orders[i]))
                 if indiv_daily_losses[i]==0:
                       self.current_storage[self.candy_types[i]] -= orders[i]
                 else:
                       self.current_storage[self.candy_types[i]] = 0
                 self.candy_loss[self.candy_types[i]] += self.loss_function(self.candy_types[i],orders[i])
            self.total_loss += self.calc_total_loss(orders)
            print(self.total_loss)
            self.apply_daily_leftovers()
            return indiv_daily_losses
        else:
            raise Exception("Uninitialized stock variable.")

    def show_storage_details(self):
        x_axis = self.candy_types
        y_axis = list(self.current_storage.values())
        ax = plt.axes()
        ax.set_facecolor("tomato")
        plt.bar(x_axis,y_axis,color=self.colors,width=0.5,align="center")
        plt.xticks(x_axis,rotation = 45)
        plt.xlabel("Candies")
        plt.ylabel("Quantities")
        plt.title(self.name+"\n Current Quantities of Candies")
        all_handles = []
        for i in range(len(x_axis)):
            all_handles.append(mpatches.Patch(color=self.colors[i],label=x_axis[i]))
        plt.legend(handles=all_handles,loc=0)
        plt.tight_layout()
        plt.show()

    def __str__(self):
        w = 20*"*"
        s = w + f"Alice's Candy Factory!" + w + f"\nCurrent Gold: {self.current_gold} G\nCurrent Stock: \n"
        for type, size in self.current_storage.items():
            s += f"\t\t\t\t\t{type}:\t\t {size}\n"
        return s
