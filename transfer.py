import os
import shutil


files = os.listdir('./_scratch')
for file in files:
	if 'slurm' in file:
		with open('./_scratch/' + file, 'r') as f:
                	lines = f.readlines()
		words = lines[46].split()
	        nb = words[2]
	        p = words[3]
	        q = words[4]
	        if int(p)*int(q) != 1:
		        shutil.move('./_scratch/' + file, './_scratch/HPL_35k/-O0/MPI_Proc_Num=' + str(int(p)*int(q)) + '/Nb=' + nb + '/PxQ=' + p + 'x' + q)
	        else:
		        shutil.move('./_scratch/' + file, './_scratch/HPL_35k/-O0/MPI_Proc_Num=' + str(int(p) * int(q)) + '/Nb=' + nb)
