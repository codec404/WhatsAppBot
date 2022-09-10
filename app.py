from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
from create import crt_evnt
from get import get_evnt
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/sms',methods=['POST'])
def sms_reply():
    msg=request.form.get('Body')
    phone_no = request.form.get('From')

    if msg.startswith("create"):
        start_date,start_time,end_date,end_time =msg.split(" ")[1:5]
        event_name = ""
        event_list = msg.split(" ")[5:]
        
        for i in event_list:
            event_name+=i+" "
        reply = crt_evnt(start_date,start_time,end_date,end_time,event_name)
    elif msg.startswith("list"):
        if len(msg.split(" ")) > 1:
            count= msg.split(" ")[1]
            reply = get_evnt(int(count))
        else:
            get_evnt()
    else:
        reply = """
            Please enter a valid command:
        Example:
        1.create 01-Jan-65 00:00AM 01-Jan-65 07:00AM Event_Name
        2.list 5
        """
    resp = MessagingResponse()
    resp.message(reply)

    return(str(resp))

if __name__== '__main__':
    app.run(debug=True)
