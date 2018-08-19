import os, hashlib, requests, re, logging
from datetime import datetime
from time import sleep


def start():
    # Get the UUIDs of all the items stored in 1Password
    os.system("rm -rf .uuids")
    os.system("./op list items | jq -r '.[].uuid' >> .uuids")

    # Create array uuid_list and put each line into the array
    passwordsfound = 0
    passwords = {}
    uuid_list = []

    with open('.uuids') as uuid_file:
        for line in uuid_file:
            uuid_list.append(line)

    # For each item in the array, get the password by making API call
    for uuid in uuid_list:
        logging.info('----------------------------------------')
        logging.info('Checking UUID: %s' % uuid.rstrip())
        sleep(5.0)
        title = os.popen("./op get item %s" % uuid.strip() + " | jq --seq -r '.overview.title'").read()
        logging.info('Checking password for: %s' % title.rstrip())
        sleep(5.0)
        pwd = os.popen("./op get item %s" % uuid.rstrip() + " | jq --seq -r '.details.fields[] | select(.designation==\"password\").value'").read() 
        if pwd == "\n":
            logging.info('Skipping %s' % title.rstrip() + " due to no password.")
        else:
            pwd = pwd.strip('\n')
            title = title.strip('\n')

            # Convert the password to sha1 hash and pass the hash to the api
            hash = hashlib.sha1(pwd).hexdigest().upper()
            logging.info('Checking hash: %s' % hash)

            try:
                response = requests.get('https://api.pwnedpasswords.com/range/' + hash[0:5])
            except Exception:
                sleep(5.0)
                response = requests.get('https://api.pwnedpasswords.com/range/' + hash[0:5])

            # For each hash returned
            for each_hash in response.text.split("\n"):
                # Try and find a match
                if hash[5:] in each_hash:
                    # If there a match, split the hash and counter using semi-colon
                    pwd_occurences = each_hash.split(":")
                    logging.warning('!!!WARNING!!! --- The password: %s' % pwd + " for: %s" % title + " has been found {} times.".format(re.sub("[^0-9]", "", pwd_occurences[1])))
                    # Increment password count for summary
                    passwordsfound = passwordsfound + 1
                    passwords = {title:pwd}
                    sleep(2.0)  # Respecting the API limit
                    
    print "Number of passwords found: %s" % passwordsfound
    for key, value in passwords.iteritems():
        logging.info((key, value))


def main():
    """Function which sets the logging up."""
    logging.basicConfig(filename='./logs/general.log', level=logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.info('Session started - %s'
                         % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    start()


if __name__ == '__main__':
    main()
