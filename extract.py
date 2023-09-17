import os
import re


def extract_hpl():
    files = os.listdir('./_scratch')

    res = []

    for file in sorted(files):
        if 'slurm' in file:
            try:
                with open('./_scratch/' + file, 'r') as f:
                    lines = f.readlines()
                words = lines[46].split()
                res.append(words[5].replace('.', ','))
                print(str(re.findall(r'\d+', file)[0]))
            except IndexError:
                res.append('NULL')
                print(str(re.findall(r'\d+', file)[0]))
    for i, r in enumerate(res):
        print(r)


def extract_g500():
    lines_to_read = {
        'bfs': [205, 219],
        'sssp': [212, 233]
    }
    files = os.listdir('/home/zelenchukgeorgiy_1864/_scratch')
    res = {}
    # print(sorted(files))
    ban_list = ['slurm-1584991.out']
    for file in sorted(files):
        if 'slurm' in file and file not in ban_list:
            # print(file)
            with open('./_scratch/'+file, 'r') as f:
                lines = f.readlines()
            try:
                proc_num = lines[198].split()[-1]
            except IndexError:
                continue

            if proc_num not in res.keys():
                res[proc_num] = {
                    'task_num': [],
                    'mean_time': [],
                    'harmonic_mean_TEPS': [],
                    'ef': [],
                }
            try:
                res[proc_num]['task_num'].append(str(re.findall(r'\d+', file)[0]))
                res[proc_num]['mean_time'].append(lines[lines_to_read['sssp'][0]].split()[-1].replace('.', ','))
                res[proc_num]['harmonic_mean_TEPS'].append(lines[lines_to_read['sssp'][1]].split()[-1].replace('.', ','))
                res[proc_num]['ef'].append(lines[195].split()[-1])
            except IndexError:
                res[proc_num]['mean_time'].append('NULL')
                res[proc_num]['harmonic_mean_TEPS'].append('NULL')

    for proc_num in sorted(res.keys()):
        print('proc_num = ' + proc_num)

        print('task_num')
        for i in range(len(res[proc_num]['task_num'])):
            print(res[proc_num]['task_num'][i])

        print('EF')
        for i in range(len(res[proc_num]['ef'])):
            print(res[proc_num]['ef'][i])

        print('mean_time')
        for i in range(len(res[proc_num]['mean_time'])):
            print(res[proc_num]['mean_time'][i])

        print('harmonic_mean_TEPS')
        for i in range(len(res[proc_num]['harmonic_mean_TEPS'])):
            print(res[proc_num]['harmonic_mean_TEPS'][i])


if __name__ == '__main__':
    extract_g500()

