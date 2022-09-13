import matplotlib.pyplot as plt
import csv
import time
from random import randint
"""
Stock class for stock objects
"""


class BinarySearchTree:
    """
    Creating a constructor of the class BinarySearchTree
    with all the required attributes.
    """
    def __init__(self, key=None, value=None): 
        self.rightChild = None
        self.leftChild = None
        self.key = key
        self.val = value
        self.size = 0
        
    def length(self): # returns the size of the tree
        return self.size

    """
    creating a put method to build a binary search tree.
    """
    def put(self, key=None, value=None):
        self.size += 1
        if self.key == None:
            self.key = key
            self.val = value
            return

        if self.key > key:
            if (self.leftChild == None):
                self.leftChild = BinarySearchTree()
            self.leftChild.put(key, value)
            return

        else:
            if (self.rightChild == None):
                self.rightChild = BinarySearchTree()
            self.rightChild.put(key, value)
            return

    def __setitem__(self, k, v):
        self.put(k, v)

class Stock:

    """
    Constructor to initialize the stock object
    """

    def __init__(self, sname, symbol, value, price_list):
        self.sname = sname
        self.symbol = symbol
        self.val = value
        self.prices = price_list

    """
    return the stock information as a string, including name, symbol, 
    market value, and the price on the last day (2021-02-01). 
    For example, the string of the first stock should be returned as: 
    “name: Exxon Mobil Corporation; symbol: XOM; val: 384845.80; price:44.84”. 
    """

    def __str__(self):
        return "name: " + self.sname + "; symbol: " + self.symbol + "; val: " + str(self.val) + "; price:" + str(self.prices[-1])


"""
StockLibrary class to mange stock objects
"""


class StockLibrary:

    """
    Constructor to initialize the StockLibrary
    """

    def __init__(self):
        self.stockList = []
        self.randstocks=[]
        self.size = 0
        self.isSorted = False
        self.bst = None
        self.datelist = []
    """
    The loadData method takes the file name of the input dataset,
    and stores the data of stocks into the library. 
    Make sure the order of the stocks is the same as the one in 
    the input file. 
    """

    def loadData(self, filename: str):
        with open(filename) as csvfile:
            csvreader = csv.reader(csvfile, delimiter="|")
            stocks = list(csvreader)
            first_line=stocks.pop(0) # removes the title line in the csv and stores it in a variable

            for dates in first_line[3:]:
                self.datelist.append(dates) # stores the dates required for plotting

            """
            Loop for extracting elements of the csv file and storing 
            them seperately.
            """

            for stock in stocks:
                price_floats = []
                for stock_price in stock[3:]:
                    price_floats.append(float(stock_price))
                ob = Stock(stock[0], stock[1], float(stock[2]), price_floats)
                self.stockList.append(ob)
                self.size += 1
            
    """
    The linearSearch method searches the stocks based on sname or symbol.
    It takes two arguments as the string for search and an attribute field 
    that we want to search (“name” or “symbol”). 
    It returns the details of the stock as described in __str__() function 
    or a “Stock not found” message when there is no match. 
    """

    def linearSearch(self, query: str, attribute: str):
        flag = False
        if attribute == "name":
            for stock in self.stockList:
                if stock.sname == query:
                    flag = True
                    return stock

        if attribute == "symbol":
            for stock in self.stockList:
                if stock.symbol == query:
                    flag = True
                    return stock

        if flag == False:
            return ("Stock not found")

    """
    Method to create a random integers an then store 
    the random stocks at those indexes in a list.
    """

    def random(self):
        for i in range(100):
            value = randint(0,len(self.stockList)-1)
            self.randstocks.append(self.stockList[value])

    """
    Linear search method which does linear search on the 
    random hundred stocks array.
    """

    def linearSearchhundred(self, query: str, attribute: str):
        flag = False
        if attribute == "name":
            for stock in self.randstocks:
                if stock.sname == query:
                    flag = True
                    return stock

        if attribute == "symbol":
            for stock in self.randstocks:
                if stock.symbol == query:
                    flag = True
                    return stock

        if flag == False:
            return ("Stock not found")
        
    """
    Helper method for quick sort which takes care of the 
    swapping and partitioning required in quicksort.
    """
    def swapping(self, lm, rm):
        l = (lm-1)
        symbol_list = []
        for stock in self.stockList:
            symbol_list.append(stock.symbol)

        h = symbol_list[rm]
        for i in range(lm, rm):
            if symbol_list[i] <= h:
                l += 1
                self.stockList[l], self.stockList[i] = self.stockList[i], self.stockList[l]
        self.stockList[l+1], self.stockList[rm] = self.stockList[rm], self.stockList[l+1]
        return (l+1)

    """
    Sort the stockList using QuickSort algorithm based on the stock symbol.
    The sorted array should be stored in the same stockList.
    Remember to change the isSorted variable after sorted
    """

    def quickSort(self):
        symbol_list = []
        for stock in self.stockList:
            symbol_list.append(stock.symbol)
        lm = 0
        rm = len(symbol_list)-1
        size = rm-lm+1
        stack = [0]*(size)
        t = -1
        t = t+1
        stack[t] = lm
        t = t+1
        stack[t] = rm
        while t >= 0:
            rm = stack[t]
            t = t-1
            lm = stack[t]
            t = t-1
            x = self.swapping(lm, rm)
            if x-1 > lm:
                t = t+1
                stack[t] = lm
                t = t+1
                stack[t] = x-1
            if x+1 < rm:
                t = t+1
                stack[t] = x+1
                t = t+1
                stack[t] = rm
        self.isSorted = True # changing value of isSorted after swapping

    """
    build a balanced BST of the stocks based on the symbol. 
    Store the root of the BST as attribute bst, which is a TreeNode type.
    """

    def buildBST(self, stock_arr=None):
        if self.isSorted == False:
            self.quickSort()
        if stock_arr == None:
            stock_arr = self.stockList
        if len(stock_arr) < 1:
            return None
        if self.bst == None:
            self.bst = BinarySearchTree()       
        mid = len(stock_arr)//2 # building balanced bst using sorted array
        leftarr = stock_arr[:mid] # storing the less valued elements to the left
        rightarr = stock_arr[mid+1:] # storing the more valued elements to the right
        self.bst.put(stock_arr[mid].symbol, stock_arr[mid]) # calling put to build the balanced bst
        self.buildBST(leftarr) # recursive calling for repeatedly finding midpoint
        self.buildBST(rightarr) # recursive calling for repeatedly finding midpoint

    """
    build a balanced BST of the random stocks based on the symbol. 
    """

    def buildBSTrandom(self, stock_arr=None):
        if self.isSorted == False:
            self.quickSort()
        if stock_arr == None:
            stock_arr = self.randstocks
        if len(stock_arr) < 1:
            return None
        if self.bst == None:
            self.bst = BinarySearchTree()       
        mid = len(stock_arr)//2
        leftarr = stock_arr[:mid]
        rightarr = stock_arr[mid+1:]
        self.bst.put(stock_arr[mid].symbol, stock_arr[mid])
        self.buildBST(leftarr)
        self.buildBST(rightarr)

    """
    Search a stock based on the symbol attribute. 
    It returns the details of the stock as described in __str__() function 
    or a “Stock not found” message when there is no match. 
    """

    def searchBST(self, query, current='dnode'):
        if self.bst == None:
           return "Stock not found"
        if current == "dnode":
            current = self.bst
        if current.key == query:
            return current.val
        if current.key > query:
            if current.leftChild is not None:
                return self.searchBST(query,current.leftChild)
            else:
                return "Stock not found"
        if current.key < query:
            if current.rightChild is not None:
                return self.searchBST(query,current.rightChild)
            else:
                return "Stock not found"
        
    """
    Creating a method which plots the graph of the prices of the
    longest stock in the list of stocks against the dates of the month.
    """

    def longestplot(self):
        dates = []
        for date in self.datelist:
            dates.append(int(date[-2:])) # storing the dates in a list
        m = self.stockList[0]
        for stock in self.stockList:
            if len(m.sname) < len(stock.sname):
                m = stock # storing the longest stock
        plt.plot(dates,m.prices) # plotting the prices with the respective day
        plt.xlabel("Dates of the month")
        plt.ylabel("Stock Prices")
        plt.xticks(range((dates[-1]+1)))
        plt.xlim(5,29)
        plt.title(m.sname)
        plt.show()

    """
    Function which gives the percentage change of the most increased
    and the most decreased stock and also prints the stock.
    """

    def maxchange(self):
        max_diff = self.stockList[0].prices[-1]-self.stockList[0].prices[0]
        min_diff = self.stockList[0].prices[-1]-self.stockList[0].prices[0]

        for stock in self.stockList:
            diff = stock.prices[-1]-stock.prices[0]
            if (diff > max_diff):
                max_diff = diff
                stock_mostprofit = stock
            if (diff < min_diff):
                min_diff = diff
                stock_mostloss = stock

        p_change1 = (max_diff/stock_mostprofit.prices[0])*100
        p_change2 = (min_diff/stock_mostloss.prices[0])*100
        print(stock_mostprofit)
        print("Percentage change: "+str(round(p_change1, 4))+"%") # positive as this stock is increased in value
        print(stock_mostloss)
        print("Percentage change: "+str((round(p_change2, 4)))+"%") # negative as this stock has decreased in value


