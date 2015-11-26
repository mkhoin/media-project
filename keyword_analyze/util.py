
def load_file(fname):
	data = []
	with open(fname, "r") as f:
		while True:
			line = f.readline()
			if not line: break
			data.append(line.replace("\n", ""))

	return data
