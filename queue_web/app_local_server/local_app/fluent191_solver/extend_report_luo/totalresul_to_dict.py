# coding=utf-8
import os


def get_data(path):
    # os.chdir(path)
    # if not os.path.exists("totalresult.txt"):
    #     return None
    key_word = ["Total Pressure",
                "Static Pressure",
                "AverageVelocity Magnitude",
                "AverageStatic Temperature",
                "Area-Wt.Static Temperature",
                "Area-Wt.Velocity",
                "Volumetric",
                "Moment Axis"]
    title = []
    star_index = []
    end_index = []
    moment_index = []
    dic_info = {}
    with open("totalresult.txt", "r") as f:
        info = f.readlines()
        for index, line in enumerate(info):  # 提取索引
            # print(index, line, end="")
            if "--------------------------------" in line.split():
                star_index.append(index)
                title.append(info[index - 2].strip() + info[index-1].strip())
                # print(index, line.split())
                # print("title\t", info[index - 2].strip() + info[index-1].strip())  # TODO
            elif "----------------" in line.split():
                end_index.append(index)
                # print(index, line.split())
            elif "-------------------------" in line.split():
                moment_index.append(index)
        # print(title)
        for key in key_word:
            if (key == "Moment Axis") and moment_index:
                dic_info["Torque"] = info[moment_index[1] + 1].split()[3]
                # print(info[moment_index[1] + 1].split()[3])
            else:
                for index, k in enumerate(title):

                    if key in k:
                        # print("key\t", key)  # TODO
                        d2 = {}
                        a = star_index[index]
                        b = end_index[index]
                        for i in range(a + 1, b):
                            # print(i, info[i], end="")  # TODO
                            d2[info[i].split()[0]] = "%f" % eval(info[i].split()[1])
                            i += 1
                        if key == "AverageStatic Temperature":
                            key1 = "Temperature"
                        elif key == "AverageVelocity Magnitude":
                            key1 = "Velocity"
                        elif key == "Area-Wt.Static Temperature":
                            key1 = "Temperature Uniformity"
                        elif key == "Area-Wt.Velocity":
                            key1 = "Velocity Uniformity"
                        elif key == "Volumetric":
                            key1 = "air flow"
                        else:
                            key1 = key
                        dic_info[key1] = d2  # TODO 修改key为实际title
        # print(star_index)
        # print(end_index)
        # print(moment_index[1])
        # print(dic_info)
        return dic_info


if __name__ == '__main__':
    info = get_data(r"D:\luopengcheng\works\WM_C1\V3_vent\WM_C1_T_V3_vent_201020_result")

    for i in info:
        print(i, info[i])


