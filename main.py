#lib importing
from bs4 import BeautifulSoup #data scrapping
import requests #data scrapping
import re #data scrapping
from matplotlib import pyplot as plt #graph
import numpy as np #data tidying
from sss import ShortScale #my own module to shorten the big number like 1M, 1B, etc.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #let you dump graph into tkinter
from tkinter import * #the GUI
import matplotlib #graph
import matplotlib.font_manager as font_manager #graph font
from annot import hover
matplotlib.use('TkAgg')

#data scrapping
url1 = 'https://www.worldometers.info/coronavirus/worldwide-graphs/#total-cases'
url2 = 'https://www.worldometers.info/coronavirus/'
page1 = requests.get(url1)
page2 = requests.get(url2)
soup1 = BeautifulSoup(page1.text, 'lxml')
soup2 = BeautifulSoup(page2.text, 'lxml')
scr = soup1.findAll('script')

def total_cases_num():
    tofind = soup2.findAll('div', {'class':'maincounter-number'})
    return [i.find('span').text for i in tofind]

#data finding
main = [str(i) for i in scr]
data = [i for i in [re.findall(r'data:.*', i)for i in main] if i]

def style(ax, fig):
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white') 
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_facecolor('#191919')
    fig.patch.set_facecolor('#191919')

def plot_line(x, y, color, label, ax, fig, title):
    datax = x
    line, = plt.plot(x, y, '.-', color=color, linewidth=5, solid_capstyle="round", label=label)
    font = font_manager.FontProperties(family='Bahnschrift', size=15)
    leg = plt.legend(handles=[line], loc=2, fontsize='large', framealpha=0.0, prop=font)
    leg.get_frame().set_linewidth(0.0)
    for text in leg.get_texts():
        text.set_color("white")
    titlefont = {'fontsize': 25, 'fontname': 'Bahnschrift'}
    plt.title(title, **titlefont, y=1.03, color='white')
    # Annotation style may be changed here
    annot = ax.annotate("", xy=(0, 0), xytext=(10, 20), textcoords="offset points", bbox=dict(boxstyle="round", fc="w"), family='Bahnschrift', size=15)
    annot.set_visible(False)
    line_info = [line, annot, y]
    style(ax, fig)
    return line_info, datax

def plot_double_line(x1, y1, x2, y2, color1, color2, label1, label2, ax, fig, title):
    global datax, line_info1, line_info2
    datax = x1
    line1, = plt.plot(x1, y1, '.-', color=color1, linewidth=5, solid_capstyle="round", label=label1)
    line2, = plt.plot(x2, y2, '.-', color=color2, linewidth=5, solid_capstyle="round", label=label2)
    font = font_manager.FontProperties(family='Bahnschrift', size=15)
    leg = plt.legend(handles=[line1, line2], loc=2, fontsize='large', framealpha=0.0, prop=font)
    leg.get_frame().set_linewidth(0.0)
    for text in leg.get_texts():
        text.set_color("white")
    # Annotation style may be changed here
    annot1 = ax.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points", bbox=dict(boxstyle="round", fc="w"))
    annot1.set_visible(False)
    annot2 = ax.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points", bbox=dict(boxstyle="round", fc="w"))
    annot2.set_visible(False)
    line_info1 = [line1, annot1, y1]
    line_info2 = [line2, annot2, y2]
    style(ax, fig)
    titlefont = {'fontsize': 25, 'fontname': 'Bahnschrift'}
    plt.title(title, **titlefont, y=1.03, color='white')
    return line_info1, line_info2, datax

def plot_bar(x, y, color, label, title, ax, fig):
    bar= plt.bar(x, y, color=color, label=label)
    font = font_manager.FontProperties(family='Bahnschrift', size=15)
    leg = plt.legend(handles=[bar], loc=2, fontsize='large', framealpha=0.0, prop=font)
    leg.get_frame().set_linewidth(0.0)
    for text in leg.get_texts():
        text.set_color("white")
    titlefont = {'fontsize': 25, 'fontname': 'Bahnschrift'}
    plt.title(title, **titlefont, y=1.03, color='white')
    style(ax, fig)

