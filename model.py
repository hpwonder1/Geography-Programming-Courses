# -*- coding: utf-8 -*-
import matplotlib

matplotlib.use('TkAgg')

import tkinter
import random
import matplotlib.pyplot

import requests
import bs4
import csv

import agentframework
from matplotlib.animation import FuncAnimation


def read_environment_from_file():
    # read environment data from "in.csv"
    with open('in.csv')as f:
        f_csv = csv.reader(f)
        # for each row
        for row in f_csv:
            rowlist = []
            # for each number in row
            for number in row:
                rowlist.append(int(number))
            # update global environment
            environment.append(rowlist)


def crawl_data():
    # sending requests
    r = requests.get(
        'https://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
    content = r.text
    # parse the website with BeautifulSoup
    soup = bs4.BeautifulSoup(content, 'html.parser')
    # get all data points
    td_ys = soup.find_all(attrs={"class": "y"})
    td_xs = soup.find_all(attrs={"class": "x"})
    # add data points to the agent list
    for i in range(num_of_agents):
        y = int(td_ys[i].text)
        x = int(td_xs[i].text)
        agents.append(agentframework.Agent(environment, agents, y, x))


def show_agents():
    # create a scatter plot for all agents
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x, agents[i].y)
    # set limits
    matplotlib.pyplot.ylim(0, 99)
    matplotlib.pyplot.xlim(0, 99)
    # show the environment
    matplotlib.pyplot.imshow(environment)


def update(frame_number):
    # a function to update the fig
    # clear the fig first
    fig.clear()
    global carry_on
    # for each iteration
    for j in range(num_of_iterations):
        # for each agent
        for i in range(num_of_agents):
            # move the agent
            agents[i].move()
            # perform "eat" operation
            agents[i].eat()
            # share with other agents
            agents[i].share_with_neighbours(neighbourhood)
    # end the model with 10% probability
    if random.random() < 0.1:
        carry_on = False
        print("stopping condition")
    # print all updated agents
    show_agents()


def gen_function(b=[0]):
    a = 0
    global carry_on
    while (a < 10) & (carry_on):
        yield a
        a = a + 1


def run():
    animation = FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.draw()


def convert_int(s, default):
    try:
        number = int(s)
        return number
    except ValueError:
        return default


if __name__ == "__main__":
    # get parameters from user
    print("Model is running")
    num_of_agents = input("Please enter the number of agents (default 10):\n")
    num_of_agents = convert_int(num_of_agents, 10)

    num_of_iterations = input("Please enter the number of iterations (default 100):\n")
    num_of_iterations = convert_int(num_of_iterations, 100)

    neighbourhood = input("Please enter the number of neighbourhood (default 20):\n")
    neighbourhood = convert_int(neighbourhood, 20)

    print("Start the model")
    # initialization
    agents = []
    environment = []
    fig = matplotlib.pyplot.figure(figsize=(7, 7))
    carry_on = True
    # read environment data from "in.csv"
    read_environment_from_file()
    # crawl agent data from website
    crawl_data()
    # print agents on the environment
    show_agents()

    # create a root tkinter
    root = tkinter.Tk()
    # set title
    root.wm_title("Model")
    # create a canvas with the fig in root
    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
    canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    # create a menu bar
    menu_bar = tkinter.Menu(root)
    root.config(menu=menu_bar)
    model_menu = tkinter.Menu(menu_bar)
    # add cascade menu
    menu_bar.add_cascade(label="Model", menu=model_menu)
    # add a run model button with the function run
    model_menu.add_command(label="Run model", command=run)
    # start the GUI
    tkinter.mainloop()
