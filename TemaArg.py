import time
import copy
import argparse
import os
class NodParcurgere:
    gr = None  # trebuie setat sa contina instanta problemei

    def __init__(self, info, parinte, cost=0, h=0, infoDrum=[]):
        self.info = info # lista de forma [[id, capacitate, cantitate, culoare], ..]
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost
        self.h = h
        self.f = self.g + self.h
        self.infoDrum = infoDrum # lista [vasul1, vasul2, culoare, litrii_turnati]

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
            infoDrum = nod.infoDrum  # [vasul1, vasul2, culoare, litrii_turnati]
            if nod.parinte is not None and infoDrum!=[]:
                print("Din vasul {} s-au turnat {} litri de apa de culoare {} in vasul {}.".
                      format(infoDrum[0], infoDrum[3], infoDrum[2], infoDrum[1]))
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
            elif vas[2]!=0:
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
        sir += "infoDrum= " + str(self.infoDrum) + "\n"
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
        self.culori = combinatii_culori
        self.cost = cost_culori
        self.scopuri = stare_finala


    def testeaza_scop(self, nodCurent):
        # verific daca gasesc toate vasele impreuna cu
        # culorile si valorile cantitatilor din scop in informatia nodului curent
        ok=0
        for (cantitate, culoare) in self.scopuri:
            # 2 mov
            # 4 portocaliu
            for vas in nodCurent.info:
                if vas[-1]== culoare and vas[-2]==cantitate:
                    ok+=1
                    break
        if ok==len(self.scopuri):
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
            # TODO: ma pot lipsi de copie vase pt ca nu-l modific
            copieVase = copy.deepcopy(nodCurent.info)

            # daca vasul este vid
            if len(copieVase[i]) == 0:
                continue

            # iterez prin toate vasele diferite de cel curent
            for j in range(len(nodCurent.info)):


                if i == j:  # sa nu fie vasul din care torn
                    continue
                infoDrum=[]
                infoNodNou = copy.deepcopy(copieVase)
                VAS1 = copy.deepcopy(copieVase[i])
                VAS2 = copy.deepcopy(copieVase[j])
                '''
                print("Nodul pe care lucrez: ", infoNodNou)
                print("Vasul 1:", VAS1)
                print("Vasul 2:", VAS2)
                '''
                infoDrum.append(VAS1[0])
                infoDrum.append(VAS2[0])

                '''
                2 cazuri: 
                    1. golesc vasul1
                    2. umplu vasul 2
                '''
                # cat ar mai avea de adaugat pana face capacitatea maxima:
                # capacitate_VAS2 - lichid_VAS2
                #(umple VAS2, altfel golesete VAS1)
                # capacitate_VAS2 - lichid_VAS2  < lichid_VAS1
                # lichid_de_transferat = capacitate_VAS2 - lichid_VAS2
                # actualizez nodul curent
                # lichid_VAS2 = VAS2[2]-= lichid_de_transferat
                lichid_de_transferat = VAS2[1] - VAS2[2]
                costMutare = 0
                if lichid_de_transferat!=0:

                    # -----------------Schimbare culoare + calcul cost mutare--------------------
                    # calculez pt culoare_VAS1
                    # daca vasul e gol pentru culoare:
                    if VAS2[2]==0:
                        VAS2[3] = VAS1[3]
                        infoDrum.append(VAS1[3])
                        for (cost, culoare) in self.cost:
                            if culoare == VAS1[3]:
                                costMutare += lichid_de_transferat * cost
                                break
                        if costMutare==0: # torn culoare nedefinita
                            costMutare += lichid_de_transferat # cost=1
                    else:
                        # setare culoare pentru vas care nu e gol
                        ok = False
                        for (c1,c2,c3) in self.culori:
                            #c1+c2==c2+c1==c3
                            if (VAS2[3] == c1 and VAS1[3] == c2) or (VAS2[3] == c2 and VAS1[3] == c1):
                                VAS2[3] = c3
                                ok = True
                                break
                        if ok == True:
                            infoDrum.append(VAS1[3])
                            for (cost, culoare) in self.cost:
                                if culoare == VAS1[3]:
                                    costMutare += lichid_de_transferat * cost
                                    break

                        if ok == False:
                            # nu este definita combinatia de culori
                            # rezultat culoare nedefinita
                            # costul va fi suma
                            cost1=0
                            cost2=0
                            for(cost, culoare) in self.cost:
                                if culoare== VAS1[3]:
                                    cost1= lichid_de_transferat * cost
                                    break
                            for (cost, culoare) in self.cost:
                                if culoare == VAS2[3]:
                                    cost2= VAS2[2] * cost
                                    break
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


                #TODO: de intrebat de cazul cu cap=7 l=1 si cap=4 l=2 daca am voie sa transfer
                #TODO: de vazut daca fiecare nod ar trebui sa retina si expandarea anterioara
                infoNodNou[j][2] = copy.deepcopy(VAS2[2])
                infoNodNou[j][3] = copy.deepcopy(VAS2[3])
                infoNodNou[i][2] = copy.deepcopy(VAS1[2])
                infoNodNou[i][3] = copy.deepcopy(VAS1[3])
                # ca sa nu sara inapoi verific daca a mai fost modelul
                #print("Noul nod nepus: ", infoNodNou)
                #print("Info DRUM: ", infoDrum)
                if not nodCurent.contineInDrum(infoNodNou):
                    #print("Noul nod: ", infoNodNou)
                    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costMutare,
                                                        self.calculeaza_h(infoNodNou, tip_euristica), infoDrum))

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
    open = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica), [])]
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

