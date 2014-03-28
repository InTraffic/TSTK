import subprocess

def start_simulator(sim_type, sim_id):
    """ This will start a new simulator daemon in a separate process.
    It has to run the soap daemon with python 2.7, because the used
    SOAP module is only available for python 2.7.
    
    :param sim_type: The type of simulator to start (eg. tcp, udp, etc)
    :type sim_type: string
    :param sim_id: The id to give to the simulator.
    :type sim_id: int
    
    """
    if sim_type == "soap":
        subprocess.Popen(["python2.7", "start_simulator.py", "restart",
                          str(sim_type), str(sim_id)]).wait()
    else:
        subprocess.Popen(["python", "start_simulator.py", "restart",
                          str(sim_type), str(sim_id)]).wait()

def stop_simulator(sim_type, sim_id):
    """ This will stop an existing simulator daemon.
    It has to run the soap daemon with python 2.7, because the used
    SOAP module is only available for python 2.7.
    
    :param sim_type: The type of simulator to stop (eg. tcp, udp, etc)
    :type sim_type: string
    :param sim_id: The id to give to the simulator.
    :type sim_id: int
    
    """
    if sim_type == "soap":
        subprocess.Popen(["python2.7", "start_simulator.py", "stop",
                          str(sim_type), str(sim_id)]).wait()
    else:
        subprocess.Popen(["python", "start_simulator.py", "stop",
                          str(sim_type), str(sim_id)]).wait()
