from ATKCommandWrapper import *
import math

space = " "
TwoDays = 172800  

def create_satellite_dict():
    return {
        'initial_coe': [],
        'impulse_t_list': [],
        'impulse_list': []
    }

def set_value(sat: dict, coe: list, t_list: list, dv_list: list):
    if sat['initial_coe']:
        print("Initial orbit elements exist, refuse to set new value.")
    elif sat['impulse_t_list']:
        print("Impulse moments list exists, refuse to set new value.")
    elif sat['impulse_list']:
        print("Impulse list exists, refuse to set new value.")
    else:
        sat['initial_coe'].extend(coe)
        sat['impulse_t_list'].extend(t_list)
        sat['impulse_list'].extend(dv_list)

def read_data(filename: str):
    satellites = []
    sum_val = 0.0

    with open(filename, 'r') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        parts = line.split()
        if len(parts) < 6:
            i += 1
            continue
        initial_coe = list(map(float, parts[:6]))
        i += 1

        impulse_t_list = []
        impulse_list = []
     
        while i < len(lines):
            imp_line = lines[i].strip()
            if not imp_line:
                i += 1
                continue

            parts_imp = imp_line.split()
            data = list(map(float, parts_imp))
          
            if len(data) == 4:
                impulse_t_list.append(data[0])
                impulse_list.append([data[1], data[2], data[3]])
                mag = math.sqrt(data[1]**2 + data[2]**2 + data[3]**2)
                sum_val += mag
                i += 1
           
            elif len(data) == 6:
                break
            else:
                i += 1
                continue

        sat = create_satellite_dict()
        set_value(sat, initial_coe, impulse_t_list, impulse_list)
        satellites.append(sat)

    print("Total impulse:", sum_val)
    return satellites



def write_single_sat(conID: int, sat: dict, sat_id: int):
    id_str = str(sat_id)
    impulse_t_list = sat['impulse_t_list']
    impulse_list = sat['impulse_list']
    initial_coe = sat['initial_coe']

    sat_path = create_sateliite(conID, id_str)
    sensor_path = create_sensor(conID, sat_path, id_str)
    print(id_str, sat_path)

    add_initialstate(conID, initial_coe, sat_path)

    if impulse_t_list:
        duration_time = impulse_t_list[0]
        add_propagator(conID, duration_time, sat_path, "")

        for i in range(len(impulse_t_list)):
            if i != 0:
                manuv_id = str(i)
            else:
                manuv_id = ""
            add_impulse(conID, impulse_list[i], sat_path, manuv_id)

            if i != len(impulse_t_list) - 1:
                prop_id = str(i + 1)
                duration_time = impulse_t_list[i + 1] - impulse_t_list[i]
                add_propagator(conID, duration_time, sat_path, prop_id)
            else:
                prop_id = str(i + 1)
                duration_time = TwoDays - impulse_t_list[i]
                add_propagator(conID, duration_time, sat_path, prop_id)
    else:
        add_propagator(conID, TwoDays, sat_path, "")

    run_astrogator(conID, sat_path)

    

def write_atk(satellites):
    conID = connect_to_atk()
    for idx, sat in enumerate(satellites, start=1):
        write_single_sat(conID, sat, idx)
    disconnect_from_atk(conID)

if __name__ == "__main__":
    data_file = "input.txt"
    satellites = read_data(data_file)
    write_atk(satellites)
