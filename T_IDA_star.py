import time
import copy
import sys


class NodParcurgere:
    gr = None  # trebuie setat sa contina instanta problemei

    def __init__(self, info, parinte, cost=0, h=0, infoDrum=[]):
        self.info = info  # lista de forma [[id, capacitate, cantitate, culoare], ..]
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost
        self.h = h
        self.f = self.g + self.h
        self.infoDrum = infoDrum  # lista [vasul1, vasul2, culoare, litrii_turnati]

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        stareai_nu_coincide_streaf = False
        for nod in l:
            infoDrum = nod.infoDrum  # [vasul1, vasul2, culoare, litrii_turnati]
            if nod.parinte is not None and infoDrum != []:
                print("Din vasul {} s-au turnat {} litri de apa de culoare {} in vasul {}.".
                      format(infoDrum[0], infoDrum[3], infoDrum[2], infoDrum[1]))
                print(str(nod))
                stareai_nu_coincide_streaf = True

        if stareai_nu_coincide_streaf == False:
            print(l[0])
            print("Starea initiala coincide cu cea finala!")

        if afisCost:
            print("Cost drum: ", self.g)
        if afisLung:
            print("Lungime drum: ", len(l))
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        # trebuie sa testez sa nu fi fost aceeasi configuratie
        # in mai multe vase goale
        # trebuie sa le ordonez si sa le compar dupa ordonare
        # le ordonez dupa canitate
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
        sir = ""
        for vas in self.info:
            sir += str(vas[0]) + ": "
            sir += str(vas[1]) + " " + str(vas[2]) + " "
            if vas[3] == None:
                if vas[2] != 0:
                    sir += "nedefinita"
            elif vas[2] != 0:
                sir += vas[3]
            sir += "\n"

        return sir

    def __repr__(self):
        sir = "info= " + str(self.info) + "\n"
        if self.parinte != None:
            sir += "parinte= " + str(self.parinte.info) + "\n"
        else:
            sir += "parinte= None\n"
        sir += "cost= " + str(self.g) + "\n"
        sir += "h= " + str(self.h) + "\n"
        sir += "f= " + str(self.f) + "\n"
        sir += "infoDrum= " + str(self.infoDrum) + "\n"
        return sir


