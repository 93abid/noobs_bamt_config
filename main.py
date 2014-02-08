import json
import os

true="true"
pools="pools"
url="url"
user="user"
passw="pass"
	
def write():#Update bamt.conf
	jsonFile = open("/etc/bamt/cgminer.conf", "w+")#change the directory here
 	jsonFile.write(json.dumps(decoded))
 	jsonFile.close()

def display_pools():#Display all worker information 
	os.system("clear")
	i=0
	lnt=len(decoded[pools])
	print "All pools\n\nTotal number of pools:",lnt,"\n"
	while i<lnt:
		print "Priority:",i+1
		print "URL:",decoded[pools][i][url]
		print "User:",decoded[pools][i][user]
		print "Password:",decoded[pools][i][passw],"\n"
		i=i+1

def display_config(): 	
	os.system("clear")
	print "CG Miner Config\n"
	print "1)Intensity:",decoded["intensity"]
	print "2)Vectors:",decoded["vectors"]
	print "3)Worksize:",decoded["worksize"]
	print "4)Kernel:",decoded["kernel"]
	print "5)Lookup-Gap:",decoded["lookup-gap"]
	print "6)Thread-Concurrency:",decoded["thread-concurrency"]
	print "7)Shaders:",decoded["shaders"]
	print "8)API-Port:",decoded["api-port"]
	print "9)GPU-Dyninterval:",decoded["gpu-dyninterval"]
	print "10)GPU-Platform:",decoded["gpu-platform"]
	print "11)GPU-Threads:",decoded["gpu-threads"]
	print "12)GPU-Engine:",decoded["gpu-engine"]
	print "13)GPU-Memclock:",decoded["gpu-memclock"]
	print "14)GPU-Powertune:",decoded["gpu-powertune"]
	print "15)Log:",decoded["log"]
	print "16)No-Pool-Disable:",decoded["no-pool-disable"]
	print "17)Queue:",decoded["queue"]
	print "18)Scan-Time:",decoded["scan-time"]
	print "19)Scrypt:",decoded["scrypt"]
	print "20)Shares:",decoded["shares"]
	print "21)Kernel-Path:",decoded["kernel-path"],"\n"

def edit_config():
	ch=raw_input("Do you want to edit the config?(y/n):")
	if ch=="y" or ch=="Y":
		ch1=raw_input("\n\nEnter Choice: ")
		inp=decoded_config[0][ch1]
		if int(ch1)>21 or int(ch1)<1:
			print "invalid option!!!"
		else:
			print "\n"+inp
			print "Current value:",decoded[inp],"\nif you dont want to change the value just type q"
			new=raw_input("Enter the new value:")
			if new!="q":				
				decoded[inp]=new
				write()
				
				
	elif ch=="n" or ch=="N":
		print "ok not changing"
	else:
		print "Invalid option!!"
	
