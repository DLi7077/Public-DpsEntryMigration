import DataMigration as migrate
import requests
import pandas as pd
import os
import sys
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

abyss_entries="Past dpsEntries\Abyss\DPSAbyss-DPS-Abyss-2022-02-21.csv"
# get oauth token
tokenOptions={
    "client_id": "______________________",
    "client_secret": "__________________",
    "audience":"https://________________",
    "grant_type":"client_credentials"
}
# fetch token
tokenRequest = requests.post("https://____/oauth/token",
                            headers = {"contentType": "application/json"}, 
                            data = tokenOptions);
# print status
print(tokenRequest)
# convert to json
tokenJson = tokenRequest.json()
# get access token
token = tokenJson["access_token"]
# print(token)


# Extract and process .csv files
cdir = os.path.dirname(__file__)
isFirstTable = True

#--------------------------DONE----------------------------------
# # post request for Abyss Entries
# migrate.migrateAbyssData(cdir,token)

# Post Request for Primo Geovishap Entries
# dpsSheets= os.path.dirname('Past_dpsEntries/Primo Geovishap/')
# migrate.migratePrimoGeovishapData(dpsSheets,token)
#----------------------------------------------------------------


migrate.migrateOverWorldData(cdir, token)

# # get all entries
# getRando= requests.get("https://tgh-server-staging.herokuapp.com/api/dps-entries/")
# # print all entries
# print("\ngetting all entries..")
# print(getRando.text)