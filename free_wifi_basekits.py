import functools

LogP = print
LogN = functools.partial(print, '[Info ] ')
LogW = functools.partial(print, '[Warn ] ')
LogE = functools.partial(print, '[Error] ')
LogD = functools.partial(print, '[Debug] ')



########################## Exception 模块 ##################################
class ParameterMissingError(Exception):
	def __str__(self):
		if len(self.args) > 0:
			return "parameters {0} missing, please check ...".format(self.args)
		return "vital parameters missing ..."

class IncorrectFormatError(Exception):
	def __str__(self):
		return "account's ssid or key has wrong format ..."

class AccountNotFoundError(Exception):
	def __str__(self):
		return "account not found due to {} ...".format(
			self.args[0] if len(self.args) > 0 else "wrong index or ssid")