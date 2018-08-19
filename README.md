#### Table of Contents

1. [Description](#description)
1. [Issues](#issues)
1. [Requirements](#requirements)


## Description

This tool will allow you to check your 1Password logins against https://haveibeenpwned.com/

I am currently no longer developing this as 1Password have already implemented a comprised password list within the application and therefore this is definitely incomplete. 

This was developed for use on a Mac.

## Issues

There are issues with hitting API limits even with the waits periods between the checks. 

### Requirements

Download the command line tool from the 1password website: https://support.1password.com/command-line-getting-started/

Following the getting started guide on the 1password website: https://support.1password.com/command-line-getting-started/#get-started-with-the-command-line-tool

    pip install -r requirements.txt
    brew install jq 