print("Solutii obtinute cu A*:")
gr = Graph("input_scurt.txt")
NodParcurgere.gr = gr
t1=time.time()
a_star(gr, nrSolutiiCautate=2,tip_euristica="euristica banala")
t2=time.time()
milis=round(1000*(t2-t1))
print("Timpul scurs: ", milis, "milisecunde")

#---------Citirea cu argumente-------
'''
 1. calea catre folderul cu fisiere de input
 2. calea pentru folderul de output
 3. NSOL
 4. Timpul de timeout
'''

ap = argparse.ArgumentParser()
# required=True => argumente obligatorii
ap.add_argument("-i", "--i", required=True, help="cale folder cu fisiere de input")
ap.add_argument("-o", "--o", required=True, help="cale folder cu fisiere de output")
ap.add_argument("-n", "--n", required=True, help="nurmarul de solutii dorite")
ap.add_argument("-t", "--t", required=True, help="valoarea de timeout")

argumente = vars(ap.parse_args())
cale_folder_input=argumente['i']
cale_folder_ouput=argumente['o']
NSOL = int (argumente['n'])
timeout = int (argumente['t'])

# ---------Sfarsit citire argumente---

# obtin o lista cu numele fișierelor de input
listaFisiereIntrare=os.listdir(cale_folder_input)


#verific daca nu există folderul folder_output, caz în care îl creez
if not os.path.exists(cale_folder_ouput):
	os.mkdir(cale_folder_ouput)

#creez fisiere de output pentru fiecare fisier de input
for numeFisierIntrare in listaFisiereIntrare:
    numeFisierOutput = "output_" + numeFisierIntrare

    Output = open(cale_folder_ouput + "\\" + numeFisierOutput, "w")

    # ----prelucrare fisier de input ---------#
    '''
    print("Solutii obtinute cu A*:")
    gr = Graph(Output)
    NodParcurgere.gr = gr
    t1 = time.time()
    a_star(gr, nrSolutiiCautate=NSOL, tip_euristica="euristica banala")
    t2 = time.time()
    milis = round(1000 * (t2 - t1))
    print("Timpul scurs: ", milis, "milisecunde")
    '''
    # închid fișierul
    Output.close()

