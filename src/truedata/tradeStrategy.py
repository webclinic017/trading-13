import os
import sys


class tradeStrategy:
    def __init__(self):
        pass

    def calculate_five_minute_stats(self, list_bars):
        time = list_bars[4][0]
        open = list_bars[0][1]
        close = list_bars[4][4]

        high = list_bars[0][1]
        low = list_bars[0][1]
        # print("Open" + str(open))
        # print("Close" + str(close))

        for i in list_bars[1:5]:
            print("Checking: " + str(i))
            i = i[1:5]
            # print(type(i))
            for j in i:
                #print("\t\tChecking: " + str(j))
                if j > high:
                    high = j

        for i in list_bars[1:5]:
            print("Checking: " + str(i))
            i = i[1:5]
            # print(type(i))
            for j in i:
                #print("\t\tChecking: " + str(j))
                if j < low:
                    low = j

        list_five_minute_bar = []
        list_five_minute_bar.append(time)
        list_five_minute_bar.append(open)
        list_five_minute_bar.append(high)
        list_five_minute_bar.append(low)
        list_five_minute_bar.append(close)

        return list_five_minute_bar
