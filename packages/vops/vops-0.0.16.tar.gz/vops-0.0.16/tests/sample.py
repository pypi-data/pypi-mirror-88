import sys
sys.path.append('../')

from vops import scraping
import vops

tickerSymbol = 'AMD'
contractName = 'AMD201218C00040000'


# optionObj = options.scrapePutOptions(tickerSymbol)
optionObj = scraping.scrapeCallOptions(tickerSymbol)
print(optionObj.getChain())

# options.graphLongPut(optionObj, contractName)
# #options.graphShortPut(optionObj, contractName)
# options.graphLongCall(optionObj, contractName)
# # options.graphShortCall(optionObj, contractName)
options.graphCalls(optionObj, contractName)