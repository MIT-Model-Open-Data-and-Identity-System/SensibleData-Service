from subprocess import Popen
from time import sleep

# multithreaded tester
for i in xrange(500):
	Popen(['python','tester.py','43082bbb-0e2f-49cb-9c32-a425d262b4c9_1375626293937_mainPipeline.db','> output_' + str(i)]);
	sleep(0.05)

