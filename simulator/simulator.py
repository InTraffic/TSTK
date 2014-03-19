import subprocess

def start_simulator(sim_type, sim_id):
    if sim_type == "soap":
        subprocess.Popen(["python2.7", "start_simulator", "restart",
                          str(sim_type), str(cc_id)]).wait()
    else:
        subprocess.Popen(["python", "start_simulator.py", "restart",
                          str(sim_type), str(cc_id)]).wait()
