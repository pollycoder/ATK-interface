from ATKConnectModule import atkOpen, atkClose, atkConnect


space = " "

def connect_to_atk():
    conID = atkOpen()
    return conID
    # if conID == 0:
    #     print("Failed to connect to ATK")
    #     return None
    # else:
    #     print("Connected to ATK with ID:", conID)
    #     return conID
    
def disconnect_from_atk(conID):
    if conID is not None:
        atkClose(conID)
        print("Disconnected from ATK")
    else:
        print("No connection to disconnect")

def create_sateliite(conID: int, id_str: str):
    sat_name = "Satellite" + id_str
    sat_path = "*/Satellite/" + sat_name

    add_new_satellite = "/" + space + "Satellite" + space + sat_name
   
    atkConnect(conID, "New", add_new_satellite)
    
    return sat_path

def create_sensor(conID: int, sat_path: str, id_str: str):
    sensor_name = "Sensor" + id_str
    sensor_path = sat_path + "/Sensor/" + sensor_name

    add_new_sensor = "/" + space + sat_path + "/Sensor" + space + sensor_name
    atkConnect(conID, "New", add_new_sensor)
    atkConnect(conID, "Define", sensor_path + space + "Rectangular 20 20")
    return sensor_path

def set_sensor_parameter(conID: int, sensor_path: str):
    projection_command = sensor_path + space + "Projection" + space + " Altitudes 500000 "
    point_command = sensor_path + space + "Fixed" + space + "Quaternion 0 1 0 0"

    atkConnect(conID, "Graphics", projection_command)
    atkConnect(conID, "Point", point_command)

def add_initialstate(conID: int, initial_coe: list, sat_path: str):
    set_prop_command = sat_path + space + "SetProp"
    set_initialstate_command = sat_path + space + "SetValue MainSequence.SegmentList.Initial_State.CoordinateType Keplerian"
    add_initialstate_sma_command = sat_path + space + "SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.sma " + str(initial_coe[0]) + " km"
    add_initialstate_ecc_command = sat_path + space + "SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.ecc " + str(initial_coe[1])
    add_initialstate_inc_command = sat_path + space + "SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.inc " + str(initial_coe[2]) + " rad"
    add_initialstate_RAAN_command = sat_path + space + "SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.RAAN " + str(initial_coe[3]) + " rad"
    add_initialstate_w_command = sat_path + space + "SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.w " + str(initial_coe[4]) + " rad"
    add_initialstate_ta_command = sat_path + space + "SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.ta " + str(initial_coe[5]) + " rad"

    atkConnect(conID, "Astrogator", set_prop_command)
    atkConnect(conID, "Astrogator", set_initialstate_command)
    atkConnect(conID, "Astrogator", add_initialstate_sma_command)
    atkConnect(conID, "Astrogator", add_initialstate_ecc_command)
    atkConnect(conID, "Astrogator", add_initialstate_inc_command)
    atkConnect(conID, "Astrogator", add_initialstate_RAAN_command)
    atkConnect(conID, "Astrogator", add_initialstate_w_command)
    atkConnect(conID, "Astrogator", add_initialstate_ta_command)

def add_propagator(conID: int, duration_time: float, sat_path: str, prop_id: str):
    insert_propagator = sat_path + space + "InsertSegment MainSequence.SegmentList.- Propagate"
    set_propagator = sat_path + space + "SetValue MainSequence.SegmentList.Propagate" + prop_id + ".StoppingConditions Duration"
    set_duration = sat_path + space + "SetValue MainSequence.SegmentList.Propagate" + prop_id + ".StoppingConditions.Duration.TripValue " + str(duration_time) + " sec"

    atkConnect(conID, "Astrogator", insert_propagator)
    atkConnect(conID, "Astrogator", set_propagator)
    atkConnect(conID, "Astrogator", set_duration)

def add_impulse(conID: int, impulse_cartesian: list, sat_path: str, manuv_id: str):
    dvx, dvy, dvz = impulse_cartesian

    add_impulse = sat_path + space + "InsertSegment MainSequence.SegmentList.- Maneuver"
    set_impulseAxis = sat_path + space + "SetValue MainSequence.SegmentList.Maneuver" + manuv_id + ".ImpulsiveMnvr.ThrustAxes Satellite J2000"
    set_impulseValueX = sat_path + space + "SetValue MainSequence.SegmentList.Maneuver" + manuv_id + ".ImpulsiveMnvr.Cartesian.X " + str(dvx) + " km/sec"
    set_impulseValueY = sat_path + space + "SetValue MainSequence.SegmentList.Maneuver" + manuv_id + ".ImpulsiveMnvr.Cartesian.Y " + str(dvy) + " km/sec"
    set_impulseValueZ = sat_path + space + "SetValue MainSequence.SegmentList.Maneuver" + manuv_id + ".ImpulsiveMnvr.Cartesian.Z " + str(dvz) + " km/sec"

    atkConnect(conID, "Astrogator", add_impulse)
    atkConnect(conID, "Astrogator", set_impulseAxis)
    atkConnect(conID, "Astrogator", set_impulseValueX)
    atkConnect(conID, "Astrogator", set_impulseValueY)
    atkConnect(conID, "Astrogator", set_impulseValueZ)

def run_astrogator(conID: int, sat_path: str):
    atkConnect(conID, "Astrogator", sat_path + space + "RunMCS")