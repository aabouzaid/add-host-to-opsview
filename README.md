Python script to automate adding a new host with templates via Opsview API.
=========================================

I wrote this script two years ago, and then updated it on year ago or so ... I'm not sure who is still using Opsview, but at least it's here if any one need it.

This script is simply used to add a new host to Opsview automatically. It can be used independently or as I used to use it as part of automation tool like Ansible.

How to use?
-------------------
```
python add_host_to_opsview.py --group-name GROUP_NAME --server-name SERVER_NAME --server-ip SERVER_IP  --ini-file PATH_TO_INI_FILE
```

The ini file has info that will used to connect to Opsview Server (Opsview URL, user, password, and host templates).


Requirement.
-------------------
No special requirements, just the user that used to connect to Opsview should have administration privileges.


Compatibility.
-------------------
This script is tested with latest Open Source version of Opsview!

