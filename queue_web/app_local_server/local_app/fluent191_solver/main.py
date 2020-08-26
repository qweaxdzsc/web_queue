"""
This script will be exec() by local
This script is the example of writing main app in local end
1. claim global variable
2. make default local variable, recommend claim all below variable in this section
3. define the function you need
4. process to get variable you want
5. run main logic

Parameter in server
all key, value in below dict will be transmitted to this script
main_task = {
    "software": self.main_app,
    'project_name': self.project_name,
    "project_address": project_address,
    'extension': extension,
    'host_name': self.host_name,
    "order_id": 105,
    'threads': threads,
    "use_mpi": use_mpi,
    "mpi_host": mpi_host,
}
"""
import subprocess
import threading
import time
import os

# claim global variable which come from exec(,dict)
global order_id
global software
global use_mpi
global mpi_host
global extension
global threads
global project_name
global project_address
global mission_status

# self defined default variable
journal_path = ''
mpi_setting = ''
command = ''
iterations = 1000


# define functions
class CalGuard(threading.Thread):
    """thread ensures calculation normally"""
    def __init__(self, directory, project_name):
        super().__init__()
        self.dir = directory
        transcript_name = '%s_transcript.txt' % project_name
        self.transcript = '%s\\%s' % (directory, transcript_name)
        print('transcript path:', self.transcript)
        self.wait_time = 50
        self.check_interval = 150

    def run(self):
        print('start Guard')
        time.sleep(self.wait_time)
        if os.path.exists(self.transcript):
            print('have transcript')
            self.check_transcript(self.check_interval)
            self.ensure_finish(self.dir)
        else:
            print('Warning: Error, transcript dose not exist')

    def check_transcript(self, check_interval):
        line_count = 0
        line_count_new = self.get_line_count()

        while line_count_new > line_count:
            time.sleep(check_interval)
            line_count = line_count_new
            line_count_new = self.get_line_count()

    def get_line_count(self):
        with open(self.transcript, 'r') as f:
            content = f.readlines()
            line_count_new = len(content)
            print('transcript line Count:', line_count_new)

        return line_count_new

    def ensure_finish(self, dir):
        file_list = os.listdir(dir)
        bat_file_name = ''
        with open(self.transcript, 'r') as f:
            content = f.readlines()
            for line in content:
                if 'host' in line:
                    line = line.split()
                    host_name = line[1]
                    pid = line[3]
                    bat_file_name = 'cleanup-fluent-%s-%s.bat' % (host_name, pid)
        for i in file_list:
            if i == bat_file_name:
                print('.bat address', os.path.join(dir, i))
                subprocess.call(os.path.join(dir, i), shell=True)
                mission_status = 'abnormal'
        print('\nall finished')
        # self.quit()


def make_journal(project_address, project_name, extension, jou_file, iterations):
    case_path = r'%s/%s%s' % (project_address, project_name, extension)
    transcript = '%s\\%s_transcript.txt' % (project_address, project_name)
    time_out_min = 1
    content = """
/file/start-transcript {transcript} ok
/file/set-idle-timeout yes {time_out} no
/file/read-case {case_path} yes
/solve/initialize/hyb-initialization yes
/solve/iterate/{iteration} yes
/file/write-case-data/ {case_path} yes
/exit yes
    """.format(iteration=iterations, case_path=case_path, transcript=transcript,
               time_out=time_out_min)
    with open(jou_file, 'w') as jou:
        jou.write(content)


# process on getting other parameter
# get mpi_setting
if use_mpi:
    mpi_setting = '-mpi=ibmmpi -cnf=mpi_host.txt'
    mpi_file = '%s/mpi_host.txt' % project_address
    with open(mpi_file, 'w') as f:
        for hose_name, cores in mpi_host.items():
            f.write('%s:%s\n' % (hose_name, cores))

# get journal_path
journal_path = '%s/%s.jou' % (project_address, project_name)

# get command
command = r'3d -t{cores} -i {journal_path} {mpi_setting}'\
    .format(cores=threads, journal_path=journal_path, mpi_setting=mpi_setting)

# get application address
ansys_root = os.environ.get('AWP_ROOT191')
app_path = r'%s\fluent\ntbin\win64\fluent' % ansys_root
print('application path:', app_path)
disk = project_address[:2]

# get make journal
if extension is not '.jou':
    make_journal(project_address, project_name, extension, journal_path, iterations)

# main start
p = subprocess.Popen(r'%s &&'
                     r'cd %s &&'
                     r'"%s" %s' %
                     (disk, project_address, app_path, command),
                     shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                     stderr=subprocess.PIPE, universal_newlines=True)

calguard = CalGuard(project_address, project_name)
calguard.start()
out, err = p.communicate()  # block calculation thread until finished
if mission_status != 'abnormal':
    mission_status = 'finished'
# calguard.quit()


