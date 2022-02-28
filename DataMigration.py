from datetime import date
import json
import os
import pandas as pd
import re
import requests
import time
import processFunction as process

# given Abyss entries
# return cleaned dataframe
def getAbyssDataframe (df):
    print("Processing abyss data...")
    
    # Default the dps entry schema
    df["discord_tag"] = "N/A"
    df["dps_category"] = "Abyss"
    df["abyss_version"] = ""
    df["video_link"] = ""
    df["attack_type"] =""
    df["stunned"]=""
    df["food_used"]=""
    
    df.rename(columns={"Version": "game_version"}, inplace=True)
    df.rename(columns={"Alias": "alias"}, inplace=True)
    df.rename(columns={"Target": "abyss_floor"}, inplace=True)
    df.rename(columns={"Damage": "damage_dealt"}, inplace=True)
    df.rename(columns={"Notes": "notes"}, inplace=True)
    df.rename(columns={"Characters": "team"}, inplace=True)
    df.rename(columns={"Region": "region"}, inplace=True)
    df["approved"] = True
    
    dropList = []
    
    #for each row
    for i, row in df.iterrows():
        # Remove null row
        nullCheck = row["alias"]
        if not isinstance(nullCheck,str):
            dropList.append(i)
            continue
            
        else:
            # Process GameVersion
            df.at[i, "game_version"] = process.processGameVersion(row["game_version"])
            
            # Set abyss floor
            abyssFloor=df.at[i, "abyss_floor"][6:]
            df.at[i, "abyss_floor"] = process.processAbyssFloor(abyssFloor)
            
            # Process EnemyLevel for Abyss floors
            abyssFloorList=abyssFloor.split("-")
            floor= int(abyssFloorList[0])
            chamber= int(abyssFloorList[1])
            df.at[i, "enemy"]= "Primo Geovishap"
            df.at[i, "enemy_lv"]= process.processAbyssMonsterLevel(floor,chamber)
            
            # Process Damage
            df.at[i, "damage_dealt"] = process.processDamage(row["damage_dealt"])
            
            # Process VideoLink
            videoLink = str(row["alias"])
            rgx = re.search("href=\"(.*?)\"", videoLink)
            videoLink = rgx.group(1)
            df.at[i, "video_link"] = videoLink
            videoTitle= process.getYoutubeTitle(videoLink)
            # Process Alias
            alias = str(row["alias"])
            rgx = re.search("\">(.*)<\/a>", alias)
            alias = rgx.group(1)
            df.at[i, "alias"] = alias
            
            # Process dps_character and team
            teamList= df.at[i, "team"].split()
            teamList= process.orderedTeam(teamList, videoTitle)
            
            if(len(teamList)>4 or len(teamList)<1):
                print("Invalid team size characters")
                print(teamList, "\nsize:", len(teamList))
                quit()

            df.at[i, "dps_character"]=process.processCharacter(teamList[0])
            df.at[i, "team"]= (teamList[1:])
            
            # Process Region
            df.at[i, "region"] = process.processRegion(row["region"])
            
            # Process Miscellaneous
            notes = row["notes"]
            df.at[i, "attack_type"]= process.processAbilityUsed(notes)
            df.at[i, "stunned"]= process.processIsMobStunned(notes)
            df.at[i, "food_used"]= process.processFoodUsed(notes)
            
            # Process Notes
            if isinstance(notes, str):
                if notes.__contains__("2.0"):
                    df.at[i, "game_version"] = "2.0"
                    df.at[i, "notes"] = ""
            else:
                df.at[i, "notes"] = ""
                
    df.drop(df.index[dropList], inplace=True)
    return df

