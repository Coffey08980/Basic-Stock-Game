import pandas as pd
import datetime as dt
import PySimpleGUI as sg

height = 400
width = 800

prices = pd.read_csv("prices.csv", index_col="Date", parse_dates=True)

today = dt.date(2000, 1, 3)
enddate = dt.date(2019, 12, 31)
tickers = []
transactionid = 0
money = 10000
worth = 0
portfolio = []

buycost = 00.00
sellcost = 00.00

df = pd.read_csv("prices.csv")
tickers = df.columns.tolist()
tickers.pop(0)


def getprice(date, ticker):
    try:
        global prices
        return prices.loc[date][ticker]
    except:
        return 0

def buy(date, ticker, amount):#buy stocks
    price = getprice(date, ticker)
    if price == 0:
        print("Transaction Error")
    else:
        cost = price * amount
        global money
        global portfolio
        holding = []
        if (money - cost >= 0):
            money -= cost
            if any(ticker in holding for holding in portfolio): #documenting and adding it to portfolio
                for i in portfolio:
                    for j in i:
                        try:
                            if j == ticker:
                                i[1] += amount
                        except:
                            print("Error Finding Ticker")
    
            else:
                holding.append(ticker)
                holding.append(amount)
                portfolio.append(holding)
        else:
            sg.popup("Not enough money to buy")
    
def sell(date, ticker, amount):
    price = getprice(date, ticker)
    if price == 0:
        print("Transaction Error")
    else:    
        cost = price * amount
        global money 
        if any(ticker in holding for holding in portfolio): #documenting and adding it to portfolio
            for i in portfolio:
                for j in i:
                    try:
                        if j == ticker:
                            i[1] -= amount
                            if (i[1] == 0):
                                money += cost
                                portfolio.remove(i)
                            elif (i[1] < 0):
                                sg.popup("Too many shares in attempted sell")
                    except:
                        print("Error Finding Ticker")

        else:
            print("Nothing to Sell")    

def checkworth():
    global money
    global worth
    global portfolio
    global today
    worth = money
    try:
        for i in portfolio:
            if getprice(today, i[0]) == 0:
                worth = "Close"
            else:
                worth += ((getprice(today, i[0]))*(i[1]))
    except:
        print("Checkworth issue")

sg.theme('Dark Grey 7')

def make_window1():
    global today
    layout = [
        [sg.Text("Today is:", justification='left'), sg.Text(today, key='-CURRENTDATE-')],
        [sg.Text("Current Account Money:", justification='left'), sg.Text(money, key='-MONEY-')],
        [sg.Text("Current Account Worth:", justification='left'), sg.Text(worth, key='-WORTH-')],
        [sg.Button("Go Forward 1 Day", size=(20, 2), disabled=False, key='-1DAY-'),
         sg.Button("Go Forward 7 Days", size=(20, 2), disabled=False, key='-7DAY-'),
         sg.Button("Go Forward 30 Days", size=(20, 2), disabled=False, key='-30DAY-'),
         sg.Button("Go Forward 365 Days", size=(20, 2), disabled=False, key='-365DAY-')],
        [sg.Text('_'*width)],
        [sg.Button("Show Portfolio", size=(20,2), key='-PORTFOLIO-')],
        [sg.Text('_'*width)],
        [sg.Button("Buy", size=(20, 2), disabled=False, key='-BUY-'),
         sg.Button("Sell", size=(20, 2), disabled=False, key='-SELL-')],
        [sg.Text('_'*width)],
        [sg.Button("Close", size=(20, 2), key='-CLOSE-')]
        ]
    return sg.Window('Stock Game', layout, size = (width,height), finalize=True)

def make_window2():
    layout = [
        [sg.Text("Enter Quantity of Shares to Purchase"),
         sg.Input(key='-AMOUNTBUY-')],
        [sg.Text("Cost of Transaction ="),
         sg.Text(buycost, size=(20, 1), key='-BUYCOST-')],
        [sg.Input(size=(20, 1), enable_events=True, key='-BUYINPUT-')],
        [sg.Listbox(tickers, size=(20, 4), enable_events=True, key='-TICKERSLIST-')],
        [sg.Button('Buy', key='-BUY-')],
        [sg.Button('Exit Buy Menu', key='-CLOSEBUY-')]
        ]
    return sg.Window('Buy Menu', layout, finalize=True)

def make_window3():
    layout = [
            [sg.Text("Enter Quantity of Shares to Purchase"),
             sg.Input(key='-AMOUNTSELL-')],
            [sg.Text("Cost of Transaction ="),
             sg.Text(buycost, size=(20, 1), key='-SELLCOST-')],
            [sg.Input(size=(20, 1), enable_events=True, key='-SELLINPUT-')],
            [sg.Listbox(tickers, size=(20, 4), enable_events=True, key='-TICKERSLIST-')],
            [sg.Button('Sell', key='-SELL-')],
            [sg.Button('Exit Sell Menu', key='-CLOSESELL-')]
            ]
    return sg.Window('Sell Menu', layout, finalize=True)


