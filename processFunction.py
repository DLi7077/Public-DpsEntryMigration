import json
import requests
import urllib
import urllib.request
from difflib import SequenceMatcher

"""
clean up:
character
enemy
enemylv
stunned
food_used
region
game_version
video_link
damage
"""

# return name if given name is similar to Official Name
def processCharacter (character):
    character= character.lower().strip()
    nameList = [
        "Albedo",
        "Aloy",
        "Amber",
        "Anemo Traveler",
        "Arataki Itto",
        "Barbara",
        "Beidou",
        "Bennett",
        "Childe",
        "Chongyun",
        "Cryo Traveler",
        "Dendro Traveler",
        "Diluc",
        "Diona",
        "Electro Traveler",
        "Eula",
        "Fischl",
        "Ganyu",
        "Gorou",
        "Hu Tao",
        "Hydro Traveler",
        "Jean",
        "Kaedehara Kazuha",
        "Kaeya",
        "Kamisato Ayaka",
        "Kamisato Ayato",
        "Keqing",
        "Klee",
        "Kujou Sara",
        "Lisa",
        "Mona",
        "Ningguang",
        "Noelle",
        "Pyro Traveler",
        "Qiqi",
        "Raiden Shogun",
        "Razor",
        "Rosaria",
        "Sangonomiya Kokomi",
        "Sayu",
        "Shenhe",
        "Sucrose",
        "Tartaglia",
        "Thoma",
        "Geo Traveler",
        "Venti",
        "Xiangling",
        "Xiao",
        "Xingqiu",
        "Xinyan",
        "Yae Miko",
        "Yanfei",
        "Yoimiya",
        "Yun Jin",
        "Zhongli "
    ]
    
    # search for best match
    bestMatch=""
    bestRatio=0
    for name in nameList:
        ratio= SequenceMatcher(a=name.lower(),b=character).ratio()
        if(character in name.lower()):
            return name
        if(ratio>0.7 and ratio>bestRatio):
            bestMatch= name
            bestRatio=ratio
    if(bestMatch==""):
        print("character not found")
        print(character)
        quit()
    return bestMatch

# return Element of character
def processCharacterElement(character):
    elementMap={
        "Albedo":"Geo",
        "Aloy":"Cryo",
        "Amber":"Pyro",
        "Anemo Traveler":"Anemo",
        "Arataki Itto":"Geo",
        "Barbara":"Hydro",
        "Beidou":"Electro",
        "Bennett":"Pyro",
        "Chongyun":"Cryo",
        "Cryo Traveler":"Cryo",
        "Dendro Traveler":"Dendro",
        "Diluc":"Pyro",
        "Diona":"Cryo",
        "Eula":"Cryo",
        "Electro Traveler":"Electro",
        "Fischl":"Electro",
        "Geo Traveler":"Geo",
        "Ganyu":"Cryo",
        "Gorou":"Geo",
        "Hu Tao":"Pyro",
        "Hydro Traveler":"Hydro",
        "Jean":"Anemo",
        "Kaedehara Kazuha":"Anemo",
        "Kaeya":"Cryo",
        "Kamisato Ayaka":"Cryo",
        "Kamisato Ayato":"Hydro",
        "Keqing":"Electro",
        "Klee":"Pyro",
        "Kujou Sara":"Electro",
        "Lisa":"Electro",
        "Mona":"Hydro",
        "Ningguang":"Geo",
        "Noelle":"Geo",
        "Pyro Traveler":"Pyro",
        "Qiqi":"Cryo",
        "Raiden Shogun":"Electro",
        "Razor":"Electro",
        "Rosaria":"Cryo",
        "Sangonomiya Kokomi":"Hydro",
        "Sayu":"Anemo",
        "Shenhe":"Cryo",
        "Sucrose":"Anemo",
        "Tartaglia":"Hydro",
        "Thoma":"Pyro",
        "Venti":"Anemo",
        "Xiangling":"Pyro",
        "Xiao":"Anemo",
        "Xingqiu":"Hydro",
        "Xinyan":"Pyro",
        "Yae Miko":"Electro",
        "Yanfei":"Pyro",
        "Yoimiya":"Pyro",
        "Yun Jin":"Geo",
        "Zhongli":"Geo"
    }
    return elementMap[character]
    
