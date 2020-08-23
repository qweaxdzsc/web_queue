import csv


use_mpi = False
host_name = 'DL5FWYWG2'
cpu_left = '14.6'
threads = '13'


cpu_left = float(cpu_left)
threads = float(threads)

if cpu_left > threads and threads <= 12:
    print('a')



# with open('./other/cluster_info.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         if host_name == row['computer_name']:
            # cpu_number = int(row['cpu_number'])
            # thread_per_cpu = int(row['thread_per_cpu'])
            # total_threads = cpu_number*thread_per_cpu

