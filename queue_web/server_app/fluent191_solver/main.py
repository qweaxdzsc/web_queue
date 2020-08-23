"""
This script will be exec() by server
This script is the example of writing main app in server end
1. claim global variable
2. make default local variable, recommend claim all below variable in this section
3. process to get variable you want, it will be collected by server

Parameter in server
all key, value in below dict will be transmitted to this script
main_task = {
    "software": self.main_app,
    'project_name': self.project_name,
    "project_address": project_address,
    'extension': extension,
    'host_name': self.host_name,
    'iterations': 1000,
    "order_id": 105,
    'threads': threads,
    "use_mpi": use_mpi,
    "mpi_host": mpi_host,
}
"""
# claim global variable which come from exec(,dict)
global extension
global host_name
global project_address
global project_name
global threads
global use_mpi

# self defined default variable
make_journal = True
journal_path = ''
iterations = 1000
mpi_setting = ''
command = ''
# command = r"3d -t4 -i G:/test/queue_test2/Test_V1_solve.jou -mpi=ibmmpi -cnf=mpi_host.txt",

# process on getting useful parameter
# get make journal
if extension == '.jou':
    make_journal = False

# get mpi_setting
if use_mpi:
    mpi_setting = '-mpi=ibmmpi -cnf=mpi_host.txt'

# get journal_path
journal_path = '%s/%s.jou' % (project_address, project_name)

# get command
command = r'3d -t{cores} -i {journal_path} {mpi_setting}'\
    .format(cores=threads, journal_path=journal_path, mpi_setting=mpi_setting)


