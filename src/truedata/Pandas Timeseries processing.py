#!/usr/bin/env python
# coding: utf-8
print("Pandas Tutorial")
import pandas as pd


pd.set_option('display.max_colwidth', -1)
#pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.expand_frame_repr', False)


df = pd.read_csv("CRUDEOIL-6M-5min")

print("Basic columns")

#df = df[['Index', 'Open', 'High', 'Low', 'Close', 'Time']]
df = df[['Index', 'Open', 'High', 'Low', 'Close']]

df["size_of_candlestick"] = df['High'] - df['Low']
df["size_of_body"] = df['Close'] - df['Open']
df['rise_or_fall'] = df['size_of_body'].apply(lambda x: '1' if x>0 else '-1')
df["proportion_of_body"] = df["size_of_body"].abs()/df["size_of_candlestick"].abs() *100

def size_of_upper_shadow(rise_or_fall, open, high, low, close):
    if int(rise_or_fall) == 1:
        return float(high) - float(close)
        
    elif int(rise_or_fall) == -1:
        return float(high) - float(open)
        
def size_of_lower_shadow(rise_or_fall, open, high, low, close):
    if int(rise_or_fall) == 1:
        return float(open) - float(low)
        
    elif int(rise_or_fall) == -1:
        return float(close) - float(low)

df["size_of_upper_shadow"] = df[['rise_or_fall','Open','High','Low','Close']].apply(lambda x: size_of_upper_shadow(*x), axis=1)
df["propertion_of_upper_shadow"] = df["size_of_upper_shadow"].abs()/df["size_of_candlestick"].abs() *100
df["size_of_lower_shadow"] = df[['rise_or_fall','Open','High','Low','Close']].apply(lambda x: size_of_lower_shadow(*x), axis=1)
df["proportion_of_lower_shadow"] = df["size_of_lower_shadow"].abs()/df["size_of_candlestick"].abs() *100

def binary_tail(a,b):
    proportion_of_tail = 75
    if a>proportion_of_tail or b>proportion_of_tail:
        return 1
    else:
        return -1

def binary_tail_lower(a,b):
    proportion_of_tail = 70
    if b>proportion_of_tail and b<101:
        return 1
    else:
        return -1    
    
df['binary_tail'] = df[['propertion_of_upper_shadow','proportion_of_lower_shadow']].apply(lambda x: binary_tail(*x), axis=1)
df['binary_tail_lower'] = df[['propertion_of_upper_shadow','proportion_of_lower_shadow']].apply(lambda x: binary_tail_lower(*x), axis=1)

df["binary_body"] = df['proportion_of_body'].apply(lambda x: '1' if x>95 else '-1') #If size of body is high

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
#df['Prev_Time'] = df.loc[df['VALUE'].shift(-1)==1, 'TIME']

k=10
def low_is_lower(a,b):
    if float(a)>=float(b):
        return 1
    else:
        return -1
    
def high_is_higher(a,b):
    if float(a)<=float(b):
        return 1
    else:
        return -1
    
    
df["previous_low"] = df['Low'].shift(1)    
df['binary_low_is_lower_than_previous_low'] = df[['Low','previous_low']].apply(lambda x: low_is_lower(*x), axis=1)
df["previous_high"] = df['High'].shift(1)
df["binary_high_is_higher_than_previous_high"] = df[['High','previous_high']].apply(lambda x: high_is_higher(*x), axis=1)


df["next_low"] = df['Low'].shift(-1)    
df['next_low_is_lower'] = df[['Low','next_low']].apply(lambda x: low_is_lower(*x), axis=1)
df["next_high"] = df['High'].shift(-1)
df["next_high_is_higher"] = df[['High','next_high']].apply(lambda x: high_is_higher(*x), axis=1)


df["value_max_high_in_next_10_instances"] =  df["High"].rolling(k).max().shift(-k)
df["value_max_low_in_next_10_instances"] = df["Low"].rolling(k).min().shift(-k)

df["value_max_high_in_next_10_instances"] = pd.to_numeric(df["value_max_high_in_next_10_instances"])
df["value_max_low_in_next_10_instances"] = pd.to_numeric(df["value_max_low_in_next_10_instances"])
df["value_max_low_if_low_is_max_low"] = pd.to_numeric(df["Low"])
df["Close"] = pd.to_numeric(df["Close"])


