import sys
import os
from tkinter import ttk
from tkinter import *
import matplotlib
import json
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import random
import pygame
from matplotlib.ticker import MaxNLocator

day_arr = []
port_value = []

CONFIG_FILE = "settings.json"

#Interest rate settings
min_rate = 0.001   # 0.1% daily
max_rate = 0.05    # 5% daily
rate_step = 0.001
rates_label = None
trade_back = None
play1_flag = False
plot_flag = False
game_start = False
stocks = ["Apple", "Tesla", "Amazon", "JPMorgan", "Pfizer", "Google", "Microsoft", "Nike", "McDonalds", "CocaCola"]
stock_trends = {s: 0 for s in stocks}
stock_returns = {stock: 0 for stock in stocks}
news_effects = {}
bank_flag = True
highlighted_news = set()
news_events = [
    # --- Company-specific ---
    {"headline": "Apple launches a revolutionary AI chip.", "impact": {"Apple": +15}},
    {"headline": "Tesla unveils affordable long-range EV.", "impact": {"Tesla": +16}},
    {"headline": "Amazon expands same-day delivery worldwide.", "impact": {"Amazon": +14}},
    {"headline": "JPMorgan posts record quarterly profits.", "impact": {"JPMorgan": +15}},
    {"headline": "Pfizer announces breakthrough cancer treatment.", "impact": {"Pfizer": +16}},
    {"headline": "Google fined heavily for privacy violations.", "impact": {"Google": -15}},
    {"headline": "Microsoft secures major government cloud contract.", "impact": {"Microsoft": +14}},
    {"headline": "Nike signs exclusive deal with sports superstar.", "impact": {"Nike": +15}},
    {"headline": "McDonald's faces backlash over supply chain issues.", "impact": {"McDonalds": -14}},
    {"headline": "Coca-Cola launches new zero-sugar flavor to strong reviews.", "impact": {"CocaCola": +13}},
    {"headline": "Apple faces antitrust investigation in Europe.", "impact": {"Apple": -14}},
    {"headline": "Tesla's self-driving software involved in safety controversy.", "impact": {"Tesla": -15}},
    {"headline": "Amazon hit with major workers' strike in key warehouses.", "impact": {"Amazon": -13}},
    {"headline": "JPMorgan expands aggressively into digital banking.", "impact": {"JPMorgan": +13}},
    {"headline": "Pfizer vaccine sales decline as competitors gain ground.", "impact": {"Pfizer": -12}},
    {"headline": "Google announces quantum computing milestone.", "impact": {"Google": +15}},
    {"headline": "Microsoft delays release of highly anticipated game.", "impact": {"Microsoft": -12}},
    {"headline": "Nike boosts sales with sustainability-focused clothing line.", "impact": {"Nike": +14}},
    {"headline": "McDonald's launches AI-powered drive-thru ordering nationwide.", "impact": {"McDonalds": +13}},
    {"headline": "Coca-Cola criticized for plastic waste in environmental report.", "impact": {"CocaCola": -12}},

    # --- Industry/Sector ---
    {"headline": "Tech industry sees investor confidence boost.", "impact": {"Apple": +12, "Google": +13, "Microsoft": +12}},
    {"headline": "Tech stocks hit by semiconductor shortages.", "impact": {"Apple": -13, "Google": -12, "Microsoft": -12}},
    {"headline": "Electric vehicle demand surges globally.", "impact": {"Tesla": +14, "Apple": +11, "Microsoft": +11}},
    {"headline": "Automotive tariffs rise sharply.", "impact": {"Tesla": -14}},
    {"headline": "Retail sector sales hit record highs.", "impact": {"Amazon": +13, "Nike": +12, "CocaCola": +11}},
    {"headline": "Retail industry faces supply chain bottlenecks.", "impact": {"Amazon": -12, "Nike": -12, "CocaCola": -11}},
    {"headline": "Healthcare sector gets funding boost.", "impact": {"Pfizer": +13}},
    {"headline": "Global banking sector rattled by rate hike fears.", "impact": {"JPMorgan": -13}},
    {"headline": "Fast food industry sees growing health-conscious shift.", "impact": {"McDonalds": -12, "CocaCola": -11}},
    {"headline": "Beverage industry enjoys summer sales boom.", "impact": {"CocaCola": +13, "McDonalds": +11}},
    {"headline": "Tech sector hit by new data privacy regulations.", "impact": {"Apple": -12, "Google": -13, "Microsoft": -12}},
    {"headline": "EV sector boosted by government subsidies.", "impact": {"Tesla": +13, "Apple": +8}},
    {"headline": "E-commerce industry benefits from festive season surge.", "impact": {"Amazon": +12, "Nike": +11, "CocaCola": +10}},
    {"headline": "Banking industry benefits from strong loan demand.", "impact": {"JPMorgan": +12}},
    {"headline": "Pharmaceutical sector shaken by stricter FDA approval process.", "impact": {"Pfizer": -13}},
    {"headline": "Athletic wear industry grows with home fitness boom.", "impact": {"Nike": +12, "Amazon": +11}},
    {"headline": "Restaurant sector faces rising labor costs.", "impact": {"McDonalds": -13, "CocaCola": -11}},
    {"headline": "Beverage sector sees rising competition from energy drinks.", "impact": {"CocaCola": -12}},
    {"headline": "Cloud computing sector continues rapid expansion.", "impact": {"Microsoft": +13, "Google": +12, "Amazon": +12}},
    {"headline": "Traditional banking threatened by fintech disruption.", "impact": {"JPMorgan": -12}},

    # --- Global ---
    {"headline": "Global economic uncertainty increases.", "impact": {"all": -13}},
    {"headline": "Stock markets rally on positive global growth forecasts.", "impact": {"all": +13}},
    {"headline": "Major geopolitical tensions disrupt trade.", "impact": {"all": -14}},
    {"headline": "Breakthrough in renewable energy tech spurs optimism.", "impact": {"all": +12}},
    {"headline": "Global pandemic fears return.", "impact": {"all": -15}},
    {"headline": "Central banks announce coordinated stimulus measures.", "impact": {"all": +14}},
    {"headline": "Natural disaster impacts major supply chains.", "impact": {"all": -12}},
    {"headline": "Cryptocurrency market crash sparks investor panic.", "impact": {"all": -13}},
    {"headline": "Global sports event boosts consumer spending.", "impact": {"all": +12}},
    {"headline": "Oil prices plummet, lowering production costs worldwide.", "impact": {"all": +13}},
    {"headline": "Global inflation fears dampen investor sentiment.", "impact": {"all": -13}},
    {"headline": "Breakthrough peace talks ease geopolitical tensions.", "impact": {"all": +12}},
    {"headline": "New trade agreements boost global commerce.", "impact": {"all": +13}},
    {"headline": "Rising energy prices spark concerns worldwide.", "impact": {"all": -12}},
    {"headline": "Cyberattack on critical infrastructure rattles markets.", "impact": {"all": -14}},
    {"headline": "AI-driven productivity gains lift global economic outlook.", "impact": {"all": +13}},
    {"headline": "Climate change summit spurs investment in green industries.", "impact": {"all": +12}},
    {"headline": "Global tourism recovers strongly after years of decline.", "impact": {"all": +11}},
    {"headline": "Worldwide chip shortage worsens.", "impact": {"all": -13}},
    {"headline": "Major breakthrough in space exploration inspires global optimism.", "impact": {"all": +12}}
]