# given Primo geovishap entries
# return cleaned dataframe
def getPrimoGeoDataframe(df,name):
    print("Processing Primo Geovishap data...")
    print("Character Name:",name)
    # Default the dps entry schema
    df["discord_tag"] = "N/A"
    df["dps_category"] = "World Boss"
    df["abyss_version"] = ""
    df["video_link"] = ""
    df["attack_type"] =""
    df["stunned"]=""
    df["food_used"]=""
    
    df.rename(columns={"Version": "game_version"}, inplace=True)
    df.rename(columns={"Alias": "alias"}, inplace=True)
    df.rename(columns={"Damage": "damage_dealt"}, inplace=True)
    df.rename(columns={"Supports": "team"}, inplace=True)
    df.rename(columns={"Notes": "notes"}, inplace=True)
    df.rename(columns={"Region": "region"}, inplace=True)
    df["approved"] = True
    dropList = []
    
    #for each row
    for i, row in df.iterrows():
        # Remove null row
        nullCheck = row["alias"]
        if not isinstance(nullCheck,str):
            dropList.append(i)
            
        else:# Process VideoLink
            videoLink = str(row["alias"])
            rgx = re.search("href=\"(.*?)\"", videoLink)
            videoLink = rgx.group(1)
            df.at[i, "video_link"] = videoLink
            videoTitle= process.getYoutubeTitle(videoLink)
                
            # Process GameVersion
            df.at[i, "game_version"] = process.processGameVersion(row["game_version"])
            # Process Damage
            df.at[i, "damage_dealt"]= process.processDamage(row["damage_dealt"])
            # set Enemy
            df.at[i, "enemy"] = "Primo Geovishap"
            df.at[i, "enemy_lv"] = 93
            # set dps Character
            df.at[i, "dps_character"] = name
            # set team
            df.at[i, "team"]= row["team"].split()[-3:]
            
            
            # Process Region
            df.at[i, "region"] = process.processRegion(row["region"])
            # Process Miscellaneous
            notes = row["notes"]
            df.at[i, "attack_type"]= process.processAbilityUsed(notes)
            df.at[i, "stunned"]= process.processIsMobStunned(notes)
            df.at[i, "food_used"]= process.processFoodUsed(notes)
            
            # check if it's actually Domain
            if('legend' in notes.lower()):
                df.at[i,"dps_category"]= "Event"
                df.at[i,"enemy_level"] = 90
            
            
            # Process Alias
            alias = str(row["alias"])
            rgx = re.search("\">(.*)<\/a>", alias)
            alias = rgx.group(1)
            df.at[i, "alias"] = alias
            
            # Process Notes
            if isinstance(notes, str):
                if notes.__contains__("2.0"):
                    df.at[i, "game_version"] = "2.0"
                    df.at[i, "notes"] = ""
            else:
                df.at[i, "notes"] = ""
        
    df.drop(df.index[dropList], inplace=True)
    return df
# given overworld entries
# return cleaned dataframe
def getOverworldDataFrame(df):
    print("Processing Overworld data...")
    
    # Default the dps entry schema
    df["discord_tag"] = "N/A"
    df["dps_category"] = "Overworld"
    df["abyss_version"] = ""
    df["video_link"] = ""
    df["attack_type"] =""
    df["stunned"]=""
    df["food_used"]=""
    
    df.rename(columns={"Version": "game_version"}, inplace=True)
    df.rename(columns={"Alias": "alias"}, inplace=True)
    df.rename(columns={"Target":"enemy"}, inplace=True)
    df.rename(columns={"Damage": "damage_dealt"}, inplace=True)
    df.rename(columns={"Characters": "team"}, inplace=True)
    df.rename(columns={"Notes": "notes"}, inplace=True)
    df.rename(columns={"Region": "region"}, inplace=True)
    df["approved"] = True
    
    
    dropList = []
    
    #for each row
    for i, row in df.iterrows():
        # Remove null row
        nullCheck = row["alias"]
        if not isinstance(nullCheck,str):
            dropList.append(i)
        else:
            
            # Process VideoLink
            videoLink = str(row["alias"])
            rgx = re.search("href=\"(.*?)\"", videoLink)
            videoLink = rgx.group(1)
            df.at[i, "video_link"] = videoLink
            
            videoTitle= process.getYoutubeTitle(videoLink)
                
            # Process Alias
            alias = str(row["alias"])
            rgx = re.search("\">(.*)<\/a>", alias)
            alias = rgx.group(1)
            df.at[i, "alias"] = alias
            
            # Process GameVersion
            df.at[i, "game_version"] = process.processGameVersion(row["game_version"])
            
            # Process Damage
            df.at[i, "damage_dealt"]= process.processDamage(row["damage_dealt"])
            
            # set Enemy
            df.at[i, "enemy"] = process.processOverworldMob(row['enemy'])
            df.at[i, "enemy_lv"] = process.processOverworldMobLevel(df.at[i, "enemy"])
            
            # set dps Character
            team= df.at[i, "team"].split()
            teamList= process.orderedTeam(team, videoTitle)
            
            df.at[i, "dps_character"]=process.processCharacter(teamList[0])
            
            # df.at[i, "dps_character_element"]=process.processCharacterElement(teamList[0])
            
            # set team
            df.at[i, "team"]= (teamList[1:])
            
            # Process Region
            df.at[i, "region"] = process.processRegion(row["region"])
            # Process Miscellaneous
            notes = row["notes"]
            df.at[i, "attack_type"]= process.processAbilityUsed(notes)
            df.at[i, "stunned"]= process.processIsMobStunned(notes)
            df.at[i, "food_used"]= process.processFoodUsed(notes)
            if(len(videoTitle)==0):
                df.at[i, "notes"]= "INVALID LINK"
            
            
            # Process Notes
            if isinstance(notes, str):
                if notes.__contains__("2.0"):
                    df.at[i, "game_version"] = "2.0"
                    df.at[i, "notes"] = ""
            else:
                df.at[i, "notes"] = ""

    df.drop(df.index[dropList], inplace=True)
    return df
            
    

