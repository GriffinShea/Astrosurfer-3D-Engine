from config import *

@attr.define
class BaseProp:
	@staticmethod
	def setup(obj):
		#print(
		#	"WARNING: abstract method setup() of a BaseProp subclass is not defined. One of:\n"
		#	+ obj.propsToStr()
		#)
		return
	