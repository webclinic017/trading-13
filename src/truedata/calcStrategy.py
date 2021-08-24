#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import sys
from playsound import playsound
from src.truedata.osUtils import *
from datetime import datetime as d


class calcStrategy:
    def __init__(self):
        pass

    def size_of_upper_shadow(self, rise_or_fall, open, high, low, close):
        if int(rise_or_fall) == 1:
            return float(high) - float(close)

        elif int(rise_or_fall) == -1:
            return float(high) - float(open)

    def size_of_lower_shadow(self, rise_or_fall, open, high, low, close):
        if int(rise_or_fall) == 1:
            return float(open) - float(low)

        elif int(rise_or_fall) == -1:
            return float(close) - float(low)

    def binary_tail(self, a, b):
        proportion_of_tail = 75
        if a > proportion_of_tail or b > proportion_of_tail:
            return 1
        else:
            return -1


    def binary_tail_lower(self, a, b):
        proportion_of_tail = 60
        if b > proportion_of_tail and b < 101:
            return 1
        else:
            return -1

    def low_is_lower(self, a, b):
        if float(a) >= float(b):
            return 1
        else:
            return -1


    def high_is_higher(self, a, b):
        if float(a) <= float(b):
            return 1
        else:
            return -1

    def actual_low(self, value_max_low_in_next_10_instances, value_max_low_if_low_is_max_low):
        return max(value_max_low_in_next_10_instances, value_max_low_if_low_is_max_low)


    def proportion_of_max_high_in_next_10_instances(self, value_max_high_in_next_10_instances, close):
        return ((value_max_high_in_next_10_instances - close) / close) * 100


    def proportion_of_max_low_in_next_10_instances(self, proportion_of_max_low_in_next_10_instances, close):
        return ((close - proportion_of_max_low_in_next_10_instances) / close) * 100


    def proportion_of_max_low_in_next_10_instances_if_close_is_max_low(self, close, low):
        return ((close - low) / close) * 100


    def proportion_of_actual_low(self, actual_low, close):
        return ((close - actual_low) / close) * 100


    # Lowest in the previous 5 instances
    def lowest_in_previous_5_instances(self, value_max_low_in_previous_5_instances, low):
        if low < value_max_low_in_previous_5_instances:
            return 1
        else:
            return 0


    def calculate(self, filename):
        print("Processing: " + str(filename))
        pd.set_option('display.max_colwidth', -1)
        # pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        pd.set_option('display.expand_frame_repr', False)

        df = pd.read_csv(filename)

        last_rows = 1
        df = df.tail(last_rows)

        print("Basic columns")

        # df = df[['Index', 'Open', 'High', 'Low', 'Close', 'Time']]
        df = df[['Index', 'Open', 'High', 'Low', 'Close']]

        df["size_of_candlestick"] = df['High'] - df['Low']
        df["size_of_body"] = df['Close'] - df['Open']
        df['rise_or_fall'] = df['size_of_body'].apply(lambda x: '1' if x > 0 else '-1')
        df["proportion_of_body"] = df["size_of_body"].abs() / df["size_of_candlestick"].abs() * 100

        df["size_of_upper_shadow"] = df[['rise_or_fall', 'Open', 'High', 'Low', 'Close']].apply(
            lambda x: self.size_of_upper_shadow(*x), axis=1)
        df["propertion_of_upper_shadow"] = df["size_of_upper_shadow"].abs() / df["size_of_candlestick"].abs() * 100
        df["size_of_lower_shadow"] = df[['rise_or_fall', 'Open', 'High', 'Low', 'Close']].apply(
            lambda x: self.size_of_lower_shadow(*x), axis=1)
        df["proportion_of_lower_shadow"] = df["size_of_lower_shadow"].abs() / df["size_of_candlestick"].abs() * 100


        df['binary_tail'] = df[['propertion_of_upper_shadow', 'proportion_of_lower_shadow']].apply(lambda x: self.binary_tail(*x),
                                                                                                   axis=1)
        df['binary_tail_lower'] = df[['propertion_of_upper_shadow', 'proportion_of_lower_shadow']].apply(
            lambda x: self.binary_tail_lower(*x), axis=1)

        df["binary_body"] = df['proportion_of_body'].apply(lambda x: '1' if x > 95 else '-1')  # If size of body is high

        df['OHLC'] = df.iloc[:, 1:5].apply(
            lambda x: ",".join(x.astype(str)), axis=1)

        df[['OHLC1nextshift']] = df[['OHLC']].shift(-1)
        df[['OHLC2nextshift']] = df[['OHLC']].shift(-2)
        df[['OHLC3nextshift']] = df[['OHLC']].shift(-3)
        df[['OHLC4nextshift']] = df[['OHLC']].shift(-4)
        df[['OHLC5nextshift']] = df[['OHLC']].shift(-5)
        df[['OHLC6nextshift']] = df[['OHLC']].shift(-6)
        df[['OHLC7nextshift']] = df[['OHLC']].shift(-7)
        df[['OHLC8nextshift']] = df[['OHLC']].shift(-8)
        df[['OHLC9nextshift']] = df[['OHLC']].shift(-9)
        df[['OHLC10nextshift']] = df[['OHLC']].shift(-10)

        print("Add a new column based on previous columns")
        # df['Prev_Time'] = df.loc[df['VALUE'].shift(-1)==1, 'TIME']

        k = 10

        df["previous_low"] = df['Low'].shift(1)
        df['binary_low_is_lower_than_previous_low'] = df[['Low', 'previous_low']].apply(lambda x: self.low_is_lower(*x), axis=1)
        df["previous_high"] = df['High'].shift(1)
        df["binary_high_is_higher_than_previous_high"] = df[['High', 'previous_high']].apply(lambda x: self.high_is_higher(*x),
                                                                                             axis=1)

        df["next_low"] = df['Low'].shift(-1)
        df['next_low_is_lower'] = df[['Low', 'next_low']].apply(lambda x: self.low_is_lower(*x), axis=1)
        df["next_high"] = df['High'].shift(-1)
        df["next_high_is_higher"] = df[['High', 'next_high']].apply(lambda x: self.high_is_higher(*x), axis=1)

        df["value_max_high_in_next_10_instances"] = df["High"].rolling(k).max().shift(-k)
        df["value_max_low_in_next_10_instances"] = df["Low"].rolling(k).min().shift(-k)

        df["value_max_high_in_next_10_instances"] = pd.to_numeric(df["value_max_high_in_next_10_instances"])
        df["value_max_low_in_next_10_instances"] = pd.to_numeric(df["value_max_low_in_next_10_instances"])
        df["value_max_low_if_low_is_max_low"] = pd.to_numeric(df["Low"])
        df["Close"] = pd.to_numeric(df["Close"])

        df["actual_low"] = df[['value_max_low_in_next_10_instances', 'value_max_low_if_low_is_max_low']].apply(
            lambda x: self.actual_low(*x), axis=1)


        df["proportion_of_max_high_in_next_10_instances"] = df[['value_max_high_in_next_10_instances', 'Close']].apply(
            lambda x: self.proportion_of_max_high_in_next_10_instances(*x), axis=1)
        df["proportion_of_max_low_in_next_10_instances"] = df[['value_max_low_in_next_10_instances', 'Close']].apply(
            lambda x: self.proportion_of_max_low_in_next_10_instances(*x), axis=1)
        df["proportion_of_max_low_in_next_10_instances_if_close_is_max_low"] = df[['Close', 'Low']].apply(
            lambda x: self.proportion_of_max_low_in_next_10_instances_if_close_is_max_low(*x), axis=1)
        df["proportion_of_actual_low"] = df[['actual_low', 'Close']].apply(lambda x: self.proportion_of_actual_low(*x), axis=1)


        df["value_max_low_in_previous_5_instances"] = df["Low"].rolling(k).min().shift(k)
        df["lowest_in_previous_5_instances"] = df[['value_max_low_in_previous_5_instances', 'Low']].apply(
            lambda x: self.lowest_in_previous_5_instances(*x), axis=1)

        # Strategy 1: Big tail
        print("Filter columns")
        # df[df.binary_tail_lower > 0 & df.rise_or_fall>0]

        # Strategy 3: Big tail with tall candlesticks next
        print("Filter columns")
        # df[df.binary_tail_lower > 0 & df.rise_or_fall>0]

        # Change to numeric
        df["rise_or_fall"] = pd.to_numeric(df["rise_or_fall"])
        df["proportion_of_max_high_in_next_10_instances"] = pd.to_numeric(df["proportion_of_max_high_in_next_10_instances"])
        df["proportion_of_max_low_in_next_10_instances"] = pd.to_numeric(df["proportion_of_max_low_in_next_10_instances"])
        df["proportion_of_actual_low"] = pd.to_numeric(df["proportion_of_actual_low"])

        pd.set_option('display.max_colwidth', None)

        if filename == "CRUDEOIL-I-5MIN":
            df = df[
                (df['binary_tail_lower'] > 0) &
                #   (df["lowest_in_previous_5_instances"] > 0) &

                # (df['size_of_candlestick'] > 0.000900) #forex

                (df['size_of_candlestick'] > 5) #&  # Crudeoil
                # (df['size_of_candlestick'] < 15)  # Crudeoil

                #     (df['size_of_candlestick'] >100)   & #gold
                #      (df['size_of_candlestick'] < 180)

                #     (df['size_of_candlestick'] > 0.5) & #natgas
                #     (df['size_of_candlestick'] < 0.7)

                #     (df['size_of_candlestick'] > 0.9) & #natgas and copper
                #     (df['size_of_candlestick'] < 1.1)

                #     (df['size_of_candlestick'] > 0.8) & #natgas
                #     (df['size_of_candlestick'] < 1.2)

                #     (df['next_low_is_lower'] == -1  ) &
                #     (df["next_high_is_higher"] == 1)

                ]
        elif filename == "GOLDM-I-5MIN":
            df = df[
                (df['binary_tail_lower'] > 0) &
                #   (df["lowest_in_previous_5_instances"] > 0) &

                # (df['size_of_candlestick'] > 0.000900) #forex

                # (df['size_of_candlestick'] > 8) &  # Crudeoil
                # (df['size_of_candlestick'] < 12)  # Crudeoil

                    (df['size_of_candlestick'] >40)   #& #gold
                     # (df['size_of_candlestick'] < 180)

                #     (df['size_of_candlestick'] > 0.5) & #natgas
                #     (df['size_of_candlestick'] < 0.7)

                #     (df['size_of_candlestick'] > 0.9) & #natgas and copper
                #     (df['size_of_candlestick'] < 1.1)

                #     (df['size_of_candlestick'] > 0.8) & #natgas
                #     (df['size_of_candlestick'] < 1.2)

                #     (df['next_low_is_lower'] == -1  ) &
                #     (df["next_high_is_higher"] == 1)

                ]

        elif filename == "NATURALGAS-I-5MIN":
            df = df[
                (df['binary_tail_lower'] > 0) &
                #   (df["lowest_in_previous_5_instances"] > 0) &

                # (df['size_of_candlestick'] > 0.000900) #forex

                # (df['size_of_candlestick'] > 8) &  # Crudeoil
                # (df['size_of_candlestick'] < 12)  # Crudeoil

                #     (df['size_of_candlestick'] >100)   & #gold
                #      (df['size_of_candlestick'] < 180)

                    (df['size_of_candlestick'] > 0.2) #& #natgas
                    # (df['size_of_candlestick'] < 0.7)

                #     (df['size_of_candlestick'] > 0.9) & #natgas and copper
                #     (df['size_of_candlestick'] < 1.1)

                #     (df['size_of_candlestick'] > 0.8) & #natgas
                #     (df['size_of_candlestick'] < 1.2)

                #     (df['next_low_is_lower'] == -1  ) &
                #     (df["next_high_is_higher"] == 1)

                ]

        elif filename == "COPPER-I-5MIN":
            df = df[
                (df['binary_tail_lower'] > 0) &
                #   (df["lowest_in_previous_5_instances"] > 0) &

                # (df['size_of_candlestick'] > 0.000900) #forex

                # (df['size_of_candlestick'] > 8) &  # Crudeoil
                # (df['size_of_candlestick'] < 12)  # Crudeoil

                #     (df['size_of_candlestick'] >100)   & #gold
                #      (df['size_of_candlestick'] < 180)

                #     (df['size_of_candlestick'] > 0.5) & #natgas
                #     (df['size_of_candlestick'] < 0.7)

                (df['size_of_candlestick'] > 0.7) #& #natgas and copper
                    # (df['size_of_candlestick'] < 1.1)

                #     (df['size_of_candlestick'] > 0.8) & #natgas
                #     (df['size_of_candlestick'] < 1.2)

                #     (df['next_low_is_lower'] == -1  ) &
                #     (df["next_high_is_higher"] == 1)


                ]

        elif filename == "ZINC-I-5MIN":
            df = df[
                (df['binary_tail_lower'] > 0) &
                #   (df["lowest_in_previous_5_instances"] > 0) &

                # (df['size_of_candlestick'] > 0.000900) #forex

                # (df['size_of_candlestick'] > 8) &  # Crudeoil
                # (df['size_of_candlestick'] < 12)  # Crudeoil

                #     (df['size_of_candlestick'] >100)   & #gold
                #      (df['size_of_candlestick'] < 180)

                #     (df['size_of_candlestick'] > 0.5) & #natgas
                #     (df['size_of_candlestick'] < 0.7)

                #(df['size_of_candlestick'] > 0.7) #& #natgas and copper
                # (df['size_of_candlestick'] < 1.1)

                #     (df['size_of_candlestick'] > 0.8) & #natgas
                #     (df['size_of_candlestick'] < 1.2)

                #     (df['next_low_is_lower'] == -1  ) &
                #     (df["next_high_is_higher"] == 1)
                (df['size_of_candlestick'] > 0.250) &  # Zinc
                (df['size_of_candlestick'] < 1.00)  # Zinc

                # (df['size_of_candlestick'] > 3.00) &  # Nickel
                # (df['size_of_candlestick'] < 6.00)  # Nickel
                ]
        elif filename == "NICKEL-I-5MIN":
            df = df[
                (df['binary_tail_lower'] > 0) &
                #   (df["lowest_in_previous_5_instances"] > 0) &

                # (df['size_of_candlestick'] > 0.000900) #forex

                # (df['size_of_candlestick'] > 8) &  # Crudeoil
                # (df['size_of_candlestick'] < 12)  # Crudeoil

                #     (df['size_of_candlestick'] >100)   & #gold
                #      (df['size_of_candlestick'] < 180)

                #     (df['size_of_candlestick'] > 0.5) & #natgas
                #     (df['size_of_candlestick'] < 0.7)

                #(df['size_of_candlestick'] > 0.7) #& #natgas and copper
                # (df['size_of_candlestick'] < 1.1)

                #     (df['size_of_candlestick'] > 0.8) & #natgas
                #     (df['size_of_candlestick'] < 1.2)

                #     (df['next_low_is_lower'] == -1  ) &
                #     (df["next_high_is_higher"] == 1)
                # (df['size_of_candlestick'] > 0.50) &  # Zinc
                # (df['size_of_candlestick'] < 1.00)  # Zinc

                (df['size_of_candlestick'] > 1.4)   # Nickel
                # (df['size_of_candlestick'] < 6.00)  # Nickel
                ]
        elif filename == "SILVER-I-5MIN":
            df = df[
                (df['binary_tail_lower'] > 0) &
                #   (df["lowest_in_previous_5_instances"] > 0) &

                # (df['size_of_candlestick'] > 0.000900) #forex

                # (df['size_of_candlestick'] > 8) &  # Crudeoil
                # (df['size_of_candlestick'] < 12)  # Crudeoil

                    (df['size_of_candlestick'] >60)   #& #silver
                #      (df['size_of_candlestick'] < 180)

                #     (df['size_of_candlestick'] > 0.5) & #natgas
                #     (df['size_of_candlestick'] < 0.7)

                #(df['size_of_candlestick'] > 0.7) #& #natgas and copper
                # (df['size_of_candlestick'] < 1.1)

                #     (df['size_of_candlestick'] > 0.8) & #natgas
                #     (df['size_of_candlestick'] < 1.2)

                #     (df['next_low_is_lower'] == -1  ) &
                #     (df["next_high_is_higher"] == 1)
                # (df['size_of_candlestick'] > 0.50) &  # Zinc
                # (df['size_of_candlestick'] < 1.00)  # Zinc

                # (df['size_of_candlestick'] > 1.4)   # Nickel
                # (df['size_of_candlestick'] < 6.00)  # Nickel
                ]
        elif filename == "BITCOIN-I-5MIN":
            df = df[
                (df['binary_tail_lower'] > 0) &
                #   (df["lowest_in_previous_5_instances"] > 0) &

                # (df['size_of_candlestick'] > 0.000900) #forex

                # (df['size_of_candlestick'] > 8) &  # Crudeoil
                # (df['size_of_candlestick'] < 12)  # Crudeoil

                #(df['size_of_candlestick'] >60)   #& #gold
                (df['size_of_candlestick'] > 50)  # bitcoin

                ]
        else:
            pass

        print("------------------Final Output------------------")
        df = df[['Index', 'Open', 'High', 'Low', 'Close', 'size_of_candlestick', 'OHLC', "binary_tail_lower", "size_of_lower_shadow", "proportion_of_lower_shadow"]]
        print(df)
        size_of_df = len(df.index)
        print("Size of df: " + str(size_of_df))

        if size_of_df > 0:
            print("Positive indicator")
            playsound('beep-01a.mp3')
            obj_osUtils = osUtils()
            print(filename)
            current_time = d.now().strftime("%Y%m%d %H%M%S")
            obj_osUtils.write_text_to_file("Indicators", current_time + ":" + filename + "\n")
        print("------------------Final Output End------------------")