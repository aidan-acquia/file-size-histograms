# Built-ins
import math
import os
import sys
import argparse

# 3rd party packages
import execnet
from pandas import Series
from seaborn import distplot

# Our stuff
import file_sizes
from remote_exec import remote_exec_module

argp = argparse.ArgumentParser(description="Gather information about file sizes on remote host")
argp.add_argument('HOST', help="Address of remote host")
argp.add_argument('-d', metavar="DIRECTORY", help="Directory to scan on remote host (default: /mnt/gfs)", default="/mnt/gfs")
argp.add_argument('-o', metavar="OUTPUT", help="Path of where to save generated histogram (default: [HOST].png)", default=None)
argp.add_argument('-u', metavar="USER", help="SSH username (default: {})".format(os.environ['USER']), default=os.environ['USER'])
argp.add_argument('-p', metavar="PORT", help="SSH port on remote host (default: 22)", default=22)

args = argp.parse_args()
# print dir(args)

# sys.exit()

ssh_spec = "ssh=-p {} {}@{}//dont_write_bytecode".format(args.p, args.u, args.HOST)
gw = execnet.makegateway(ssh_spec)

res = []
remote_exec_module(gw, file_sizes, args.d, res.append)

sizes = (math.log(i[1], 10) for i in res)
dataset = Series(sizes, name="File sizes ({} on {})".format(args.d, args.HOST))
hist = distplot(dataset, rug=True).get_figure()

output_file = args.o if args.o else '{}.png'.format(args.HOST)
hist.savefig(output_file)
print "Histogram image saved to {}".format(output_file)

print "Mean: {}\nMedian: {}\nLargest: {}".format(10**dataset.mean(), 10**dataset.median(), 10**dataset.max())
print "Done!"