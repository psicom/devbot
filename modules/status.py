import willie
import urllib
import datetime

laststate = True
fucking = False

def query_api(mode='viewstatus'):
    url = "https://devlol.org/status/hackerspaceapi/"
    return urllib.urlopen(url + mode).read()

@willie.module.commands('fuckingstatus')
def fuckingstatus(bot, trigger):
    global fucking
    fucking = True
    status(bot, trigger)

@willie.module.commands('status')
def status(bot, trigger):
    global laststate
    global fucking
    cmd = trigger.group(2)
    if cmd != None:
        cmd = cmd.lower()
    if cmd == 'open':
        mode = 'set/open'
    elif cmd == 'close' or cmd == 'closed':
        mode = 'set/close'
    else:
        mode = 'viewstatus'
    status = query_api(mode)
    laststate = 'OPEN' in status
    if fucking:
        status = status.replace('is', 'is fucking').replace('since', 'since fucking')
    bot.say(status)
    # trigger the topic broadcast
    bot.write(('TOPIC', '#devlol'))
    fucking = False

@willie.module.commands('isitChristmas')
def christmas(bot, trigger):
    days_to_go = (datetime.date(datetime.date.today().year, 12, 24) - datetime.date.today()).days
    if days_to_go == 0:
        boy.say("Happy Birthday Brian!")
    else:
        bot.say("No. But it's only %i days to go." % days_to_go)

@willie.module.interval(60)
def check_status(bot):
    global laststate
    state = 'OPEN' in query_api()
    if laststate is not state:
        laststate = state
        if state:
            bot.msg('#devlol', 'the space is now OPEN')
        else:
            bot.msg('#devlol', 'the space is now CLOSED')

@willie.module.rule('.*')
@willie.module.event('332')
def topic_set(bot, trigger):
    s = query_api()
    if 'OPEN' in s:
        prefix = '[OPEN]'
    else:
        prefix = '[CLOSED]'
    if not trigger.startswith(prefix):
        bot.write(('TOPIC', '#devlol'), prefix + " " + trigger.strip('[OPEN]').strip('[CLOSED]'))

@willie.module.rule('.*')
@willie.module.event('TOPIC')
def topic_trigger(bot, trigger):
    bot.write(('TOPIC', '#devlol'))

#init state on startup
laststate = 'OPEN' in query_api()
