# Work with Python 3.6 make sure dependencies are installed correctly. 
# See discord.py github for installing correct dependencies
import discord
import pickle


    #events[names of all events] each event is a dict
    #individual_events_from above[ details, rsvp ]


client = discord.Client()

@client.event
async def on_message(message):

    global events; 

    if message.author == client.user:
        return
    
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    if message.content.startswith('!help'):
        msg =( 
                '''
                Available Commands:
                Thanks for using event-bot. If you feel generous, give daniel some power nine cardboard
                Anytime you see {} that shows how to format the command to make it work correctly. 
                Anytime you see () that means you can use as many words as you want. 

                !events - Returns a list of current events
                !newevent - create a new event.{ !newevent neweventname }

                !details - checks details of an event that has been created using the new event name as a delimiter. {!details myevent}
                !setdetails - create or change the details of an existing event. { !setdetails eventname event (description)}

                !rsvp - {!rsvp eventname name (arrival time or whatever)} will add you to the rsvp list
                !going - {!going eventname} -> shows a list of folks going to an certain event. 

                !delete - {!delete eventname supersecretpassword} - deletes an event. 
                ''')
        await client.send_message(message.channel, msg)


    if message.content.startswith('!events'):
        string = " "
        for key in events:
            string = string + " " + key
        msg = ('These are the upcoming events:%s' %string).format(message)
        await client.send_message(message.channel, msg)
    
    #new event. if exists, list details, if not make a new event and prompt for 
    #description
    if message.content.startswith('!newevent'.format(message)):
        args = message.content.split(" ")
        if (args[1] in events):
            msg = 'There is already an event under this name.'.format(message)
            await client.send_message(message.channel, msg)
        else: 
            events[args[1]] = dict()
            save_obj(events, NAME)
            msg = 'Just finished setting up your event. Please use !details *event_event name *description.'.format(message)
            await client.send_message(message.channel, msg)


    if message.content.startswith('!setdetails'.format(message)):
        #sets details for an event. 
        #will overwrite without saving the old version. 
        #Maybe add a check for this. 
        args = message.content.split(" ")
        string = build_string(args)
        tempdict = events[args[1]]
        tempdict['details'] = string
        save_obj(events, NAME)
        msg = 'Just finished saving your description'.format(message)
        await client.send_message(message.channel, msg) 

    if message.content.startswith('!details'.format(message)):
        
        args = message.content.split(" ")
        tempdict = events[args[1]]
        string = tempdict['details']
        msg = string.format(message)
        await client.send_message(message.channel, msg)
    
    if message.content.startswith('!rsvp'.format(message)):
        args = message.content.split(" ")
        if 'rsvp' in events[args[1]]:
            #adds to RSVP dict
            tempdict = events[args[1]]
            second_dict = tempdict['rsvp']
            second_dict[args[2]] = build_deeper(args)
            save_obj(events, NAME)
        else:
            #initializes dictionary for RSVP list. 
            tempdict = events[args[1]]
            tempdict['rsvp'] = dict()
            second_dict = tempdict['rsvp']
            second_dict[args[2]] = build_deeper(args)
            save_obj(events,NAME)

    if (message.content.startswith('!going'.format(message))):
        args = message.content.split(" ")
        if 'rsvp' in events[args[1]]:
            tempdict = events[args[1]]
            second_dict = tempdict['rsvp']
            string = " "
            for key in second_dict: 
                string = string +", "+ key
            msg = ('these are the folks rsvped for the event:%s' %string).format(message) 
        else: 
            msg = ('this event does not exist?').format(message)

        await client.send_message(message.channel, msg)

    if (message.content.startswith('!delete'.format(message))):
        args = message.content.split(" ")
        if args[1] in events and args[2] == 'supersecretpassword': 
            del events[args[1]]
            save_obj(events, NAME)
            msg = ('Event has been deleted successfully').format(message)
        else: 
            msg = ('Error deleting event, password is incorrect').format(message)
        await client.send_message(message.channel, msg) 

#eventdict -> keys are event names values are dictionaries.
        #event names are links to dictionaries with key being


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def save_obj(obj, name):
    with open('obj/'+ name +'.pkl', 'wb') as f: 
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def build_string(args):
    i = 3
    string = args[2]
    while (i < len(args)):
        string = string +" "+ args[i]
        i = i+1
    return string

def build_deeper(args):
    i = 4
    string = args[3]
    while (i < len(args)):
        string = string+" "+ args[i]
        i = i+1
    return string



NAME = 'eventdict'
TOKEN = ''
events = load_obj(NAME)



#run this if eventdict.pkl does not exist yet and comment out the code above. 
#please note a folder named obj needs to exist in current working directory. 
#then you have to make a new event to save the pkl. 
#restart bot afterwards and comment this following line and uncomment the top line.
#events = dict()
#save_obj(events, NAME)


client.run(TOKEN)
