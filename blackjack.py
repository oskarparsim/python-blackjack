#Autorid: Oskar Pärsim ja Ruud Tammel
#Hasartmäng blackjack. Mängu eesmärk on mängijal hoida iga vooru lõpus kaarte,
#mille summa on suurem kui diileril, kuid väiksem või võrdne summaga 21.
#Esijalgu jagatakse mängijale ja diilerile kaks kaarti, ning seejärel on mängijal
#võimalik valida kas võtta kaarte juurde või mitte.
#Diiler kaarte juurde ei võta kuniks mängija on oma valikud ära teinud.
#Reeglitest lähemalt: https://pastebin.com/wZyAmMFn
    
    #Vajalikud moodulid
from easygui import *
from random import *

    #Avab kaardipaki failist ja paneb nad järjendisse
kaardifail = open("kaardid.txt", encoding="UTF-8")
kaardid = []
uuspakk = []
    
    #Lisab kaardid failist järjendisse
for kaart in kaardifail:
    kaardid.append(kaart.strip())
    uuspakk.append(kaart.strip())
kaardifail.close()

    #Kasutaja saab sisestada oma sissemakse
saldo = integerbox("Sisestage enda sissemakse eurodes (maksimaalne sissemakse on 10 000 eurot): ", "SALDO", upperbound = 10000, lowerbound = 0)
    
    #Mis juhtub kui sissemakset ei sisestatud
if saldo is None:
    saldo = integerbox("Te ei sisestanud midagi, tehke sissemakse (maksimaalne sissemakse on 10 000 eurot)", "VIGA", upperbound = 10000, lowerbound = 0)
    
    #Laseb kasutajal valida mitu pakki kaarte mängus kasutatakse
mitupakki = integerbox("Mitme kaardipakiga soovite mängida (max 3) ", upperbound = 3, lowerbound = 1)
kaardid = mitupakki * kaardid

    #Segab kaardipaki ära
shuffle(kaardid)
    
    #Funktsioon mis annab käele numbrilised väärtused
def numval(kaart, käsi):
    for täht in kaart:
            #Kui täht on 1, siis lisab programm listi "10"
            #Ilma selle koodijupita lisaks programm listi vaid "1" ja "0" eraldi
        if täht.isdigit():
            if täht == "1":
                käsi.append(10)
            elif täht == "0":
                continue
            else:
                käsi.append(int(täht))  
            #Kui kaart on "J", "Q" või "K", annab programm kaardile väärtuse 10
        elif täht == "J" or täht == "Q" or täht == "K":
            käsi.append(10)            
            #Kui kaart on "A", siis otsustab programm, kas anda kaardile väärtus 1 või 11
        elif täht == "A":
            if sum(käsi) + 11 <= 21:
                käsi.append(11)
            else:
                käsi.append(1)

    #Funktsioon, mis määrab mis juhtub kui kasutaja valib mängus "hit"
def hit(käsi):
    käsi.append(kaardid[0])
    del kaardid[0]
    #Funktsioon, mis määrab mis juhtub kui kasutaja valib mängus "double down"
def doubledown(käsi):
    global panus
    käsi.append(kaardid[0])
    panus = panus * 2
    del kaardid[0]
 
lõppkäik = ""
panus = 0
    #Tsükkel mis otsustab, kas programm jätkab töötamist
