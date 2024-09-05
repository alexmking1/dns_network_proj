# Header
Alex King,CSCI4211S23,03/01/2023\
Python3,DNSServerV3.py,,DNSServerV3.py
# Compilation
1. install python3
* No additional libraries are required (outside of the standard python libraries)

# Execution
1. Launch the terminal
2. `cd` to the directory where the **DNSServerV3.py** file is located
3. Enter the following command in the terminal: `python3 DNSServerV3.py`
    * In the terminal you should see: `server is listening...`
4. Open a **separate** terminal. (we'll refer to as the client-terminal)
    * make sure you `cd` to the directory where the `DNSClientV3.py` file is located
5. Enter the following command in this new client-terminal: `python3 DNSClientV3.py`
6. In the client-terminal you should see: `Type in a domain name to query, or 'q' to quit:`
7. In the client-terminal, type a domain name, such as `www.google.com` and press enter
8. The client terminal will then return the results, in the form of: 

    * Received: (the domain name given):(the ip of the domain name):(how the ip was determined)

    * For example, www.github.com, may return a message similar to this: `Received: www.github.com:140.82.112.4:API`
    * This means the ip address for www.github.com is 140.82.112.4 and it used an API call to find it.
9. The client-terminal should then prompt you again for another domain name.
    * Try entering the same domain name again, and you will likely see CACHE instead of API in the return statement. This is because the server saves previous queries into a cache file so that it doesn't have to make an API call for every query. 
10. You can open up another separate client-terminal and connect to the server the same way as explained for the first client-terminal. The server will be able to handle 20 clients at once. 

* Note: make sure to use python3 and not python, which will default to python2
* Note: make sure you run the server before the client(s) code. So you should always run the **DNSServerV3.py** file before the **DNSClientV3.py** file
* Note: make sure you launch the **DNSClientV3.py** file in a **separate** terminal from the server.


# Description
This program acts as a DNS Server where clients can connect and send domain-name queries. The server then returns the ip address associated with the given domain name specified by the query. Along with returning the ip address, it will also specify which of the two methods were used to find the ip address (CACHE or API).
* The cache system: the server uses a cache system so previous queries can be returned more efficiently. Upon receiving a query, the server first searches for that domain name in the cache. The cache itself is a basic .txt file named DNS_mapping.txt that's mapping domain-names to ip addresses. It's also capable of mapping 1 domain-name to many ip addresses. The server will create its own .txt file if there isn't one already present. 

* The DNS API: If no matches were found in the cache, then the server uses an API call to its local DNS Server, passing along the given domain-name that previously could not be found in cache. Because this API call is querying an actual DNS Server, it's very likely to find the associated ip address (assuming it was given a valid domain name). Once the API call returns with the ip address, the server saves this new mapping to the cache (so it can be quickly found if requested again) and returns the details to the client. It's costly to have to call the DNS API for every query, which is why the server uses the cache system to reduce the number of API calls required. If
* Multi-Threaded: The server is multi-threaded so it can handle up to 20 clients at once. When a client connects to the server, the server will create a new thread specifically for handling that clients requests. This allows the server to continuously be listening for new client requests while also handling all current requests in progress.
* The log file: The server will output a log file named dns-server-log.csv, which will log the details and results of every query the server handled. Each query is a row with 3 columns, displaying the same details that the clients receive:

    |domain-name|ip-address|method|
    |----|-----|-------|
    |www.google.com|172.217.5.4|API|
    |www.github.com|32.23.42.34.234|CACHE|
    |www.amazon.com|32.23.42.34.234|CACHE|
* Cache implementation: Although there is a cache file, the server only reads and writes to this file periodically, because opening and closing files for every query is inefficient. Instead, at launch, the server converts any current cache data into a list data structure (specifically a list of tuples). This way, searching the cache can be done very quickly, which is important because the search must be done once for every query. After a certain amount of time has passed, the server will then write to the cache .txt file by iterating through the list data structure.

