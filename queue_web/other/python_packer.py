import os
import shutil


class PythonPacker(object):
    def __init__(self, project_path, project_name):
        self.project_path = project_path
        self.project_name = project_name
        self.out_path = '%s/pack' % project_path
        self.packed_path = '%s/%s' % (self.out_path, self.project_name[:-3])

    def pack_python(self, command="-D -w"):
        # command = "-F"               # create one file
        package = self.project_path + "\\" + self.project_name
        print(package)
        os.system("pyinstaller %s %s --distpath %s" % (command, package, self.out_path))

    def copy_directory(self, file_list):
        if file_list:
            for directory in file_list:
                file_path, file_name = os.path.split(directory)
                source_path = directory
                target_path = '%s/%s' % (self.packed_path, file_name)
                if os.path.exists(target_path):
                    print('directory already exist in packed file, please review it first')
                else:
                    shutil.copytree(source_path, target_path)
                    print('copy dir from %s to %s' % (source_path, target_path))

    def copy_qt5core(self):
        dll_file = 'Qt5Core.dll'
        dll_path = '%s/%s' % (self.packed_path, dll_file)
        target_path = r'%s/PyQt5\Qt\bin' % (self.packed_path)
        if os.path.exists(dll_path):
            shutil.copy(dll_path, target_path)
        else:
            print('dll file not exist')

    def simple_packer(self, file_list, command="-D -w"):
        self.pack_python(command)
        self.copy_directory(file_list)
        # self.copy_qt5core()

    def get_command(self, command="-D -w"):
        # command = "-F"               # create one file
        package = self.project_path + "\\" + self.project_name
        print("pyinstaller %s %s --distpath %s" % (command, package, self.out_path))


if __name__ == "__main__":
    python_path = r"F:\zonghui\tool"
    python_name = "PDF_TO_JPG.py"
    copy_file_list = [
        r'C:\Users\BZMBN4\Desktop\web_queue\queue_web\app_local_server\local_app',
        r'C:\Users\BZMBN4\Desktop\web_queue\queue_web\app_local_server\temp_store',
        # r'C:\Users\BZMBN4\Desktop\fluent_add_on\fluent_queue\config',
        # r'C:\Users\BZMBN4\Desktop\fluent_add_on\fluent_queue\ui_translate',
    ]
    packer = PythonPacker(python_path, python_name)
    # packer.get_command("-D")
    # packer.simple_packer(copy_file_list, "-F")
    packer.pack_python("-D -w")
