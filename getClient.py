
import requests
import re

HOST_URL = "http://localhost:8080/senaite"

def getClient(session):
    answers=["yes","no"]
    i=0
    url = "{}/@@API/senaite/v1/client".format(HOST_URL)
    strangs =session.get(url)
    search = strangs.text

    uid=re.findall("(?<!_)uid\":\s\"([0-9a-z]{32})", str(search))
    title=re.findall("(?<=title\":\s\")(.+?)\"", str(search))

    while i==0:
        print("The available clients are:")
        print(title)
        print()
        client=raw_input("Please enter the client's name you wish to add samples for (without spaces or quotation marks) and press enter: ")
        correct=raw_input("Is this correct? Please enter yes or no: ")
        if correct.strip().lower() == "yes" and title and correct.strip().lower() in answers:
            if client in title:
               for name in title:
                    if name == client and uid:
                        #data["Client"] = "{}".format(uid[title.index(name)])
                        print("You did it!")
                        i=1
            else:
                while True:
                    print("Could not find {} in the system. Do you want to enter another name?".format(client))
                    again=raw_input("Please enter yes or no: ")
                    if again in answers:
                        if again.strip().lower() == "yes":
                            break
                        else:
                            i=1
                            break
                    else:
                        print("Your answer was invalid.")
                        continue
        elif correct.strip().lower() == "no" and title and correct.strip().lower() in answers:
            continue
        else:
            print("Your answer was invalid")
            continue


def get_session(user, password):
    session = requests.Session()
    session.auth = (user, password)
    url = "{}/@@API/senaite/v1/auth".format(HOST_URL)
    response = session.get(url)
    if response.status_code != 200:
        session = None
    return session


if __name__ == "__main__":

    user = "admin"
    password = "admin"


    # Get an authenticated session
    session = get_session(user, password)
    if not session:
        print "Cannot authenticate"
    else:
        # Create the Sample
        getClient(session)