class Graph:
    def __init__(self, nume_fisier):
        try:
            f = open(nume_fisier, "r")
        except:
            print("Eroare la deschiderea fisierului!")
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
            print("Eroare la parsarea fisierului!")
            sys.exit(0)

    def testeaza_scop(self, InfonodCurent):
        ok = 0
        for (cantitate, culoare) in self.scopuri:
            for vas in InfonodCurent:
                if vas[-1] == culoare and vas[-2] == cantitate:
                    ok += 1
                    break

        if ok == len(self.scopuri):
            return True
        return False

    def testeaza_nod_de_exapandat(self, infoNod):
        '''
                2 tipuri de culori:
                    1.culori rezultate prin combinare
                    2.culori care merg combinate
        '''
        # print("Nodul: ", infoNod)
        culori_scop = 0
        culori_de_combinat = 0
        set_culori_de_combinat = set()
        # formez un set cu culorile care se combina
        # evit duplicatele
        for (c1, c2, c3) in self.culori:
            set_culori_de_combinat.add(c1)
            set_culori_de_combinat.add(c2)

        for culoare in set_culori_de_combinat:
            for vas in infoNod:
                if vas[3] == culoare:
                    culori_de_combinat += 1

        for (c1, c2, c3) in self.culori:
            for vas in infoNod:
                culoare = vas[3]
                if c3 == culoare:
                    culori_scop += 1
                    break
        # print("culori de combinat",culori_de_combinat)
        # print("culori scop", culori_scop)
        if culori_de_combinat == 0 and culori_scop == len(self.culori):
            # nu am nicio culoare rezultata prin combinare
            # dar am toate culorile care merg combinate
            return True
        elif culori_de_combinat == len(set_culori_de_combinat) and culori_scop == 0:
            # am toate culorile rezultate prin combinare
            # dar nu am nicio culoare care merge combinata
            return True
        elif culori_de_combinat != 0 and culori_scop != 0:
            # am din fiecare tip de culoare
            return True
        return False

    # functia de generare a succesorilor, facuta la laborator
    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        '''
        print("************************************")
        print("Nodul curent: ", nodCurent.info)
        print("************************************")
        '''
        for i in range(len(nodCurent.info)):
            # copieVase o sa reprezinte un aranjament
            # copieVase[i] = un vas

            # daca vasul este vid
            if len(nodCurent.info[i]) == 0:
                continue

            # iterez prin toate vasele diferite de cel curent
            for j in range(len(nodCurent.info)):

                if i == j:  # sa nu fie vasul din care torn
                    continue
                infoDrum = []
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
                if lichid_de_transferat != 0:
                    # -----------------Schimbare culoare + calcul cost mutare--------------------
                    # daca vasul e gol pentru culoare:
                    if VAS2[2] == 0:
                        VAS2[3] = VAS1[3]
                        infoDrum.append(VAS1[3])
                        if VAS1[3] in self.cost.keys():
                            costMutare += lichid_de_transferat * self.cost.get(VAS1[3])

                        if costMutare == 0:  # torn culoare nedefinita
                            costMutare += lichid_de_transferat  # cost=1
                    else:
                        # setare culoare pentru vas care nu e gol
                        ok = False
                        if VAS1[3] == VAS2[3] and VAS1[3] != None:
                            infoDrum.append(VAS1[3])
                            if VAS1[3] in self.cost.keys():
                                costMutare += lichid_de_transferat * self.cost.get(VAS1[3])
                        else:
                            for (c1, c2, c3) in self.culori:
                                # c1+c2==c2+c1==c3
                                if (VAS2[3] == c1 and VAS1[3] == c2) or (VAS2[3] == c2 and VAS1[3] == c1):
                                    VAS2[3] = c3
                                    ok = True
                                    break
                            if ok == True:
                                infoDrum.append(VAS1[3])
                                if VAS1[3] in self.cost.keys():
                                    costMutare += lichid_de_transferat * self.cost.get(VAS1[3])

                        if ok == False and VAS1[2] > 0:
                            # nu este definita combinatia de culori

                            # rezultat culoare nedefinita
                            # costul va fi suma
                            cost1 = 0
                            cost2 = 0
                            if VAS1[3] in self.cost.keys():
                                cost1 = lichid_de_transferat * self.cost.get(VAS1[3])

                            if VAS2[3] in self.cost.keys():
                                cost2 = VAS2[2] * self.cost.get(VAS2[3])

                            if cost1 == 0:  # torn culoare nedefinita
                                infoDrum.append('nedefinita')
                                costMutare += lichid_de_transferat  # cost=1
                            elif cost2 == 0:  # torn culoare nedefinita
                                infoDrum.append('nedefinita')
                                costMutare += VAS2[2]  # cost=1
                            else:
                                infoDrum.append(VAS1[3])
                                costMutare += cost1 + cost2
                            VAS2[3] = None
                    # -----------------Sfarsit schimbare culoare--------------------

                    # -----------------Schimbare cantitate lichid---------------------
                    if lichid_de_transferat <= VAS1[2]:
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
                    listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costMutare,
                                                        self.calculeaza_h(infoNodNou, tip_euristica), infoDrum))

        return listaSuccesori

    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            if gr.testeaza_scop(infoNod):
                return 1
            return 0
        elif tip_euristica == "euristica admisibila 1":

            '''
            trebuie sa vad daca in starea mea exista culorile din starile finale
            daca nu exista iau minimul costului unui L de culoare1 sau culoare2
            unde culoare1 + culoare2 = culoare din starea scop

            '''
            euristici = []
            for (cantitae_scop, culoare_scop) in self.scopuri:
                gasit = False
                h = 0
                for (id, capacitate, cantitate, culoare_vas) in infoNod:
                    if culoare_scop == culoare_vas:
                        gasit = True
                        break
                if gasit == False:
                    # minimul dintre costurile pentru 1L pentru obtinere
                    for (c1, c2, c3) in self.culori:
                        if c3 == culoare_scop:
                            cost_c1 = self.cost.get(c3)
                            cost_c2 = self.cost.get(c3)
                            if cost_c1 > cost_c2:
                                h = cost_c2
                            else:
                                h = cost_c1
                euristici.append(h)

            return min(euristici)


        elif tip_euristica == "euristica admisibila 2":
            '''
             trebuie sa vad din cate mutari obtin culorile din starea finala 
             iau minimul
            '''
            euristici = []
            for (cantitae_scop, culoare_scop) in self.scopuri:
                gasit = False
                h = 0
                for (id, capacitate, cantitate, culoare_vas) in infoNod:
                    if culoare_scop == culoare_vas:
                        gasit = True
                        break
                if gasit == False:
                    #  trebuie sa vad din cate mutari obtin culorile din starea finala
                    for (c1, c2, c3) in self.culori:
                        if c3 == culoare_scop:
                            cost_c1 = self.cost.get(c3)
                            cost_c2 = self.cost.get(c3)
                            nr_c1 = 0
                            nr_c2 = 0
                            for (id, capacitate, cantitate, culoare_vas) in infoNod:
                                if c1 == culoare_vas:
                                    nr_c1 += 1
                                if c2 == culoare_vas:
                                    nr_c2 += 1
                            # calculez minimul dintre costuri
                            cost_c1 = cost_c1 * nr_c1
                            cost_c2 = cost_c2 * nr_c2
                            if cost_c1 > cost_c2:
                                h = cost_c2
                            else:
                                h = cost_c1
                euristici.append(h)


            return min(euristici)

        elif tip_euristica == "neadmisibila":
            euristici = []
            for (cantitae_scop, culoare_scop) in self.scopuri:
                gasit = False
                h = 0
                for (id, capacitate, cantitate, culoare_vas) in infoNod:
                    if culoare_scop == culoare_vas:
                        gasit = True
                        break
                if gasit == False:
                    #  trebuie sa vad din cate mutari obtin culorile din starea finala
                    for (c1, c2, c3) in self.culori:
                        if c3 == culoare_scop:
                            cost_c1 = self.cost.get(c3)
                            cost_c2 = self.cost.get(c3)
                            nr_c1 = 0
                            nr_c2 = 0
                            for (id, capacitate, cantitate, culoare_vas) in infoNod:
                                if c1 == culoare_vas:
                                    nr_c1 += 1
                                if c2 == culoare_vas:
                                    nr_c2 += 1
                            # calculez minimul dintre costuri
                            cost_c1 = cost_c1 * nr_c1
                            cost_c2 = cost_c2 * nr_c2
                            if cost_c1 < cost_c2:
                                h = cost_c2
                            else:
                                h = cost_c1
                euristici.append(h)
            print(max(euristici))
            return max(euristici)
        '''
        de numarat prin cate vase sa mai trec ca sa ajung la culori
        la cea neadmisibila orice peste costul drumului
        '''

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir



