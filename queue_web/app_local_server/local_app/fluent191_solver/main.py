import subprocess
import threading
import time
import os

global order_id
global software
global use_mpi
global command
global mpi_host
global project_name
global project_address
global mission_status

ansys_root = os.environ.get('AWP_ROOT191')
app_path = r'%s\fluent\ntbin\win64\fluent' % ansys_root
print('application path:', app_path)
disk = project_address[:2]


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


if use_mpi:
    mpi_file = '%s/mpi_host.txt' % project_address
    with open(mpi_file, 'w') as f:
        for hose_name, cores in mpi_host.items():
            f.write('%s:%s\n' % (hose_name, cores))

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


