
def remote_exec_module(gateway, module, send_item=None, callback=None):
	chan = gateway.remote_exec(module)
	
	if send_item:
		chan.send(send_item)

	if callback:
		chan.setcallback(callback)
		chan.waitclose()
	else:
		return [item for item in chan]

