import os, functools, random

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

########################## 通用模块 ##################################
# 随机 ID 生成
_CHAR_SAMPLER = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
def GenRandomUUID(size=16):
	uuid = []
	if size > 0:
		for i in range(size):
			uuid.append(random.choice(_CHAR_SAMPLER))
	return "".join(uuid)

# 搜索符合指定条件的文件名
def SearchFilesInCondition(path, cond=(lambda x:False)):
	if isinstance(path, str) and os.path.isdir(path):
		return tuple(obj for obj in os.listdir(path) if os.path.isfile(obj) and cond(obj))
	return ()

if __name__ == "__main__":
	for i in range(10):
		print(GenRandomUUID(size=32))
	for fn in SearchFilesInCondition(path=".", cond=(lambda obj:bool(obj.find("free") >= 0))):
		print(fn)