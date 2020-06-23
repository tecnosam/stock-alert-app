import sys, os, math
import datetime

__PATH__ = os.path.realpath("")

__PRICE_PER_COIN_IN_DOLLARS__ = 0.5

def buildUp(args):
	end = ""
	for i in range(len(args)):
		if (args[i] == args[-1]):
			end += str(args[i])
		else:
			end += str(args[i]) + ","
	return end

def superBuildUp(args):
	end = ""
	for i in range(len(args)):
		if (args[i] == args[-1]):
			end += buildUp(args[i])
		else:
			end += buildUp(args[i]) + ";"
	return end


def BuildStandardDateTime():
	obj = datetime.datetime.now()
	return "%d-%d-%d %s:%s:%s" % (obj.day, obj.month, obj.year, obj.hour, obj.minute, obj.second)
