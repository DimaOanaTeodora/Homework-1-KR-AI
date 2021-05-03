import math
import copy
class NodParcurgere:
    gr = None  # trebuie setat sa contina instanta problemei

    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info # lista de forma [[id, capacitate, cantitate, culoare], ..]
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            if nod.parinte is not None:
                print("Din vasul {} s-au turnat {} litri de apa de culoare {} in vasul {}.".
                      format('X', 'Y', 'Z', 'W'))
                print(str(nod))
        if afisCost:
            print("Cost drum: ", self.g)
        if afisLung:
            print("Lungime drum: ", len(l))
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __str__(self):
        sir=""
        for vas in self.info:
            sir+=str(vas[0])+": "
            sir += str(vas[1]) + " " + str(vas[2]) + " "
            if vas[3]==None:
                if vas[2] !=0:
                    sir+="nedefinita"
            else:
                sir+=vas[3]
            sir+="\n"
        return sir

    def __repr__(self):
        sir = "info= " +str(self.info)+"\n"
        if self.parinte != None:
            sir+= "parinte= " +str(self.parinte.info)+"\n"
        else:
            sir += "parinte= None\n"
        sir += "cost= " + str(self.g) + "\n"
        sir += "h= " + str(self.h) + "\n"
        sir += "f= " + str(self.f) + "\n"
        return sir

class Graph:
    def __init__(self, nume_fisier):

        f = open(nume_fisier, "r")
        textFisier = f.read()
        text1 = textFisier.strip().split("stare_initiala")
        text2 = text1[1].strip().split("stare_finala")
        p1 = text1[0].strip().split('\n')
        p2 = text2[0].strip().split('\n')
        p3 = text2[1].strip().split('\n')

        combinatii_culori = []
        cost_culori = []
        for line in p1:
            v = line.split()
            if len(v) == 3:
                combinatii_culori.append((v[0], v[1], v[2]))
            elif len(v) == 2:
                cost_culori.append((v[0], int(v[1])))
        stare_initiala = []
        for id in range(len(p2)):
            line = p2[id]
            v = line.split()
            if len(v) == 3:
                stare_initiala.append([id, int(v[0]), int(v[1]), v[2]])
            elif len(v) == 2:
                stare_initiala.append([id, int(v[0]), 0, None])

        stare_finala = []
        for id in range(len(p3)):
            line = p3[id]
            v = line.split()
            stare_finala.append((int(v[0]), v[1]))

        self.start = stare_initiala  # informatia nodului de start
        self.culori=combinatii_culori
        self.cost=cost_culori
        self.scopuri =stare_finala
        print("Stare initiala: ", self.start)
        print("Stare finala: ", self.scopuri)


    def testeaza_scop(self, nodCurent):
        # verific daca gasesc toate vasele impreuna cu
        # culorile si valorile cantitatilor din scop in informatia nodului curent
        ok=0
        #print("--------------------")
        #print("Nod curent:\n", nodCurent)
        for (cantitate, culoare) in self.scopuri:
            # 2 mov
            # 4 portocaliu
            for vas in nodCurent.info:
                if vas[-1]== culoare and vas[-2]==cantitate:
                    #print("******a gasit o culoare din starea finala******")
                    ok+=1
                    break
        if ok==len(self.scopuri):
            return True
        return False



    # functia de generare a succesorilor, facuta la laborator
    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        for i in range(len(nodCurent.info)):
            # iau fiecare vas in parte
            # am nevoie sa compar cu aranjamentul initial
            copieVase = copy.deepcopy(nodCurent.info)

            # daca este vas vid
            if len(copieVase[i]) == 0:
                continue
            # iau cantitatea de lichid din vas
            # copieVase[i] = un singur vas
            lichid = copieVase[i][-2]
            culoare= copieVase[i][-1]
            print("------------------------")
            print("Nod de expandat: ",nodCurent.info[i])
            # iterez prin toate vasele
            for j in range(len(nodCurent.info)):

                if i == j:  # sa nu fie vasul din care am torn
                    continue

                costMutare = 1  # este 1 daca am culoare nedefinita
                # si acum incep sa torn lichidul in celelalte vase
                infoNodNou = copy.deepcopy(copieVase)

                print("Info(j) nod nou: ", nodCurent.info[j])
                # Trebuie sa am 2 cazuri : torn tot ce se afla in vas sau umplu celelalt vas
                # infoNodNou[j][-3]-infoNodNou[j][-3] cat ar mai avea de adaugat pana face capacitatea maxima
                # infoNodNou[j][-3]-infoNodNou[j][-3] < lichid
                # lichid_de_transferat = infoNodNou[j][-3]-infoNodNou[j][-3]
                # infoNodNou[i][-2] -= lichid_de_transferat actualizez nodul curent
                lichid_de_transferat = infoNodNou[j][-3] - infoNodNou[j][-2]
                if lichid_de_transferat!=0 and lichid_de_transferat <= lichid:
                    # -----------------Schimbare culoare--------------------
                    # tratez cazul daca vasul e gol pentru culoare:
                    if infoNodNou[j][-2] == 0:
                        infoNodNou[j][-1]=culoare
                    else:
                        # setare culoare pentru vas care nu e gol
                        c = infoNodNou[j][-1]
                        ok = False
                        for combinatie in self.culori:
                            if (c == combinatie[0] and culoare == combinatie[1]) or (
                                    c == combinatie[1] and culoare == combinatie[0]):
                                infoNodNou[j][-1] = combinatie[2]
                                ok = True
                                break
                        if ok == False:
                            infoNodNou[j][-1] = None
                    # -----------------Sfarsit schimbare culoare--------------------

                    #-----------------Schimbare cantitate lichid---------------------
                    # cazul cand umplu al doilea vas
                    # adaug lichidul in vasul nou
                    infoNodNou[j][-2] += lichid_de_transferat
                    # actualizez si vasul din care am trunat
                    infoNodNou[i][-2] -= lichid_de_transferat

                    # -----------------sfarsit schimbare cantitate lichid---------------------

                    #cost mutare e cost lichid transferat * cost culoare
                    for (cost, cul) in self.cost:
                        if cul ==  culoare:
                            costMutare= lichid_de_transferat * cost
                            break

                #TODO: de intrebat de cazul cu cap=7 l=1 si cap=4 l=2 daca am voie sa transfer
                #TODO: de vazut daca fiecare nod ar trebui sa retina si expandarea anterioara

                # ca sa nu sara inapoi verific daca a mai fost modelul
                if not nodCurent.contineInDrum(infoNodNou):
                    print("noul nou expandat: ", infoNodNou)
                    listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costMutare,
                                                        self.calculeaza_h(infoNodNou, tip_euristica)))

        return listaSuccesori

    # euristica banala
    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            ok = 0
            for (cantitate, culoare) in self.scopuri:
                for vas in infoNod:
                    if vas[-1] == culoare and vas[-2] == cantitate:
                        ok += 1
                        break
                if ok == len(self.scopuri):
                    return 1
            return 0


    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir



