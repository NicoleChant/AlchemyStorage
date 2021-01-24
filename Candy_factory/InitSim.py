from Candy_Factory import CandyFactory
from Simulate_Candy_Factory import Simulation
from model import pdfModel
import logging
import random
import math
import time
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn")

class Main():
    gold = 1000
    discounter = 0
    run_times = 7
    initial_stock = [100,150,250]
    orders = [20,20,20]
    simulation = Simulation(gold,discounter,run_times,orders)
    simulation.initialize_stock(*initial_stock)
    simulation.initialize_simulation(show_me=True)
    print(simulation.total_loss)
    simulation.graph_simresults(show_losses=True,show_cdlosses=True)
    #print(simulation.total_avg_loss(10000))
    #print(simulation.total_variance(10000))

    # candyFactory = CandyFactory(gold,discounter,50,150,200)
    # print(candyFactory.current_storage)
    # print(candyFactory.candy_types)
    # candyFactory.show_storage_details()
    # candyFactory.apply_daily_orders(20,30,50)
    # candyFactory.show_storage_details()
    # print(candyFactory)
    # candyFactory.restore_sim()
    # print(candyFactory)


if __name__=="__main__": Main()