bullet_point1 = "\u2012 You have $50,000 to spend on 10 different stocks"
bullet_point2 = "\u2012 From day 5, share prices will change every day; 1 day = 8 seconds"
bullet_point3 = "\u2012 Every 10 days, news stories will appear on the news log,"
bullet_point4 = "which will directly impact share prices, so keep a close eye..."
bullet_point_bank = "\u2012 The bank will open on day 10, offering loans and a savings account"
bullet_point_bank3 = "\u2012 Note: Interest rates may change between news stories"
bullet_point5 = "\u2012 Hint: Buy low and sell high"
bullet_point6 = "Good luck and have fun!"
flag = True
canvas = None
canvas2 = None
current_screen = False
tree_rows = {}
tree_port_rows = {}
window = Tk()
window.title("Menu")
window.geometry("800x800")
previous_screen = None
bg = '#C0C3BF'
fg = '#2C3E50'
bank_state = DISABLED
stock_show = None
stock_buymax = None
hint_label = None
graph_button = None
stock_sellten = None
frame_bottom = None
stock_buyten = None
stock_sellall = None
stock_buy = None
current_stock = None
stock_sell = None
alert_label = None
alert_label_buy = None
hide_button = None
total = 50000
formatted_total = format(total, ',')
k = 0
current_day = 0
day_label_ref = None
EL = None
canvas3 = None
news_history = []
day_arr2 = []
news_log = Listbox(window, height=10, width=60, bg=bg, fg=fg)
news_log.pack(side="bottom", fill="x")
port_value = []
day_arr = []

#Banking system
loan_balance = 0
loan_interest_rate = 0.005
savings_balance = 0
savings_interest_rate = 0.001
loan_limit = 20000

#Port_view graphs
portfolio_history = [total]
gains_losses_history = [0]

stock_prices_plot = {
    "Apple": [195],
    "Tesla": [250],
    "Amazon": [130],
    "JPMorgan": [160],
    "Pfizer": [35],
    "Google": [135],
    "Microsoft": [370],
    "Nike": [100],
    "McDonalds": [290],
    "CocaCola": [60]
}

stock_prices = {
    "Apple": [195],
    "Tesla": [250],
    "Amazon": [130],
    "JPMorgan": [160],
    "Pfizer": [35],
    "Google": [135],
    "Microsoft": [370],
    "Nike": [100],
    "McDonalds": [290],
    "CocaCola": [60]
}

stock_owned = {
    "Apple": 0,
    "Tesla": 0,
    "Amazon": 0,
    "JPMorgan": 0,
    "Pfizer": 0,
    "Google": 0,
    "Microsoft": 0,
    "Nike": 0,
    "McDonalds": 0,
    "CocaCola": 0
}

stock_returns = { "Apple": 0,
    "Tesla": 0,
    "Amazon": 0,
    "JPMorgan": 0,
    "Pfizer": 0,
    "Google": 0,
    "Microsoft": 0,
    "Nike": 0,
    "McDonalds": 0,
    "CocaCola": 0
}

purchase_history = { "Apple": 0,
    "Tesla": 0,
    "Amazon": 0,
    "JPMorgan": 0,
    "Pfizer": 0,
    "Google": 0,
    "Microsoft": 0,
    "Nike": 0,
    "McDonalds": 0,
    "CocaCola": 0
}

sale_history = { "Apple": 0,
    "Tesla": 0,
    "Amazon": 0,
    "JPMorgan": 0,
    "Pfizer": 0,
    "Google": 0,
    "Microsoft": 0,
    "Nike": 0,
    "McDonalds": 0,
    "CocaCola": 0
}

stock_values = {"Apple": (stock_owned['Apple'] * stock_prices['Apple'][k]),
    "Tesla": (stock_owned['Tesla'] * stock_prices['Tesla'][k]),
    "Amazon": ((stock_prices["Amazon"][k]) * (stock_owned["Amazon"])),
    "JPMorgan": ((stock_owned['JPMorgan']) * (stock_prices['JPMorgan'][k])),
    "Pfizer": (stock_owned['Pfizer'] * stock_prices['Pfizer'][k]),
    "Google": (stock_owned['Google'] * stock_prices['Google'][k]),
    "Microsoft": (stock_owned['Microsoft'] * stock_prices['Microsoft'][k]),
    "Nike": (stock_owned['Nike'] * stock_prices['Nike'][k]),
    "McDonalds": (stock_owned['McDonalds'] * stock_prices['McDonalds'][k]),
    "CocaCola": (stock_owned['CocaCola'] * stock_prices['CocaCola'][k])}

def enter(event):
    event.widget.config(bg=bg)
def leave(event):
    event.widget.config(bg='SystemButtonFace')
def enter_diff(event):
    event.widget.config(relief=RAISED)
def leave_diff(event):
    event.widget.config(relief=SUNKEN)
def enter_exchange(event):
    event.widget.config(bd=5)
def leave_exchange(event):
    event.widget.config(bd=3)

def clear():
    global day_label_ref
    day_label_ref = None
    for widget in window.winfo_children():
        if 'news_log' in globals() and widget == news_log:
            continue
        widget.pack_forget()

def save_settings(settings):
    with open(CONFIG_FILE, "w") as f:
        json.dump(settings, f)

def back():
    if previous_screen:
        back_btn = Button(window, font=('arial', 25, "bold"), text="Back", relief=RIDGE, bd=10, command=previous_screen)
        back_btn.pack(pady=10, anchor='center')
        back_btn.bind("<Enter>", enter)
        back_btn.bind("<Leave>", leave)

def quit():
    sys.exit()

    if previous_screen:
        back_btn = Button(window, font=('arial', 30, "bold"), text="Back", relief=RIDGE, bd=10, command=previous_screen)
        back_btn.pack(pady=10, anchor='center')
        back_btn.bind("<Enter>", enter)
        back_btn.bind("<Leave>", leave)

def Menu():
    global news_log, current_day, play1_flag
    global day_label_ref, plot_flag
    play1_flag = False
    plot_flag = False
    if 'news_log' in globals() and news_log.winfo_exists():
        news_log.destroy()
    window.title("Menu")
    clear()
    Title = Label(window, text="Menu", font=("arial",40,"bold", "underline"), fg=fg, bd=10, relief=FLAT)
    Title.pack()

    Game1 = Button(window, text="Stock Market Simulation", font=("arial",30,"bold"), fg=fg, bd=10, relief=RIDGE, command=Rules)
    Game1.pack(pady=40)
    Game1.bind("<Enter>", enter)
    Game1.bind("<Leave>", leave)

    volume_button = Button(window, text="Volume settings", font=("arial", 30, "bold"), fg=fg, bd=10, relief=RIDGE, command=volume_settings)
    volume_button.pack(pady=30)
    volume_button.bind("<Enter>", enter)
    volume_button.bind("<Leave>", leave)

    rules_button = Button(window, text="Game Rules", font=("arial",30,"bold"), fg=fg, bd=10, relief=RIDGE, command=Rules_perm)
    rules_button.pack(pady=30)
    rules_button.bind("<Enter>", enter)
    rules_button.bind("<Leave>", leave)

    Quit = Button(window, text="Exit", font=("arial",30,"bold"), fg=fg, bd=10, relief=RIDGE, command=quit)
    Quit.pack(pady=30)
    Quit.bind("<Enter>", enter)
    Quit.bind("<Leave>", leave)