# # WRITE YOUR OWN TEST UNDER THIS IF YOU NEED
if __name__ == '__main__':
    stockLib = StockLibrary()
    testSymbol = 'GE'
    testName = 'General Electric Company'

    print("\n-------load dataset-------")
    stockLib.loadData("stock_database.csv")
    print(stockLib.size)

    print("\n-------linear search-------")
    print(stockLib.linearSearch(testSymbol, "symbol"))
    print(stockLib.linearSearch(testName, "name"))


    print("\n-------linear search of hundred stocks-------")
    start = time.time()
    stockLib.random()
    print(stockLib.linearSearchhundred(testSymbol, "symbol"))
    end = time.time()
    t1 = end-start
    print("Time of linear search for hundred random stocks is: "+str(end-start)+" s")

    print("\n-------quick sort-------")
    start = time.time()
    print(stockLib.isSorted)
    stockLib.quickSort()
    end = time.time()
    print("Time of quick sort is: "+str(end-start)+" s")
    print(stockLib.isSorted)

    print("\n-------build BST-------")
    start = time.time()
    stockLib.buildBST()
    end = time.time()
    t2=end-start
    print("Time of building a BST is: "+str(end-start)+" s")

    print("\n---------search BST---------")
    print(stockLib.searchBST(testSymbol))

    print("\n-------build and search BST for 100 random nodes-------")
    stockLib.buildBSTrandom()
    start = time.time()
    stockLib.searchBST(testSymbol)
    end = time.time()
    t3 = end-start
    print("Time of searching a BST of 100 stocks is: "+str(end-start)+" s")

    print("\n-------number of linear searches needed to increase the time-------")
    print(str(round(t2/(t1-t3)))+" linear searches would be required before the overall run time of the linear searches would be more than the combined total of building a BST (only performed once) and 𝒏 searches in the BST.")

    print("\n-------most change-------")
    stockLib.maxchange()

    print("\n-------plot stocks-------")
    stockLib.longestplot()
