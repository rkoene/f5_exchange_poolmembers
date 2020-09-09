# Import F5 miscroservice
import F5_ms

def memberStatus():
    # Init status dicts
    odcStatus = {"Aan":0, "Uit":0, "Up":0, "Down":0}
    apdStatus = {"Aan":0, "Uit":0, "Up":0, "Down":0}

    # Uitvragen huidige status van de poolmembers
    poolMembers = msF5.get_poolmembers("dev-adc01.koene.tld",
                                       "SSCICT~exch_test",
                                       "exch_test_pool")
    for member in poolMembers['items'] :
        if str(member['address']).startswith(dictSubnets["O"]):
            if member['session'] == "user-disabled" : odcStatus["Uit"] += 1
            else : odcStatus["Aan"] += 1
            if member['state'] == "down": odcStatus["Down"] += 1
            else : odcStatus["Up"] += 1
        elif str(member['address']).startswith(dictSubnets["A"]):
            if member['session'] == "user-disabled" : apdStatus["Uit"] += 1
            else : apdStatus["Aan"] += 1
            if member['state'] == "down": apdStatus["Down"] += 1
            else : apdStatus["Up"] += 1

    print ("Huidige status poolmembers:")
    print ("+--------------------------------------------+")
    print ("| ODC                                        |")
    print ("+-----------+----------+----------+----------+")
    print (str("|  Aan : {:2d} | Uit : {:2d} | Up : {:2d} | Down : {:2d} |").format(odcStatus["Aan"],odcStatus["Uit"],odcStatus["Up"],odcStatus["Down"]))
    print ("+-----------+----------+----------+----------+")
    print ("| APD                                        |")
    print ("+-----------+----------+----------+----------+")
    print (str("|  Aan : {:2d} | Uit : {:2d} | Up : {:2d} | Down : {:2d} |").format(apdStatus["Aan"],apdStatus["Uit"],apdStatus["Up"],apdStatus["Down"]))
    print ("+-----------+----------+----------+----------+")

# Aanmaken F5 microservice object
msF5 = F5_ms.F5_microservice()

# Vul datacenter subnets voor Exchange servers
odc = "172.17.1."
apd = "172.18.2."
dictSubnets = {"O":odc, "A":apd}

# Tonen doel van het script
print ("\n")
print ("\n")
print ("Met deze tool kan je in 1 keer alle Exchange poolmembers in Rijswijk of Apeldoorn tegelijk enablen of disablen.")
print ("Controleer vooraf de huidige status. Deze tool doet dat niet. Het is dus mogelijk om hiermee alle exchange servers te disablen.")
print ("Menu keuze Q stopt het script.")
print ("\n")

memberStatus()

# Menu voor het uitvragen van de keuze
dcKeuze = ""
while dcKeuze not in ['A','O','Q']:
    dcKeuze = str.upper(input("Wil je de nodes in het (O)DC bewerken, of die in (A)peldoorn? "))
if dcKeuze == 'Q': exit(0)

statusKeuze = ""
while statusKeuze not in ['A','U','Q']:
    statusKeuze = str.upper(input("Wil je de nodes (A)an of (U)itzetten)? "))
if statusKeuze =='Q': exit(0)

# Aan/uit schakelen van de betreffende poolmembers
poolMembers = msF5.get_poolmembers("dev-adc01.koene.tld",
                                   "SSCICT~exch_test",
                                   "exch_test_pool")
for member in poolMembers['items'] :
    if str(member['address']).startswith(dictSubnets[dcKeuze]):
        msF5.set_poolmember_disabled_by_name("dev-adc01.koene.tld",
                                             "SSCICT~exch_test",
                                             "exch_test_pool",
                                             member['name'],
                                             statusKeuze == "U")

# Uitvragen en tonen van de nieuwe status
memberStatus()

# Einde script