def Rules():
    if not game_start:
        clear()

        rules_label = Label(window, font=("arial", 25, "bold"), fg=fg, text='Rules')
        rules_label.pack()

        rules_label1 = Label(window, font=("arial", 15, "bold"), fg=fg, text=bullet_point1)
        rules_label1.pack(pady=20)

        rules_label2 = Label(window, font=("arial", 15, "bold"), fg=fg, text=bullet_point2)
        rules_label2.pack(pady=20)

        rules_label3 = Label(window, font=("arial", 15, "bold"), fg=fg, text=bullet_point3)
        rules_label3.pack(pady=20)

        rules_label4 = Label(window, font=("arial", 15, "bold"), fg=fg, text=bullet_point4)
        rules_label4.pack()

        rules_label_bank= Label(window, font=("arial", 15, "bold"), fg=fg, text=bullet_point_bank)
        rules_label_bank.pack(pady=40)

        rules_label_bank3 = Label(window, font=("arial", 15, "bold"), fg=fg, text=bullet_point_bank3)
        rules_label_bank3.pack(pady=10)

        rules_label5 = Label(window, font=("arial", 15, "bold"), fg=fg, text=bullet_point5)
        rules_label5.pack(pady=30)

        rules_label6 = Label(window, font=("arial", 20, "bold"), fg=fg, text=bullet_point6)
        rules_label6.pack(pady=30)

        ready_button = Button(window, text="Play", font=("arial", 20, "bold"), fg=fg, bd=10, relief=RIDGE, command=Play1)
        ready_button.pack(pady=20)
        ready_button.bind("<Enter>", enter)
        ready_button.bind("<Leave>", leave)
    else:
        Play1()

def stop_music():
    pygame.mixer.music.stop()

def Rules_perm():
    global previous_screen
    previous_screen = Menu
    clear()

    rules_label = Label(window, font=("arial", 25, "bold"), fg=fg, text='Rules')
    rules_label.pack()

    rules_label1 = Label(window, font=("arial", 15, "bold"), fg=fg, text=bullet_point1)
    rules_label1.pack(pady=20)

    rules_label2 = Label(window, font=("arial", 15, "bold"), fg=fg, text=bullet_point2)
    rules_label2.pack(pady=20)

    rules_label3 = Label(window, font=("arial", 15, "bold"), fg=fg, text=bullet_point3)
    rules_label3.pack(pady=20)

    rules_label4 = Label(window, font=("arial", 15, "bold"), fg=fg, text=bullet_point4)
    rules_label4.pack()

    rules_label_bank = Label(window, font=("arial", 15, "bold"), fg=fg, text=bullet_point_bank)
    rules_label_bank.pack(pady=40)

    rules_label_bank3 = Label(window, font=("arial", 15, "bold"), fg=fg, text=bullet_point_bank3)
    rules_label_bank3.pack(pady=10)

    rules_label5 = Label(window, font=("arial", 15, "bold"), fg=fg, text=bullet_point5)
    rules_label5.pack(pady=30)

    back()

def adjust_interest_rates():
    global loan_interest_rate, savings_interest_rate

    direction = random.choice(["up", "down", "hold"])

    if direction == "up":
        loan_interest_rate = min(loan_interest_rate + rate_step, max_rate)
        savings_interest_rate = min(savings_interest_rate + rate_step, loan_interest_rate - 0.001)
        broadcast_news(f"Central Bank raises interest rates! Loans now {loan_interest_rate*100:.1f}%, Savings {savings_interest_rate*100:.1f}%.", "yellow")

    elif direction == "down":
        loan_interest_rate = max(loan_interest_rate - rate_step, savings_interest_rate + 0.001)
        savings_interest_rate = max(savings_interest_rate - rate_step, min_rate)
        broadcast_news(f"Central Bank cuts interest rates! Loans now {loan_interest_rate*100:.1f}%, Savings {savings_interest_rate*100:.1f}%.", "yellow")

    else:
        broadcast_news("Markets steady — interest rates remain unchanged.", "green")

    if loan_interest_rate <= savings_interest_rate:
        loan_interest_rate = savings_interest_rate + 0.001

def Play1():
    global frame, frame_bottom, previous_screen, news_log, bank_state
    global total_balance, table, table_pnl, day_label_ref, bank_button, play1_flag
    global port_image, back_image, current_screen, tree_rows, game_start, bank_image, flag
    play1_flag = True
    current_screen = False
    window.title("Stock Market Simulation")
    previous_screen = Menu
    clear()
    game_start = True

    if flag:
        update_day()
        flag = False

    if 'news_log' not in globals() or not news_log.winfo_exists():
        news_log = Listbox(window, height=10, width=60, bg=bg, fg=fg)
        for i, item in enumerate(news_history):
            news_log.insert(END, item)
            if item in highlighted_news:
                try:
                    news_log.itemconfig(i, fg='green')
                except Exception:
                    try:
                        news_log.itemconfig(i, foreground='green')
                    except Exception:
                        pass
    news_log.pack(side="bottom", fill="x")

    start_frame = Frame(window)
    start_frame.pack()

    frame = Frame(window)
    frame.pack()

    total_balance = Label(start_frame, text=("Current Balance: $" + str(formatted_total)), bd=5, fg=fg, font=('arial',20,'bold'))
    total_balance.pack(side=LEFT)

    day_label_ref = Label(start_frame, text=f"Day: {current_day}", font=('arial', 20, 'bold'), fg=fg)
    day_label_ref.pack(side=RIGHT, padx=10)

    table_frame = Frame(frame)
    table_frame.pack()

    table = ttk.Treeview(table_frame, columns=('name', 'price', 'stocks owned'), show='headings', height=10)
    table.heading('name', text='Stock name')
    table.heading('price', text='Price ($)')
    table.heading('stocks owned', text="Shares owned")
    table.pack(side=LEFT)

    table_pnl = ttk.Treeview(table_frame, columns=('return',), show='headings', height=10)
    table_pnl.heading('return', text='PnL ($)')
    table_pnl.tag_configure('pnl_positive', foreground='green')
    table_pnl.tag_configure('pnl_negative', foreground='red')
    table_pnl.tag_configure('pnl_neutral', foreground='black')
    table_pnl.pack(side=LEFT, padx=5)

    tree_rows = {}
    for stock in stocks:
        tree_rows[stock] = table.insert('', 'end', values=(stock, stock_prices[stock][k], stock_owned[stock]))
        tag = 'pnl_positive' if stock_returns[stock] > 0 else 'pnl_negative' if stock_returns[stock] < 0 else 'pnl_neutral'
        table_pnl.insert('', 'end', iid=stock+"_pnl", values=(stock_returns[stock],), tags=(tag,))

    table.bind('<<TreeviewSelect>>', lambda event: Popup(table.selection()))

    port_image = PhotoImage(file='photo_port_resized.png')
    port_button = Button(start_frame, image=port_image, compound=CENTER, width=75, height=70, relief=SUNKEN, bd=5, command= Port_view)
    port_button.pack(side=LEFT)
    port_button.bind("<Enter>", enter_diff)
    port_button.bind("<Leave>", leave_diff)

    bank_image = PhotoImage(file='47c6b791f81e376fa0259c42b22c066e4222f824a35a9aad031c7ec4079f.png')
    bank_button = Button(start_frame, image=bank_image, compound=CENTER, width=75, height=70, relief=SUNKEN, bd=5, command=Bank, state=bank_state)
    bank_button.pack(side=LEFT)
    bank_button.bind("<Enter>", enter_diff)
    bank_button.bind("<Leave>", leave_diff)

    back_image = PhotoImage(file='OIP_resized.png')
    back_button = Button(start_frame, image=back_image, compound=CENTER, width=75, height=70, relief=SUNKEN, bd=5, command=Menu)
    back_button.pack(side=LEFT)
    back_button.bind("<Enter>", enter_diff)
    back_button.bind("<Leave>", leave_diff)

    news_label = Label(window, text="News log", font=("arial",20,"bold"), fg=fg)
    news_label.pack(side=BOTTOM)