def actual_low(value_max_low_in_next_10_instances,value_max_low_if_low_is_max_low):
    return max(value_max_low_in_next_10_instances, value_max_low_if_low_is_max_low)
df["actual_low"] =  df[['value_max_low_in_next_10_instances','value_max_low_if_low_is_max_low']].apply(lambda x: actual_low(*x), axis=1)

def proportion_of_max_high_in_next_10_instances(value_max_high_in_next_10_instances, close):
    return ((value_max_high_in_next_10_instances-close)/close)*100
    

def proportion_of_max_low_in_next_10_instances(proportion_of_max_low_in_next_10_instances, close):
    return ((close-proportion_of_max_low_in_next_10_instances)/close)*100

def proportion_of_max_low_in_next_10_instances_if_close_is_max_low(close, low):
    return ((close-low)/close)*100

def proportion_of_actual_low(actual_low,close):
    return ((close-actual_low)/close)*100
    

df["proportion_of_max_high_in_next_10_instances"] = df[['value_max_high_in_next_10_instances','Close']].apply(lambda x: proportion_of_max_high_in_next_10_instances(*x), axis=1)
df["proportion_of_max_low_in_next_10_instances"] = df[['value_max_low_in_next_10_instances','Close']].apply(lambda x: proportion_of_max_low_in_next_10_instances(*x), axis=1)
df["proportion_of_max_low_in_next_10_instances_if_close_is_max_low"] = df[['Close','Low']].apply(lambda x: proportion_of_max_low_in_next_10_instances_if_close_is_max_low(*x), axis=1)
df["proportion_of_actual_low"] = df[['actual_low','Close']].apply(lambda x: proportion_of_actual_low(*x), axis=1)


#Lowest in the previous 5 instances
def lowest_in_previous_5_instances(value_max_low_in_previous_5_instances, low):
    if low < value_max_low_in_previous_5_instances:
        return 1
    else:
        return 0

df["value_max_low_in_previous_5_instances"] = df["Low"].rolling(k).min().shift(k)
df["lowest_in_previous_5_instances"] = df[['value_max_low_in_previous_5_instances','Low']].apply(lambda x: lowest_in_previous_5_instances(*x), axis=1)


# In[10]:


#Stratey 2: When two or more candlesticks have big tails

# df['rolling_sum_of_two_values'] = df['binary_tail_lower'].rolling(2).sum()

# df = df[
#     (df['rolling_sum_of_two_values'] > 0) &
#     (df['size_of_candlestick'] > 0.000100)
    
# ]

# def check_if_max_low_breaches_low(a,b):
#     if float(a)<float(b):
#         return -1
#     else:
#         return 0

# df["max_low_breaches_candlestick_low"] = df[['value_max_low_in_next_10_instances','Low']].apply(lambda x: check_if_max_low_breaches_low(*x), axis=1)


# df


# In[11]:


# print("T")
# Total = df['proportion_of_max_high_in_next_10_instances'].median()
# print (Total)
# Total = df['proportion_of_max_low_in_next_10_instances'].median()
# print (Total)
# Total = df['proportion_of_max_low_in_next_10_instances_if_close_is_max_low'].median()
# print (Total)

# Total = df['max_low_breaches_candlestick_low'].sum()
# print (Total)
# print(len(df.index))


# In[12]:


#Strategy 1: Big tail
print("Filter columns")
#df[df.binary_tail_lower > 0 & df.rise_or_fall>0]

