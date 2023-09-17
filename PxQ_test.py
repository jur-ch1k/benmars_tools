import subprocess
import time
from datetime import datetime
import sys
import traceback
import shutil


hpl_start = """HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any)
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
60000        Ns
1            # of NBs
120           Nbs
0            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
"""

hpl_fin = """16.0         threshold
1            # of panel fact
1            PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterium
4            NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
1            RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
0            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
0            DEPTHs (>=0)
2            SWAP (0=bin-exch,1=long,2=mix)
64           swapping threshold
0            L1 in (0=transposed,1=no-transposed) form
0            U  in (0=transposed,1=no-transposed) form
1            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
"""

task_num = []
vals = [['1', '8'], ['8', '1'], ['2', '4'], ['4', '2']]
#vals = [['1', '14'], ['14', '1'], ['2', '7'], ['7', '2']]
#vals = [['1', '28'], ['28', '1'], ['2', '14'], ['14', '2'], ['4', '7'], ['7', '4']]
#vals = [['1', '56'], ['56', '1'], ['2', '28'], ['28', '2'], ['4', '14'], ['14', '4'], ['7', '8'], ['8', '7']]
output = subprocess.check_output(['squeue', '-u', 'zelenchukgeorgiy_1864']).decode('ascii')
test_num = 10

print('Start at: ' + datetime.now().strftime("%H:%M:%S"))
sys.stdout.flush()

try:

	for val in vals:
		hpl_research_part = val[0] + '            Ps\n' + val[1] + '            Qs\n'
		with open('/home/zelenchukgeorgiy_1864/_scratch/HPL.dat', 'w') as file:
			file.write(hpl_start + hpl_research_part + hpl_fin)
		print('\n=====  val = ' + val[0] + 'x' + val[1] + ' started at: ' + datetime.now().strftime('%H:%M:%S') + '  =====')
		sys.stdout.flush()
	
		for i in range(test_num):
			while True:
				if output.count('zelenchu') != 3:
					output = subprocess.check_output(['sbatch', '-p', 'test', '-n', '8', 'ompi', './xhpl_o3']).decode('ascii')
					task_num.append(output.split(' ')[-1])
					print('Started: ' + output.split(' ')[-1])
					output = subprocess.check_output(['squeue', '-u', 'zelenchukgeorgiy_1864']).decode('ascii')
					# print(output)
					break
				else:
					print('Waiting...')
					sys.stdout.flush()
					time.sleep(60)
					output = subprocess.check_output(['squeue', '-u', 'zelenchukgeorgiy_1864']).decode('ascii')
					#print(output)
			sys.stdout.flush()
		while output.count('zelenchu') != 0:
			output = subprocess.check_output(['squeue', '-u', 'zelenchukgeorgiy_1864']).decode('ascii')
			print('Waiting: ' + val[0] + 'x' + val[1])
			# print(output)
	        	sys.stdout.flush()
			time.sleep(60)
except Exception:
	print(traceback.print_exc(file=sys.stdout))
	
print('Main loop finished, whaitig all tasks...\n')
sys.stdout.flush()

output = subprocess.check_output(['squeue', '-u', 'zelenchukgeorgiy_1864']).decode('ascii')
while output.count('zelenchu') != 0:
	time.sleep(60)
	print('Waiting...')
	output = subprocess.check_output(['squeue', '-u', 'zelenchukgeorgiy_1864']).decode('ascii')
	sys.stdout.flush()
try:
	res = {}
	for task in task_num:
		with open('/home/zelenchukgeorgiy_1864/_scratch/slurm-' + str(task[:-1]) + '.out', 'r') as f:
			lines = f.readlines()
		words = lines[46].split()
		nb = words[2]
	        p = words[3]
	        q = words[4]
		res[task[:-1]] = words[5].replace('.', ',')
		if int(p)*int(q) != 1:
			shutil.move('/home/zelenchukgeorgiy_1864/_scratch/slurm-' + str(task[:-1]) + '.out', 
					'/home/zelenchukgeorgiy_1864/_scratch/HPL_out/N=60k/-O3/MPI_Proc_Num=' + str(int(p)*int(q)) + '/Nb=' + nb + '/PxQ=' + p + 'x' + q)
		else:
			shutil.move('/home/zelenchukgeorgiy_1864/_scratch/slurm-' + str(task[:-1]) + '.out', 
					'/home/zelenchukgeorgiy_1864/_scratch/HPL_out/N=60k/-O3/MPI_Proc_Num=' + str(int(p)*int(q)) + '/Nb=' + nb)

	print('I\'m done)))\nResuls:\n\n')

	for key in res.keys():
		print(key)
	for val in res.values():
		print(val)

except Exception:
	print(traceback.print_exc(file=sys.stdout))

print('\nFinish at: ' + datetime.now().strftime("%H:%M:%S"))
sys.stdout.flush()
