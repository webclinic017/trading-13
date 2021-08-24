import os
import sys
import time
from src.truedata.timeUtils import *
from src.truedata.apiUtils import *
from src.truedata.osUtils import *
from src.truedata.tradeStrategy import *
from src.truedata.calcStrategy import *
import requests

def main(stocks="true", crypto="true"):
    obj_timeUtils = timeUtils()
    obj_apiUtils = apiUtils()
    obj_osUtils = osUtils()
    obj_strategy = tradeStrategy()
    obj_calcstrategy = calcStrategy()

    if stocks == "true":
        #Check if current time is one second at the end of a minute

        list_scrips = ["CRUDEOIL-I", "GOLDM-I", "NATURALGAS-I", "COPPER-I", "ZINC-I", "NICKEL-I", "SILVER-I"]
        obj_apiUtils.authenticate()
        while True:
            current_time_is_end_of_minute = obj_timeUtils.check_if_current_time_is_end_of_minute()



            if current_time_is_end_of_minute:
                # Get the last bar for the scripts
                for i in list_scrips:
                    print("\n\n\n\nProcessing " + str(i))

                    response_text = obj_apiUtils.get_last_bar(i)

                    # Write text to file
                    obj_osUtils.write_text_to_file(i, response_text.split("\n")[1])

                    #Read from file, get last five minutes data and calculate 5 min chart.
                    list_one_minute_bars = obj_osUtils.read_text_from_file(i, 5)

                    current_time_is_end_of_five_minutes = obj_timeUtils.check_if_current_time_is_end_of_five_minutes()

                    if current_time_is_end_of_five_minutes:
                        print("Calculating 5 minutes")
                        #Calculate 5 minutes at the end of 5 minutes
                        list_one_minute_bars = obj_osUtils.text_to_array(list_one_minute_bars)
                        list_five_minute_stats = obj_strategy.calculate_five_minute_stats(list_one_minute_bars)
                        print(list_five_minute_stats)

                        #Write to file
                        str_five_minute_stats = ','.join(list_five_minute_stats)
                        obj_osUtils.write_text_to_file(i + "-5MIN", str_five_minute_stats)
                        obj_osUtils.write_text_to_file(i + "-5MIN", "\n")
                        print("5 minutes written to file completed")

                        #Calculate strategy

                        #print(list_one_minute_bars)
                        obj_calcstrategy.calculate(i + "-5MIN")

                        #time.sleep(1)
                    else:
                        print("Not End of five minutes")
            else:
                #print("No", end='\r')
                sys.stdout.write('\r' + "Not end of minute")
            time.sleep(1)

    if crypto == "true":
        while True:
            current_time_is_end_of_minute = obj_timeUtils.check_if_current_time_is_end_of_minute()

            if current_time_is_end_of_minute:
                current_time_is_end_of_five_minutes = obj_timeUtils.check_if_current_time_is_end_of_five_minutes()

                if current_time_is_end_of_five_minutes:
                    # Get five minute data
                    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
                    url = 'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=BTC&market=USD&interval=5min&datatype=csv&apikey=75C9100OJGINJSD5'
                    r = requests.get(url)
                    # data = r.json()

                    # print(str(r.content.decode("utf-8")))
                    data = r.content.decode("utf-8")

                    arr_data = r.content.decode("utf-8").split("\r\n")

                    print(len(arr_data))
                    last_minute = (arr_data)[1]
                    print(last_minute)
                    obj_osUtils.write_text_to_file("BITCOIN-I-" + "5MIN", last_minute + "\n")

                    list_one_minute_bars = obj_osUtils.read_text_from_file("BITCOIN-I-5MIN", 5)
                    print(list_one_minute_bars)
                    obj_calcstrategy.calculate("BITCOIN-I" + "-5MIN")

            else:
                sys.stdout.write('\r' + "Not end of minute")
            time.sleep(1)




        #Append five minute to file


        #Run strategy


    
    #Add the data to a file

    #Check if current time is 5 minutes

    #Retreive data from the file and calculate 5 minute bars

    #Add this data to another file
    
    #Run the strategy

    #Play alarm if strategy is successful

    #Thank me later
    pass



try:
    main(stocks="true", crypto="false")
except Exception as e:
    print(str(e))








