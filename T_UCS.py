import time
import copy
import sys
import argparse
import os

class NodParcurgere:
    gr = None # ma ajuta la testarea timpului de timeout

    def __init__(self, info, parinte, cost=0, infoDrum=[]):
        """
        Constructor

        :param info: lista de forma [[id, capacitate, cantitate, culoare], ..]
        :param parinte: parintele din arborele de parcurgere
        :param cost: costul drumului pana la nodul curent
        :param infoDrum: lista [vasul1, vasul2, culoare, litrii_turnati]
        """
        # testez timpul de timeout
        gr.depasire_timeout()

        self.info = info
        self.parinte = parinte
        self.g = cost
        self.infoDrum = infoDrum

    def obtineDrum(self):
        # testez timpul de timeout
        gr.depasire_timeout()

        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def initial_egal_final(self, stare_finala):
        """
        Metoda care verifica daca starea finala se gaseste in nodul de start.

        :param stare_finala: configuratia scop

        :return: True/False
        """
        # testez timpul de timeout
        gr.depasire_timeout()

        for (cantitate, culoare) in stare_finala:
            gasit = False
            for (i, cap, cant, cul) in self.info: # informatia nodului initial
                if cant == cantitate and cul == culoare:
                    gasit = True
                    break
            if gasit == False:
                return False
        return True

    def afisDrum(self, afisCost=False, afisLung=False):
        """
        Metoda pentru afisarea drumului in formatul dorit

        :param afisCost: daca se doreste si afisarea costului
        :param afisLung: daca se doreste si afisarea lungimii (nr de noduri)

        :return: lungimea drumului (nr de noduri)
        """
        # testez timpul de timeout
        gr.depasire_timeout()

        str=""
        l = self.obtineDrum()

        for nod in l:
            infoDrum = nod.infoDrum  # [vasul1, vasul2, culoare, litrii_turnati]
            if nod.parinte is not None and infoDrum!=[]:
                str += "Din vasul {} s-au turnat {} litri de apa de culoare {} in vasul {}.".format(infoDrum[0], infoDrum[3], infoDrum[2], infoDrum[1]) +"\n"
                str += nod.__str__()+"\n"

        if afisCost:
            str += "Cost drum: "+ (self.g).__str__() +"\n"
        if afisLung:
            str += "Lungime drum: "+ len(l).__str__() +"\n"
        return str

    def contineInDrum(self, infoNodNou):
        """
        Metoda care verifica daca informatia unui nod se afla in drumul generat pana la ea.
        Testeaza sa nu existe deja in drum aceeasi configuratie de vase indiferent de capacitatea lor.
        Sortare dupa cantitate

        :param infoNodNou: informatia nodului de testat

        :return: True/ False
        """
        # testez timpul de timeout
        gr.depasire_timeout()

        nodDrum = self

        infoNou = sorted(infoNodNou, key=lambda t: t[2])
        while nodDrum is not None:
            infoParinte = sorted(nodDrum.info, key=lambda t: t[2])
            l1 = []
            l2 = []
            for vas in infoNou:
                l1.append(vas[2:])
            for vas in infoParinte:
                l2.append(vas[2:])
            if l1 == l2:
                return True
            nodDrum = nodDrum.parinte
        return False

    def __str__(self):
        """
        Metoda care stilizeaza afisarea unui nod.
        La lipsa de lichid dintr-un vas nu se va afisa nicio culoare

        :return: returneaza sirul pentru afisarea unui nod
        """
        # testez timpul de timeout
        gr.depasire_timeout()

        sir=""
        for vas in self.info:
            sir +=str(vas[0])+": "
            sir += str(vas[1]) + " " + str(vas[2]) + " "
            if vas[3]==None:
                if vas[2] !=0:
                    sir+="nedefinita"
            elif vas[2]!=0:
                sir+=vas[3]
            sir+="\n"
        return sir

    def __repr__(self):
        """
        Metoda utilizata pentru debugging

        :return: sirul de afisat
        """

        sir = "info= " +str(self.info)+"\n"
        if self.parinte != None:
            sir+= "parinte= " +str(self.parinte.info)+"\n"
        else:
            sir += "parinte= None\n"
        sir += "cost= " + str(self.g) + "\n"
        sir += "infoDrum= " + str(self.infoDrum) + "\n"
        return sir

