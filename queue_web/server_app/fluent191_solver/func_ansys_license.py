import subprocess
import argparse
import configparser


class LicenseAnsys(object):
    def __init__(self):
        # -------------init variable-------------------------
        self.config_file = r'..\config\config.ini'
        self.server_list = list()
        self.application = str()
        self.license_command = str()
        self.module_dict = dict()
        self.license_dict = dict()              # record total number of license and how many left
        self.license_info = str()               # record the original license info from cmd
        self.return_value = bool()
        # -------------init function-------------------------
        self.parse_config()
        self.license_info = self.get_license_info()
        self.license_usage_dict(self.module_dict)
        self.arg_parser()

    def parse_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)

        self.server_list = eval(config['License']['server_list'])
        self.application = eval(config['License']['application'])
        self.license_command = eval(config['License']['license_command'])
        self.module_dict = eval(config['License']['module_dict'])

    def get_license_info(self):
        info = ''
        for i in self.server_list:
            command = self.license_command + i
            p = subprocess.Popen('"%s" %s' % (self.application, command), shell=True, stdout=subprocess.PIPE,
                                 stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            out = p.stdout.read()
            info += out

        info = info.split("\n")

        return info

    def print_license_info(self):
        print('license info: ', self.license_info)

    def license_usage_dict(self, module_dict):
        self.license_dict = {}                                # clear self.license_dict
        for item in module_dict.keys():                       # create empty list(reservoir) to reserve license number
            self.license_dict[item] = [0, 0]
        for row in self.license_info:                         # loop self.license_info
            for k, v in module_dict.items():                  # loop module_dict
                for i in v:                                   # loop the list inside module_dict
                    self.check_usage(row, i, self.license_dict[k])
        # print('license dict:', self.license_dict)

    def check_usage(self, info, flag, reserv_list):
        """
        check if flag in info, if does, add one to total_lic
        if it is being used, add one to used_lic
        :param info:
        :param flag:
        :param reserv_list:
        :return:
        """
        if flag in info:
            try:
                total_lic = int(info.split("of")[2][1])             # TODO might have bug here
                used_lic = int(info.split("of")[3][1])
            except Exception as e:
                reserv_list[0] += 0
                reserv_list[1] += 0
            else:
                reserv_list[0] += total_lic
                reserv_list[1] += total_lic - used_lic

    def is_license(self, license_name):
        try:
            usable_license = self.license_dict[license_name][1]
            # print('license "%s" left:' % (license_name), usable_license)
        except Exception as e:
            print('error:', e)
            print('the license you type is not exist')
        else:
            if usable_license:
                return True
            else:
                return False

    def is_enough(self, required_cores):
        solver_left = self.license_dict['solver'][1]
        if not solver_left:
            # print('not enough solver')
            return False
        hpc_left = self.license_dict['hpc'][1]
        if hpc_left:
            core_left = 4 + 8 * 4 ** (hpc_left - 1)
        else:
            core_left = 4

        if required_cores > core_left:
            # print('not enough HPC')
            return False
        else:
            return True

    def arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--cores", help="show if have enough cores compare with -c XX; "
                                                  "Use Example: -c 4")
        parser.add_argument("-l", "--license", help="show if have enough license compare with -l XX; "
                                                    "Use Example: -l pre_post; here only have 4 kinds of license:"
                                                    "'spaceclaim', 'hpc', 'pre_post', 'solver'")
        args = parser.parse_args()
        if args.cores:
            cores = int(args.cores)
            self.return_value = self.is_enough(cores)
        if args.license:
            self.return_value = self.is_license(args.license)


if __name__ == '__main__':
    return_value = bool()
    ansys_license = LicenseAnsys()
    # print(ansys_license.license_info)
    print(ansys_license.return_value)