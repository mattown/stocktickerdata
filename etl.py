import TickerInfo
import GetBars
import sys, os


#
# Variables
#
ticker, target_dir = sys.argv[1], sys.argv[2]


# Check to make sure our target directory exists, else throw an error message and exit
try:
    assert os.path.isdir(target_dir)
except:
    print("Invalid Target Directory")
    exit(1)


TickerInfo.get_quotes(ticker, target_dir)
GetBars.writedailyfile(ticker,5000,target_dir)
GetBars.writeweeklyfile(ticker,5000,target_dir)