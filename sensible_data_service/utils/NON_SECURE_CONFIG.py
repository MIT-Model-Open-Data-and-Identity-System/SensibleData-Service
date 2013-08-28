TRAIL_DATABASE = { 
    "backend":"mongodb", 
    "params": { 
        "url":"mongodb://%s:%s@ds041228.mongolab.com:41248/trail_database",
        "database":"trail_database" ,
        "username":"cardoppler", 
        "password":"cardoppler",
    }
}

EVOLVING_KEY_DATABASE = { 
    "backend":"mongodb", 
    "params": { 
        "url":"mongodb://%s:%s@ds041188.mongolab.com:41188/evolving_key_database",
        "database":"evolving_key_database" ,
        "username":"cardoppler", 
        "password":"cardoppler",
	"evolving":"evolving",
    }
}

SECRET_KEY_DATABASE = { 
    "backend":"mongodb", 
    "params": { 
        "url":"mongodb://%s:%s@ds041238.mongolab.com:41238/secret_key_database",
        "database":"secret_key_database" ,
        "username":"cardoppler", 
        "password":"cardoppler",
	"secret":"secret",
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