def a_star(gr, nrSolutiiCautate, tip_euristica):
    # open = coada noduri descoperite care nu au fost expandate
    # closed= noduri descoperite si expandate
    open = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica))]
    # face parte din optimizare
    closed = []  # n-am expandat pe nimeni la momentul asta
    while len(open) > 0:
        #print("Coada actuala: ", str(open))
        #input()
        nodCurent = open.pop(0)
        closed.append(nodCurent)  # a fost vizitat

        if gr.testeaza_scop(nodCurent):  # daca am ajuns la un nod scop
            print("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True) #---------aici se modifica
            #return #daca vreau sa-mi afiseze doar solutia optima
            print("\n----------------\n")
            nrSolutiiCautate -= 1  # scad nr de solutii
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent,tip_euristica=tip_euristica)
        #print("Lista Succesori:", lSuccesori)


        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(open)):
                # diferenta fata de UCS e ca ordonez dupa f

                # ---------------- Optimizare 2------------------------
                # daca f-urile sunt egale ordonez descrescator dupa g
                if open[i].f > s.f or (open[i].f == s.f and open[i].g <= s.g):
                    gasit_loc = True
                    break
                # -------------------------------------------------------
                #if open[i].f >= s.f:
                    #gasit_loc = True
                    #break
            if gasit_loc:
                open.insert(i, s)
            else:
                open.append(s)

print("\n\n##################\nSolutii obtinute cu A*:")
gr = Graph("input_scurt.txt")
NodParcurgere.gr = gr
a_star(gr, nrSolutiiCautate=4,tip_euristica="euristica banala")
