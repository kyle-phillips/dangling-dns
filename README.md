# dangling-dns
A project to discover dangling DNS records  

This script is useful in researching dangling DNS.  

Step 1: Enumerate a domain to find all subdomains (Suggested tool: amass)  
Step 2: Store all discovered domains in a text file, one domain per line.  
Step 3: Use dom-enum.py script to return A Record IP address, ASN, HTTP and HTTPS responses, and if an MX record exists
```USAGE: python dom-enum.py filename.txt  ```  
```USAGE: python dom-enum.py filename.txt > results.txt ``` (pipe it to a text file)  
