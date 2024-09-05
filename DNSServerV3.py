# Spring 2023 CSci4211: Introduction to Computer Networks
# This program serves as the server of DNS query.
# Written in Python v3.

import sys, threading, os, random, socket, time
from csv import writer

DNS_FILE = "DNS_mapping.txt"
CSV_FILE = "dns-server-log.csv"
cacheDataStruct = []

def main():
	# make DNS FILE (if does not exist already)
	fileName = DNS_FILE
	if not os.path.exists(fileName):
		with open(fileName, 'w'):
			pass

	# make .csv file (if does not exist already)
	csvFileName = CSV_FILE
	if not os.path.exists(csvFileName):
		with open(csvFileName, 'w'):
			pass


	# Read DNS FILE, Populating the list data structure with the DNS_FILE contents
	with open(fileName, 'r') as f:
		# for each line, grab the string, split at ',' and append(left,right) the two halfs to dataStruct
		for line in f: # we're expecting each line of this cache-file to look like: "www.abc.com:999.99.0.99"
			xhostname, xip = line.strip().split(",") # string ops splitting into <hostname> and <ip> format (separate)
			cacheDataStruct.append((xhostname,xip))
	

	# NOW CACHE .txt DATA IS FULLY CONVERTED INTO DATA STRUCT cacheDataStruct

       



	host = "localhost" # Hostname. It can be changed to anything you desire.
	port = 9889 # Port number.

	#create a socket object, SOCK_STREAM for TCP
	tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#bind socket to the current address on port
	tcp_socket.bind(('', port))
	#Listen on the given socket maximum number of connections queued is 20
	tcp_socket.listen(20)

	monitor = threading.Thread(target=monitorQuit, args=[]) 
	monitor.start()

	save = threading.Thread(target=saveFile, args=[])
	save.start()

	print("Server is listening...")

	while 1:
		#blocked until a remote machine connects to the local port
		connectionSock, addr = tcp_socket.accept()
		server = threading.Thread(target=dnsQuery, args=[connectionSock, addr[0]]) # create thread for this specific client request
		server.start()

		

def dnsQuery(connectionSock, srcAddress):
	# READING SOCKET TO GET CLIENTS INPUT...
	buff = connectionSock.recv(50).decode()

	# CHECK IF 'q' INPUT...
	clientInput = str(buff)
	if clientInput == "":
		connectionSock.close() # (client entered 'q' --> CLOSE and EXIT)
		return

	# SETTING 3 PRIMARY VARIABLES NEEDED TO RETURN
	hostname = str(buff)
	ip = ""
	method = ""

	# CHECKING IF HOSTNAME ALREADY IN CACHE...
	ipList = [] #holds list of all matching ip's to targ hostname
	targ = hostname
	# searching data struct for target hosttname...
	for host, ip in cacheDataStruct:
		if host == targ:
			ipList.append(ip) # data found in cache, so add to ipList

	# checking if any matches were found in search...
	if ipList:
		# CASE 1: MATCH(s) FOUND IN CACHE... (no need to call API OR add cache entry)
		ip = dnsSelection(ipList) # at least 1 match found, so call dnsSelection and return the ans
		method = "CACHE" # now that we have vals for both 'ip' and 'method', we have enough for the response
		
	else:
		# CASE 2: NO MATCH IN CACHE [so must call API]
		# a) query the local machine DNS lookup to get the IP resolution
		try:
			dnsReturn = socket.gethostbyname(hostname) # OPTION 1
			# ASSUMING DNS API only returns 1 ip here...
			ip = dnsReturn
			method = "API"
			cacheDataStruct.append((hostname,ip))

		except socket.gaierror as e:
			#this means NO 'DNS' MATCHES FOUND
			ip = "Host-not-found"
			method = "API"
			cacheDataStruct.append((hostname,ip))

	# now all logic related to determining which case is completed
	
	# format response string for client...
	strIp1 = str(ip)
	strHostname = str(hostname)
	responseToClient = strHostname + ":" + strIp1 + ":" + method

	# (ALL) print response to the terminal
	print(responseToClient)

	# (ALL) sending the response back to the client
	connectionSock.send(responseToClient.encode()) 

	# (ALL) closing the server socket.
	connectionSock.close()

	# (ALL) update CSV_FILE file
	csvRow = [hostname, ip, method] # csvRow is a list that we want to add as a new row:

	#ipList.clear() # RESETTING ipList() (likely only needed for optional part of project)
	
	# Open our existing CSV file in append mode, Create a file obj for this file
	with open(CSV_FILE, 'a') as f_obj:
	
		# Pass this file obj to csv.writer() and get a writer obj
		writer_obj = writer(f_obj)
	
		# Pass the list as an arg to the writerow()
		writer_obj.writerow(csvRow)
	
		# Close the file object
		f_obj.close()


# SELECTS WHICH MATCHING IP TO RETURN TO CLIENT (relevant when mult matching ips)
def dnsSelection(ipList):
	#checking the number of IP addresses in the cache
	#if there is only one IP address, return the IP address
	#if there are multiple IP addresses, select one and return.
	if len(ipList) == 1: # checking num ip addresses in cache
		return ipList[0]
	else:
		return random.choice(ipList)


def saveFile():
	while(1):
		#check updates from data struct and save your "DNS_mapping.txt" here
		updateCacheFile(DNS_FILE) # iterates through our cache data struct and writes each entry to DNF_FILE
		time.sleep(15)


def monitorQuit():
	while 1:
		sentence = input()
		if sentence == "exit":
			os.kill(os.getpid(),9)


# MY METHOD: funct to call at end that converts our cacheDataStruct and writes to a given txt file (aka DNS_mapping.txt)
def updateCacheFile(nameOfTxtFile):
	with open(nameOfTxtFile, 'w') as f:
		f.seek(0)
		for host, ip in cacheDataStruct:
			strIp = str(ip)
			strRet = host + "," + strIp #combining tuple into 1 string w proper "host,ip" format
			# write each entry on a new line
			f.write("%s\n" % strRet)
			f.truncate()
		print('Updated cache file')


main()
