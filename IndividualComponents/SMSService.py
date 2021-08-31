from twilio.rest import Client

def main():
    account_sid = "AC35b622ad2fd3094dfd47f9b94e4ef723"
    auth_token = "7bc6635a41ecd3131d29b1f39e43fff4"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+65" + str(96388495),
        from_="+16182081528",
        body="Testing from RPi")

    print(message)
main()