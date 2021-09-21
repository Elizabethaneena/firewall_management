#!/usr/bin/python3
import os

from rich.prompt import Prompt

CONF ={}

def fw_reload():
	print(os.popen("sudo firewall-cmd --reload").read())

def fw_get_active_zones():
	zone = os.popen("sudo firewall-cmd --get-active-zones").read()
	CONF["ZONE"] = zone.split("\n")[0]
	print(zone)

def fw_activate():
	print("Activating the firewall")
	os.popen("sudo systemctl start firewalld").read()

def fw_get_status():
	state = os.popen("sudo firewall-cmd --state").read()
	if state == "running\n":
		print("Firewall is active")
	else:
		print("Firewall is not active")
		fw_activate()
	fw_get_active_zones()


def get_zone_list():
	zone_lst = os.popen("sudo firewall-cmd --get-zones").read().split(" ")
	zone_lst[-1] = zone_lst[-1][:-1] 
	return zone_lst

def fw_add_port():
	port = Prompt.ask("Enter port number : ")
	proto = Prompt.ask("Enter protocol :", choices=["tcp","udp"],default="tcp")
	zone =  Prompt.ask("Enter zone :", choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --add-port="+port+"/"+proto+" --zone="+zone+" --permanent "
	print(os.popen(cmd).read())

def fw_get_services():
	print("___________________")
	print("Service List:")
	cmd = "sudo firewall-cmd --get-services"
	print(os.popen(cmd).read())
	print("___________________")

def fw_add_services():
	fw_get_services()
	service = Prompt.ask("Enter service name from above list : ")
	zone =  Prompt.ask("Enter zone :", choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --add-service="+service+" --zone="+zone+" --permanent" 
	print(os.popen(cmd).read())
	
def fw_add_sources():
	ip = input('Enter source ip address : ')
	cmd = f'sudo firewall-cmd --add-source ={ip}'
	print(os.popen(cmd).read)   

def fw_add_rule_menu():
	print("\t1.Add Port")
	print("\t2.Add services")
	print("\t3.Add sources")
	print("\t4.Back to Main menu")

def fw_add_rule():
	while True:

		fw_add_rule_menu()
		ch = int(input("Enter the choice : "))
		if ch == 1:
			#add port
			fw_add_port()

		elif ch == 2:
			fw_add_services()
			#add services

		elif ch == 3:
			fw_add_sources()
			#add sources

		elif ch == 4:
			break
		else:
			print("Invalid choice")

def dlt_rule_menu():
	print("\t1.Remove Port")
	print("\t2.Remove services")
	print("\t3.Remove sources")
	print("\t4.Back to Main menu") 

def dlt_port():
	port = Prompt.ask("Enter port number : ")
	proto = Prompt.ask("Enter protocol :", choices=["tcp","udp"],default="tcp")
	zone =  Prompt.ask("Enter zone :", choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --remove-port="+port+"/"+proto+" --zone="+zone+" --permanent "
	print(os.popen(cmd).read())    

def dlt_services():
	get_services()
	service = Prompt.ask("Enter service name from above list : ")
	zone =  Prompt.ask("Enter zone :", choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --remove-service="+service+" --zone="+zone+" --permanent" 
	print(os.popen(cmd).read())

def dlt_sources():
	ip = input('Enter source ip address : ')
	cmd = f'sudo firewall-cmd --remove-source ={ip}'
	print(os.popen(cmd).read)  
    
    
def delete_rules():
	while True:
		dlt_rule_menu()
		ch = int(input("Enter the choice : "))
		if ch == 1:
			dlt_port()
		elif ch == 2:
			dlt_services()
		elif ch == 3: 
			dlt_sources()
		elif ch == 4:
			break
		else:
			print("Invalid choice")

        
def main_menu():
	print("   Firewall Management    ")
	print("1. Display Status of firewall")
	print("2. Add rules")
	print("3. Delete rules")
	print("4. Reload firewall")
	print("5. Exit")



while True:
	main_menu()
	ch = int(input("Enter the choice : "))
	if ch == 1:
		#Display Status of firewall
		fw_get_status()
	elif ch == 2:
		#add rules
		fw_add_rule()
	elif ch == 3:
		#delete rules
		delete_rules()
	elif ch == 4:
		#reload rules
		fw_reload()
	elif ch == 5:
		#exit
		break;
	else:
		print("Wrong option! Type option again ")
