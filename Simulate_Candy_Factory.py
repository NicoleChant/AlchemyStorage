from Candy_Factory import CandyFactory
from model import pdfModel
import numpy as np
import random
import logging
import time
import math
import matplotlib.pyplot as plt

plt.style.use("seaborn")

class Simulation(CandyFactory):

    def __init__(self,initial_gold,discounter,run_times,model,name="Alice's Candy Factory"):
        super().__init__(initial_gold,discounter,name)
        self.run_times = int(run_times)
        self.orders = model
        #keeping track of records
        self.stats_quantities = dict()
        self.stats_dailylosses = dict()

        # self.initialize_simulation()
        # self.graph_simulation_results()
        # self.orders_sampler = pdfModel

    def initialize_stock(self,*quantities):
        super().initialize_stock(*quantities)
        for candy, quantity in self.initial_stock.items():
            self.stats_quantities.update({candy: [quantity]})
            self.stats_dailylosses.update({candy: [0]})

    def store_stats(self):
        pass #TODO

    def update_stats(self,ind_losses):
        idx = 0
        for candy, quantity in self.current_storage.items():
            self.stats_quantities[candy].append(quantity)
            self.stats_dailylosses[candy].append(ind_losses[idx])
            idx += 1

    def cdloss_per_candy(self):
        cdflosses = dict()
        for i in range(self.candy_num):
            cdflosses.update({self.candy_types[i]:[0]})

        for i in range(self.candy_num):
            for j in range(1,self.run_times+1):
                  cdflosses[self.candy_types[i]].append(self.stats_dailylosses[self.candy_types[i]][j] + cdflosses[self.candy_types[i]][-1])
        return cdflosses

    def clear_stats(self):
        for candy,quantity in self.initial_stock.items():
            self.stats_quantities.update({candy:[quantity]})
            self.stats_dailylosses.update({candy:[0]})
            self.total_loss = 0
            self.candy_loss.update({candy:0})

    def average_loss(self,candy,accuracy,moment=1):
        if candy in self.candy_types:
            M = accuracy
            avg = 0
            while M>0:
                self.initialize_simulation()
                avg += self.candy_loss[candy]**moment
                self.clear_stats()
                M -=1
            return float(avg)/accuracy
        else:
            raise ValueError

    def total_avg_loss(self,accuracy):
        total_avg = 0
        for candy in self.candy_types:
            total_avg += self.average_loss(candy,accuracy,1)
        return total_avg

    def total_average_loss2nd(self,candy,accuracy,moment=1):
        '''This applies for any moment of the total loss random variable'''
        M = accuracy
        avg = 0
        while M>0:
            self.initialize_simulation()
            avg += self.total_loss**moment
            self.clear_stats()
            M -=1
        return float(avg)/accuracy

    def variance_loss(self, candy, accuracy):
        if candy in self.candy_types:
            return self.average_loss(candy,accuracy,2)-self.average_loss(candy,accuracy,1)**2
        else:
            raise ValueError

    def total_variance(self,accuracy):
        '''this formula applies due to the independence of random variables (incoming candy orders)
        which allows us to add the individual variances and obtain the total variance of total orders'''
        total_var = 0
        for candy in self.candy_types:
            total_var += self.variance_loss(candy,accuracy)
        return total_var

    def initialize_simulation(self,show_me=False):
        if self.stock_initialized:
            runner = self.run_times
            while(runner>0):
                  indiv_losses = self.apply_daily_orders(*self.orders)
                  self.update_stats(indiv_losses)
                  runner -= 1
            if show_me:
                self.show_results()
            return True
        else:
            raise Exception("Uninitialized Stock variable!")

    def show_results(self):
        cdf_losses = self.cdloss_per_candy()
        print("\nCandies Simulation Analytics: \n")
        for candy in self.candy_types:
            print(f"Analytics for candy {candy}: \n")
            print("Day \t Quantities \t Losses \t Cummulative Losses")
            for i in range(len(self.stats_quantities[candy])):
                print(f"{i}: \t\t\t {self.stats_quantities[candy][i]} \t\t\t {self.stats_dailylosses[candy][i]} \t\t\t\t {cdf_losses[candy][i]}")
            print(f"Total loss occurred from {candy}: \t\t {cdf_losses[candy][-1]}\n\n\n")

    def graph_simresults(self,show_losses=True,show_cdlosses=True):
           y_labels = ["daily cummulative losses","daily losses","daily quantities"]
           y_label = None
           y_axes = []
           if show_losses:
               if show_cdlosses:
                   stats_cdlosses = self.cdloss_per_candy()
                   y_label = y_labels[0]
                   for candy in self.candy_types:
                       y_axes.append(stats_cdlosses[candy])
               else:
                   y_label = y_labels[1]
                   for candy in self.candy_types:
                       y_axes.append(self.stats_dailylosses[candy])
           else:
               y_label = y_labels[2]
               for candy in self.candy_types:
                   y_axes.append(self.stats_quantities[candy])
           x_axis = [i for i in range(len(y_axes[0]))]
           for i in range(len(self.candy_types)):
               plt.plot(x_axis,y_axes[i],f"o:{self.colors[i]}",ms=7)
           plt.xticks(x_axis,rotation=45)
           plt.xlabel("days")
           plt.ylabel(y_label)
           plt.title(self.name+"\n Candies losses timeseries")
           plt.legend(self.candy_types)
           plt.tight_layout()
           plt.show()
           self.clear_stats()