class Graph:
    def __init__(self, nume_fisier_intrare, cale_folder_ouput, nume_fisier_iesire, timeout ):
        """
        Constructor
        Citeste datele din fisierul de intrare si initializeaza datele membre

        self.start: informatia nodului de start [[id_vas, capacitate, cantitate, culoare]..]
        self.culori: combinatiile de culori [(c1,c2,c3)..]
        self.cost: costul culorilor {c1:cost1, c2:cost2..}
        self.scopuri: starea finala [(cantitate, culoare)..]
        self.t1: timpul de incepere al programului
        self.output: fisierul de output
        self.timeout: timpul de timeout

        :param nume_fisier_intrare: calea + numele fisierului de intrare
        :param cale_folder_ouput: cale folder output
        :param nume_fisier_iesire: numele fisierului de iesire
        :param timeout: timpul de timeout pentru verificare constanta
        """

        self.timeout = timeout
        self.t1 = time.time()
        self.output = open(cale_folder_ouput + "\\" + nume_fisier_iesire, "w")

        # testez timpul de timeout
        self.depasire_timeout()

        try:
            f = open(nume_fisier_intrare, "r")
        except:
            print("Eroare la deschiderea fisierului!", file=self.output)
            sys.exit(0)

        try:
            textFisier = f.read()

            text1 = textFisier.strip().split("stare_initiala")
            text2 = text1[1].strip().split("stare_finala")
            p1 = text1[0].strip().split('\n')
            p2 = text2[0].strip().split('\n')
            p3 = text2[1].strip().split('\n')

            combinatii_culori = []
            cost_culori = {}
            for line in p1:
                v = line.split()
                if len(v) == 3:
                    combinatii_culori.append((v[0], v[1], v[2]))
                elif len(v) == 2:
                    cost_culori[v[0]] = int(v[1])

            stare_initiala = []
            for id in range(len(p2)):
                line = p2[id]
                v = line.split()
                if len(v) == 3:
                    stare_initiala.append([id, int(v[0]), int(v[1]), v[2]])
                    # verific daca culoarea data se gaseste printre culorile puse
                    if v[2] not in cost_culori.keys():
                        raise Exception
                elif len(v) == 2:
                    stare_initiala.append([id, int(v[0]), 0, None])

            stare_finala = []
            for id in range(len(p3)):
                line = p3[id]
                v = line.split()
                stare_finala.append((int(v[0]), v[1]))
                # verific daca culoarea data se gaseste printre culorile puse
                if v[1] not in cost_culori.keys():
                    raise Exception

            self.start = stare_initiala  # informatia nodului de start
            self.culori = combinatii_culori
            self.cost = cost_culori
            self.scopuri = stare_finala
        except:
            print("Eroare la parsarea fisierului!", file=self.output)
            sys.exit(0)

    def depasire_timeout(self):
        """
        Metoda care verifica daca a fost depasit timpul de timeout.
        In caz afirmativ, opreste programul definitiv.
        """
        t2 = time.time()
        milis = round(1000 * (t2 - self.t1))
        if milis > self.timeout:
            print("Solutia a depasit timpul dat", file=self.output)
            sys.exit(0)

    def testeaza_scop(self, InfonodCurent):
        # testez timpul de timeout
        self.depasire_timeout()

        ok=0
        for (cantitate, culoare) in self.scopuri:
            for vas in InfonodCurent:
                if vas[-1]== culoare and vas[-2]==cantitate:
                    ok+=1
                    break

        if ok==len(self.scopuri):
            return True
        return False

    def testeaza_nod_de_exapandat(self, infoNod):
        """
        Metoda care testeaza daca un nod are potentialul ca prin expandare sa ajunga la o solutie.
        Formez un set cu culorile care se combina ca sa evit duplicatele.

        :param infoNod: informatia nodului

        :return: True/False
        """
        # testez timpul de timeout
        self.depasire_timeout()

        culori_scop=0
        culori_de_combinat=0
        set_culori_de_combinat=set()

        for (c1, c2, c3) in self.culori:
            set_culori_de_combinat.add(c1)
            set_culori_de_combinat.add(c2)

        for culoare in set_culori_de_combinat:
            for vas in infoNod:
                if vas[3]==culoare:
                    culori_de_combinat += 1

        for (c1, c2, c3) in self.culori:
            for vas in infoNod:
                culoare =vas[3]
                if c3 == culoare:
                    culori_scop +=1
                    break
        # verific sa nu am cantitatea data mai mare ca si capacitatea data
        for (cantitate, culoare) in self.scopuri:
            nr=0
            for (id, cap, cant, cul) in infoNod:
                if cantitate > cap:
                    nr+=1
            if nr==len(infoNod):
                return False

        # verificari referitoare la culori
        if culori_de_combinat == 0 and culori_scop == len(self.culori):
            # nu am nicio culoare rezultata prin combinare
            # dar am toate culorile care merg combinate
            return True
        elif culori_de_combinat >=2 and culori_scop ==0:
            # presupun ca am minim 2 culori din care pot sa obtin o noua culoare prin combinare
            # dar nu am nicio culoare care merge combinata
            return True
        elif culori_de_combinat !=0 and culori_scop !=0:
            # am din fiecare tip de culoare
            return True
        return False

    def genereazaSuccesori(self, nodCurent):
        """
        Metoda care genereaza toti succesorii posibili nodului curent.
        Fiecare nod generat este verificat daca a mai fost deja generat si
        daca are potential de a ajunge la o solutie.

        :param nodCurent: nodul caruia i se vor genera succesorii

        :return: lista succesorilor nodului primit ca parametru
        """
        listaSuccesori = []

        for i in range(len(nodCurent.info)):
            # testez timpul de timeout
            self.depasire_timeout()

            # copieVase o sa reprezinte o configurare
            # nodCurent.info[i] = un vas

            # daca vasul este vid
            if len(nodCurent.info[i]) == 0:
                continue

            # iterez prin toate vasele diferite de cel curent
            for j in range(len(nodCurent.info)):

                if i == j:  # sa nu fie vasul din care torn
                    continue

                infoDrum=[]
                infoNodNou = copy.deepcopy(nodCurent.info)
                VAS1 = copy.deepcopy(nodCurent.info[i])
                VAS2 = copy.deepcopy(nodCurent.info[j])

                infoDrum.append(VAS1[0])
                infoDrum.append(VAS2[0])

                '''
                2 cazuri: 
                    1. golesc vasul1
                    2. umplu vasul 2
                '''
                # cat ar mai avea de adaugat pana face capacitatea maxima:
                # capacitate_VAS2 - lichid_VAS2
                # (umple VAS2, altfel golesete VAS1)
                # lichid_de_transferat = capacitate_VAS2 - lichid_VAS2

                lichid_de_transferat = VAS2[1] - VAS2[2]
                costMutare = 0
                if lichid_de_transferat!=0:
                    # -----------------Schimbare culoare + calcul cost mutare--------------------
                    # daca vasul e gol pentru culoare:
                    if VAS2[2]==0:
                        VAS2[3] = VAS1[3]
                        infoDrum.append(VAS1[3])
                        if  VAS1[3] in self.cost.keys():
                            costMutare += lichid_de_transferat * self.cost.get(VAS1[3])

                        if costMutare==0: # torn culoare nedefinita
                            costMutare += lichid_de_transferat # cost=1
                    else:
                        # setare culoare pentru vas care nu e gol
                        ok = False
                        if VAS1[3] == VAS2[3] and VAS1[3]!=None:
                            infoDrum.append(VAS1[3])
                            if VAS1[3] in self.cost.keys():
                                costMutare += lichid_de_transferat * self.cost.get(VAS1[3])
                        else:
                            for (c1,c2,c3) in self.culori:
                                #c1+c2==c2+c1==c3
                                if (VAS2[3] == c1 and VAS1[3] == c2) or (VAS2[3] == c2 and VAS1[3] == c1):
                                    VAS2[3] = c3
                                    ok = True
                                    break
                            if ok == True:
                                infoDrum.append(VAS1[3])
                                if VAS1[3] in self.cost.keys():
                                        costMutare += lichid_de_transferat * self.cost.get(VAS1[3])

                        if ok == False and VAS1[2]>0:
                            # nu este definita combinatia de culori

                            # rezultat culoare nedefinita
                            # costul va fi suma
                            cost1=0
                            cost2=0
                            if VAS1[3] in self.cost.keys():
                                cost1= lichid_de_transferat * self.cost.get(VAS1[3])

                            if VAS2[3] in self.cost.keys():
                                    cost2= VAS2[2] * self.cost.get(VAS2[3])

                            if cost1 == 0:  # torn culoare nedefinita
                                infoDrum.append('nedefinita')
                                costMutare += lichid_de_transferat  # cost=1
                            elif cost2 == 0:  # torn culoare nedefinita
                                infoDrum.append('nedefinita')
                                costMutare += VAS2[2]  # cost=1
                            else:
                                infoDrum.append(VAS1[3])
                                costMutare+= cost1+ cost2
                            VAS2[3] = None
                    # -----------------Sfarsit schimbare culoare--------------------

                    #-----------------Schimbare cantitate lichid---------------------
                    if lichid_de_transferat <= VAS1[2] :
                        VAS1[2] -= lichid_de_transferat
                        # setez lichidul pentru VAS2
                        VAS2[2] += lichid_de_transferat
                        infoDrum.append(lichid_de_transferat)
                    else:
                        # daca e mai mare il golesc pe cel din care torn
                        VAS2[2] += VAS1[2]
                        infoDrum.append(VAS1[2])
                        VAS1[2] = 0
                    # -----------------sfarsit schimbare cantitate lichid---------------------
                if VAS2[2] == 0:
                    VAS2[3] = None
                if VAS1[2] == 0:
                    VAS1[3] = None
                infoNodNou[j][2] = copy.deepcopy(VAS2[2])
                infoNodNou[j][3] = copy.deepcopy(VAS2[3])
                infoNodNou[i][2] = copy.deepcopy(VAS1[2])
                infoNodNou[i][3] = copy.deepcopy(VAS1[3])

                if (not nodCurent.contineInDrum(infoNodNou)) and self.testeaza_nod_de_exapandat(infoNodNou):
                    # verific daca a mai fost deja pus in drum
                    # testez daca merita expandat (nodul nu are solutie)
                    listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costMutare, infoDrum))
        return listaSuccesori

    def __repr__(self):
        """
        Metoda utilitara pentru debugging.

        :return: sir de afisat
        """
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir

