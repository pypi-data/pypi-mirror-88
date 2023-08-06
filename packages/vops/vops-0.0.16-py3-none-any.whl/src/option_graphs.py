import matplotlib.pyplot as plt

#Inputs: x = stock price, strike = strike price, p = premium
#Output: Net Profit or Loss

def longCall(x, strike, p):
	if x < strike:
		return -p
	elif x >= strike:
		return x - strike - p
	else:
		return None

def shortCall(x, strike, p):
	if x < strike:
		return p
	elif x >= strike:
		return p - (x - strike)
	else:
		return None

def longPut(x, strike, p):
	if x < strike:
		return strike - x - p
	elif x >= strike:
		return -p


def shortPut(x, strike, p):
	if x < strike:
		return p + (x - strike)
	elif x >= strike:
		return p

def graphCalls(optionObj, contractName):

	s = float(optionObj.getAttr(contractName, 'Strike'))
	lp = float(optionObj.getAttr(contractName, 'Last Price'))

	x = [i for i in range(0, 2 * round(float(s)))]
	y_long = [longCall(i, s, lp) for i in x]
	y_short = [shortCall(i, s, lp) for i in x]

	plt.style.use('dark_background')

	fig, axs = plt.subplots(2)
	fig.suptitle("Call: " + contractName)
	axs[0].plot(x, y_long)
	axs[0].title.set_text("Long Call")

	axs[1].plot(x, y_short)
	axs[1]. title.set_text("Short Call")

	fig = plt.gcf().subplots_adjust(hspace = 0.5)
	# fig.subplots_adjust(hspace = 0.2)

	plt.show()


def graphLongCall(optionObj, contractName):
	s = float(optionObj.getAttr(contractName, 'Strike'))
	lp = float(optionObj.getAttr(contractName, 'Last Price'))

	x = [i for i in range(0, 2 * round(float(s)))]
	y = [longCall(i, s, lp) for i in x]

	# plt.figure(num='Options Graph', edgecolor='black')
	plt.style.use('dark_background')

	plot_title = contractName
	plt.title(plot_title)
	plt.plot(x, y, ':')
	plt.show()

def graphShortCall(optionObj, contractName):
	s = float(str(optionObj.getAttr(contractName, 'Strike')).replace(',', '').replace('\n', ''))
	lp = float(optionObj.getAttr(contractName, 'Last Price'))

	x = [i for i in range(0, 2 * round(float(s)))]
	y = [shortCall(i, s, lp) for i in x]

	# plt.figure(num='Options Graph', edgecolor='black')
	plt.style.use('dark_background')

	plot_title = contractName
	plt.title(plot_title)
	plt.plot(x, y, ':')
	plt.show()

def graphLongPut(optionObj, contractName):
	s = float(str(optionObj.getAttr(contractName, 'Strike')).replace(',', '').replace('\n', ''))
	lp = float(optionObj.getAttr(contractName, 'Last Price'))

	x = [i for i in range(0, 2 * round(float(s)))]
	y = [longPut(i, s, lp) for i in x]

	# plt.figure(num='Options Graph', edgecolor='black')
	plt.style.use('dark_background')

	plot_title = contractName
	plt.title(plot_title)
	plt.plot(x, y, ':')
	plt.show()

def graphShortPut(optionObj, contractName):
	s = float(str(optionObj.getAttr(contractName, 'Strike')).replace(',', '').replace('\n', ''))
	lp = float(optionObj.getAttr(contractName, 'Last Price'))

	x = [i for i in range(0, 2 * round(float(s)))]
	y = [shortPut(i, s, lp) for i in x]

	# plt.figure(num='Options Graph', edgecolor='black')
	plt.style.use('dark_background')

	plot_title = contractName
	plt.title(plot_title)
	plt.plot(x, y, ':')
	plt.show()
