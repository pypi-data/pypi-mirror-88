# Syst3m
Author(s):  Daan van den Bergh.<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved.<br>
Supported Operating Systems: ubuntu.
<br>
<br>
<p align="center">
  <img src="https://github.com/vandenberghinc/storage/blob/master/images/logo.png?raw=true" alt="Bergh-Encryption" width="50"/>
</p>

## Installation
	pip3 install syst3m --upgrade && python3 -c "import syst3m" --create-alias


## CLI:
The syst3m cli tool.

	Usage: syst3m <mode> <options> 
	Modes:
	    --user myuser : Configure a system user (linux).
	        --check : Check the existance of the specified group.
	        --create : Create the specified group.
	        --delete : Delete the specified group.
	        --password MyPassword : Set the password of the specifed user (leave password blank for safe prompt).
	        --add-groups group1,group2 : Add the specified user to groups.
	        --delete-groups group1,group2 : Remove the specified user from groups.
	    --group mygroup : Configure a system group (linux).
	        --list-users : List the users of the specified group.
	        --add-users user1,user2 : Add users from the specified group.
	        --delete-users user1,user2 : Delete users from the specified group.
	        --force-users user1,user2 : Add the specified users to the group and remove all others.
	    -h / --help : Show the documentation.
	Options:
	    -c : Do not clear the logs.
	Author: Daan van den Bergh. 
	Copyright: © Daan van den Bergh 2020. All rights reserved.



## Python Examples.

### The Defaults() object class.
Create a config.py file for your project with the following content:

```python

# universal variables.
ALIAS = "poker-analyser"
VERSION = "v2"
SOURCE_PATH = syst3m.defaults.get_source_path(__file__, back=4)
OS = syst3m.defaults.check_operating_system(supported=["osx", "linux"])
syst3m.defaults.check_alias(alias=ALIAS, executable=f"{SOURCE_PATH}/{VERSION}")

```

### The Env() object class.
The syst3m.env object class. 
```python

# import the package.
import syst3m

# retrieving a string environment variable.
str = syst3m.env.get_string("AUTHOR")

# retrieving a boolean environment variable.
bool = syst3m.env.get_boolean("PRODUCTION", default=False)

# retrieving a integer environment variable.
int = syst3m.env.get_integer("ID")

# retrieving a array environment variable.
list = syst3m.env.get_array("ITEMS", default=[])

# retrieving a tuple environment variable.
tuple = syst3m.env.get_tuple("TUPLE")

# retrieving a dictionary environment variable.
dict = syst3m.env.get_dictionary("DICTIONARY")

```

### The User() object class.
The User() object class. 
```python

# import the package.
import syst3m

# initialize a user object.
user = syst3m.User("testuser")

# check if the user exists.
response = user.check()
if response["success"]: print("User existance:",response["exists"])

# create a user.
response = user.create()

# delete a user.
response = user.delete()

# set a users password.
response = user.set_password(password="Doeman12!")

# add the user to groups.
response = user.add_groups(groups=[])

# delete the user from groups.
response = user.add_groups(groups=[])

```

### The Group() object class.
The Group() object class. 
```python

# import the package.
import syst3m

# initialize a group object.
group = syst3m.Group("testgroup")

# check if the group exists.
response = group.check()
if response["success"]: print("Group existance:",response["exists"])

# create a group.
response = group.create()

# delete a group.
response = group.delete()

# list the current users.
response = group.list_users()
if response["success"]: print(f"Users of group {group.name}:",response["users"])

# add users to the group.
response = group.add_users(users=["testuser"])

# delete users from the group.
response = group.delete_users(users=["testuser"])

# check if the specified users are enabled and remove all other users.
response = group.check_users(users=["testuser"])


```

### Response Object.
When a function completed successfully, the "success" variable will be "True". When an error has occured the "error" variable will not be "None". The function returnables will also be included in the response.

	{
		"success":False,
		"message":None,
		"error":None,
		"...":"...",
	}