def edit_pools():
	ch=raw_input("Do you want to edit the pool list?(y/n):")
	if ch=="y" or ch=="Y":
		ch1=input("\n1)Do you want to add a new pool\n2)Do you want to edit an existing pool\n\nEnter Choice: ")
		if ch1==1:
			#add new pool
			lent=len(decoded["pools"])
			print "Number of workers: ",lent
			pri=input("Enter the priority:")
			url=raw_input("Enter The URL of the pool(eg:stratum+tcp://coinotron.com:3334):")
			worker=raw_input("Enter the worker name (eg:UserName.WorkerName):")
			passw=raw_input("Enter the password: ")
			decoded["pools"].append({"url":url, "user":worker, "pass":passw})
			i=lent
			while i>=pri:
				decoded["pools"][i]=decoded["pools"][i-1]
				i=i-1
			decoded["pools"][i]=({"url":url, "user":worker, "pass":passw})
			write()
		elif ch1==2:
			ch=input("Enter the priority of the worker that you want to edit: ")
			print "\nPriority:",ch
			ch=ch-1
			print "\nURL:"+decoded["pools"][ch]["url"]+"\nWorker:"+decoded["pools"][ch]["user"]+"\nPassword:"+decoded["pools"][ch]["pass"]+"\n\n1)Edit this worker\n2)Delete this worker\n3)Change priority\n\nEnter your choice: "
			c=input()
			if c==1:
				print "Current url:",decoded["pools"][ch]["url"]
				q=raw_input("Would you like to change the url?(y/n):")
				if q=="y" or q=="Y":
					
					url=raw_input("Enter the new url:")
					#add new url
					decoded["pools"][ch]["url"]=url
				elif q=="n" or q=="N":
					print "okay not changing"
				else:
					print "Invalid option!!"
				print "Current Worker name: ",decoded["pools"][ch]["user"]
				q=raw_input("Would you like to change the worker name?(y/n):")
				if q=="y" or q=="Y":
					
					worker=raw_input("Enter the new worker name:")
					#add new worker name
					decoded["pools"][ch]["user"]=worker
				elif q=="n" or q=="N":
					print "okay not changing"
				else:
					print "Invalid option!!"
				print "Current password: ",decoded["pools"][ch]["pass"]
				q=raw_input("Would you like to change the password?(y/n):")
				if q=="y" or q=="Y":
					
					passwd=raw_input("Enter the new Password:")
					#add new password
					decoded["pools"][ch]["pass"]=passwd
				elif q=="n" or q=="N":
					print "okay not changing"
				else:
					print "Invalid option!!"
			
			elif c==2:
				inp=raw_input("Are you sure that you want to delete this element?(y/n): ")
				if inp=="y"or inp=="Y":		
					del decoded["pools"][ch]
					write()
				elif inp=="n" or inp=="N":
					print "ok not deleting"
				else:
					print "Invalid input!!!"
			elif c==3:
				pri=input("Enter the priority to be swapped with:")
				pri=pri-1
				temp=decoded["pools"][ch]
				decoded["pools"][ch]=decoded["pools"][pri]
				decoded["pools"][pri]=temp
				write()
			#edit existing pool
	elif ch=="n" or ch=="N":
		print "continue"
	else:
		print "Invalid option!!"


def create_pools():
	with open("/etc/bamt/cgminer.conf") as data_file:
		pool=json.load(data_file)
	p=pool["pools"]
	lent=len(p)
	i=0
	o=open("/etc/bamt/pools","w")
	u="http://"
	while i<lent:
		user=p[i]["user"]
		passwd=p[i]["pass"]
		url=p[i]["url"]
		i=i+1
		out=u+user+":"+passwd+"@"+url+"\n"
		o.write(out)

def create_backup():
	os.system("cp /etc/bamt/cgminer.conf /etc/bamt/cgminer_backup.conf")
	os.system("cp /etc/bamt/pools /etc/bamt/pools_backup")

def restore_backup():
	os.system("rm /etc/bamt/pools")
	os.system("rm /etc/bamt/cgminer.conf")
	os.system("mv /etc/bamt/cgminer_backup.conf /etc/bamt/cgminer.conf")
	os.system("mv /etc/bamt/pools_backup /etc/bamt/pools")

with open("/etc/bamt/cgminer.conf") as data_file:
	decoded=json.load(data_file)

config=[{1:"intensity",2:"vectors",3:"worksize",4:"kernel",5:"lookup-gap",6:"thread-concurrency",7:"shaders",8:"api-port",9:"gpu-dyninterval",10:"gpu-platform",11:"gpu-threads",12:"gpu-engine",13:"gpu-memclock",14:"gpu-powertune",15:"log",16:"no-pool-disable",17:"queue",18:"scan-time",19:"scrypt",20:"shares",21:"kernel-path"}]


config_string=json.dumps(config)


decoded_config=json.loads(config_string)

#main
os.system("whoami>t")
o=open("t","rw+")
a=o.read()
if a=="root\n":
	go=True
else:
	print "\nYou must be logged in as root to run this program\n"
	go=False
o.close()
os.system("rm t")
os.system("/etc/init.d/mine stop")
while go:
	
	
	print "\n\n\tNOOBS BAMT CONFIGURATION\n\n1)View all pools\n2)View cgminer config\n3)Create backup of existing configuration\n4)Restore backup\n5)Check for update's\n6)EXIT\n\nEnter your choice: "
	ch=input()
	if ch==1:
		display_pools()
		edit_pools()
		display_pools()
		
	elif ch==2:
		display_config()
		edit_config()
		display_config()
	elif ch==3:
		create_backup()
		print "\nBackup created in /etc/bamt"
	elif ch==4:
		restore_backup()
		print "backup restored"	
	elif ch==5:
		print "option coming soon.."
		continue#TODO check for updates
	elif ch==6:
		os.system("clear")
		print "Exiting..."
		os.system("/etc/init.d/mine start")
		break
	create_pools()