def main():
    global today
    global tickers
    global portfolio
    global worth
    worth = money

    window1 = make_window1()
    window2 = None
    window3 = None

    #check if buttons will give valid date in next press
    def boundcheck():
        if today >= dt.date(2019,12,31):
            window1['-1DAY-'].update(disabled=True)
            window1['-7DAY-'].update(disabled=True)
            window1['-30DAY-'].update(disabled=True)
            window1['-365DAY-'].update(disabled=True)          
        if today >= dt.date(2019,12,25):
            window1['-7DAY-'].update(disabled=True)
            window1['-30DAY-'].update(disabled=True)
            window1['-365DAY-'].update(disabled=True)        
        if today >= dt.date(2019,11,30):
            window1['-30DAY-'].update(disabled=True)
            window1['-365DAY-'].update(disabled=True)
        if today >= dt.date(2019,1,1):
            window1['-365DAY-'].update(disabled=True)
            
    #main loop
    while True:
        window, event, values = sg.read_all_windows()
        window1['-MONEY-'].update(money)
        window1['-WORTH-'].update(worth)
        
        #Time iteration
        if event == '-1DAY-':
            today += dt.timedelta(days=1)
            window1['-CURRENTDATE-'].update(today)
            boundcheck()
            checkworth()
        if event == '-7DAY-':
            today += dt.timedelta(weeks=1)
            window1['-CURRENTDATE-'].update(today)
            boundcheck()
            checkworth()
        if event == '-30DAY-':
            today += dt.timedelta(days=30)
            window1['-CURRENTDATE-'].update(today)
            boundcheck()
            checkworth()
        if event == '-365DAY-':
            today += dt.timedelta(days=365)
            window1['-CURRENTDATE-'].update(today)
            boundcheck()
            checkworth()
            
            
        if event == '-PORTFOLIO-':
            sg.popup(portfolio)
    
        #windows management
        #create buy and sell windows and run them
        
        #BUY WINDOW
        if event == '-BUY-' and not window2:
            window1.hide()
            window2 = make_window2()            
        if window == window2:
            if event in (sg.WIN_CLOSED, '-CLOSEBUY-'):
                window1.un_hide()
                window2.close()
                window2 = None
            else:
                if values['-BUYINPUT-'] != '':# if a keystroke entered in search field
                    search = values['-BUYINPUT-']
                    new_values = [x for x in tickers if search in x]# do the filtering
                    window['-TICKERSLIST-'].update(new_values)# display in the listbox
                else:
                    window['-TICKERSLIST-'].update(tickers)
                if event == '-TICKERSLIST-' and len(values['-TICKERSLIST-']):
                    selectedticker = str(values['-TICKERSLIST-'])[2:-2]
                    todayprice = getprice(today, selectedticker)
                    try:
                        amountbuy = int(values['-AMOUNTBUY-'])
                        buycost = (todayprice)*(amountbuy)
                        window2['-BUYCOST-'].update(buycost)
                    except:
                        sg.popup("Error")

                elif event == '-BUY-':
                    try:
                        buy(today, selectedticker, amountbuy)
                        sg.popup("Bought", amountbuy, "of", selectedticker, "at", todayprice, "for a total of", buycost)
                        selectedticker = ''
                        todayprice = 0
                        amountbuy = 0
                        buycost = (todayprice)*(amountbuy)
                    except:
                        sg.popup("Error")


            
        #SELL WINDOW
        if event == '-SELL-' and not window3:
            window1.hide()
            window3 = make_window3()
        if window == window3:
            if event in (sg.WIN_CLOSED, '-CLOSESELL-'):
                window1.un_hide()
                window3.close()
                window3 = None
            else:
                if values['-SELLINPUT-'] != '':# if a keystroke entered in search field
                    search = values['-SELLINPUT-']
                    new_values = [x for x in tickers if search in x]# do the filtering
                    window['-TICKERSLIST-'].update(new_values)# display in the listbox
                else:
                    window['-TICKERSLIST-'].update(tickers)
                if event == '-TICKERSLIST-' and len(values['-TICKERSLIST-']):
                    selectedticker = str(values['-TICKERSLIST-'])[2:-2]
                    todayprice = getprice(today, selectedticker)
                    try:
                        amountsell = int(values['-AMOUNTSELL-'])
                        sellcost = (todayprice)*(amountsell)
                        window3['-SELLCOST-'].update(sellcost)
                    except:
                        sg.popup("Error")
                elif event == '-SELL-':
                    try:
                        sell(today, selectedticker, amountsell)
                        sg.popup("Sold", amountsell, "of", selectedticker, "at", todayprice, "for a total of", sellcost)
                        selectedticker = ''
                        todayprice = 0
                        amountsell = 0
                        sellcost = (todayprice)*(amountsell)
                    except:
                        sg.popup("Error")

                
        #close main window    
        if event == '-CLOSE-' or sg.WIN_CLOSED:
            break
    
    window1.close()
    if window == window2:
        window2.close()
        window2 = None
    if window == window3:
        window3.close()
        window3 = None


if __name__ == '__main__':
    main()