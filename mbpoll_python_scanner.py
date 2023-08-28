import os
import subprocess  
# https://manpages.ubuntu.com/manpages/lunar/man1/mbpoll.1.html
base_command="sudo ./modpoll -b 115200 -p none -d 8 -s 1 -m rtu -4 100 -t 3 -c 100 -r 100 -1 /dev/ttyUSB0"
interface="/dev/ttyUSB0" #"COM3" "/dev/ttyUSB0"
mode="rtu" #rtu/ascii
baudrate= 115200
parity= "none"
databits=8 #7/8
stopbits=1
waitForReply=200 #IN MILISECONDS
timeout=0.1 #100 (in SECONDS)
registers_type= 4 # 0 discrete out, 1 discrete in, 3 ir, 4 hr
registerCountInOneRequest=1
poolRate=200 #(500ms) min is 10ms
start_reg=1
highest_register=4000
foundedRegisters=[]
def prepareCommand(i):
    cmd="sudo ./modpoll "
    cmd+="-b " + str(baudrate) + " "
    cmd+="-p " + str(parity) + " "
    cmd+="-d " + str(databits) + " "
    cmd+="-s " + str(stopbits) + " "
    cmd+="-m " + str(mode) + " "
    cmd+="-4 " + str(waitForReply) + " "
    cmd+="-o " + str(timeout) + " "
    cmd+="-t " + str(registers_type) + " "
    cmd+="-c " + str(registerCountInOneRequest) + " "  
    cmd+="-l " + str(poolRate) + " "  
    cmd+="-r " + str(i) + " "
    cmd+="-1 " + " " #request only once
    cmd+= interface
    return cmd
if __name__=="__main__":
    for i in range (start_reg,highest_register):
        print("Pooling register: ",i)
        cmd=prepareCommand(i)
        #make subprocess of modpoll
        mbRequest = subprocess.run([cmd], capture_output=True, shell=True) 
        # get the output 
        output = str(mbRequest.stdout) 
        
        if "time-out!":
            print("Reply time-out!")
        else:
            print(output)
            foundedRegisters.append(i)
    print("__________________")
    print("Founded not null registers: " + str(foundedRegisters))
    print("________END__________")    
        
    #command_to_run="ls -l"
    #os.system(command_to_run)
