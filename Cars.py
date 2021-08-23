def float_func(string):
    try:
        valid2 = float(string)
        return {"error": False, "message": ""}
    except:
        return {"error": True, "message": f"{string} is not float"}
########################################################################################################################
def length_func(string, min_val=1, max_val=25):
    valid = min_val <= len(string) <= max_val
    if valid:
        return {"error": False, "message": ""}
    return {"error": True, "message": "must be between 1 and 25 characters!"}
########################################################################################################################
car = {
    "East": ["required", float_func],
    "North": ["required", float_func],
    "Name": ["required", length_func],
    "Speed": ["required", float_func],
    "IP": ["required"],
    "Port":["required"],
    "Key": ["required"]
}
########################################################################################################################
def validate(json_input):
    for key in car:
        for requirement in car[key]:
            if requirement == "required":
                if key not in json_input:
                    return {"error": True, "message": f"key {key} not found"}
            elif key in json_input:
                value = json_input[key]
                return requirement(value)
    return {"error": False, "message": ""}
