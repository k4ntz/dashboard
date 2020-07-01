#!/usr/bin/python3
from fabric import SerialGroup
from fabric.exceptions import GroupException
from fabric.runners import Result
from termcolor import cprint
import sys


def format_proc(line):
    if len(line) < 4 or '-' * 5 in line or '=' * 5 in line or "/usr/" in line:
        return
    else:
        line_args = line.split()
        if "@QD" in line_args[4]:
            name, rtime = line_args[4].split('#')
            rdays = rtime.split("d")[0]
            if rdays == "first_epoch":
                color = "white"
            elif int(rdays) > 6:
                color = 'red'
            elif int(rdays) > 4:
                color = 'yellow'
            elif int(rdays) >= 1:
                color = 'blue'
            else: # = 0
                color = 'green'
            return [line_args[1], name[4:] + ":" + rtime, color, ['bold'], "QD"]
        else:
            return [line_args[1], line_args[4], None, ['dark'], "other"]


def retrieve_smis(server_list, out_filename=".smi_saves"):
    out_file = open(out_filename, "w", encoding="utf-8")
    server_group = SerialGroup(*server_list)
    try:
        return server_group.run('echo "new connection:" && hostname && \
                                 nvidia-smi', out_stream=out_file, hide=True)
    except GroupException as e:
        problem_list = []
        for key, val in e.result.items():
            if type(val) is not Result or val.failed:
                problem_list.append(key.original_host)
        return 'Err', problem_list



def format_smis(filename=".smi_saves"):
    smi_content = open(filename, "r", encoding="utf-8").read()
    all_processes_dict = {}
    smis = smi_content.split("new connection:")[1:]
    for smi in smis:
        smi = smi[1:]
        hostname = smi.partition('\n')[0]
        if "-------------------------------------------------" not in smi:
            all_processes_dict[hostname] = {}
            all_processes_dict[hostname]["ERR"] = ["Not able to retrieve processes"]
            continue
        processes = smi.split("="*77)[1].split("\n")[1:]
        gpu_set = False
        if "mlstudent" in hostname:
            gpu_num = hostname[9]
            hostname = "mlstudentpool"
            gpu_set = True
        if hostname not in all_processes_dict:
            all_processes_dict[hostname] = {}
        for process in processes:
            results = format_proc(process)
            if results is None:
                continue
            if not gpu_set:
                gpu_num = results.pop(0)
            else:
                results.pop(0)
            if gpu_num not in all_processes_dict[hostname]:
                all_processes_dict[hostname][gpu_num] = []
            all_processes_dict[hostname][gpu_num].append(results)
    return all_processes_dict


if __name__ == '__main__':
    server_list = ["mlstudentpool", "mlstudentpool2", "mlstudentpool3",
                   "mlstudentpool4",  "dl1", "stevens", "chichis",
                   "dgx-a", "dgx-b"]
    # server_list = ["dl1", "stevens"]
    # list = ["dl1", "chichis", "stevens", "dgx-a", "dgx-b"]
    retrieve_smis(server_list)
    if "-term" in sys.argv:
        formated_dict = format_smis()
        for hostname, gpus in formated_dict.items():
            print(hostname)
            for gpu, process_list in gpus.items():
                print(gpu, end=": ")
                for process in process_list:
                    process_name = process[0]
                    process_name += " " * (42 - len(process_name))
                    if len(process) == 4:
                        cprint(process_name, process[1], attrs=process[2], end="")
                    else:
                        print(process, end="")

                print()