# Splits dataframe into chunks to export
def split_dataframe(df, chunk_size = 250): 
    chunks = list()
    num_chunks = len(df) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(df[i*chunk_size:(i+1)*chunk_size])
    return chunks

# Sends create request to db using a dataframe
def submit_request(data, token):
    print(data.to_string())
    print("Done printing!")
    time.sleep(1)

    header = {
        "contentType": "application/json",
        "authorization": "Bearer {0}".format(token)
    }
    
    url = "https://tgh-server-staging.herokuapp.com/api/dps-entries/create-all"
    data_json = json.loads(data.to_json(orient='records'))
    
    print("Sending post request...")
    response = requests.post(url, headers = header, json = data_json)
    print(response)
    time.sleep(2)

# Given csv directory and token, adds entries to data base
def migrateAbyssData(cdir, token):
    filepath = "Past_dpsEntries\Abyss\DPSAbyss-DPS-Abyss-2022-02-21.csv"
    # export Abyss Entry File
    file_res = os.path.join(cdir, filepath)
    data = pd.read_csv(file_res, dtype=object)
    data = getAbyssDataframe(data)

    datalist= split_dataframe(data)

    for x in datalist:
        submit_request(x, token)

# cdir = os.path.dirname(__file__)
# isFirstTable = True
def migratePrimoGeovishapData(cdir, token):
    date = '2022-02-21'
    characterMap={
        "Albedo":"primoAlbedo-Albedo-",
        "Aloy":"primoAloy-Aloy-",
        "Amber":"primoAmber-Amber-",
        # "Arataki Itto":"",
        "Barbara":"primoBarbara-Barbara-",
        "Beidou":"primoBeidou-Beidou-",
        "Bennett":"primoBennett-Bennett-",
        "Chongyun":"primoChongyun-Chongyun-",
        "Diluc":"primoDiluc-Diluc-",
        "Diona":"primoDiona-Diona-",
        "Eula":"primoEula-Eula-",
        "Fischl":"primoFischl-Fischl-",
        "Ganyu":"primoGanyu-Ganyu-",
        # "Gorou":"primoGorou-Gorou",
        "Hu Tao":"primoHutao-Hutao-",
        "Jean":"primoJean-Jean-",
        "Kaedehara Kazuha":"primoKazuha-Kazuha-",
        "Kaeya":"primoKaeya-Kaeya-",
        "Kamisato Ayaka":"primoAyaka-Ayaka-",
        # "Kamisato Ayato":"",
        "Keqing":"primoKeqing-Keqing-",
        "Klee":"primoKlee-Klee-",
        "Kujou Sara":"primoSara-Sara-",
        "Lisa":"primoLisa-Lisa-",
        "Mona":"primoMona-Mona-",
        "Ningguang":"primoNingguang-Ningguang-",
        "Noelle":"primoNoelle-Noelle-",
        "Qiqi":"primoQiqi-Qiqi-",
        "Raiden Shogun":"primoRaiden-Raiden-",
        "Razor":"primoRazor-Razor-",
        "Rosaria":"primoRosaria-Rosaria-",
        # "Sangonomiya Kokomi":"primoKokomi-Kokomi-",
        "Sayu":"primoSayu-Sayu-",
        # "Shenhe":"",
        "Sucrose":"primoSucrose-Sucrose-",
        "Tartaglia":"primoTartaglia-Tartaglia-",
        # "Thoma":"",
        # "Traveler":"",
        "Venti":"primoVenti-Venti-",
        "Xiangling":"primoXiangling-Xiangling-",
        "Xiao":"primoXiao-Xiao-",
        "Xingqiu":"primoXingqiu-Xingqiu-",
        "Xinyan":"primoXinyan-Xinyan-",
        # "Yae Miko":"",
        "Yanfei":"primoYanfei-Yanfei-",
        "Yoimiya":"primoYoimiya-Yoimiya-",
        # "Yun Jin":"",
        "Zhongli":"primoZhongli-Zhongli-"
    }
    for character in characterMap:
        # get file name for each character
        filepath= characterMap[character] + date + '.csv'
        file_res = os.path.join(cdir,filepath)
        data = pd.read_csv(file_res,dtype= object)
        
        data = getPrimoGeoDataframe(data,character)
        
        datalist = split_dataframe(data)
        for x in datalist:
            submit_request(x,token)


def migrateOverWorldData(cdir,token):
    filepath= "Past_dpsEntries\Overworld\DPSOpenWorld-DPS-Open-World-2022-02-21.csv"
    
    file_res= os.path .join(cdir, filepath)
    data= pd.read_csv(file_res, dtype= object)
    data= data.iloc[30:40]
    data= getOverworldDataFrame(data)
    
    datalist= split_dataframe(data)
    
    for x in datalist:
        submit_request(x,token)