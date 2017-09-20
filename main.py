# Built-ins
import math
import os
import argparse

# 3rd party packages
import execnet
from pandas import Series
from seaborn import distplot

# Our stuff
import file_sizes
from remote_exec import remote_exec_module, spinner_collector

# setup command line arguments
argp = argparse.ArgumentParser(description="Gather information about file sizes on remote host")
argp.add_argument('HOST', help="Address of remote host")
argp.add_argument('-d', metavar="DIRECTORY", help="Directory to scan on remote host (default: /mnt/gfs)", default="/mnt/gfs")
argp.add_argument('-o', metavar="OUTPUT", help="Where to save generated histogram (default: [HOST].png)", default=None)
argp.add_argument('-u', metavar="USER", help="SSH username (default: {})".format(os.environ['USER']), default=os.environ['USER'])
argp.add_argument('-p', metavar="PORT", help="SSH port on remote host (default: 22)", default=22)

args = argp.parse_args()

# create the gateway to the remote host
ssh_spec = "ssh=-p {} {}@{}//dont_write_bytecode".format(args.p, args.u, args.HOST)
gw = execnet.makegateway(ssh_spec)

# execute the module and collect results
res = []
cb = spinner_collector(res.append, prefix="Scanning... ")
remote_exec_module(gw, file_sizes, send_item=args.d, callback=cb)
print "Done! Building data set object..."

# create a dataset of the log10(file size values), and generate histogram
sizes = (math.log10(i[1]) if i[1] > 0 else 0 for i in res)
dataset = Series(sizes, name="File sizes ({} on {})".format(args.d, args.HOST))
print "Done! Creating histogram from dataset..."
hist = distplot(dataset).get_figure()

# save histogram image
output_file = args.o if args.o else '{}.png'.format(args.HOST)
hist.savefig(output_file)
print "Histogram image saved to {}".format(output_file)

# Output a few more data points
print "File Size Stats (bytes):\n  Mean: {}\n  Median: {}\n  Largest: {}".format(
	10**dataset.mean(), 
	10**dataset.median(), 
	10**dataset.max()
)