def afis_suplimentar(nr_max_noduri_in_memorie, nr_total_noduri_calculate ):
    print("Numarul maxim de noduri existente la un moment dat in memorie: ", nr_max_noduri_in_memorie, file=gr.output)
    print("Totalul de succesori generati: ", nr_total_noduri_calculate, file=gr.output)

def uniform_cost(gr, nrSolutiiCautate=1):

    print("##### Solutii obtinute cu UCS #####\n", file= gr.output)


    nr_max_noduri_in_memorie = 1 # plec de la primul nod
    nr_total_noduri_calculate = 1 # plec de la primul nod

    gasitSolutie = False

    c = [NodParcurgere(gr.start, None, 0, [])]


    print("***Starea initiala***\n", c[0], file= gr.output)

    print("*********************", file= gr.output)


    if c[0].initial_egal_final(gr.scopuri) == True:
        print("!! Starea initiala coincide cu cea finala !!\n", file=gr.output)
        t2 = time.time()
        milis = round(1000 * (t2 - gr.t1))
        print("Timpul scurs de la inceputul programului: ", milis, "milisecunde", file=gr.output)
        afis_suplimentar(nr_max_noduri_in_memorie, nr_total_noduri_calculate)
        return

    if gr.testeaza_nod_de_exapandat(c[0].info) == False:
        print("!! Input fara solutie !!\n", file=gr.output)
        t2 = time.time()
        milis = round(1000 * (t2 - gr.t1))
        print("Timpul scurs de la inceputul programului: ", milis, "milisecunde", file=gr.output)
        afis_suplimentar(nr_max_noduri_in_memorie, nr_total_noduri_calculate)
        return

    while len(c) > 0:
        gr.depasire_timeout()

        if nr_max_noduri_in_memorie < len(c):
            nr_max_noduri_in_memorie = len(c)

        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent.info):

            print("\n-------->Solutie<--------", file= gr.output)
            gasitSolutie = True

            print(nodCurent.afisDrum(afisCost=True, afisLung=True), file= gr.output)

            gr.depasire_timeout()

            t2 = time.time()
            milis = round(1000 * (t2 - gr.t1))
            print("Timpul scurs de la inceputul programului: ", milis, "milisecunde", file=  gr.output)
            afis_suplimentar(nr_max_noduri_in_memorie, nr_total_noduri_calculate)

            print("----------------", file=  gr.output)

            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return

        lSuccesori = gr.genereazaSuccesori(nodCurent)
        nr_total_noduri_calculate += len(lSuccesori)

        gr.depasire_timeout()

        for s in lSuccesori:  # parcurg succesorii
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # ordonez dupa cost coada
                # daca elementul din coada are costul mai mare decat succesorul
                if c[i].g > s.g:  # g e costul total de la start pana la nodul curent
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)  # inserez pe pozitia i
                                # (cea pe care imi ramane ordinea)
            else:
                c.append(s)  # inserez la finalul cozii

    gr.depasire_timeout()

    if gasitSolutie == False:
        print("!! Input fara solutie !!\n", file= gr.output)
        t2 = time.time()
        milis = round(1000 * (t2 - gr.t1))
        print("Timpul scurs de la inceputul programului: ", milis, "milisecunde", file=gr.output)
        afis_suplimentar(nr_max_noduri_in_memorie, nr_total_noduri_calculate)

    elif nrSolutiiCautate > 0 : # daca nrSolutiiCautate > nrSolutiiGasite
        print("Nu mai sunt alte solutii :( ", file=gr.output)
        print("----------------\n", file=gr.output)


    # inchid fisierul de iesire
    gr.output.close()

