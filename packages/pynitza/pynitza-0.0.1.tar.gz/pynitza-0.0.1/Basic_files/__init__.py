import requests
import os
import logging #DEBUG  INFO  WARNING  ERROR  CRITICAL
import datetime
from datetime import datetime , timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pytz import utc , timezone
from time import mktime

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# working with this lib:
# 
# initialize projekt with its parameters [ExampleProject = Janitza.Project(ip="123.456.789.000",port="8080",project="example")]
# build devicelist [ExampleProject.BuildDeviceList()]
# assign devices to project [ExampleProject.AssignDevices()]
# now your ready to go ;)
# 
# Warning !!! -> this lib is designed to work with just one project at a time !!!
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#||||||||||||||||| basic functions |||||||||||||||||

# making folder relative to programms directory
def MakeFolder(folder=""):
    parrentdir = os.path.dirname(os.path.abspath(__file__))
    mypath =  parrentdir + folder
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
        logging.info("Folder created " + mypath)
    else:
        logging.info("Folder already existed at " + mypath)

# removing folder relative to programms directory 
def RemoveFolder(folder=""):
    parrentdir = os.path.dirname(os.path.abspath(__file__))
    mypath =  parrentdir + folder
    if not os.path.isdir(mypath):
        logging.info("No Folder " + folder + " found at " + parrentdir)
    else:
        os.rmdir(mypath)
        logging.info("Folder removed from " + parrentdir)

# checking wether input to class functions is a single device / a list / a device id (int) / or "all" and returning a list with specified devices
def CheckInput(arg=""):
    id = []
            
    if arg == "all":
        logging.debug("inputmode 'all'")
        for device in Project.devices:
            id.append(Project.devices[device]["id"])
        return(id)
            
    if isinstance(arg, int):
        logging.debug("reading device " + str(arg) + "inputmode 'Int'")
        id.append(str(arg))
        return(id)
        
    if isinstance(arg, str) and arg != "all":
        logging.debug("inputmode 'Str'")
        id.append(arg)
        return(id)

    if isinstance(arg, list):
        logging.debug("inputmode 'List'")
        for item in arg:
            id.append(str(item))
        return(id)

    if arg == "":
        logging.debug("no devices were given to this function")
        id.append("empty list")
        return(id)

# converting timestamp in UTCNANO 
def DateTimeToUTCNANO(year=0,month=0,day=0,hour=0,minute=0,second=0,thistimezone="utc"):

    dt = datetime(year=year , month=month,day=day,hour=hour ,minute=minute ,second=second ,tzinfo=timezone(thistimezone))
    timestamp = int((dt - datetime(1970,1,1, tzinfo=timezone(thistimezone))) / timedelta(seconds=1))
    timestamp = timestamp * 1000000000
    return(timestamp)

# converting UTCNANO in timestamp
def UTCNANOToDateTime(UTCNANO):
    UTCSEC = int(UTCNANO)/1000000000
    this_datetime = datetime.utcfromtimestamp(UTCSEC)
    return(str(this_datetime))


#||||||||||||||||| basic class definitions ||||||||||||||||||||

# creating device Class
class Device(object):

    # initializing device class 
    def __init__(self, id="",name="",type=""):
        self.id = id
        self.name = ""
        self.type = ""

    # fetching devices available online values ///////////////////////// Work in Progress ////////////////////////////
    def AvailableOnlineValues(self):
        self.availableOnlineValues = []
        url = "http://" + Project.connection + "/rest/1/projects/" + Project.project + "/devices/" + str(self.id) + "/online/values.json"
        response = requests.request("GET", url) # sending GET-request
        data = response.json()                  # parsing response to JSON
        return(data)
        for value in data:
            pass


