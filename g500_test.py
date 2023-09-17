import subprocess
import time
from datetime import datetime
import sys
import traceback
import shutil

# source_file = './g500_non_pwr_2_O3_valid_off'
# source_file = './g500_non_pwr_2_O2_valid_off'
# source_file = './g500_non_pwr_2_O1_valid_off'
# source_file = './sssp_non_pwr_2_O3_valid_off'
# source_file = './sssp_non_pwr_2_O2_valid_off'
source_file = './sssp_non_pwr_2_O1_valid_off'

# proc_nums = ['14', '28', '56']
# proc_nums = ['16', '32']
# proc_per_node = '14'
# proc_per_node = '8'
scale = '25'
# edgefactor = ['8', '16', '32']
test_num = 10

proc_nums = ['14', '16']
ef = '32'


output = subprocess.check_output(['squeue', '-u', 'zelenchukgeorgiy_1864']).decode('ascii')

print('Start at: ' + datetime.now().strftime("%H:%M:%S"))
sys.stdout.flush()

task_info = {'task_num': [],
             'proc_num': [],
             # 'ppn': []
             }

try:
    for proc_num in proc_nums:
        print('\n===== proc_num = ' + proc_num + ' started at: ' + datetime.now().strftime('%H:%M:%S') + '  =====')
        sys.stdout.flush()
        # for ef in edgefactor:
        #     print('\n===== ef = ' + ef + ' started at: ' + datetime.now().strftime('%H:%M:%S') + '  =====')
        #     sys.stdout.flush()
        # for ppn in proc_per_node:
        #     print('\n===== proc_per_node = ' + ppn + ' started at: ' + datetime.now().strftime('%H:%M:%S') + '  =====')
        #     sys.stdout.flush()
        if proc_num == '14':
            proc_per_node = '14'
        else:
            proc_per_node = '8'
        for i in range(test_num):
            while True:
                if output.count('zelenchu') != 3:
                    output = subprocess.check_output(['sbatch', '-p', 'compute', '-n', proc_num, '--ntasks-per-node', proc_per_node, 'ompi', source_file, scale, ef]).decode('ascii')
                    task_info['task_num'].append(output.split(' ')[-1])
                    task_info['proc_num'].append(proc_num)
                    # task_info['ppn'].append(proc_per_node)
                    print('Started: ' + output.split(' ')[-1])
                    output = subprocess.check_output(['squeue', '-u', 'zelenchukgeorgiy_1864']).decode('ascii')
                    break
                else:
                    print('Waiting...')
                    sys.stdout.flush()
                    time.sleep(60)
                    output = subprocess.check_output(['squeue', '-u', 'zelenchukgeorgiy_1864']).decode('ascii')
            sys.stdout.flush()
            # while output.count('zelenchu') != 0:
            #     output = subprocess.check_output(['squeue', '-u', 'zelenchukgeorgiy_1864']).decode('ascii')
            #     print('Waiting: ' + 'scale = ' + scale + ' proc_num = ' + proc_num + ' ppn = ' + ppn)
            #     sys.stdout.flush()
            #     time.sleep(60)
except Exception:
    print(traceback.print_exc(file=sys.stdout))
    sys.stdout.flush()

print('Main loop finished, whaitig all tasks...\n')
sys.stdout.flush()

output = subprocess.check_output(['squeue', '-u', 'zelenchukgeorgiy_1864']).decode('ascii')
while output.count('zelenchu') != 0:
    time.sleep(60)
    print('Waiting...')
    output = subprocess.check_output(['squeue', '-u', 'zelenchukgeorgiy_1864']).decode('ascii')
    sys.stdout.flush()

try:
    print('I\'m done)))\nResuls:\n\n')
    res = {}
    for task_num in sorted(task_info['task_num']):
        with open('/home/zelenchukgeorgiy_1864/_scratch/slurm-' + str(task_num[:-1]) + '.out', 'r') as f:
            lines = f.readlines()
        proc_num = lines[198].split()[-1]
        
        if proc_num not in res.keys():
            res[proc_num] = {
                'task_num': [],
                'mean_time': [],
                'harmonic_mean_TEPS': [],
            }

        res[proc_num]['task_num'].append(str(task_num[:-1]))
        # res[proc_num]['mean_time'].append(lines[205].split()[-1].replace('.', ',')) # bfs
        res[proc_num]['mean_time'].append(lines[212].split()[-1].replace('.', ','))
        # res[proc_num]['harmonic_mean_TEPS'].append(lines[219].split()[-1].replace('.', ',')) # bfs
        res[proc_num]['harmonic_mean_TEPS'].append(lines[233].split()[-1].replace('.', ','))

        # n = 1
        # scale_from_file = lines[n]
        # ef_from_file = lines[n]
        # shutil.move('/home/zelenchukgeorgiy_1864/_scratch/slurm-' + str(task[:-1]) + '.out',
        # '/home/zelenchukgeorgiy_1864/_scratch/g500_res/proc_num=' + task['proc_num'] + 'ppn=' + task['ppn'] +'/scale= ' + scale_from_file + '/ef=' + ef_from_file)

    for proc_num in sorted(res.keys()):
        print('proc_num = '+proc_num)

        print('task_num')
        for i in range(len(res[proc_num]['task_num'])):
            print(res[proc_num]['task_num'][i])

        print('mean_time')
        for i in range(len(res[proc_num]['mean_time'])):
            print(res[proc_num]['mean_time'][i])

        print('harmonic_mean_TEPS')
        for i in range(len(res[proc_num]['harmonic_mean_TEPS'])):
            print(res[proc_num]['harmonic_mean_TEPS'][i])


except Exception:
    print(traceback.print_exc(file=sys.stdout))

print('\nFinish at: ' + datetime.now().strftime("%H:%M:%S"))
sys.stdout.flush()
