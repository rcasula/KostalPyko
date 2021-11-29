BASE_INDICES = {
    "current_power": 0,
    "total_energy": 1,
    "daily_energy": 2,
    "string1_voltage": 3,
    "l1_voltage": 4,
    "string1_current": 5,
    "l1_power": 6,
}

SINGLE_STRING_INDICES = {
    **BASE_INDICES,
    "status": 7
}

DOUBLE_STRING_INDICES = {
    **BASE_INDICES,
    "string2_voltage": 7,
    "l2_voltage": 8,
    "string2_current": 9,
    "l2_power": 10,
    "status": 11 
}

TRIPLE_STRING_INDICES = {
    **BASE_INDICES,
    "string2_voltage": 7,
    "l2_voltage": 8,
    "string2_current": 9,
    "l2_power": 10,
    "string3_voltage": 11,
    "l3_voltage": 12,
    "string3_current": 13,
    "l3_power": 14,
    "status": 15 
}