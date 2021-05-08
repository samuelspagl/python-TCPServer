# **Python TCP-Reciever**

This repository is a subrepo of 

In this repository you will find an easy to configure TCP-reciever class structure.<br>
The main parts are the the "tcpListener.py" and the actions in the "/dataActions/".

## How to use it:

Clone or just download this repo. Put the tcp folder into your project, and use the TCPListener Class.
<br>

<br>

## Functions:
TCP Listener:

```python
    def __init(self,ip_adress,port) #When creating the Object an IP-Adress and Port is needed
```

```python
   def connect(self)                #Call this function to bind the server to the given ip-adress and port, starts itself as a NON-deamon thread
```

```python
    def disconnect(self)            #call this to close the server
```

<br>

## Data Actions:

As mentioned this repo is a subrepo. In the mainrepo a certain wireprotocol is enabled in all of the subs. 
This Protocol is using a data structure as following:
```
[argLength]     [arg]       [dataLength]    [data]
 4 bytes      arg Length      4 bytes     data length
                bytes                       bytes
```

The TCP Listner searches in the class of DataTypes for an action with the ID of [arg], and executes its run function with the data as argument.

That way its pretty easy to add Data actions, bc the code is dynamicly searching for the right ID.

<br>

## How to add a Data Action:

Take a look at the "actionTemplate.py" in the "dataActions/" Folder. There you can see how the class should be structured.

```python
class action:
    id = "YOUR_ID_HERE"
    def run(data):
        print("Doing Stuff all the way down here!")
```

After you created your file and class you need to edit the *"dataTypes.py"*.

```python
from .actionTemplate import action
from .fileTransfer import FileTransfer
from .message import Message
from .YOUR_NEW_FILE import YOUR_CLASS


acs = []
acs.append(FileTransfer)
acs.append(Message)
acs.append(YOUR_NEW_CLASS)
```

After that your action is added to the dataTypes Library and you're ready to go. 



## Testing:

In this repo there is the *"server.py"* script included. Just launch it, to start the server and test your stuff out! 👍 Have fun