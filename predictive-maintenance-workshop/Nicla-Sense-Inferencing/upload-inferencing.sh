fqbn="arduino:mbed_nicla:nicla_sense"
#default_library_folder="$HOME/Documents/Arduino/libraries"
#library_path="../Predictive_Maintenance_-_Vibration_inferencing"
#--library $default_library_folder --libraries $library_path
echo "Compiling for $fqbn"
arduino-cli compile  --clean --fqbn $fqbn

if [ $? -ne 0 ]; then
    exit -1
fi

port_name=$(arduino-cli board list | grep Nicla  -m 1 | awk -F' ' '{print $1}')
if [ -z "$port_name" ]; then
    echo "No board found"
    exit -1
fi

echo "Found board on $port_name"
echo "Uploading to $port_name"
arduino-cli upload -p $port_name --fqbn $fqbn