def Bank():
    global stock_image, news_log, port_image, current_screen, total_balance, rates_label, plot_flag
    global day_label_ref, loan_balance, savings_balance, loan_label, savings_label, bank_controls, play1_flag
    current_screen = False
    plot_flag = False
    play1_flag = False
    clear()

    if 'news_log' not in globals() or not news_log.winfo_exists():
        news_log = Listbox(window, height=10, width=60, bg=bg, fg=fg)
        for i, item in enumerate(news_history):
            news_log.insert(END, item)
            if item in highlighted_news:
                try:
                    news_log.itemconfig(i, fg='green')
                except Exception:
                    try:
                        news_log.itemconfig(i, foreground='green')
                    except Exception:
                        pass
    news_log.pack(side="bottom", fill="x")

    bank_frame = Frame(window)
    bank_frame.pack()

    bank_title = Label(bank_frame, font=("arial", 30, "bold"), text="The Bank", fg='green')
    bank_title.pack(side=LEFT)

    stock_image = PhotoImage(file='Stock-Market-Outline-Icon-Graphics-59193762-1 (1)_resized.png')
    stock_button = Button(bank_frame, image=stock_image, compound=CENTER, width=75, height=70, relief=SUNKEN, bd=5, command=Play1)
    stock_button.pack(padx=10, side=LEFT)
    stock_button.bind("<Enter>", enter_diff); stock_button.bind("<Leave>", leave_diff)

    port_button = Button(bank_frame, image=port_image, compound=CENTER, width=75, height=70, relief=SUNKEN, bd=5, command=Port_view)
    port_button.pack(side=LEFT)
    port_button.bind("<Enter>", enter_diff); port_button.bind("<Leave>", leave_diff)

    day_label_ref = Label(bank_frame, text=f"Day: {current_day}", font=('arial', 20, 'bold'), fg=fg)
    day_label_ref.pack(side=RIGHT, padx=10)

    formatted_total = format(int(total), ',')
    total_balance = Label(window, text=("Current Balance: $" + str(formatted_total)), bd=5, fg=fg, font=('arial', 30, 'bold'))
    total_balance.pack(pady=20)

    balances_frame = Frame(window)
    balances_frame.pack(pady=20)

    loan_label = Label(balances_frame, text=f"Loan Balance: ${loan_balance:,.2f}", font=("arial", 18, "bold"), fg="red")
    loan_label.pack(pady=5)

    savings_label = Label(balances_frame, text=f"Savings Balance: ${savings_balance:,.2f}", font=("arial", 18, "bold"), fg="blue")
    savings_label.pack(pady=5)

    rates_label = Label(window, text=f"Loan Rate: {loan_interest_rate * 100:.1f}%  |  Savings Rate: {savings_interest_rate * 100:.1f}%", font=("arial", 15, "bold"), fg="orange")
    rates_label.pack(pady=10)
    update_rates_label()
    try:
        rates_label.after(500, lambda: rates_label.config(
            text=f"Loan Rate: {loan_interest_rate * 100:.1f}%  |  Savings Rate: {savings_interest_rate * 100:.1f}%"
        ))
    except Exception:
        pass

    bank_controls = Frame(window)
    bank_controls.pack(pady=20)

    Button(bank_controls, text="Borrow $1000", font=("arial", 15, "bold"), fg="red",
           command=lambda: borrow_money(1000)).grid(row=0, column=0, padx=10, pady=5)
    Button(bank_controls, text="Borrow MAX", font=("arial", 15, "bold"), fg="red",
           command=borrow_money_max).grid(row=0, column=1, padx=10, pady=5)

    Button(bank_controls, text="Repay $1000", font=("arial", 15, "bold"), fg="green",
           command=lambda: repay_money(1000)).grid(row=0, column=2, padx=10, pady=5)
    Button(bank_controls, text="Repay MAX", font=("arial", 15, "bold"), fg="green",
           command=repay_money_max).grid(row=0, column=3, padx=10, pady=5)

    Button(bank_controls, text="Deposit $1000", font=("arial", 15, "bold"), fg="blue",
           command=lambda: deposit_money(1000)).grid(row=1, column=0, padx=10, pady=10)
    Button(bank_controls, text="Deposit MAX", font=("arial", 15, "bold"), fg="blue",
           command=deposit_money_max).grid(row=1, column=1, padx=10, pady=10)

    Button(bank_controls, text="Withdraw $1000", font=("arial", 15, "bold"), fg="purple",
           command=withdraw_money_1000).grid(row=1, column=2, padx=10, pady=10)
    Button(bank_controls, text="Withdraw MAX", font=("arial", 15, "bold"), fg="purple",
           command=withdraw_money_max).grid(row=1, column=3, padx=10, pady=10)

    news_label = Label(window, text="News log", font=("arial",20,"bold"), fg=fg)
    news_label.pack(side=BOTTOM)

#-----------------------------------------
def borrow_money_max():
    global loan_balance, total, formatted_total, savings_balance, loan_limit

    net_portfolio_value = total + savings_balance - loan_balance
    loan_limit = max(1000, int(net_portfolio_value * 0.5))

    amount = loan_limit - loan_balance
    if amount > 0:
        loan_balance += amount
        total += amount
        loan_balance = int(loan_balance); savings_balance = int(savings_balance); total = int(total)
        formatted_total = format(total, ',')
        try:
            total_balance.config(text=f"Current Balance: ${formatted_total}")
            if 'loan_label' in globals() and loan_label.winfo_exists():
                loan_label.config(text=f"Loan Balance: ${loan_balance:,.2f}")
        except Exception:
            pass
    else:
        broadcast_news("Bank refused your loan request (limit reached).", "red")

def repay_money_max():
    global loan_balance, total, formatted_total, savings_balance
    if loan_balance > 0 and total > 0:
        repayment = min(loan_balance, total)
        total -= repayment
        loan_balance -= repayment
        loan_balance = int(loan_balance); savings_balance = int(savings_balance); total = int(total)
        formatted_total = format(total, ',')
        try:
            total_balance.config(text=f"Current Balance: ${formatted_total}")
            if 'loan_label' in globals() and loan_label.winfo_exists():
                loan_label.config(text=f"Loan Balance: ${loan_balance:,.2f}")
        except Exception:
            pass
    else:
        broadcast_news("Cannot repay: insufficient funds or no loan.", "red")

def deposit_money_max():
    global savings_balance, total, formatted_total, loan_balance
    if total > 0:
        amount = int(total)
        total -= amount
        savings_balance += amount
        loan_balance = int(loan_balance); savings_balance = int(savings_balance); total = int(total)
        formatted_total = format(total, ',')
        try:
            total_balance.config(text=f"Current Balance: ${formatted_total}")
            if 'savings_label' in globals() and savings_label.winfo_exists():
                savings_label.config(text=f"Savings Balance: ${savings_balance:,.2f}")
        except Exception:
            pass
    else:
        broadcast_news("Not enough cash to deposit.", "red")

