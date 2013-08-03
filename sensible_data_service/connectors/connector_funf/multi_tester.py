from subprocess import Popen
from time import sleep

# multithreaded tester
for i in xrange(100):
	Popen(['python','tester.py','ef1ba605-7a6d-48f0-a0f3-67df81ce8be4_1374932793219_mainPipeline.db','> output_' + str(i)]);
	sleep(0.05)

