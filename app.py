from Trader.fetcher import Trade, TradeHandler, datetime
from utils import utilities

######################################
#### creating Trade class object. ####
######################################

trader = Trade()

###############################
#### taking data from user ####
###############################

user_ip_syear = int(input("Enter the start Year(YYYY): "))
user_ip_smonth = int(input("Enter the start Month(MM): "))
user_ip_sdate = int(input("Enter the start Date(DD): "))
start_time = trader.convert_to_ts(datetime(user_ip_syear, user_ip_smonth, user_ip_sdate))
print(f'start time: {start_time}')

user_ip = input('Press enter if you want data till Today or press Y if you want data till a specific date: ')
if user_ip.lower() == '':
    user_ip_end_time = datetime.today()
    print(f"your end date is set to: {user_ip_end_time}")
    end_time = trader.convert_to_ts(user_ip_end_time)
    print(f'end time: {end_time}')

elif user_ip.lower() == 'y':
    user_ip_eyear = int(input("Enter the end Year(YYYY): "))
    user_ip_emonth = int(input("Enter the end Month(MM): "))
    user_ip_edate = int(input("Enter the end Date(DD): "))
    print(f"your end date is set to: {user_ip_eyear, user_ip_emonth, user_ip_edate}")
    end_time = trader.convert_to_ts(datetime(user_ip_eyear, user_ip_emonth, user_ip_edate))
    print(f'end time: {end_time}')
else:
    raise TradeHandler('Invalid end date input.')

########################
#### Main Execution ####
########################

url_to_fetch = f'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol=RELIANCE&resolution=5&from={start_time}&to={end_time}&countback=329&currencyCode=INR'
data_frame = trader.resp_to_dataframe(url_to_fetch)
print(data_frame)
try:
    path = utilities.save_to_xls(data_frame)
except Exception as e:
    raise TradeHandler('Exception occured while saving dataframe to xls...')

print(f"Dataframe successfully saved to xls at : {path}")