def citire_linie_de_comanda():

    """
     1. calea catre folderul cu fisiere de input
     2. calea pentru folderul de output
     3. NSOL
     4. Timpul de timeout

    Obtin o lista cu numele fișierelor de input.
    Creez fisiere de output pentru fiecare fisier de input.

    """
    global gr

    # ---------Citirea cu argumente-------
    ap = argparse.ArgumentParser()
    # required=True => argumente obligatorii
    ap.add_argument("-i", "--i", required=True, help="cale folder cu fisiere de input")
    ap.add_argument("-o", "--o", required=True, help="cale folder cu fisiere de output")
    ap.add_argument("-n", "--n", required=True, help="nurmarul de solutii dorite")
    ap.add_argument("-t", "--t", required=True, help="valoarea de timeout in milisecunde")

    argumente = vars(ap.parse_args())
    cale_folder_input = argumente['i']
    cale_folder_ouput = argumente['o']
    NSOL = int(argumente['n'])
    timeout = int(argumente['t'])

    # ---------Sfarsit citire argumente-----------

    listaFisiereIntrare = os.listdir(cale_folder_input)


    # verific daca nu există folderul folder_output, caz în care îl creez
    if not os.path.exists(cale_folder_ouput):
        os.mkdir(cale_folder_ouput)

    for nume_fisier_intrare in listaFisiereIntrare:
        nume_intreg = cale_folder_input + "\\" + nume_fisier_intrare
        nume_fisier_iesire = "output_" + nume_fisier_intrare.split(".")[0]

        # ----prelucrare fisier de input ---------#
        gr = Graph(nume_intreg, cale_folder_ouput, nume_fisier_iesire, timeout)
        NodParcurgere.gr = gr
        uniform_cost(gr, nrSolutiiCautate=NSOL)


citire_linie_de_comanda()