def ida_star(gr, nrSolutiiCautate, tip_euristica="euristica banala"):
    nodStart = NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica), [])
    limita = nodStart.f
    while True:

        # print("Limita de pornire: ", limita)
        nrSolutiiCautate, rez = construieste_drum(gr, nodStart, limita, nrSolutiiCautate, tip_euristica )
        if rez == "gata":
            break
        if rez == float('inf'):
            print("Nu exista solutii!")
            break
        limita = rez
        # print(">>> Limita noua: ", limita)
        # input()


def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate, tip_euristica):
    # print("A ajuns la: ", nodCurent)
    if nodCurent.f > limita:
        return nrSolutiiCautate, nodCurent.f
    if gr.testeaza_scop(nodCurent.info) and nodCurent.f == limita:
        print("Solutie: ")
        nodCurent.afisDrum()
        # print(limita)
        print("\n----------------\n")
        # input()
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return 0 , "gata"
    lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
    minim = float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate, tip_euristica)
        if rez == "gata":
            return 0, "gata"
        # print("Compara ", rez, " cu ", minim)
        if rez < minim:
            minim = rez
            # print("Noul minim: ", minim)
    return nrSolutiiCautate, minim

print("#####Solutii obtinute cu IDA* #####\n")
gr = Graph("input_tema1.txt")
NodParcurgere.gr = gr
t1 = time.time()
ida_star(gr, nrSolutiiCautate=3, tip_euristica="euristica admisibila 2")
t2 = time.time()
milis = round(1000 * (t2 - t1))
print("Timpul scurs: ", milis, "milisecunde")
