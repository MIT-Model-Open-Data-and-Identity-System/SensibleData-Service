DATA_DATABASE = { 
    "backend":"mongodb", 
    "params": { 
        "url":"mongodb://%s:%s@ds035498.mongolab.com:35498/sensible_data_saper", 
        "database":"sensible_data_saper" ,
        "username":"saperro", 
        "password":"saperro" 
    }
}

TRAIL_DATABASE = { 
    "backend":"mongodb", 
    "params": { 
        "url":"mongodb://%s:%s@ds041228.mongolab.com:41228/sensible_auditing",
        "database":"sensible_auditing" ,
        "username":"cardoppler", 
        "password":"cardoppler",
        "keystore":"keystore",
    }
}

SETUP = {
    "flow_id" : 0,
    "saved_data" : {
        "key_1" : "value_1",
        "key_2" : "value_2"
        },
    "checksum" : "this_is_the_first_checksum",
    "link" : "this_is_the_first_link",
}

