import F5_ms

msF5 = F5_ms.F5_microservice()

odc = "172.17.1."
apd = "172.18.2."

print ("Met deze tool kan je in 1 keer alle Exchange poolmembers in Rijswijk of Apeldoorn tegelijk enablen of disablen.")
print ("Controleer vooraf de huidige status. Deze tool doet dat niet. Het is dus mogelijk om hiermee alle exchange servers te disablen.")
print ("\n")

dcKeuze = "999"

while dcKeuze not in ['A','O']:
    dcKeuze = input("Wil je de nodes in het (O)DC bewerken, of die in (A)peldoorn?")

statusKeuze = "999"
while statusKeuze not in ['A','U']:
    statusKeuze = input("Wil je de nodes (A)an of (U)itzetten)?")

if dcKeuze == "A" :
    serverSubnet = apd
else :
    serverSubnet = odc

poolMembers = msF5.get_poolmembers("dev-adc01.koene.tld", "SSCICT~exch_test", "exch_test_pool")

for member in poolMembers['items'] :
    print (member['address'])