while lõppkäik == "Jah" or lõppkäik == "":
        #Kontrollib kui palju kaarte on kaardipakis
    if len(kaardid) < 6:
        kaardidotsas = buttonbox("Kaardipakk on otsa saamas. Kas soovid uue paki võtta? (Kui valid 'ei', siis programm sulgub)", choices = ["Jah", "Ei"])
        if kaardidotsas == "Jah":
            kaardid = uuspakk
            shuffle(kaardid)
        elif kaardidotsas == "Ei":
            msgbox("Head aega!")
            exit()
    
        #Kui saldo on suurem kui 0 siis algab mäng
    if saldo > 0:
        
        if panus == 0:
               #Kasutaja sisestab panuse, millega ta mängib
            panus = integerbox(f'Teie saldo on {saldo} eurot. Palun sisestage panus, millega soovite mängida: ', "PANUS", upperbound = saldo, lowerbound = 0)        
                  
                  #Mis juhtub kui panust ei sisestatud
            if panus is None:
                panus = integerbox("Te ei sisestanud midagi, tehke uus panus", "VIGA", upperbound = saldo, lowerbound = 0)
            elif panus > saldo:
                panus = integerbox("Panus on liiga suur, tehke uus panus: ", "VIGA", upperbound = saldo, lowerbound = 0)
            elif panus <= 0:
                panus = integerbox("Panus on liiga väike, tehke uus panus: ", "VIGA", upperbound = saldo, lowerbound = 0)
            
        minu_k2si = []
        diileri_k2si = []

            #Jagab kasutajale ja diilerile 2 kaarti    
        a = 0
        while a < 2:
            minu_k2si.append(kaardid[a])
            del kaardid[a]
            a += 1
        a = 0
        while a < 2:
            diileri_k2si.append(kaardid[a])
            del kaardid[a]
            a += 1
        
        #Annab diileri ja mängija kaartidele numbrilised väärtused
        minu_k2si_int = []
        for kaart in minu_k2si:
            numval(kaart, minu_k2si_int)    
        diileri_k2si_int = []
        for kaart in diileri_k2si:
            numval(kaart, diileri_k2si_int)
        
        #Käiguvalikud
        lõppkäigud = ["Jah", "Ei"]
        
            #Otsustab esimeste jagatud kaartide põhjal kas on mõtet edasi mängida. Näiteks kui mängija saab kohe blackjacki on ta võitnud ning pole mõtet edasi mängida
        y = 0
        x = 0
        while x < 1:
            if sum(diileri_k2si_int) == 21 and sum(minu_k2si_int) == 21:
                lõppkäik = buttonbox("Nii diileril kui sul on käes 21. Saad oma raha tagasi. \n Saldo: " + str(saldo) + "\n Kas soovite uuesti mängida?", choices = lõppkäigud) 
                y += 1
                panus = integerbox(f'Teie saldo on {saldo} eurot. Palun sisestage panus, millega soovite mängida: ', "PANUS", upperbound = saldo, lowerbound = 0)
                
            elif sum(minu_k2si_int) == 21:
                saldo += 1.5 * panus
                lõppkäik = buttonbox("Blackjack! Teie võit! \n Saldo: " + str(saldo) + "\n Kas soovite uuesti mängida?", choices = lõppkäigud)
                y += 1
                panus = integerbox(f'Teie saldo on {saldo} eurot. Palun sisestage panus, millega soovite mängida: ', "PANUS", upperbound = saldo, lowerbound = 0)
                
            elif sum(diileri_k2si_int) == 21:
                saldo -= panus
                lõppkäik = buttonbox(f'Diiler sai blackjacki! Sa kaotasid! \n Sinu saldo: {str(saldo)} \n Kas soovite uuesti mängida?', choices = lõppkäigud)
                y += 1
                panus = integerbox(f'Teie saldo on {saldo} eurot. Palun sisestage panus, millega soovite mängida: ', "PANUS", upperbound = saldo, lowerbound = 0)
                
            x += 1
            #Tingimused, olenevalt kasutaja valitud käigust
            k2igud = ["Hit", "Double Down", "Stand"]
            
            z = 0
        while sum(minu_k2si_int) < 21:
            k2ik = buttonbox("Diileri käsi: " + diileri_k2si[0] + ", ***" + "\n" + "Teie käsi: " + str(minu_k2si) + " | Kokku: " + str(sum(minu_k2si_int)) + "\n" + "Panus: " + str(panus) + "\n" + "Saldo: " + str(saldo) + "\n" + "Mis on teie järgmine käik?", "Käik", choices = k2igud)
            if k2ik == "Hit" or k2ik == "Double Down" or k2ik == "Stand":
                    #Kui kasutaja valib hit, annab programm talle ühe kaardi juurde
                if k2ik == "Hit":
                    hit(minu_k2si)
                    numval(minu_k2si[len(minu_k2si)-1], minu_k2si_int)
                    #Kui kasutaja valib double down, kahekordistab programm kasutaja panuse ning annab talle ainult ühe kaardi juurde ning enne
                    # järgmist roundi pole võimalik käike valida
                elif k2ik == "Double Down":
                    doubledown(minu_k2si)
                    numval(minu_k2si[len(minu_k2si)-1], minu_k2si_int)
                    break
                    #Kui kasutaja valib stand, hakkab diiler endale kaarte juurde võtma kuni ta kaartide väärtus ületab 17
                elif k2ik == "Stand":
                    while sum(diileri_k2si_int) < 17:
                        vaheaeg = buttonbox(f'Diileri käsi: {diileri_k2si} \n Kokku: {sum(diileri_k2si_int)}', choices = ["Edasi"])
                        hit(diileri_k2si)
                        numval(diileri_k2si[len(diileri_k2si)-1], diileri_k2si_int)
                    vaheaeg = buttonbox(f'Diileri käsi: {diileri_k2si} \n Kokku: {sum(diileri_k2si_int)}', choices = ["Edasi"])
                    break
            #Eemaldab peale esimest käiku kasutajalt võimaluse valida "Double Down"
            while z == 0:
                k2igud.pop(1)
                z += 1
                
            #Kontrollib võidutingimusi, kui mängu alguses pole keegi blackjacki saanud
        if y == 0:
            if sum(minu_k2si_int) <= 21 and sum(diileri_k2si_int) < sum(minu_k2si_int):
                saldo += panus
                lõppkäik = buttonbox(f'Võit! Sinu käsi oli suurema väärtusega kui diileril! \n Sinu kaardid: {minu_k2si} | Kokku : {sum(minu_k2si_int)} \n Diileri kaardid: {diileri_k2si} | Kokku : {sum(diileri_k2si_int)} \n Sinu saldo: {str(saldo)} \n Kas soovite uuesti mängida?', choices = lõppkäigud)
                panus = 0

            elif sum(diileri_k2si_int) > 21:
                saldo += panus
                lõppkäik = buttonbox(f'Diiler bustis! \n Sinu kaardid: {minu_k2si} | Kokku : {sum(minu_k2si_int)} \n Diileri kaardid: {diileri_k2si} | Kokku : {sum(diileri_k2si_int)} \n Sinu saldo: {str(saldo)} \n Kas soovite uuesti mängida?', choices = lõppkäigud)
                panus = 0
            
            elif sum(diileri_k2si_int) > sum(minu_k2si_int) and sum(diileri_k2si_int) <= 21:
                saldo -= panus
                lõppkäik = buttonbox(f'Diileri käsi on suurema väärtusega, sa kaotasid! \n Sinu kaardid: {minu_k2si} | Kokku : {sum(minu_k2si_int)} \n Diileri kaardid: {diileri_k2si} | Kokku : {sum(diileri_k2si_int)} \n Sinu saldo: {str(saldo)} \n Kas soovite uuesti mängida?', choices = lõppkäigud)
                panus = 0
              
            elif sum(diileri_k2si_int) == sum(minu_k2si_int) and sum(diileri_k2si_int) <= 21 and sum(minu_k2si_int) <= 21:
                panus = 0
                lõppkäik = buttonbox(f'Sinu ja diileri käsi on võrdsed, saad oma panuse tagasi! \n Sinu kaardid: {minu_k2si} | Kokku : {sum(minu_k2si_int)} \n Diileri kaardid: {diileri_k2si} | Kokku : {sum(diileri_k2si_int)} \n Sinu saldo: {str(saldo)}\n Kas soovite uuesti mängida?', choices = lõppkäigud)

            elif sum(minu_k2si_int) > 21:
                saldo -= panus
                lõppkäik = buttonbox(f'Sa kaotasid! Summa ületas arvu 21. \n Sinu kaardid: {minu_k2si} | Kokku : {sum(minu_k2si_int)} \n Diileri kaardid: {diileri_k2si} | Kokku : {sum(diileri_k2si_int)} \n Sinu saldo:  {str(saldo)} \n Kas soovite uuesti mängida?', choices = lõppkäigud)
                panus = 0
        #Kui saldo on 0 pole võimalik endam edasi mängida
    else:
        msgbox(f'Su saldo on liiga väike, mängisid ennast vaeseks! :) \n Programm sulgub')
        exit()
    #Kui kasutaja vastab küsimusele "Kas soovid edasi mängida?" ei, siis programm sulgub
if lõppkäik == "Ei":
    exit()