# takes url string and returns title of video as string
def getYoutubeTitle(url):
    params = {"format": "json", "url": url}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string
    status= requests.get(url)
    if(status.status_code==200):
        print("good link")
        with urllib.request.urlopen(url) as response:
                response_text = response.read()
                data = json.loads(response_text.decode())
                if("title" in data):
                    return data['title']
    else:
        print("no vid found")
        return ""
# given a list parameter, and youtube url
# returns a list of 4 strings where the 1st string is the dps character
def orderedTeam(team, video_title):
    # correct team members
    for i in range (len(team)):
        team[i]=processCharacter(team[i])
    
    dps=""
    found= False
    # in case someone has childe instead of tart in name
    video_title.replace("childe","tartaglia")
    
    # look for dps character
    for i in team:
        if(i.lower() in video_title):
            dps= processCharacter(i)
            found= True
            break
    if(not found):
        return team
    # found, put dps to front
    new_team_list= [dps]
    team.remove(dps)
    new_team_list+= team
    return new_team_list

# Process abyss floor
def processAbyssFloor(floorChamber):
    chambers=[
    '1-1',
    '1-2',
    '1-3',
    '2-1',
    '2-2',
    '2-3',
    '3-1',
    '3-2',
    '3-3',
    '4-1',
    '4-2',
    '4-3',
    '5-1-1',
    '5-1-2',
    '5-2-1',
    '5-2-2',
    '5-3-1',
    '5-3-2',
    '6-1-1',
    '6-1-2',
    '6-2-1',
    '6-2-2',
    '6-3-1',
    '6-3-2',
    '7-1-1',
    '7-1-2',
    '7-2-1',
    '7-2-2',
    '7-3-1',
    '7-3-2',
    '8-1-1',
    '8-1-2',
    '8-2-1',
    '8-2-2',
    '8-3-1',
    '8-3-2',
    '9-1-1',
    '9-1-2',
    '9-2-1',
    '9-2-2',
    '9-3-1',
    '9-3-2',
    '10-1-1',
    '10-1-2',
    '10-2-1',
    '10-2-2',
    '10-3-1',
    '10-3-2',
    '11-1-1',
    '11-1-2',
    '11-2-1',
    '11-2-2',
    '11-3-1',
    '11-3-2',
    '12-1-1',
    '12-1-2',
    '12-2-1',
    '12-2-2',
    '12-3-1',
    '12-3-2']
    if(floorChamber not in chambers):
        print("chamber not found")
        print(floorChamber)
        quit()
        
    return floorChamber;
# ONLY FOR ABYSS takes a pair value: floor and chamber
# returns monster level in that Floor-Chamber 
def processAbyssMonsterLevel(floor, chamber):
    if(floor<1 or floor> 12 or chamber<1 or chamber >3):
        print("invalid floor/ chamber")
        print(floor, chamber)
        quit()
    # floor 7 enemies are lv 65
    # floor 8  70 70 70
    # floor 9  72 74 76
    # floor 10 80 82 85
    # floor 11 88 90 92
    # floor 12 95 98 100
    chamber-=1
    levelMap= {
        9: [72, 74, 76],
        10:[80, 82, 85],
        11:[88, 90, 92],
        12:[95, 98, 100]
    }
    if(floor>8): return levelMap[floor][chamber]
    if(floor==1): return 25
    else: return floor*5 +30

# returns validated Damage as integer
def processDamage(damage):
    damage= int(damage)
    if(damage> 8000000):
        print("That's a lot of damage.. Is it correct?")
        print(damage)
        quit()
    
    return damage