'''
df["rise_or_fall"] = pd.to_numeric(df["rise_or_fall"])
df["proportion_of_max_high_in_next_10_instances"] = pd.to_numeric(df["proportion_of_max_high_in_next_10_instances"])
df["proportion_of_max_low_in_next_10_instances"] = pd.to_numeric(df["proportion_of_max_low_in_next_10_instances"])
df["proportion_of_actual_low"] = pd.to_numeric(df["proportion_of_actual_low"])

pd.set_option('display.max_colwidth', None)

df = df[
    (df['binary_tail_lower'] > 0) &
    (df['size_of_candlestick'] > 0.000400) &
    (df['size_of_candlestick'] < 0.000800)     
    
]

print("Size")
print(len(df.index))


#(df['size_of_candlestick'] > 0.000000) 
#(df['binary_tail_lower'] > 0) & 
#(df['size_of_candlestick'] > 0.000100) &

def check_if_high_is_more_possible_than_low(a,b):
    if float(a)>float(b):
        return 1
    else:
        return -1

#df["check_if_high_is_more_possible_than_low"] = df[['proportion_of_max_high_in_next_10_instances','proportion_of_max_low_in_next_10_instances']].apply(lambda x: check_if_high_is_more_possible_than_low(*x), axis=1)

df["diff_in_high_and_low"] = df["proportion_of_max_high_in_next_10_instances"] - df["proportion_of_max_low_in_next_10_instances"]

def check_if_max_low_breaches_low(a,b):
    if float(a)<float(b):
        return -1
    else:
        return 0

df["max_low_breaches_candlestick_low"] = df[['value_max_low_in_next_10_instances','Low']].apply(lambda x: check_if_max_low_breaches_low(*x), axis=1)

    
df
'''


# In[13]:


#Strategy 3: Big tail with tall candlesticks next
print("Filter columns")
#df[df.binary_tail_lower > 0 & df.rise_or_fall>0]

#Change to numeric
df["rise_or_fall"] = pd.to_numeric(df["rise_or_fall"])
df["proportion_of_max_high_in_next_10_instances"] = pd.to_numeric(df["proportion_of_max_high_in_next_10_instances"])
df["proportion_of_max_low_in_next_10_instances"] = pd.to_numeric(df["proportion_of_max_low_in_next_10_instances"])
df["proportion_of_actual_low"] = pd.to_numeric(df["proportion_of_actual_low"])

pd.set_option('display.max_colwidth', None)