def withdraw_money_max(amount=None):
    global savings_balance, total, formatted_total
    if savings_balance > 0:
        if amount is None or amount > savings_balance:
            amount = int(savings_balance)

        savings_balance -= amount
        total += amount

        savings_balance = int(savings_balance)
        total = int(total)

        formatted_total = format(total, ',')
        total_balance.config(text=f"Current Balance: ${formatted_total}")
        if 'savings_label' in globals():
            savings_label.config(text=f"Savings Balance: ${savings_balance:,}")
    else:
        broadcast_news("No savings to withdraw.", "red")
#--------------------------------------------------
def update_day():
    global current_day, k, day_arr, current_screen, stock_prices, stock_trends, news_effects, table, bank_state, bank_button, bank_flag, loan_balance, savings_balance
    global day_arr2, stock_prices_plot, plot_flag, current_stock
    current_day += 1
    new_port_value()
    day_arr.append(current_day)

    if current_screen:
        piechart()
    if day_label_ref:
        day_label_ref.config(text=f"Day: {current_day}")

    window.after(8000, update_day)
    if current_day > 4:
        for stock in stocks:
            drift = stock_trends[stock] + random.randint(-5, 5)

            if stock in news_effects:
                news_drift, days_left = news_effects[stock]
                drift += int(round(news_drift))
                days_left -= 1
                if days_left <= 0:
                    del news_effects[stock]
                else:
                    news_effects[stock] = (news_drift, days_left)

            if drift == 0 and random.random() < 0.8:
                drift = random.choice([-1, 1])

            old_price = stock_prices[stock][k]
            new_price = old_price + drift

            if drift < 0 and old_price < 20:
                new_price = old_price + int(drift / 2)

            avg_price = sum(stock_prices[stock]) / len(stock_prices[stock])
            min_floor = max(5, int(avg_price * 0.25))
            new_price = max(min_floor, new_price)

            stock_prices[stock].append(int(new_price))

        if loan_balance > 0:
            loan_balance *= (1 + loan_interest_rate)
        if savings_balance > 0:
            savings_balance *= (1 + savings_interest_rate)
        loan_balance = int(loan_balance)
        savings_balance = int(savings_balance)
        try:
            if 'loan_label' in globals() and loan_label.winfo_exists():
                loan_label.config(text=f"Loan Balance: ${loan_balance:,.2f}")
            if 'savings_label' in globals() and savings_label.winfo_exists():
                savings_label.config(text=f"Savings Balance: ${savings_balance:,.2f}")
        except Exception:
            pass

        net_worth = total + savings_balance - loan_balance
        portfolio_history.append(net_worth)

        if len(portfolio_history) > 1:
            daily_change = portfolio_history[-1] - portfolio_history[-2]
        else:
            daily_change = 0
        gains_losses_history.append(daily_change)

        k += 1
        for stock in stocks:
            stock_prices_plot[stock].append(stock_prices[stock][k])
        new_returns()

        for stock in stocks:
            update_table_row(stock)
    else:
        if current_day > 1:
            for stock in stocks:
                stock_prices_plot[stock].append(stock_prices[stock][k])
    if current_day > 9:
        if bank_flag:
            bank_button.config(state=NORMAL)
            bank_state = NORMAL
            bank_flag = False
            news_log.insert(0, "BANK OPEN! You can now use the Bank.")
            news_log.itemconfig(0, fg="green")

    if current_day % 10 == 0:
        apply_news()

    if current_day % 30 == 0:
        pay_dividends()

    if current_day > 10 and current_day % 5 == 0 and current_day % 10 != 0:
        adjust_interest_rates()
    day_arr2.append(current_day)
    if plot_flag:
        Plot_stock(current_stock)

def borrow_money(amount):
    global loan_balance, total, formatted_total, savings_balance
    if loan_balance + amount <= loan_limit:
        loan_balance += amount
        total += amount
        loan_balance = int(loan_balance)
        savings_balance = int(savings_balance)
        total = int(total)
        formatted_total = format(total, ',')
        total_balance.config(text=f"Current Balance: ${formatted_total}")
        if 'loan_label' in globals():
            loan_label.config(text=f"Loan Balance: ${loan_balance:,.2f}")
    else:
        broadcast_news("Bank refused your loan request (limit reached).", "red")

def new_port_value():
    global port_value
    pve = 0
    for stock in stocks:
        pve += (stock_owned[stock] * stock_prices[stock][k])
    pve += total
    pve += savings_balance
    port_value.append(pve)

def repay_money(amount):
    global loan_balance, total, formatted_total, savings_balance
    if total >= amount and loan_balance > 0:
        repayment = min(amount, loan_balance)
        total -= repayment
        total = int(total)
        loan_balance -= repayment
        loan_balance = int(loan_balance)
        savings_balance = int(savings_balance)
        total = int(total)
        formatted_total = format(total, ',')
        total_balance.config(text=f"Current Balance: ${formatted_total}")
        if 'loan_label' in globals():
            loan_label.config(text=f"Loan Balance: ${loan_balance:,.2f}")
    else:
        broadcast_news("Cannot repay: insufficient funds or no loan.", "red")

def deposit_money(amount):
    global savings_balance, total, formatted_total, savings_balance, loan_balance
    if total >= amount:
        total -= amount
        savings_balance += amount
        loan_balance = int(loan_balance)
        savings_balance = int(savings_balance)
        total = int(total)
        formatted_total = format(total, ',')
        total_balance.config(text=f"Current Balance: ${formatted_total}")
        if 'savings_label' in globals():
            savings_label.config(text=f"Savings Balance: ${savings_balance:,.2f}")
    else:
        broadcast_news("Not enough cash to deposit.", "red")

def apply_news():
    global stock_trends, news_effects

    news_today = random.sample(news_events, k=random.choice([1, 2]))

    for news in news_today:
        entry = f"Day {current_day}: {news['headline']}"
        news_history.insert(0, entry)
        if news_log.winfo_exists():
            news_log.insert(0, entry)

        for stock, change in news["impact"].items():
            target_stocks = [stock] if stock != "all" else stocks
            for s in target_stocks:
                daily_change = change / 5
                if s in news_effects:
                    existing_change, days_left = news_effects[s]
                    news_effects[s] = (existing_change + daily_change, max(days_left, 5))
                else:
                    news_effects[s] = (daily_change, 5)

def update_table_row(stock_id):
    if stock_owned[stock_id] > 0:
        pnl = (stock_owned[stock_id] * stock_prices[stock_id][k]) - purchase_history[stock_id]
        pnl = int(round(pnl))
    else:
        pnl = 0
    stock_returns[stock_id] = pnl
    try:
        if 'table' in globals() and table.winfo_exists():
            table.item(tree_rows[stock_id], values=(stock_id, stock_prices[stock_id][k], stock_owned[stock_id]))
        if 'table_pnl' in globals() and table_pnl.winfo_exists():
            tag = 'pnl_positive' if pnl > 0 else 'pnl_negative' if pnl < 0 else 'pnl_neutral'
            table_pnl.item(stock_id + "_pnl", values=(pnl,), tags=(tag,))
    except Exception:
        pass
    try:
        if 'table_port' in globals() and table_port.winfo_exists():
            stock_values[stock_id] = stock_owned[stock_id] * stock_prices[stock_id][k]
            table_port.item(tree_port_rows[stock_id], values=(stock_id, stock_owned[stock_id], stock_values[stock_id]))
        if 'table_port_pnl' in globals() and table_port_pnl.winfo_exists():
            tag2 = 'pnl_positive' if pnl > 0 else 'pnl_negative' if pnl < 0 else 'pnl_neutral'
            table_port_pnl.item(stock_id + "_port_pnl", values=(pnl,), tags=(tag2,))
    except Exception:
        pass

def broadcast_news(msg, color=None):
    news_history.insert(0, msg)

    if 'news_log' in globals() and news_log.winfo_exists():
        news_log.insert(0, msg)
        if color:
            try:
                news_log.itemconfig(0, fg=color)
            except Exception:
                try:
                    news_log.itemconfig(0, foreground=color)
                except Exception:
                    pass

def new_returns():
    for stock in stocks:
        if stock_owned[stock] > 0:
            pnl = (stock_owned[stock] * stock_prices[stock][k]) - purchase_history[stock]
            stock_returns[stock] = pnl if pnl != 0 else 0
        else:
            stock_returns[stock] = 0

def Port_view():
    global previous_screen, stock_image, stock_values, bank_image, bank_state, bank_button, play1_flag
    global day_label_ref, table_port, table_port_pnl, current_screen, tree_port_rows, plot_flag
    play1_flag = False
    plot_flag = False
    previous_screen = Play1
    current_screen = True
    clear()

    update_stock_values()

    port_frame = Frame(window)
    port_frame.pack()

    port_title = Label(port_frame, font=("arial",30,"bold"), text="Portfolio Overview", fg=fg)
    port_title.pack(padx=10, side=LEFT)

    stock_image = PhotoImage(file='Stock-Market-Outline-Icon-Graphics-59193762-1 (1)_resized.png')
    stock_button = Button(port_frame, image=stock_image, compound=CENTER, width=75, height=70, relief=SUNKEN, bd=5, command=Play1)
    stock_button.pack(padx=10, side=LEFT)
    stock_button.bind("<Enter>", enter_diff)
    stock_button.bind("<Leave>", leave_diff)

    bank_button = Button(port_frame, image=bank_image, compound=CENTER, width=75, height=70, relief=SUNKEN, bd=5, command=Bank, state=bank_state)
    bank_button.pack(side=LEFT)
    bank_button.bind("<Enter>", enter_diff)
    bank_button.bind("<Leave>", leave_diff)

    day_label_ref = Label(port_frame, text=f"Day: {current_day}", font=('arial', 20, 'bold'), fg=fg)
    day_label_ref.pack(side=RIGHT, padx=10)

    port_table_frame = Frame(window)
    port_table_frame.pack()

    table_port = ttk.Treeview(port_table_frame, columns=('name', 'stocks owned','Balance'), show='headings', height=10)
    table_port.heading('name', text='Stock name')
    table_port.heading('stocks owned', text='Shares owned')
    table_port.heading('Balance', text='Balance ($)')
    table_port.pack(side=LEFT)

    table_port_pnl = ttk.Treeview(port_table_frame, columns=('return',), show='headings', height=10)
    table_port_pnl.heading('return', text='PnL ($)')
    table_port_pnl.tag_configure('pnl_positive', foreground='green')
    table_port_pnl.tag_configure('pnl_negative', foreground='red')
    table_port_pnl.tag_configure('pnl_neutral', foreground='black')
    table_port_pnl.pack(side=LEFT, padx=5)

    tree_port_rows = {}
    for stock in stocks:
        stock_values[stock] = stock_owned[stock] * stock_prices[stock][k]
        tree_port_rows[stock] = table_port.insert('', 'end', values=(stock, stock_owned[stock], stock_values[stock]))
        tag = 'pnl_positive' if stock_returns[stock] > 0 else 'pnl_negative' if stock_returns[stock] < 0 else 'pnl_neutral'
        table_port_pnl.insert('', 'end', iid=stock+"_port_pnl", values=(stock_returns[stock],), tags=(tag,))
    news_label = Label(window, text="News log", font=("arial", 20, "bold"), fg=fg)

    news_label.pack(side=BOTTOM)
    piechart()

    news_log.pack(side="bottom", fill="x")

def piechart():
    global canvas, hint_label, portfolio_history, canvas2, port_value, day_arr2, EL
    if canvas:
        canvas.get_tk_widget().destroy()
        canvas = None
    if hint_label:
        hint_label.destroy()
        hint_label = None
    if EL != None:
        EL.forget()
        EL = None
    if canvas2:
        canvas2.get_tk_widget().destroy()
        canvas2 = None

    matplotlib.use("TkAgg")
    fig = Figure(figsize=(3, 3), dpi=100)
    ax = fig.add_subplot(111)

    labels = ["Apple", "Tesla", "Amazon", "JPMorgan", "Pfizer", "Google", "Microsoft", "Nike", "McDonalds", "CocaCola"]
    sizes = [stock_owned[s] * stock_prices[s][k] for s in labels]  # Dynamic calc

    count = sum(1 for s in sizes if s > 0)

    if count > 0:
        filtered = [(label, size) for label, size in zip(labels, sizes) if size > 0]
        labels_filtered, sizes_filtered = zip(*filtered)

        ax.pie(sizes_filtered, labels=labels_filtered, autopct="%.1f%%", pctdistance=0.7, startangle=90)
        ax.set_title("Stock Diversification (By value)")

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().pack(pady=20, padx=10, side=LEFT)
        canvas.draw()
#----------------------------------------------------------
        fig2 = Figure(figsize=(5, 3), dpi=100)
        plot = fig2.add_subplot(111)
        plot.set_title("Portfolio Value Over Time")
        plot.set_xlabel("Day")
        plot.set_ylabel("Portfolio Value ($)")

        import matplotlib.ticker as mtick
        plot.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

        plot.plot(day_arr, port_value, marker='o', markersize=4, linestyle='-',
                  linewidth=1.5, color='blue', label='Portfolio Value')

        plot.grid(True, linestyle='--', alpha=0.6)

        fig2.tight_layout()
        plot.legend(loc='upper left')

        canvas2 = FigureCanvasTkAgg(fig2, master=window)
        canvas2.draw()
        canvas2_widget = canvas2.get_tk_widget()
        canvas2_widget.pack(pady=20, side=RIGHT, fill=BOTH, expand=True)
    else:
        hint_label = Label(window, text="You own 0 shares", fg=fg, font=("arial", 30, "bold"))
        hint_label.pack(pady=20)

def Popup(ID):
    global alert_label
    global alert_label_buy
    if alert_label != None:
        alert_label.forget()
        alert_label = None
    if alert_label_buy != None:
        alert_label_buy.forget()
        alert_label_buy = None
    ID = ID[0]
    if  ID == 'I001':
        ID = 'Apple'
    elif ID == 'I002':
        ID = 'Tesla'
    elif ID == 'I003':
        ID = 'Amazon'
    elif ID == 'I004':
        ID = 'JPMorgan'
    elif ID == 'I005':
        ID = 'Pfizer'
    elif ID == 'I00A':
        ID = 'CocaCola'
    elif ID == 'I009':
        ID = 'McDonalds'
    elif ID == 'I008':
        ID = 'Nike'
    elif ID == 'I007':
        ID = 'Microsoft'
    elif ID == 'I006':
        ID = 'Google'
    Stock_ID(ID)