#total cases chart (plot)
def total_cases_chart(root):
    total_cases_date = [i.replace('\"', '') for i in list(set(re.findall(r'categories:.*', main[23])))[0].replace('categories: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    total_cases = [int(i) for i in data[1][0].replace('data: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    fig, ax = plt.subplots()
    plt.xticks(np.arange(0, len(total_cases_date), 10.0))
    def format_func(value, tick_number):
        return ShortScale(int(value))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    fig.set_size_inches(13, 6)
    line_info, datax = plot_line(total_cases_date, total_cases, 'white', 'Cases', ax, fig, 'Total Cases')
    plt.xticks(rotation=45)
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    fig.canvas.mpl_connect("motion_notify_event", lambda event: hover(event, line_info, fig, ax, datax))
    return plot_widget

#total serious and critical cases (plot)
def total_serious_and_critical_cases(root):
    total_serious_and_critical_cases_date = [i.replace('\"', '') for i in list(set(re.findall(r'categories:.*', main[31])))[0].replace('categories: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    total_serious_and_critical_cases = [i for i in data[7][0].replace('data: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    total_serious_and_critical_cases = [0 if total_serious_and_critical_cases[i] == 'null' else int(total_serious_and_critical_cases[i]) for i in range(len(total_serious_and_critical_cases))]
    fig, ax = plt.subplots()
    x_ticks = np.arange(0, len(total_serious_and_critical_cases_date), 10)
    plt.xticks(x_ticks)
    def format_func(value, tick_number):
        return ShortScale(int(value))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    fig.set_size_inches(13, 6)
    line_info, datax = plot_line(total_serious_and_critical_cases_date, total_serious_and_critical_cases, 'white', 'Serious and Critical Cases', ax, fig, 'Total Serious and Critical Cases')
    plt.xticks(rotation=45)
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    fig.canvas.mpl_connect("motion_notify_event", lambda event: hover(event, line_info, fig, ax, datax))
    return plot_widget

#daily cases chart (bar)
def daily_cases_chart(root):
    daily_cases_date = [i.replace('\"', '') for i in list(set(re.findall(r'categories:.*', main[24])))[0].replace('categories: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    daily_cases = [i for i in data[2][0].replace('data: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    daily_cases = [0 if daily_cases[i] == 'null' else int(daily_cases[i]) for i in range(len(daily_cases))]
    fig, ax = plt.subplots()
    x_ticks = np.arange(0, len(daily_cases_date), 10)
    plt.xticks(x_ticks)
    fig.set_size_inches(13, 6)
    plot_bar(daily_cases_date, daily_cases, 'white', 'Daily Cases', 'Daily Cases', ax, fig)
    plt.xticks(rotation=45)
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    return plot_widget

#active cases chart (plot)
def active_cases_chart(root):
    active_cases_date = [i.replace('\"', '') for i in list(set(re.findall(r'categories:.*', main[25])))[0].replace('categories: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    active_cases = [int(i) for i in data[3][0].replace('data: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    fig, ax = plt.subplots()
    x_ticks = np.arange(0, len(active_cases_date), 10)
    plt.xticks(x_ticks)
    def format_func(value, tick_number):
        return ShortScale(int(value))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    fig.set_size_inches(13, 6)
    line_info, datax = plot_line(active_cases_date, active_cases, 'white', 'Currently Infected', ax, fig, 'Active Cases')
    plt.xticks(rotation=45)
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    fig.canvas.mpl_connect("motion_notify_event", lambda event: hover(event, line_info, fig, ax, datax))
    return plot_widget

#total cured chart (plot)
def total_cured_chart(root):
    total_cured_date = [i.replace('\"', '') for i in list(set(re.findall(r'categories:.*', main[26])))[0].replace('categories: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    total_cured = [int(i) for i in data[4][0].replace('data: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    fig, ax = plt.subplots()
    x_ticks = np.arange(0, len(total_cured_date), 10)
    plt.xticks(x_ticks)
    def format_func(value, tick_number):
        return ShortScale(int(value))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    fig.set_size_inches(13, 6)
    line_info, datax = plot_line(total_cured_date, total_cured, 'white', 'Cured', ax, fig, 'Total Cured')
    plt.xticks(rotation=45)
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    fig.canvas.mpl_connect("motion_notify_event", lambda event: hover(event, line_info, fig, ax, datax))
    return plot_widget

#daily cured chart (bar)
def daily_cured_chart(root):
    daily_cured_date = [i.replace('\"', '') for i in list(set(re.findall(r'categories:.*', main[27])))[0].replace('categories: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    daily_cured = [i for i in data[5][0].replace('data: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    daily_cured = [0 if daily_cured[i] == 'null' else int(daily_cured[i]) for i in range(len(daily_cured))]
    fig, ax = plt.subplots()
    x_ticks = np.arange(0, len(daily_cured_date), 10)
    plt.xticks(x_ticks)
    def format_func(value, tick_number):
        return ShortScale(int(value))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    fig.set_size_inches(13, 6)
    plot_bar(daily_cured_date, daily_cured, 'white', 'Dialy Cured', 'Daily Cured', ax, fig)
    plt.xticks(rotation=45)
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    return plot_widget

#infected and recovered chart (multiple plot)
def infected_vs_recovered_chart(root):
    date = [i.replace('\"', '') for i in list(set(re.findall(r'categories:.*', main[28])))[0].replace('categories: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    daily_cases = [i for i in data[2][0].replace('data: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    daily_cases = [0 if daily_cases[i] == 'null' else int(daily_cases[i]) for i in range(len(daily_cases))]
    daily_cured = [i for i in data[5][0].replace('data: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    daily_cured = [0 if daily_cured[i] == 'null' else int(daily_cured[i]) for i in range(len(daily_cured))]
    fig, ax = plt.subplots()
    x_ticks = np.arange(0, len(date), 10)
    plt.xticks(x_ticks)
    def format_func(value, tick_number):
        return ShortScale(int(value))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    fig.set_size_inches(13, 6)
    line_info1, line_info2, datax = plot_double_line(date, daily_cured, date, daily_cases, '#baffba', '#ffbaba', 'New Recoviries', 'New Infected', ax, fig, 'New Cases vs. New Recoveries')
    plt.xticks(rotation=45)
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    fig.canvas.mpl_connect("motion_notify_event", lambda event: hover(event, line_info1, fig, ax, datax))
    fig.canvas.mpl_connect("motion_notify_event", lambda event: hover(event, line_info2, fig, ax, datax))
    return plot_widget

#outcome of total cases (multiple plot)
def outcome_of_total_close_cases(root):
    date = [i.replace('\"', '') for i in list(set(re.findall(r'categories:.*', main[32])))[0].replace('categories: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    death_rate = [i for i in data[9][0].replace('data: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    death_rate = [0 if death_rate[i] == 'null' else float(death_rate[i]) for i in range(len(death_rate))]
    recovery_rate = [i for i in data[9][1].replace('data: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    recovery_rate = [0 if recovery_rate[i] == 'null' else float(recovery_rate[i]) for i in range(len(recovery_rate))]
    fig, ax = plt.subplots()
    x_ticks = np.arange(0, len(date), 10)
    plt.xticks(x_ticks)
    fig.set_size_inches(13, 6)
    line_info1, line_info2, datax = plot_double_line(date, death_rate, date, recovery_rate, '#ffbaba', '#baffba', 'Death Rate', 'Recovery Rate', ax, fig, 'Outcome of total closed cases (recovery rate vs death rate)')
    plt.xticks(rotation=45)
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    fig.canvas.mpl_connect("motion_notify_event", lambda event: hover(event, line_info1, fig, ax, datax))
    fig.canvas.mpl_connect("motion_notify_event", lambda event: hover(event, line_info2, fig, ax, datax))
    return plot_widget

#total death chart (plot)
def total_death_chart(root):
    global fig, ax
    total_death_date = [i.replace('\"', '') for i in list(set(re.findall(r'categories:.*', main[33])))[0].replace('categories: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    total_death = [int(i) for i in data[10][0].replace('data: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    fig, ax = plt.subplots()
    plt.xticks(np.arange(0, len(total_death_date), 10.0))
    def format_func(value, tick_number):
        return ShortScale(int(value))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    fig.set_size_inches(13, 6)
    line_info, datax = plot_line(total_death_date, total_death, 'white', 'Deaths', ax, fig, 'Total Deaths')
    plt.xticks(rotation=45)
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    fig.canvas.mpl_connect("motion_notify_event", lambda event: hover(event, line_info, fig, ax, datax))
    return plot_widget

#daily death chart (bar)
def daily_death_chart(root):
    daily_death_date = [i.replace('\"', '') for i in list(set(re.findall(r'categories:.*', main[34])))[0].replace('categories: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    daily_death = [i for i in data[11][0].replace('data: [', '').replace(']', '').replace('}', '').replace(' ', '').split(',') if i != '']
    daily_death = [0 if daily_death[i] == 'null' else int(daily_death[i]) for i in range(len(daily_death))]
    fig, ax = plt.subplots()
    x_ticks = np.arange(0, len(daily_death_date), 10)
    plt.xticks(x_ticks)
    def format_func(value, tick_number):
        return ShortScale(int(value))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    fig.set_size_inches(13, 6)
    plot_bar(daily_death_date, daily_death, 'white', 'Daily Deaths', 'Daily Deaths', ax, fig)
    plt.xticks(rotation=45)
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    return plot_widget

#distribution of cases (pie)
def distribution_of_cases(root):
    count = 0
    country = [i2.split(',') for i2 in [i.replace('}', '').replace('                        ', '').replace('                    ,                 ', '').split('{') for i in re.findall('data:.*', main[22].replace('\n', ''))][0]]
    country = [[i2.replace('name: ', '').replace('\'', '').replace('y: ', '').replace('value: ', '').replace('                    ', '').replace('&amp;', '&') for i2 in i] for i in country]
    country[len(country)-1].pop()
    country.pop(0)
    print(country)
    [country.pop() for i in range(3)]
    countryname = [i[0]+': ' + str(i[1]) + '% ('+ str(i[2]) + ' cases)' for i in country]
    countryname2 = [i[0]+'\n' + str(i[1]) + '% ('+ str(i[2]) + ' cases)' for i in country]
    country_y = [float(i[1]) for i in country]
    country_value = [int(i[2]) for i in country]
    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"), figsize=(15, 10))
    ax.set_facecolor('#191919')
    fig.patch.set_facecolor('#191919')
    colors = ['#191919']
    p,texts = ax.pie(country_value, wedgeprops=dict(width=0.65, edgecolor='w', linewidth=1), startangle=145, colors=colors)
    kw = dict(arrowprops=dict(arrowstyle="-", color='w'),bbox=dict(boxstyle="square,pad=0.3", fc="#191919", ec="#191919", lw=0.72), zorder=1, va="center")
    w = [list(enumerate(p))[i][1] for i in range(len(list(enumerate(p))))]
    for i, p in enumerate(p):
        if count < 12:
            x, y = np.cos(np.deg2rad((p.theta2 - p.theta1)/2 + p.theta1)), np.sin(np.deg2rad((p.theta2 - p.theta1)/2 + p.theta1))
            kw["arrowprops"].update({"connectionstyle": "angle,angleA=0,angleB={}".format((p.theta2 - p.theta1)/2 + p.theta1)})
            ax.annotate(countryname[i], xy=(x, y), xytext=(1.3*np.sign(x), 1.38*y), color='white', horizontalalignment={-1: "right", 1: "left"}[int(np.sign(x))], **kw, family='Bahnschrift', fontsize=13)
            count += 1
    print(w)
    annot = ax.annotate("", xy=(0, 0), ha='center', va='center', xytext=(0,0), textcoords="offset points",bbox=dict(boxstyle="circle", fc="#191919", ec='#191919'), color='white', family='Bahnschrift', fontsize=13)

    def update(event):
        if True in [i.contains_point([event.x, event.y]) for i in w]:
            annot.set_visible(True)
            annot.set_text(countryname2[[i.contains_point([event.x, event.y]) for i in w].index(True)])
            fig.canvas.draw_idle()
        else:
                annot.set_visible(False)
                fig.canvas.draw_idle()
    
    titlefont = {'fontsize': 25, 'fontname': 'Bahnschrift'}
    ax.set_title("Distribution of cases", **titlefont, y=1.03, color='white')
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    fig.canvas.mpl_connect("motion_notify_event", update)
    return plot_widget


#root = Tk()
#total_cases_num()
#total_cases_chart(root).pack()
#daily_cases_chart(root).pack()
#active_cases_chart(root).pack()
#total_cured_chart(root).pack()
#daily_cured_chart(root).pack()
#infected_vs_recovered_chart(root).pack()
#total_serious_and_critical_cases(root).pack()
#outcome_of_total_close_cases(root).pack()
#total_death_chart(root).pack()
#daily_death_chart(root).pack()
#distribution_of_cases(root).pack()
#root.mainloop()