# creating the project class which stores multiple device class objects 
class Project(object):

    # initializing project class with connection and project info
    def __init__(self,project="",ip="",port=""):
        self.project = str(project)               # project name 
        self.ip = str(ip)                         # project ip (or Url)
        self.port = str(port)                     # project port
        self.devices = []                         # list with all devices and general information
        Project.project = str(project)            # shared project variable to interface with device specific requests
        self.mailserver = ""
        self.mailAs = ""
        self.mailserverisok = False


        # checking if ip or Url 
        if self.port == "" or self.port == "none" or self.port == "None":
            
            Project.connection = str(self.ip)
            self.connection = str(self.ip)
            logging.info("no port specified!")
            logging.info("using ip as url")
        
        else:
            
            Project.connection = str(self.ip) + ":" + str(self.port)
            self.connection = str(self.ip) + ":" + str(self.port)
            logging.info("port specified!")
            logging.info("using ip and port")

        logging.debug("project "+ self.project + " initialized !")

    # setting up the mailserver
    def SetupMailserver(self,mailserver="empty",sendmailwiththisaddress="empty"):
        if mailserver == "empty" or sendmailwiththisaddress == "empty":
            logging.warning("mailserver= '" + mailserver + "' alias= '" + sendmailwiththisaddress + "' (none of these values is allowed to be 'empty')")
        else:
            self.mailserver = mailserver
            self.mailAs = sendmailwiththisaddress
            self.mailserverisok = True
            logging.info("setup mailserver with server : " + self.mailserver + " and mails are send from the adresse '" + self.mailAs +"'")

        return(True)

    # sending mail via mailserver
    def SendMail(self,To=[],Subject="empty",Text="empty",Type="plain",MailTo="Energie-Team",attachment_txt=""):
        atm=False
        if self.mailserverisok == True:
            if To == []:
                logging.error("no recipiants have been provided !")
            else:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = Subject
                msg['From'] = self.mailAs
                msg['To'] = MailTo

                if attachment_txt != "":
                    try:
                        atm=True
                        f=open(attachment_txt)
                        attachment = MIMEText(f.read())
                        attachment.add_header('Content-Disposition', 'attachment', filename=attachment_txt) 
                    except:
                        atm=False
                        logging.error("attachment creation failed", exc_info=True)
                else:
                    pass

                # Create the body of the message (a plain-text and an HTML version).
                body = MIMEText(Text, Type)

                # Attach parts into message container.
                # According to RFC 2046, the last part of a multipart message, in this case
                # the HTML message, is best and preferred.
                msg.attach(body)
                if atm==True:
                    msg.attach(attachment)

                # Send the message via local SMTP server.
                mail = smtplib.SMTP(self.mailserver)
                # sendmail function takes 3 arguments: sender's address, recipient's address
                # and message to send - here it is sent as one string.
                mail.sendmail(self.mailAs, To, msg.as_string())
                mail.quit()
                logging.info("mail send")
        else:
            logging.error("mailserver was not setup properly")

    # generate a simple mail table (mail must be send as 'html')
    def MailTable(self,Group,values):
        text = "<html><body>Werte der Gruppe '" + Group.name + "' :<br><table border="'1'"><tr><br><th>ID</th><th>Wert pro Schicht</th><th>Einheit</th><th>Name</th></tr>"
        for item in values:
            try:
                text = text + "<tr><td><center>" + item + "</center></td><td>" + values[item]["value"] + "</td><td><center>" + values[item]["unit"] + "</center></td><td>" + self.NameById(item) + "</td></tr>"
            except:
                logging.warning("Tabelleneintrag für Gerät " + item + " konnte nicht generiert werden", exc_info=True)
        text = text = text + "</table></body></html>"
        return(text)


    # builds a list with devices and their general info
    def BuildDeviceList(self):
        url = "http://" + self.connection + "/rest/1/projects/" + self.project + "/devices.json"
        response = requests.request("GET", url) # sending GET-request
        data = response.json() #parsing response to JSON
        #with open('DevicesResponse.json', 'r') as myfile:           # just for testing purposes
        #    data = myfile.read()                                    # just for testing purposes
        #data = json.loads(data)                                     # just for testing purposes
        
        logging.debug(data)
        # setting up the storage for the devices
        devicedict = {} # form -> {'id': {'name': '', 'id': '', 'type': '', 'description': '', 'typeDisplayName': '', 'connectionString': '', 'serialNr': '', 'image': ''}}

        for item in data["device"]:
            # template for the entrys inside the devicedict{}
            template = {"name": "no value","id": "no value","type": "no value","description": "no value","typeDisplayName": "no value","connectionString": "no value","serialNr": "no value","image": "no value"}
            # filling the template with data
            template["name"] = item["name"]
            template["id"] = item["id"]
            template["type"] = item["type"]
            template["description"] = item["description"]
            template["typeDisplayName"] = item["typeDisplayName"]
            template["connectionString"] = item["connectionString"]
            template["serialNr"] = item["serialNr"]
            # adding template to storage and assigning device id
            devicedict[item["id"]] = template

        self.devices = devicedict
        Project.devices = devicedict
        logging.info("Devicelist build !")
        return(devicedict)

    # assigning devices to project (needs a build devicelist to work)
    def AssignDevices(self):
        for thisdevice in self.devices:
            device = "device" + str(thisdevice)
            logging.debug(device) 
            device = Device(thisdevice)

    # creating a group of devices
    class Group(object):
        def __init__(self,name="",ids=[]):
            self.ids = CheckInput(ids)
            self.name = str(name)

        # append ids to a group
        def append(self,id_input):
            temp = self.ids
            temp_ids = CheckInput(id_input)
            for id in temp_ids:
                temp.append(id)
            self.ids = temp
        
        # returns a list of ids
        def ids(self):
            return(list(self.ids))

        # returns group name
        def name(self):
            return(str(self.name))

        # sets group name
        def setname(self,name=""):
            if not name == "":
                self.name = str(name)
            else:
                print("no name specified")

        # removes ids from group
        def remove(self,id_input="empty"):
            # clears all ids
            if id_input == "all":
                self.ids.clear()
                logging.info(self.name + " ids cleared")

            # checks for no input
            if id_input == "empty":
                logging.error("no ids passes into group.remove() function")

            # tries to remove id(s)
            if type(id_input)==list or type(id_input)==int or ( type(id_input)==str and id_input != "all" and id_input != "empty"):
                temp = self.ids
                rem_ids = CheckInput(id_input)
                errors = 0
                
                for id in rem_ids:
                    
                    try:
                        temp.remove(id)
                        logging.debug("removed " + str(id) + " from " + self.name)
                    except:
                        logging.error("failed to remove " + str(id) + " from " + self.name, exc_info=True)
                        errors += 1 
                
                if errors > 0:
                    logging.info(str(errors) + " errors occured while removing ids")
                if errors == 0:
                    logging.info("no errrors while removing ids")


    def NameById(self,id=0):
        this_name = self.devices[int(id)]["name"]
        return(str(this_name))
    
    def TypeById(self,id=0):
        this_type = self.devices[int(id)]["type"]
        return(str(this_type))

    def DescriptionById(self,id=0):
        this_description = self.devices[int(id)]["description"]
        return(str(this_description))

    def TypeDisplayNameById(self,id=0):
        this_typeDisplayName = self.devices[int(id)]["typeDisplayName"]
        return(str(this_typeDisplayName))

    def ConnectionStringById(self,id=0):
        this_connectionString = self.devices[int(id)]["connectionString"]
        return(str(this_connectionString))

    def SerialNrById(self,id=0):
        this_serialNr = self.devices[int(id)]["serialNr"]
        return(str(this_serialNr))


    # reading devices available online values [arguments for type -> "all" / device_id [as string or int] / device_list [as list of string and or int]] ///////////////////////////////////////////////////////////////////////////////////
    def ReadAvailableOnlineValues(self, arg=""):
        id = CheckInput(arg)   

    # getting Images from all devices 
    def GetDeviceImages(self,devices,size,save_location="//IMAGES"):
        id = CheckInput(devices)
        MakeFolder(save_location)
        parentdir = os.path.dirname(os.path.abspath(__file__))
        logging.info(parentdir + save_location + "//" + size)
        for device in id:
            
            try:
                recieve = requests.get('http://' + str(self.connection) + '/rest/1/projects/' + str(self.project) + '/deviceicon/' + str(device) + '?size=' + size )
                if recieve.status_code == 200 :
                    with open(parentdir + save_location + '//device_' + str(device) + '.png','wb') as f:
                        f.write(recieve.content)
                
                else:
                    logging.WARNING("device " + str(device) + " no Image recieved")
            
            except:
                logging.ERROR("device " + str(device) + " got no Image", exc_info=True)

    # getting online values(reliable Version)
    def GetOnlineValues(self,devices,value="ActiveEnergyConsumed",phase="SUM13",retries=10,mode="fast",timeout="500",appendValueType="False"):
        
        id = CheckInput(devices) # making a List of device ids
        devicestring = ""
        # creates a string with all devices data for the GET request
        for device in id:
            if devicestring =="":
                # prevents the String from starting with the deviding charakter
                devicestring = "?value=" + str(device) + ";" + str(value) + ";" + str(phase) 
            else:
                # Adds the next String to the previous
                devicestring = str(devicestring) + "&value=" + str(device) + ";" + str(value) + ";" + str(phase) 
        logging.debug("devicestring generated : " + devicestring)
        
        urltimeout =  "&timeout="+str(timeout)
        urlappendValueType = "&appendValueType="+str(appendValueType)

        url = "http://" + str(self.connection) + "/rest/1/projects/" + str(self.project) + "/onlinevalues/.json" + devicestring + urltimeout + urlappendValueType
        
        if mode != "fast" and mode != "precise":
            mode = "fast"
            logging.warning("no or wrong mode for onlinevalues specified must be 'fast' or 'precise' ! mode set to default 'fast'")

        if mode == "precise":
            x = 0
            allvaluesokay = False
            while x < retries and allvaluesokay == False:
                try:
                    logging.info("try no. " + str(x+1))
                    response = requests.request("GET", url) # sending GET-request
                    if response.status_code == 200 :
                        allvaluesokay = True
                        data = response.json() #parsing response to JSON
                        logging.debug(data)
                        # checking if returned Block od data contains "NaN" entries
                        for item in data["value"]:
                            if  data["value"][item] == "NaN":
                                allvaluesokay = False
                                logging.debug("found NaN")
                                break
                    else:
                        logging.error("bad request")
                except:
                    logging.error("try not succesfull", exc_info=True)
                x += 1    
            

        
            # making a named dict for easy data access
            value_dict = {}
            for item in data["value"]:
                id = str(item.replace("." + value + "." + phase,""))
                this_data = { "value": str(data["value"][item]) , "time": str(data["time"][item]) ,"type" :{"typeName": str(data["valueType"][item]["typeName"]) , "unit":str(data["valueType"][item]["unit"]), "valueName":str(data["valueType"][item]["valueName"]),"value":str(data["valueType"][item]["unit"]), "valueName":str(data["valueType"][item]["value"]),"valueName":str(data["valueType"][item]["valueName"]),"value":str(data["valueType"][item]["value"]), "type":str(data["valueType"][item]["type"]) }}
                value_dict[id] = this_data

        elif mode == "fast":
            value_dict = {}
            x = 0
            allvaluesokay = False
            while x < retries and allvaluesokay == False:
                try:
                    logging.info("try no. " + str(x+1))
                    response = requests.request("GET", url) # sending GET-request

                    if response.status_code == 200 :
                        allvaluesokay = True
                        data = response.json() #parsing response to JSON
                        logging.debug(data)
                        # checking if returned Block od data contains "NaN" entries
                        for item in data["value"]:
                            if data["value"][item] != "NaN":
                                id = str(item.replace("." + value + "." + phase,""))
                                this_data = { "value": str(data["value"][item]) , "time": str(data["time"][item]) ,"type" :{"typeName": str(data["valueType"][item]["typeName"]) , "unit":str(data["valueType"][item]["unit"]), "valueName":str(data["valueType"][item]["valueName"]),"value":str(data["valueType"][item]["unit"]), "valueName":str(data["valueType"][item]["value"]),"valueName":str(data["valueType"][item]["valueName"]),"value":str(data["valueType"][item]["value"]), "type":str(data["valueType"][item]["type"]) }}
                                value_dict[id] = this_data
                                this_device = "value=" + str(item.replace(".",";"))
                                url = url.replace(this_device,"")
                                logging.debug("device " + str(id) + " removed from next request")
                            else:
                                pass

                        for item in data["value"]:
                            if data["value"][item] == "NaN":
                                allvaluesokay = False
                                logging.debug("found NaN")
                                break
                            else:
                                pass
                    elif response.status_code == 404 :
                        data = response.text
                        logging.debug(data)
                        id = int(data.replace("Device not found for id:",""))
                        this_device = "value=" + str(id) + ";" + str(value) + ";" + str(phase)
                        url = url.replace(this_device,"")
                        logging.debug("removed device " + str(id) + " because no data is present")
                        x -= 1
                    else:
                        logging.error("bad request")
                except:
                    logging.error("try not succesfull", exc_info=True)
                x += 1    

        return(value_dict)


    # getting historical values by timeframe
    def GetHistoricalValueByTimeframe(self,id,start,end,retries=10, value="ActiveEnergyConsumed",phase="SUM13",mode="fast",timeoutIfLive="500"):
        ids = CheckInput(id)
        
        # checks if timeframe is set to end on live time
        if end == "live":
            
            # getting live values for the end of the timeframe
            onlinedevices = self.GetOnlineValues(id,retries=retries,mode=mode,timeout=timeoutIfLive,value=value,appendValueType="True")
            print(onlinedevices)
            result = {}
            
            # requesting every devices timeframe 
            for id in ids:
                
                try:
                    url = "http://" + self.connection + "/rest/1/projects/" + self.project + "/devices/" + str(id) + "/hist/energy/" + str(value) + "/" + str(phase) + ".json?start=UTCNANO_" + str(start) + "&end=UTCNANO_" + str(onlinedevices[str(id)]["time"])
                    response = requests.request("GET", url) # sending GET-request
                    #checking for responsecode
                    if response.status_code == 200:
                        data = response.json() # parsing response to json
                        result[str(id)] = {"start" : str(data["startTime"]), "end" : str(data["endTime"]), "value" : str(data["energy"]), "unit" : str(data["valueType"]["unit"]) , "value_name" : str(data["valueType"]["valueName"]) }
                    
                    else:
                        # filling the results with "empty" to see errors
                        result[str(id)] = {"start" : "empty", "end" : "empty", "value" : "statuscode " + str(response.status_code), "unit" : "empty" , "value_name" : "empty" }
                        logging.error("http status code : " + str(response.status_code) + " on device : " + id)
                except:
                    logging.error("http request failed", exc_info=True)
                pass
            pass
        
        # if timeframe is not "live" use end time
        else:
            result = {}
            # requesting every devices timeframe 
            for id in ids:
                url = "http://" + self.connection + "/rest/1/projects/" + self.project + "/devices/" + str(id) + "/hist/energy/" + str(value) + "/" + str(phase) + ".json?start=UTCNANO_" + str(start) + "&end=UTCNANO_" + str(end)
                
                try:
                    response = requests.request("GET", url) # sending GET-request
                    #checking for responsecode
                    if response.status_code == 200:
                        data = response.json()
                        result[str(id)] = {"start" : str(data["startTime"]), "end" : str(data["endTime"]), "value" : str(data["energy"]), "unit" : str(data["valueType"]["unit"]) , "value_name" : str(data["valueType"]["valueName"]) }
                    
                    else:
                        # filling the results with "empty" to see errors
                        result[str(id)] = {"start" : "empty", "end" : "empty", "value" : "empty", "unit" : "empty" , "value_name" : "empty" }
                        logging.error("http status code : " + str(response.status_code) + " on device : " + id)
                except:
                    logging.error("http request failed")
                pass
            pass
        return(result)

