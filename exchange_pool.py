import F5_ms

msF5 = F5_ms.F5_microservice()

odc = "172.17.1."
apd = "172.18.2."
odcMember ={}
apdMember ={}

print ("Met deze tool kan je in 1 keer alle Exchange poolmembers in Rijswijk of Apeldoorn tegelijk enablen of disablen.")
print ("Controleer vooraf de huidige status. Deze tool doet dat niet. Het is dus mogelijk om hiermee alle exchange servers te disablen.")
print ("\n")

poolMembers = msF5.get_poolmembers("dev-adc01.koene.tld",
                                   "SSCICT~exch_test",
                                   "exch_test_pool")

dcKeuze = ""
while dcKeuze not in ['A','O']:
    dcKeuze = str.upper(input("Wil je de nodes in het (O)DC bewerken, of die in (A)peldoorn? "))

statusKeuze = ""
while statusKeuze not in ['A','U']:
    statusKeuze = str.upper(input("Wil je de nodes (A)an of (U)itzetten)? "))

if dcKeuze == "A" :
    serverSubnet = apd
else :
    serverSubnet = odc

poolMembers = msF5.get_poolmembers("dev-adc01.koene.tld",
                                   "SSCICT~exch_test",
                                   "exch_test_pool")

for member in poolMembers['items'] :
    if str(member['address']).startswith(serverSubnet):
        msF5.set_poolmember_disabled_by_name("dev-adc01.koene.tld",
                                             "SSCICT~exch_test",
                                             "exch_test_pool",
                                             member['name'],
                                             statusKeuze == "U")

poolMembers = msF5.get_poolmembers("dev-adc01.koene.tld",
                                   "SSCICT~exch_test",
                                   "exch_test_pool")
for member in poolMembers['items'] :
    print (member['name'] + ' - ' + member['address'] + ' - ' + member['session'])
