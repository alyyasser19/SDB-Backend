def float_func(string):
    try:
        valid2 = float(string)
        return {"error": False, "message": ""}
    except:
        return {"error": True, "message": f"{string} is not float"}
########################################################################################################################
def bool_func(string):
    if string == "False" or string == "True":
        return {"error": False, "message": ""}
    return {"error": True, "message": f"{string} is not boolean"}
########################################################################################################################
def length_func(string, min_val=1, max_val=25):
    valid = min_val <= len(string) <= max_val
    if valid:
        return {"error": False, "message": ""}
    return {"error": True, "message": "must be between 1 and 25 characters!"}
########################################################################################################################
bike = {
    "East": ["required", float_func],
    "North": ["required", float_func],
    "Speed": ["required", float_func],
    "Name": ["required", length_func],
    "Locked": ["required", bool_func],
    "Shared": ["required", bool_func],
    "IP": ["required"],
    "Port": ["required"],
    "Execute":["required", bool_func],
    "Command": ["required"],                                   
    "Current_Network_Name": ["required"],
    "Current_Network_Password": ["required"]
}
########################################################################################################################
def validate(json_input):
    for key in bike:
        for requirement in bike[key]:
            if requirement == "required":
                if key not in json_input:
                    return {"error": True, "message": f"key {key} not found"}
            elif key in json_input:
                value = json_input[key]
                valid = requirement(value)
                if valid['error']:
                    return valid
    return {"error": False, "message": ""}