def withdraw_money_1000():
    global savings_balance, total, formatted_total, loan_balance
    if savings_balance >= 1000:
        savings_balance -= 1000
        total += 1000
        loan_balance = int(loan_balance); savings_balance = int(savings_balance); total = int(total)
        formatted_total = format(total, ',')
        try:
            total_balance.config(text=f"Current Balance: ${formatted_total}")
            if 'savings_label' in globals() and savings_label.winfo_exists():
                savings_label.config(text=f"Savings Balance: ${savings_balance:,.2f}")
        except Exception:
            pass
    else:
        broadcast_news("Not enough savings to withdraw $1000.", "red")

def Stock_ID(ID):
    global stock_show
    global stock_buy
    global stock_sell, stock_buyten
    global stock_sellall, stock_sellten
    global hide_button
    global frame, trade_back
    global stock_buymax
    global frame_bottom
    global graph_button
    global canvas3, plot_flag
    plot_flag = False
    if canvas3:
        canvas3.get_tk_widget().destroy()
        canvas3 = None
    if stock_show != None:
        stock_show.forget()
    if stock_sellten != None:
        stock_sellten.forget()
    if stock_buyten != None:
        stock_buyten.forget()
    if stock_buy != None:
        stock_buy.forget()
    if stock_sell != None:
        stock_sell.forget()
    if hide_button != None:
        hide_button.forget()
    if stock_buymax != None:
        stock_buymax.forget()
    if stock_sellall != None:
        stock_sellall.forget()
    if graph_button != None:
        graph_button.forget()
    if frame_bottom != None:
        frame_bottom.forget()
    if trade_back != None:
        trade_back.forget()

    if play1_flag:
        frame_bottom = Frame(window)
        frame_bottom.pack()

        stock_show = Label(frame, font=('arial', 30, 'bold'), text=(ID+":"), fg=fg)
        stock_show.pack(pady=30, padx=40, side=LEFT)

        stock_buy = Button(frame_bottom, font=('arial',15,'bold'), text='Buy 1', fg='green', relief=RIDGE, bd=10, command=lambda: Stock_buy(ID))
        stock_buy.pack(padx=10, side=LEFT)
        stock_buy.bind("<Enter>", enter)
        stock_buy.bind("<Leave>", leave)

        stock_buyten = Button(frame_bottom, font=('arial', 15, 'bold'), text='Buy 10', fg='green', relief=RIDGE, bd=10, command=lambda: Stock_buyten(ID))
        stock_buyten.pack(padx=10, side=LEFT)
        stock_buyten.bind("<Enter>", enter)
        stock_buyten.bind("<Leave>", leave)

        stock_buymax = Button(frame_bottom, font=('arial',15,'bold'), text='Buy Max', fg='green', relief=RIDGE, bd=10, command=lambda: Stock_buymax(ID))
        stock_buymax.pack(padx=10, side=LEFT)
        stock_buymax.bind("<Enter>", enter)
        stock_buymax.bind("<Leave>", leave)

        stock_sell = Button(frame_bottom, font=('arial',15,'bold'), text='Sell 1', fg='red', relief=RIDGE, bd=10, command=lambda: Stock_sell(ID))
        stock_sell.pack(padx=10, side=LEFT)
        stock_sell.bind("<Enter>", enter)
        stock_sell.bind("<Leave>", leave)

        stock_sellten = Button(frame_bottom, font=('arial', 15, 'bold'), text='Sell 10', fg='red', relief=RIDGE, bd=10, command=lambda: Stock_sellten(ID))
        stock_sellten.pack(padx=10, side=LEFT)
        stock_sellten.bind("<Enter>", enter)
        stock_sellten.bind("<Leave>", leave)

        stock_sellall = Button(frame_bottom, font=('arial', 15,'bold'), text='Sell All', fg='red', relief=RIDGE, bd=10, command=lambda: Stock_sellall(ID))
        stock_sellall.pack(padx=10, side=LEFT)
        stock_sellall.bind("<Enter>", enter)
        stock_sellall.bind("<Leave>", leave)

        hide_button = Button(frame_bottom, font=('arial',10,'bold'), text='X', fg='black', relief=RAISED, bd=5, command=lambda: Hide())
        hide_button.pack(padx=20, side=LEFT)
        hide_button.bind("<Enter>", enter)
        hide_button.bind("<Leave>", leave)

        graph_button = Button(window, font=('arial',15,'bold'), text='Show ' + ID + ' stock history', fg=fg, relief=RAISED, bd=5, command=lambda: Plot_stock(ID))
        graph_button.pack(pady=40, side=BOTTOM)
        graph_button.bind("<Enter>", enter)
        graph_button.bind("<Leave>", leave)

def Plot_stock(ID):
    global canvas3, day_arr2, stock_prices_plot, frame_bottom, current_stock, plot_flag, trade_back
    if canvas3:
        canvas3.get_tk_widget().destroy()
        canvas3 = None
    if trade_back != None:
        trade_back.forget()
    plot_flag = True
    current_stock = ID
    Hide()
    if frame_bottom != None:
        frame_bottom.forget()
    fig3 = Figure(figsize=(6, 3), dpi=100)
    plot = fig3.add_subplot(111)
    plot.set_title(ID + " stock history")
    plot.set_xlabel("Day")
    plot.set_ylabel("Share price ($)")

    import matplotlib.ticker as mtick
    plot.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

    plot.plot(day_arr2, stock_prices_plot[ID], marker='o', markersize=4, linestyle='-',
              linewidth=1.5, color='blue', label='Share price')

    plot.grid(True, linestyle='--', alpha=0.6)

    fig3.tight_layout()
    plot.legend(loc='upper left')

    canvas3 = FigureCanvasTkAgg(fig3, master=window)
    canvas3.draw()
    canvas3_widget = canvas3.get_tk_widget()
    canvas3_widget.pack(pady=20, side=RIGHT, fill=BOTH, expand=True)

    trade_back = Button(window, command=lambda: Stock_ID(ID), font=("arial",20,"bold"), bg='red', relief=SUNKEN, text="<", fg="white")
    trade_back.pack(pady=100)
    trade_back.bind("<Enter>", enter_diff)
    trade_back.bind("<Leave>", leave_diff)

def Stock_buy(ID):
    global alert_label, alert_label_buy, total, formatted_total
    if alert_label:
        alert_label.forget()
        alert_label = None
    if total >= stock_prices[ID][k]:
        total -= stock_prices[ID][k]
        stock_owned[ID] += 1
        purchase_history[ID] += stock_prices[ID][k]
        formatted_total = format(total, ',')
        total_balance.config(text=f"Current Balance: ${formatted_total}")
        update_table_row(ID)
    else:
        if not alert_label_buy:
            alert_label_buy = Label(window, text="Cannot afford this stock", fg='red', font=("arial", 20, "bold"))
            alert_label_buy.pack(pady=10)

