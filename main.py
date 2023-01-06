from rich import print as rprint
from rich import box
from rich.prompt import Prompt, Confirm
from rich.console import Console
from rich.markdown import Markdown
from rich.terminal_theme import MONOKAI
from rich.theme import Theme
from rich.table import Table
from utils import df_to_table

import numpy as np
from screener_investor import MarketScreener

# Header
print("\n\n")
console = Console()

markdown = Markdown("## WELCOME TRADERS")
console.print(markdown, style="bold yellow", highlight=True)
print("\n")


state = True

while state:
    # Lookback Period Input
    mark_lookback = Markdown("\n- Enter lookback period (Default is 365 i.e. 1 year): ")
    console.print(mark_lookback, style="bold yellow")
    lookback = int(Prompt.ask('[bold red] >>> [/bold red]'))


    prefer_markdown = Markdown("\n\n1. Stock Screener\n2. Baseline Performance\n3. Individual Stock Details\n4. Asset Allocation\n5. Correlation Check\n6. Exit\n")
    console.print(prefer_markdown, style="bold magenta")
    prefer = str(Prompt.ask('[bold red] >>> [/bold red]'))

    # Driver Code
    if prefer == "1":
        index_markdown = Markdown("\n- Enter your preferred Index Name\n\n")
        console.print(index_markdown, style="bold blue")

        indexes = ['NIFTY_50', 'NIFTY_BANK', 'NASDAQ', 'SP500', 'FTSE250', 'FTSE100', 'DOW', 'IBOVESPA', 'NSE', 'NSE Custom']
        index_option_md = Markdown('1. Nifty 50\n2. Bank Nifty\n3. Nasdaq\n4. S&P500\n5. FTSE250\n6. FTSE100\n7. DOW\n8. IBOVESPA\n9. NSE All\n10. NSE Custom\n')
        console.print(index_option_md, style="bold green")
        index = indexes[int(Prompt.ask('[bold red] >>> [/bold red]')) - 1]

        obj = MarketScreener(index, lookback=lookback)
        dataf = obj._index_stocks_stats()
        dataf.set_index('TIC', inplace=True)
        dataf = dataf.astype('float')

        for cols in dataf.columns:
            dataf[cols] = dataf[cols].apply(lambda x: np.around(x, 2))

        # Show tables
        table = Table(show_header=True,  header_style="bold magenta", style="green")
        table = df_to_table(dataf, table)
        table.row_styles = ["none", "dim"]
        table.box = box.ROUNDED
        console.print(table)

        save = str(Confirm.ask("\n[bold green] Want it in an Excel file[/bold green]")).strip().upper()

        if save == "Y":
            dataf.to_excel(f"{index}.xlsx", index=False)

        use_filter = True
        temp = dataf.copy()

        while use_filter:
            filter_mark = Markdown("\n- Enter your screening conditions\n\n- Note:\n1. Enter conditions seperated by _. For Eg: Annual Volatility greater than 40% can be written as AV_>_40\n2. SR-Sharpe Ratio\t- AV-Annual Volatility\t- MDD-Maximum Drawdown\t- VaR-Value at Risk\t- cVaR-Conditional Value at Risk\t- SC-Score\n")
            console.print(filter_mark, style="bold blue")
            filters = str(Prompt.ask("\n[bold red] >>> [/bold red]")).split()

            for filt in filters:
                facts = filt.split("_")
                if facts[0]=="AV":
                    if facts[1]==">":
                        temp = temp[temp['Annual Volatility']>float(facts[2])]
                    elif facts[1]=="<":
                        temp = temp[temp['Annual Volatility']<float(facts[2])]
                    else:
                        temp = temp[temp['Annual Volatility']==float(facts[2])]
                elif facts[0]=="SR":
                    if facts[1]==">":
                        temp = temp[temp['Sharpe Ratio']>float(facts[2])]
                    elif facts[1]=="<":
                        temp = temp[temp['Sharpe Ratio']<float(facts[2])]
                    else:
                        temp = temp[temp['Sharpe Ratio']==float(facts[2])]
                elif facts[0]=="MDD":
                    if facts[1]==">":
                        temp = temp[temp['MaxDD']>float(facts[2])]
                    elif facts[1]=="<":
                        temp = temp[temp['MaxDD']<float(facts[2])]
                    else:
                        temp = temp[temp['MaxDD']==float(facts[2])]
                elif facts[0]=="cVaR":
                    if facts[1]==">":
                        temp = temp[temp['CVaR']>float(facts[2])]
                    elif facts[1]=="<":
                        temp = temp[temp['CVaR']<float(facts[2])]
                    else:
                        temp = temp[temp['CVaR']==float(facts[2])]
                elif facts[0]=="VaR":
                    if facts[1]==">":
                        temp = temp[temp['VaR']>float(facts[2])]
                    elif facts[1]=="<":
                        temp = temp[temp['VaR']<float(facts[2])]
                    else:
                        temp = temp[temp['VaR']==float(facts[2])]
                elif facts[0]=="PER":
                    if facts[1]==">":
                        temp = temp[temp['PE Ratio']>float(facts[2])]
                    elif facts[1]=="<":
                        temp = temp[temp['PE Ratio']<float(facts[2])]
                    else:
                        temp = temp[temp['PE Ratio']==float(facts[2])]
                elif facts[0]=="DVD":
                    if facts[1]==">":
                        temp = temp[temp['Dividend']>float(facts[2])]
                    elif facts[1]=="<":
                        temp = temp[temp['Dividend']<float(facts[2])]
                    else:
                        temp = temp[temp['Dividend']==float(facts[2])]
                else:
                    if facts[1]==">":
                        temp = temp[temp['Score']>float(facts[2])]
                    elif facts[1]=="<":
                        temp = temp[temp['Score']<float(facts[2])]
                    else:
                        temp = temp[temp['Score']==float(facts[2])]

            # Show tables
            table1 = Table(show_header=True,  header_style="bold magenta", style="green")
            table1 = df_to_table(temp, table1)
            table1.row_styles = ["none", "dim"]
            table1.box = box.ROUNDED
            console.print(table1)
            use_filter = False


    # Next Baseline
    if prefer == "2":
        print("\nEnter your preferred Index Name\n")

        indexes = ['NIFTY_50', 'NIFTY_BANK', 'NASDAQ', 'SP500', 'FTSE250', 'FTSE100', 'DOW', 'IBOVESPA', 'NSE', 'NSE Custom']
        index = indexes[int(input('1.Nifty 50\n2.Bank Nifty\n3.Nasdaq\n4.S&P500\n5.FTSE250\n6.FTSE100\n7.DOW\n8.IBOVESPA\n9.NSE All\n10.NSE Custom\n\nEnter Option: '))-1]

        obj = MarketScreener(index, lookback=lookback)
        print(obj.get_baseline_stats())


    # Details Individual Stocks
    if prefer == "3":
        print("\nEnter your preferred Index Name\n")

        indexes = ['NIFTY_50', 'NIFTY_BANK', 'NASDAQ', 'SP500', 'FTSE250', 'FTSE100', 'DOW', 'IBOVESPA', 'NSE', 'NSE Custom']
        index = indexes[int(input('1.Nifty 50\n2.Bank Nifty\n3.Nasdaq\n4.S&P500\n5.FTSE250\n6.FTSE100\n7.DOW\n8.IBOVESPA\n9.NSE All\n10.NSE Custom\n\nEnter Option: '))-1]

        obj = MarketScreener(index, lookback=lookback)
        tick = input("\nEnter Stock Ticker\n\nEnter Option: ")
        df = obj.individual_details(tick)
        print("\n")
        print(df)


    # Asset Allocation
    if prefer == "4":
        cash = input("\nEnter Cash: ").strip()
        if cash.isnumeric():
            cash = int(cash)
            # Optimisation method check
            print("\nSelect the desired Optimisation Method \n")
            print("1. Max Sharpe")
            print("2. Kelly")
            print("3. HRP")
            print("4. Min Vol")

            option = input("\nEnter Option: ")
            if option == "1":
                method = "max_sharpe"
            elif option == "2":
                method = "kelly"
            elif option == "3":
                method = "HRP"
            elif option == "4":
                method = "min_vol"
            else:
                print("You have given an invalid response\n")
                print("Enter a valid response")

            # Shrinkage Method
            print("\nSelect the desired Shrinkage Method\n")
            print("1. Ledoit Wolf")
            print("2. Semi-Covariance")
            print("3. Sample Covarinace")
            print("4. Exp. Covariance")

            option = input("\nEnter Option: ")
            if option == "1":
                shrinkage = "ledoit_wolf"
            elif option == "2":
                shrinkage = "semicovariance"
            elif option == "3":
                shrinkage = "sample_cov"
            elif option == "4":
                shrinkage = "exp_cov"
            else:
                print("You have given an invalid response\n")
                print("Enter a valid response")

            num_stocks = min(int(input("\nEnter the number of unique stocks for portfolio construction (Max. 10): ")), 10)

            stock_names = []
            for i in range(num_stocks):
                print(f"\nEnter Symbol No.{i+1} ")
                stock_names.append(input(">>> ").strip().upper())

            gre_lin = input("\nEnter G for Greedy Portfolio and L for Linear Portfolio:\n\nEnter Option: ").upper().strip()
            print("\n")
            if gre_lin == "G":
                alloc = "Greedy"
            elif gre_lin == "L":
                alloc = "Linear"

            print("\nEnter your preferred Index Name\n")

            indexes = ['NIFTY_50', 'NIFTY_BANK', 'NASDAQ', 'SP500', 'FTSE250', 'FTSE100', 'DOW', 'IBOVESPA', 'NSE', 'NSE Custom']
            index = indexes[int(input('1.Nifty 50\n2.Bank Nifty\n3.Nasdaq\n4.S&P500\n5.FTSE250\n6.FTSE100\n7.DOW\n8.IBOVESPA\n9.NSE All\n10.NSE Custom\n\nEnter Option: '))-1]

            obj = MarketScreener(index, lookback=lookback)
            freq = input('\nEnter Allocation Frequency (M-Monthly, D-Daily): ').upper().strip()
            A = obj.asset_allocation(cash, stock_names, method, shrinkage, alloc, freq)
            print("\nQuantity of Shares to buy for each ticker\n\n", A)


    # Correlation Check
    if prefer == "5":
        num_stocks_corr = min(int(input("\nEnter the number of unique stocks for portfolio construction (Max. 10): ")), 10)

        stock_names_corr = []
        for i in range(num_stocks_corr):
            print(f"\nEnter Symbol No.{i+1} ")
            stock_names_corr.append(input("\nEnter Option: ").strip().upper())

        print("\nThe correlation matrix for the given stocks\n", obj.corr_cals(stock_names_corr))


    # Continue to use the screener
    if prefer == "6":
        print("Exiting...")
        break
