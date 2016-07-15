#!/usr/bin/python
"""
fm_worker 1.93
 LOG: 
	- Change to read/write directly to Dropbox (API)
 	- Using fm_globals.py
	- Taken from fm_eval samsung running well.
"""

"""
Check for new workunits.
It checks new ones; if processed before, and if not then processes it.
It move from wunit to output repository, and call the evaluation 
program to put results on a output directory
"""

import os, sys
import time    # sleep
import shutil  # move
import fm_synchro as SynchroTable

# Main directories and paths
FM_HOME    = os.getenv ("DROPBOX_HOME")
inputDir   = "%s/%s" % (FM_HOME, "Dropbox/workunits")
outputDir  = "%s/%s" % (FM_HOME, "output")
resultsDir = "%s/%s" % (FM_HOME, "Dropbox/results")

SLEEP_TIME = 10   # Time to sleep to check new workunits 
#--------------------------------------------------------------------
def main (args):
	consumeWorkunits (inputDir, outputDir, resultsDir)
#--------------------------------------------------------------------

#--------------------------------------------------------------------
# Main function
# It checks for new workunits.
# if processed before, and if not then processes it.
# It move from wunit to output repository, and call the evaluation 
# program to put results on a output directory
#--------------------------------------------------------------------
def consumeWorkunits (inputDir, outputDir, resultsDir):
	workunitsDir = inputDir

	while True:
		print "\n>>>>>>>  Waiting for work units...<<<<<<<\n"
		# Check for new work units
		if not os.path.exists (workunitsDir):
			time.sleep (SLEEP_TIME)
			continue
			
		workunitList = filter (lambda x: ".tgz" in x, os.listdir (workunitsDir))
		if workunitList == []:
			time.sleep (SLEEP_TIME)
			continue

		# There are work units, then move the first one from wunit to output
		workunit = workunitList[0]
		source  = "%s/%s" % (workunitsDir, workunit)
		destiny = "%s/%s" % (outputDir, workunit)
		os.system ("mv -f %s %s" % (source, destiny))

		# Check if the work unit has been previously processed
		try:
			if SynchroTable.existsOtherWorkunit (workunit):
				print ">>>", "Already being processing the workunit: ", workunit
				continue
		except: 
			print ">>>", "Exception in existsOtherWorkunit"
			os.system ("mv -f %s %s" % (destiny, source))
			print "Unexpected error:", sys.exc_info()[0]	
			time.sleep (SLEEP_TIME)

		# Process a work unit: register, remove, eval
		SynchroTable.registerStarting (workunit)
		eval (destiny, resultsDir)
		SynchroTable.registerEnding (workunit)

#----------------------------------------------------------------------
# Call the evaluation program with the package (full path) and
# the directory (in the cloud) where to put results
#----------------------------------------------------------------------
import multiprocessing, math
def eval (fullPackageName, resultsDir):
	############ Filenames preparation ####
	outputDir   = fullPackageName.split (".tgz")[0]
	workunit = os.path.basename (outputDir)
	resultsFilename = "%s/%s.values" % (resultsDir, workunit)
	outputLog = "%s/%s.log" % (os.path.dirname (outputDir), workunit)

	print ">>>>>>>>>> Starting Processing package ", workunit, "<<<<<<"

	# Half of the number of processor
	#processors = int (math.ceil (multiprocessing.cpu_count()))  
	processors = 1
	############ Start time ###############
	startTime = time.time ()
	cmm = "echo %s > %s " % ('">>>>> TIME: Start time : %s"' % time.ctime (), outputLog)
	os.system (cmm)
	print ""
	############ Evaluation ###############
	cmm ="fm-eval.py %s %s %s %s &>> %s" % \
      	 (fullPackageName, outputDir, resultsFilename, processors, outputLog)
	print "\t", cmm, "\n"
	print ">>> Starting time", time.ctime(), "\n"
	os.system (cmm)
	print ">>> Ending time", time.ctime(), "\n"
	############ End time #################
	cmm = "echo %s >> %s " % ('">>>>> TIME: End time : %s"' % time.ctime (), outputLog)
	os.system (cmm)

	endTime = time.time ()
	totalTime = (endTime - startTime) / 60
	timeStr = ">>> TIME (minutes): %s. Start:%s, End:%s"  % (totalTime, startTime, endTime)
	print timeStr, "\n"
	cmm = "echo '%s' >> %s " % (timeStr, outputLog)
	os.system (cmm)
	print ">>>>>>>>>>> Ending EVAL <<<<<<<<<<<"

	######### Remove temporal dirs/files #####
	cmm = "rm -rf %s %s" % (fullPackageName, outputDir)
	os.system (cmm)

###############################################################################
# MAIN
###############################################################################
if __name__ == "__main__":
	main (sys.argv)
