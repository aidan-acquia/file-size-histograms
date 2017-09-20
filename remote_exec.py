import sys
import itertools

def remote_exec_module(gateway, module, send_item=None, callback=None):
	chan = gateway.remote_exec(module)
	
	if send_item:
		chan.send(send_item)

	if callback:
		chan.setcallback(callback)
		chan.waitclose()
	else:
		return [item for item in chan]

def spinner_collector(func, prefix=None):
	if prefix:
		sys.stdout.write(prefix)

	prop = itertools.cycle("|/-\\")

	def spinner(item):
		sys.stdout.write(prop.next())
		sys.stdout.flush()
		sys.stdout.write("\b")
		func(item)

	return spinner