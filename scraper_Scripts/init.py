import os
# this is the init file for the program - needs to be run to auto gen a .env

if(os.path.exists('.env') == False):
    print("file not found, creating a new file")
    password = input(str("Choose password : "))
    presetVals = ["host=db", "sqlusername=root", ("password=" + password), "database=db"]
    env = open(".env", "w")
    for i in presetVals:
        env.write(i + "\n")
    env.close()

else:
    print("file found, ignore this file")