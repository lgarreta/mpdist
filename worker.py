"!/usr/bin/python"

inputDir  = "/dev/shm/io/in"
ouptudDir = "/dev/shm/io/out"

program = "ncd_clusters_from_matches.py"

files = sort (os.listdir (inputDir))

for file in files: 
	if os.path.exists ("%s/%s" % (inputDir, file)):
		command = "%s %s" % (program, file)