# returns validated enemyTarget as string
def processOverworldMob(enemyTarget):
    mobList= [
        "Andrius",
        "Anemo Hypostasis",
        "Anemoboxer Vanguards",
        "Azhdaha",
        "Childe",
        "Cryo Hypostasis",
        "Cryogunner Legionnaires",
        "Cryo Regisvine",
        "Dvalin",
        "Electrohammer Vanguard",
        "Electro Hypostasis",
        "Cryo Cicin Mage",
        "Electro Cicin Mage",
        "Pyro Agent",
        "Geochanter Bracers",
        "Geo Hypostasis",
        "Golden Wolflord",
        "Hydro Hypostasis",
        "Hydrogunner Legionnaires",
        "Maguu Kenki",
        "Masanori",
        "Mirror Maiden",
        "Mitachurl",
        "Oceanid",
        "Perpetual Mechanical Array",
        "Primo Geovishap",
        "Pyroslinger Bracers",
        "Pyro Hypostasis",
        "Pyro Regisvine",
        "Raiden Shogun",
        "Ruin Cruiser",
        "Ruin Defender",
        "Ruin Destroyer",
        "Ruin Grader",
        "Ruin Guard",
        "Ruin Hunter",
        "Ruin Scout",
        "Signora",
        "Tartaglia",
        "Thunder Manifestation"
    ]
    bestMatch=""
    bestRatio=0
    enemyTarget=enemyTarget.lower()
    for enemy in mobList:
        ratio=SequenceMatcher(a=enemy.lower(),b=enemyTarget).ratio()
        if(ratio>bestRatio and ratio>0.7):
            bestMatch=enemy
            bestRatio=ratio
    if(len(bestMatch)==0):
        print("Unrecognized Name")
        print(enemyTarget)
        quit()
    return bestMatch
# returns expected level as integer of given overworld mob
def processOverworldMobLevel(enemyTarget):
    other={
        'Andrius':90,
        'Azhdaha':90,
        'Masanori':90,
        'Childe':90,
        'Electrohammer Vanguard':90,
        'Mitachurl':91,
        'Ruin Guard': 94
    }
    if(enemyTarget in other):
        return other[enemyTarget]
    
    worldBoss=[#lv 93s
        'Anemo Hypostasis',
        'Cryo Hypostasis',
        'Cryo Regisvine',
        'Electro Hypostasis',
        'Geo Hypostasis',
        'Golden Wolflord',
        'Hydro Hypostasis',
        'Maguu Kenki',
        'Oceanid',
        'Perpetual Mechanical Array',
        'Primo Geovishap',
        'Pyro Hypostasis',
        'Pyro Regisvine',
        'Thunder Manifestation'
    ]
    if(enemyTarget in worldBoss):
        return 93
    print("enemy not found")
    print(enemyTarget)
    quit()

# returns validated ability used as string
def processAbilityUsed(notes):
    if(type(notes)!=str):
        #if nothing, assume Elemental burst
        return "Elemental Burst"
    notes= notes.lower()
    AbilityList=[
        "Normal Attack",
        "Charged Attack",
        "Plunge Attack",
        "Elemental Skill",
        "Elemental Burst",
        "A1 Talent",
        "A4 talent"
    ]
    for abilities in AbilityList:
        if(abilities.lower() in notes):
            return abilities
    if("charge" in notes):
        return "Charged Attack"
    if("plunge" in notes):
        return "Plunge Attack"
    if("skill" in notes):
        return "Elemental Skill"
    if("burst" in notes):
        return "Elemental Burst"
    
    
    #exiting loop, ability not found
    print("Ability not found")
    print(notes.lower())
    quit()

# returns validated boolean of mob is stunned/ downed
def processIsMobStunned(notes):
    if(type(notes)!=str):
        return False
    notes=notes.lower()
    if("stun" in notes or "down" in notes):
        return True
    return False

# returns validated boolean of food being used
def processFoodUsed(notes):
    if(type(notes)!=str):
        return False
    if("Food".lower() in notes.lower()):
        return True
    return False

# returns validated gameVersion as string
def processGameVersion(gameVersion):
    gameVersion = gameVersion.strip()
    
    nameMapping = {
        "2.4": "2.4",
        "2,4": "2.4",
        "2.3": "2.3",
        "2,3": "2.3",
        "2.2": "2.3",
        "2,2": "2.2",
        "2.1": "2.1",
        "2.0": "2.0",
         "2" : "2.0",
         "2.": "2.0",
        "1.6": "1.6",
        "1.5": "1.5"
    }

    version = nameMapping[gameVersion]
    if(version == None):
        print ("Unrecognized GameVersion Detected")
        print (gameVersion)
        quit()
    
    return version

# return validated region as string
def processRegion(region):
    region = region.strip()
    
    regionList = {
        "China": "China",
        "America": "America",
        "Europe": "Europe",
        "Asia": "Asia",
        "TW/HK/MO": "TW/HK/MO"
    }

    newName = regionList.get(region)
    if(newName == None):
        print ("Unrecognized Region Detected")
        print (region)
        quit()
    
    return newName
       
# Takes a dataframe, and an abyss floor
# returns df of abyss submissions