def Stock_buyten(ID):
    global alert_label, alert_label_buy, total, formatted_total
    if alert_label:
        alert_label.forget()
        alert_label = None

    shares_to_buy = 10
    price_per_share = stock_prices[ID][k]

    affordable_shares = min(shares_to_buy, total // price_per_share)

    if affordable_shares > 0:
        total_cost = price_per_share * affordable_shares
        total -= total_cost
        stock_owned[ID] += affordable_shares
        purchase_history[ID] += total_cost
        formatted_total = format(total, ',')
        total_balance.config(text=f"Current Balance: ${formatted_total}")
        update_table_row(ID)
    else:
        if not alert_label_buy:
            alert_label_buy = Label(window, text="Cannot afford this stock", fg='red', font=("arial", 20, "bold"))
            alert_label_buy.pack(pady=10)

def Stock_sellten(ID):
    global alert_label, alert_label_buy, total, formatted_total, purchase_history, sale_history
    if alert_label_buy:
        alert_label_buy.forget()
        alert_label_buy = None

    if stock_owned[ID] > 0:
        shares_to_sell = min(10, stock_owned[ID])

        curr_price = stock_prices[ID][k]
        avg_cost = purchase_history[ID] / stock_owned[ID] if stock_owned[ID] else 0.0

        total += curr_price * shares_to_sell
        sale_history[ID] += curr_price * shares_to_sell

        stock_owned[ID] -= shares_to_sell
        purchase_history[ID] -= avg_cost * shares_to_sell

        if stock_owned[ID] == 0:
            purchase_history[ID] = 0
        else:
            purchase_history[ID] = float(purchase_history[ID])

        formatted_total = format(int(total), ',')
        total_balance.config(text=f"Current Balance: ${formatted_total}")
        update_table_row(ID)
    else:
        if not alert_label:
            alert_label = Label(window, text="You own zero of this stock", fg='red', font=("arial", 20, "bold"))
            alert_label.pack(pady=10)

def Stock_buymax(ID):
    global alert_label, alert_label_buy, total, formatted_total
    if alert_label:
        alert_label.forget()
        alert_label = None
    if total >= stock_prices[ID][k]:
        qty = total // stock_prices[ID][k]
        total -= qty * stock_prices[ID][k]
        stock_owned[ID] += qty
        purchase_history[ID] += qty * stock_prices[ID][k]
        formatted_total = format(total, ',')
        total_balance.config(text=f"Current Balance: ${formatted_total}")
        update_table_row(ID)
    else:
        if not alert_label_buy:
            alert_label_buy = Label(window, text="Cannot afford this stock", fg='red', font=("arial", 20, "bold"))
            alert_label_buy.pack(pady=10)

def Stock_sellall(ID):
    global total, formatted_total
    global alert_label, alert_label_buy, sale_history
    if alert_label_buy:
        alert_label_buy.forget()
        alert_label_buy = None
    if stock_owned[ID] > 0:
        sale_value = stock_owned[ID] * stock_prices[ID][k]
        sale_history[ID] += sale_value
        total += sale_value
        stock_owned[ID] = 0
        formatted_total = format(total, ',')
        total_balance.config(text=("Current Balance: $" + str(formatted_total)))
        update_table_row(ID)
        purchase_history[ID] = 0
    else:
        if not alert_label:
            alert_label = Label(window, text="You own zero of this stock", fg='red', font=("arial", 20, "bold"))
            alert_label.pack(pady=10)

def update_rates_label():
    global rates_label
    if rates_label and rates_label.winfo_exists():
        rates_label.config(
            text=f"Loan Rate: {loan_interest_rate*100:.1f}%  |  Savings Rate: {savings_interest_rate*100:.1f}%"
        )
        rates_label.after(1000, update_rates_label)

def Stock_sell(ID):
    global alert_label, alert_label_buy, total, formatted_total, purchase_history, sale_history
    if alert_label_buy:
        alert_label_buy.forget()
        alert_label_buy = None

    if stock_owned[ID] > 0:
        curr_price = stock_prices[ID][k]
        avg_cost = purchase_history[ID] / stock_owned[ID] if stock_owned[ID] else 0.0

        total += curr_price
        sale_history[ID] += curr_price

        stock_owned[ID] -= 1
        purchase_history[ID] -= avg_cost

        if stock_owned[ID] == 0:
            purchase_history[ID] = 0
        else:
            purchase_history[ID] = float(purchase_history[ID])

        formatted_total = format(int(total), ',')
        total_balance.config(text=f"Current Balance: ${formatted_total}")
        update_table_row(ID)
    else:
        if not alert_label:
            alert_label = Label(window, text="You own zero of this stock", fg='red', font=("arial", 20, "bold"))
            alert_label.pack(pady=10)

def update_stock_values():
    for stock in stock_owned:
        stock_values[stock] = stock_owned[stock] * stock_prices[stock][k]

def Hide():
    global alert_label
    global stock_show
    global stock_buy
    global stock_sell, trade_back
    global alert_label_buy
    global hide_button, graph_button
    global stock_sellall, stock_sellten
    global stock_buymax, stock_buyten
    if alert_label != None:
        alert_label.forget()
        alert_label = None
    if alert_label_buy != None:
        alert_label_buy.forget()
        alert_label_buy = None
    if stock_show != None:
        stock_show.forget()
    if stock_buy != None:
        stock_buy.forget()
    if stock_buyten != None:
        stock_buyten.forget()
    if stock_sellten != None:
        stock_sellten.forget()
    if stock_sell != None:
        stock_sell.forget()
    if hide_button != None:
        hide_button.forget()
    if stock_sellall != None:
        stock_sellall.forget()
    if stock_buymax != None:
        stock_buymax.forget()
    if graph_button != None:
        graph_button.forget()
    if trade_back != None:
        trade_back.forget()

def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)
    save_settings({"volume": volume})

def volume_settings():
    global previous_screen
    clear()
    previous_screen = Menu

    v_title = Label(window, text="Volume settings", font=("arial",30,"bold"), fg=fg)
    v_title.pack()

    vol_frame = Frame(window)
    vol_frame.pack(pady=10)

    min_label = Label(vol_frame, text="0", font=("arial",20,"bold"))
    min_label.pack(side="left", padx=5)

    volume_slider = Scale(vol_frame, from_=0, to=100, orient="horizontal", command=set_volume, length=300,
                         font=("Arial", 12, 'bold'), sliderlength=20, showvalue=TRUE, width=25)
    volume_slider.set(int(settings["volume"] * 100))
    volume_slider.pack(pady=100, side=LEFT)

    max_label = Label(vol_frame, text="100", font=("arial",20,"bold"))
    max_label.pack(side="left", padx=5)

    back()

def load_settings():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"volume": 0.5}

def pay_dividends():
    global total, formatted_total, news_log
    dividend_yields = {
        "Apple": 0.006,
        "Tesla": 0.0,
        "Amazon": 0.0,
        "JPMorgan": 0.03,
        "Pfizer": 0.025,
        "Google": 0.0,
        "Microsoft": 0.01,
        "Nike": 0.012,
        "McDonalds": 0.02,
        "CocaCola": 0.03
    }
    periods_per_year = 4

    dividend_income = 0
    for stock in stocks:
        if stock_owned[stock] > 0 and dividend_yields[stock] > 0:
            stock_prices[stock][k] = stock_prices[stock][-1]
            payout = stock_owned[stock] * stock_prices[stock][k] * (dividend_yields[stock] / periods_per_year)
            dividend_income += payout

    if dividend_income > 0:
        total += int(dividend_income)
        formatted_total = format(total, ',')
        try:
            total_balance.config(text=f"Current Balance: ${formatted_total}")
        except Exception:
            pass

        news_log.insert(0, f"Dividend payout received: ${int(dividend_income):,}")
        news_log.itemconfig(0, fg="blue")

pygame.mixer.init()
pygame.mixer.music.load("soft-calm-background-music-374964.mp3")
settings = load_settings()
pygame.mixer.music.set_volume(settings["volume"])
pygame.mixer.music.play(-1)
Menu()

window.mainloop()