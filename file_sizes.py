import os
import os.path

def get_file_sizes(channel, dir):
	files = os.listdir(dir)

	for file in files:
		if file.startswith('.'): continue # skip dot files and directories

		fpath = os.path.join(dir, file)

		if os.path.isfile(fpath):
			channel.send((fpath, os.path.getsize(fpath)))
		elif os.path.isdir(fpath):
			get_file_sizes(channel, fpath)


if __name__ == '__channelexec__':
	scandir = channel.receive()
	get_file_sizes(channel, scandir)
