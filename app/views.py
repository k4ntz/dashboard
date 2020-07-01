from flask import render_template, jsonify, request
from app import app
from getp import format_smis, retrieve_smis
import time

last_time_retrieved = None

def get_colors_and_users(smis_dict):
    users = []
    colors = []
    for host in smis_dict.values():
        for gpu_processes in host.values():
            for process in gpu_processes:
                if process[3] not in users:
                    users.append(process[3])
                if process[1] is None:
                    process[1] = "black"
                if process[1] not in colors:
                    colors.append(process[1])
    return colors, users


@app.route('/')
def index():
    formated_dict = format_smis()
    colors, users = get_colors_and_users(formated_dict)
    res = render_template('template.html', formated_dict=formated_dict,
                          color_list=colors, users=users)
    return res


@app.route('/retrieve_smis/', methods=['POST'])
def square():
    global last_time_retrieved
    if last_time_retrieved is not None:
        if time.time() - last_time_retrieved < 10 * 60:
            return jsonify({'msg': "Processes retrieved less than 10 mins ago, please wait.",
                            "color": "orange"})
    list = ["mlstudentpool", "mlstudentpool2", "mlstudentpool3",
            "mlstudentpool4",  "dl1", "chichis", "stevens",
            "dgx-a", "dgx-b"]
    last_time_retrieved = time.time()
    print("last time retrieved: ", last_time_retrieved)
    results = retrieve_smis(list)
    if results[0] != "Err":
        return jsonify({'msg': "Processes retrieved, please refresh !",
                        "color": "green"})
    else:
        msg = "Something went wrong with "
        for bad_res in results[1]:
            msg += bad_res + " "
        return jsonify({'msg': msg, "color": "red"})