df = df[
    (df['binary_tail_lower'] > 0) &
    #   (df["lowest_in_previous_5_instances"] > 0) &
    
    
    #(df['size_of_candlestick'] > 0.000900) #forex
    
    
    (df['size_of_candlestick'] > 8) & #Crudeoil
   (df['size_of_candlestick'] < 12) #Crudeoil
    
    
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

print(df)

print("Size")
print(len(df.index))


import sys
sys.exit()

#(df['size_of_candlestick'] < 0.000900) &
#(df['size_of_candlestick'] > 0.000000) 
#(df['binary_tail_lower'] > 0) & 
#(df['size_of_candlestick'] > 0.000100) &

def check_if_high_is_more_possible_than_low(a,b):
    if float(a)>float(b):
        return 1
    else:
        return -1

#df["check_if_high_is_more_possible_than_low"] = df[['proportion_of_max_high_in_next_10_instances','proportion_of_max_low_in_next_10_instances']].apply(lambda x: check_if_high_is_more_possible_than_low(*x), axis=1)

df["diff_in_high_and_low"] = df["proportion_of_max_high_in_next_10_instances"] - df["proportion_of_max_low_in_next_10_instances"]

def check_if_max_low_breaches_low(a,b):
    if float(a)<float(b):
        return -1
    else:
        return 0

df["max_low_breaches_candlestick_low"] = df[['value_max_low_in_next_10_instances','Low']].apply(lambda x: check_if_max_low_breaches_low(*x), axis=1)

    
df


# In[ ]:





# In[14]:


df_positive=df[
    (df['max_low_breaches_candlestick_low'] == 0) 
]
df_negative=df[
    (df['max_low_breaches_candlestick_low'] != 0) 
]


# In[15]:


#Results for Strategy 1
'''
print("P")
Total = df_positive['proportion_of_max_high_in_next_10_instances'].median()
print (Total)
Total = df_positive['proportion_of_max_low_in_next_10_instances'].median()
print (Total)
Total = df_positive['proportion_of_max_low_in_next_10_instances_if_close_is_max_low'].median()
print (Total)



print("N")
Total = df_negative['proportion_of_max_high_in_next_10_instances'].median()
print (Total)
Total = df_negative['proportion_of_max_low_in_next_10_instances'].median()
print (Total)
Total = df_negative['proportion_of_max_low_in_next_10_instances_if_close_is_max_low'].median()
print (Total)


print("T")
Total = df['proportion_of_max_high_in_next_10_instances'].median()
print (Total)
Total = df['proportion_of_max_low_in_next_10_instances'].median()
print (Total)
Total = df['proportion_of_max_low_in_next_10_instances_if_close_is_max_low'].median()
print (Total)
print("TS")
Total = df['proportion_of_max_high_in_next_10_instances'].sum()
print (Total)
Total = df['proportion_of_max_low_in_next_10_instances'].sum()
print (Total)
Total = df['proportion_of_max_low_in_next_10_instances_if_close_is_max_low'].sum()
print (Total)

Total = df['diff_in_high_and_low'].mean()
print (Total)
Total = df['diff_in_high_and_low'].median()
print (Total)
Total = df['diff_in_high_and_low'].sum()
print (Total)
'''


#Stop loss hit
print("#Stop loss hit")
breach = df['max_low_breaches_candlestick_low'].sum()

print (breach)
print("Out of")
print (len(df.index))

print("% of breach: " + str(
    abs(int(breach)/int(len(df.index))*(100))
        )
     )

breach_percentage = abs(int(breach)/int(len(df.index))*(100))

Total = len(df.index)
unbreach = Total+breach
print("Unbreach " + str(unbreach))

df_stop_loss_hit=df[
    (df['max_low_breaches_candlestick_low'] <0
) 
]
#breach_loss = df_stop_loss_hit['proportion_of_max_low_in_next_10_instances_if_close_is_max_low'].median()
breach_loss = df['proportion_of_actual_low'].median()
print("When stop loss was hit, the average loss was: " + str(breach_loss))
print("Total balance loss: " + str(breach_loss * breach))
total_loss=breach_loss * breach

print("#Stop loss not hit")
df_stop_loss_nothit=df[
    (df['max_low_breaches_candlestick_low'] == 0
) 
]
unbreach_loss = df_stop_loss_nothit['proportion_of_max_high_in_next_10_instances'].median()

print("\n")
print("When stop loss was not hit, the average gain was: " + str(unbreach_loss))
print("Total balance gain: " + str(unbreach_loss * unbreach))
total_gain = unbreach_loss * unbreach
print("\n")
print("Net: " + str(total_gain+total_loss))
print("\n")


print(df['proportion_of_max_high_in_next_10_instances'].sum())
print(df['proportion_of_actual_low'].sum())

print("Difference: " + str(df['proportion_of_max_high_in_next_10_instances'].sum() - df['proportion_of_actual_low'].sum()))
print("Difference in terms of %: " + str(df['proportion_of_max_high_in_next_10_instances'].sum() - df['proportion_of_actual_low'].sum()/df['proportion_of_max_high_in_next_10_instances'].sum()*100))

diff_percentage = df['proportion_of_max_high_in_next_10_instances'].sum() - df['proportion_of_actual_low'].sum()/df['proportion_of_max_high_in_next_10_instances'].sum()*100

total_score = abs(breach_percentage) * abs(diff_percentage)
print(str(total_score) + str( " : should be less than 2000"))


# In[16]:


df = df[['Index', 'Open', 'High', 'Low', 'Close', 'size_of_candlestick', 'OHLC', 'OHLC1nextshift', 'OHLC2nextshift', 'OHLC3nextshift', 'OHLC4nextshift', 'OHLC5nextshift', 'OHLC6nextshift', 'OHLC7nextshift', 'OHLC8nextshift', 'OHLC9nextshift', 'OHLC10nextshift']]



source_col_loc = df.columns.get_loc('OHLC') # column position starts from 0
number_of_bars=12
df['OHLCconcat'] = df.iloc[:, source_col_loc:source_col_loc+number_of_bars].apply(
    lambda x: ",".join(x.astype(str)), axis=1)


def split_string(input_str):
    #spilt the string into arrays
    list_ohlc = []
    list_ohlc_split = input_str.split(",")
    list_temp = []
    
    for i in range(0,len(list_ohlc_split)):
        if (i+1)%4!=0:
            
            list_temp.append(list_ohlc_split[i])
        else:
            list_temp.append(list_ohlc_split[i])
            list_ohlc.append(list_temp)
            list_temp = []
            

    return list_ohlc


import math
# def calc_profit(list_ohlc):
    
    
#     #print(list_ohlc)
#     #print(len(list_ohlc))
#     stop_loss = list_ohlc[0][2]
#     stop_loss_hit = False
#     max_low=0
#     max_profit = 0
#     for i in range(1,len(list_ohlc)):

#         if float(list_ohlc[i][2])<float(stop_loss):
#             stop_loss_hit = True
#             max_low=list_ohlc[i][2]
#             max_profit=max_low
#             break
#         else:
#             stop_loss_hit=False

#     #Calculate profit

#     if stop_loss_hit:
#         return max_profit
#     else:
#         #Calculate max profit
#         for i in range(1,len(list_ohlc)):
#             if float(list_ohlc[i][1])>float(max_profit):
#                 max_profit = list_ohlc[i][1]                


#     return max_profit
    

global target 
target = 0.015
def calc_profit(list_ohlc):
    
    
    #print(list_ohlc)
    #print(len(list_ohlc))
    stop_loss = list_ohlc[0][2]
    close = list_ohlc[0][3]
    
    
    stop_loss_hit = False
    max_low=0
    max_profit = 0
    stop_loss_hit_at=0
    
    stop_loss_perc = (float(close) - float(stop_loss))/float(close) * 100
    target_and_stop_loss = abs(stop_loss_perc)
    #target_and_stop_loss=0.13
    
    
    for i in range(1,len(list_ohlc)):
        curr_low = list_ohlc[i][2]
        perc_curr_low = (float(close) - float(curr_low)) / float(close) * 100
        curr_high=list_ohlc[i][1]
        #if float(list_ohlc[i][2])<float(stop_loss):
        
        if (float(curr_high)-float(close))/float(close)*100>(target_and_stop_loss*1.5):
            #Calculate max profit
            max_profit = float(list_ohlc[i][3])
            max_profit = float(close) + (target_and_stop_loss / 100  * float(close))
            break
        elif float(perc_curr_low)>float(target_and_stop_loss):               
            stop_loss_hit = True
            max_low = float(close) - (target_and_stop_loss / 100  * float(close))
            max_profit =max_low
            stop_loss_hit_at = list_ohlc[i][2]
            break

        
#         elif float(stop_loss)>float(curr_low) or float(perc_curr_low)>float(0.1):    
#             if float(perc_curr_low)>float(0.1):
#                 stop_loss_hit = True
#                 max_low=float(close) - (target_and_stop_loss / 100  * float(close))
#                 max_profit=max_low
#             elif float(stop_loss)>float(curr_low):
#                 stop_loss_hit = True
#                 max_low=list_ohlc[i][2]
#                 max_profit=max_low
#                 stop_loss_hit_at = list_ohlc[i][2]

#             stop_loss_hit_at= max_low
            
            
        else:
            max_profit = float(list_ohlc[i][3])
    
    max_profit_proportion = (float(max_profit)-float(close))/float(close)*100    
    
    return max_profit, max_profit_proportion, target_and_stop_loss, stop_loss_hit_at
    

    
    
    
def calc_max_low(list_ohlc):    
    max_low = list_ohlc[0][3]
    max_high = list_ohlc[0][3]
    close = list_ohlc[0][3]

    
    for i in range(2,len(list_ohlc)):
        curr_low = list_ohlc[i][2]
        curr_high=list_ohlc[i][1]
        
        if curr_low < max_low:
            max_low = curr_low
            
        if curr_high > max_high:
            max_high = curr_high
        
    max_low_perc = (float(close) - float(max_low))  / float(close) * 100
    return max_low_perc




def calc_max_high(list_ohlc):    
    max_low = list_ohlc[0][3]
    max_high = list_ohlc[0][3]
    close = list_ohlc[0][3]
    
    for i in range(2,len(list_ohlc)):
        curr_low = list_ohlc[i][2]
        curr_high=list_ohlc[i][1]
        
        if curr_low < max_low:
            max_low = curr_low
            
        if curr_high > max_high:
            max_high = curr_high

    max_high_perc = (float(max_high) - float(close))    / float(close) * 100            
    return max_high_perc



def stop_loss_hit(list_ohlc):
    
    
    #print(list_ohlc)
    #print(len(list_ohlc))
    stop_loss = list_ohlc[0][2]
    stop_loss_hit = False
    max_low=0
    max_profit = 0
    for i in range(1,len(list_ohlc)):

        if float(list_ohlc[i][2])<float(stop_loss):
            stop_loss_hit = True
            max_low=list_ohlc[i][2]
            max_profit=max_low
            break
        else:
            stop_loss_hit=False
    return stop_loss_hit

df["split_string"] = df[['OHLCconcat']].apply(lambda x: split_string(*x), axis=1)

df["calc_profit_all_fields"] = df[['split_string']].apply(lambda x: calc_profit(*x), axis=1)


df["max_possible_low"] = df[['split_string']].apply(lambda x: calc_max_low(*x), axis=1)
df["max_possible_high"] = df[['split_string']].apply(lambda x: calc_max_high(*x), axis=1)



df["calc_profit"] = df[['calc_profit_all_fields']].apply(lambda x:  str(x[0][0]), axis=1)
df["proportion_calc_profit"] = df[['calc_profit_all_fields']].apply(lambda x:  str(x[0][1]), axis=1)
df["target"] = df[['calc_profit_all_fields']].apply(lambda x: str(x[0][2]), axis=1)
df["stop_loss_hit_at"] = df[['calc_profit_all_fields']].apply(lambda x: str(x[0][3]), axis=1)



df["calc_profit"] = pd.to_numeric(df["calc_profit"])
df["proportion_calc_profit"] = pd.to_numeric(df["proportion_calc_profit"])
df["target"] = pd.to_numeric(df["target"])
df["stop_loss_hit_at"] = pd.to_numeric(df["stop_loss_hit_at"])



# df["stop_loss_hit"] = df[['split_string']].apply(lambda x: stop_loss_hit(*x), axis=1)

#df["calc_profit_all_fields"] = pd.to_numeric(df["calc_profit_all_fields"])


#df["proportion_calc_profit"] = (df["calc_profit"] - df['Close'])/df['Close']*100
# df["proportion_calc_profit"] = df[['split_string']].apply(lambda x: calc_profit_proportion(*x), axis=1)


df = df[(df['proportion_calc_profit'] != -100)]
sum_calc_profit = df['proportion_calc_profit'].sum()
median_calc_profit = df['proportion_calc_profit'].median()
mean_calc_profit = df['proportion_calc_profit'].mean()
max_calc_profit = df['proportion_calc_profit'].max()
min_calc_profit = df['proportion_calc_profit'].min()





print( "Total size of df: " + str(len(df.index)))
print( "Target hit: " + str(len(df[
    (df['proportion_calc_profit'] > target) 
])))
print("Sum of profit: " +  str(sum_calc_profit))
print("Median of profit: " +  str(median_calc_profit))
print("Mean of profit: " +  str(mean_calc_profit))
print("Max of profit: " +  str(max_calc_profit))
print("Min of profit: " +  str(min_calc_profit))
df_neg = df[(df['proportion_calc_profit'] < 0)]
print("Negative: " +  str(len(df_neg.index)))
df_pos = df[(df['proportion_calc_profit'] > 0.02)]
print("0.03: " +  str(len(df_pos.index)))
print("\n")


print("Sum of max_possible_low: " +  str(df['max_possible_low'].sum()))
print("Mean of max_possible_low: " +  str(df['max_possible_low'].mean()))
print("Sum of max_possible_high: " +  str(df['max_possible_high'].sum()))
print("Mean of max_possible_high: " +  str(df['max_possible_high'].mean()))
print("\n")


print("Value count")
#print(df['stop_loss_hit'].value_counts(normalize=True))

print("\n")
print("Target hit perc")
print(int(len(df[
    (df['proportion_calc_profit'] > target) 
])) / int(len(df.index)) * 100)

print("\n")
print("Stop loss hit")
print(int(len(df[
    (df['proportion_calc_profit'] < 0) 
])) / int(len(df.index)) * 100)


#Region end
#df.head(20)


# In[17]:


pd.set_option('display.max_rows', 500)
df


# In[18]:


df.to_csv("GOLD-calculations.csv")


# In[ ]:




