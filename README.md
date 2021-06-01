# Problema vaselor cu apa

Link enunt: [Problema vaselor cu apa](http://irinaciocan.ro/inteligenta_artificiala/exemple-teme-a-star.php)

## Citire din linia de comanda

```
python main.py -i path_to_input_folder -o path_to_output_folder -n NSOL -t TIMEOUT
```

#### Exemple:

```
Ex1: python main.py -i Input -o Output -n 4 -t 4000
Ex2: python T_UCS.py -i C:\Users\Lenovo\Desktop\Input -o C:\Users\Lenovo\Desktop\Output -n 4 -t 4000
Ex3: python main.py -i C:\Users\Lenovo\Desktop\Test" "Input -o C:\Users\Lenovo\Desktop\Test" "Output -n 4 -t 4000
Obs: " " reprezinta spatiul din numele folderului: Test Input sau Test Output
```

## Fisierele de intrare:

- 1_fara_solutii.txt : inputul fara solutii, afiseaza un mesaj corespunzator
- 2_egale : starea initiala si cea finala sunt egale, afiseaza un mesaj corespunzator
- 3_scurt : input scurt care genereaza solutii pe toti cei 4 agloritmi (fara depasirea timpului de timeout)
- 4_lung : input lung care depaseste timpul de timeout, exceptie A* optimizat

### Format fisiere de intrare:

- c1 c2 c3 reprezentand combinatiile de culori (c1 + c2 = c2 + c1 = c3)
- numele culorilor folosite si costul/litru : culoare cost
- stare_initiala
- capacitatea vasului, lichidul existent in el, culoarea lichidului
- stare_finala
- lichidul existent si culoarea lichidului


## Validari

Datorita blocurilor try-except voi semnala prin doua mesaje "Eroare la deschiderea fisierului" si "Eroare la parsarea fisierului!", erori de genul : input literal unde ar trebui sa fie numeric (eroare la transformarea string -> int),
arunc intentionat o eroare daca culorile atat din starea initiala, cat si din cea finala nu se regasesc in lista cost culoare, nu contine delimitatorii: "stare_initiala", "stare_finala",

## Optimizari

- folosirea unui dictionar pentru memorarea culorii si a costului asociat
- o metoda prin care verific daca un nod are potentialul ca prin expandare sa ajunga la o solutie, in caz negativ nu-l mai adaug la lista de succesori
- o metoda care verifica daca starea initiala este egala cu cea scop, nemaifacand arborele de succesori
- metoda care testeaza daca un nod a mai fost generat, testeaza dupa ordonarea crescatoare in functie de cantitatea de lichid continuta in vase,
  astfel mai multe noduri cu aceleasi configuratii dar in vase diferite nu vor fi adaugate in drumul curent

## Găsirea unui mod de a realiza din starea initială că problema nu are soluții

Cele 2 metode apelata inaintea inceperii generarii succesorilor pentru nodul de start pot semnaleaza daca starile initiala si cea scop
coincid sau daca un nod nu poate genera o solutie

```python
def testeaza_nod_de_exapandat(self, infoNod)
def initial_egal_final(self, stare_finala)
```

## Euristici folosite:

#### Euristica banala:

```python
if tip_euristica == "euristica banala":
    if gr.testeaza_scop(infoNod):
        return 1
    return 0
```

Estimez costul ca fiind 1 daca nu am ajuns in starea scop, si 0 daca am ajuns.  
Astfel, o data ce se gaseste o solutie, ea va fi pusa la inceputul cozii pentru a putea fi afisata.

#### Euristica Admisibila 1

Verific daca in starea currenta exista culorile din starile scop.
Daca nu exista iau minimul costului unui litru de culoare1 sau culoare2, unde culoare1 + culoare2 = culoarea din starea scop.

```python
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
        for (c1,c2,c3) in self.culori:
            if c3 == culoare_scop:
                cost_c1 = self.cost.get(c3)
                cost_c2 = self.cost.get(c3)
                if cost_c1 > cost_c2:
                    h = cost_c2
                else:
                    h = cost_c1
    euristici.append(h)
return min(euristici)
```

Demonstratie:
O euristica este admisibila daca:

    (costul estimat de la nodul curent la nodul scop) <= (costul real de la nodul curent la nodul scop pe un anumit drum)

Euristica este admisibila, deoarece presupun ca pentru a ajunge la o culoare din starea scop este nevoie sa torn un litru de lichid dintr-o culoare complementara,
iar in realitate se va turna <b>cel putin un litru</b> de culoare complementara dintr-un alt vas, astfel ca, valoarea estimata va fi cel mult egala cu cea reala.



#### Euristica Admisibila 2

Calculez numarul de mutari prin care pot obtine culorile din starea scop si iau minimul dintre acestea.

```python
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
                    for (c1,c2,c3) in self.culori:
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
```

Demonstratie:

O euristica este admisibila daca:

    (costul estimat de la nodul curent la nodul scop) <= (costul real de la nodul curent la nodul scop)

Euristica este admisibila, deoarece calculez numarul minimul de mutari prin care pot obtine culorile din configuratia scop
si iau si minimul dintre costurile acestora. Cum configuratia finala are toate culorile scop, costul pe care il estimeaza
aceasta euristica va fi cel mult egal cu costul minim real al mutarilor.

#### Euristica Neadmisibila

Calculez numarul de litrii de lichid care ar trebui transferati pentru fiecare vas in parte pentru a ajunge la cantitatea
si culoarea vaselor din starea scop.
```python
            euristici = []
            for (cantitae_scop, culoare_scop) in self.scopuri:
                gasit = False
                h = 0
                for (id, capacitate, cantitate, culoare_vas) in infoNod:
                    if culoare_scop == culoare_vas:
                        gasit = True
                        break
                if gasit == False:
                    for (c1, c2, c3) in self.culori:
                        if c3 == culoare_scop:
                            cost_c1 = self.cost.get(c3)
                            cost_c2 = self.cost.get(c3)
                            if cost_c1 < cost_c2:
                                h = cost_c2 * 4
                            else:
                                h = cost_c1 * 4
                euristici.append(h)

            return max(euristici)
```
O euristica este admisibila daca:

    (costul estimat de la nodul curent la nodul scop) <= (costul real de la nodul curent la nodul scop)


Euristica este neadmisibila, deoarece presupun ca pentru a ajunge la o culoare din starea scop este nevoie sa torn 4 litrii de lichid dintr-o culoare complementara si iau maximul dintre costurile acestora,
iar in realitate se va turna <b>cel putin un litru</b> de culoare complementara dintr-un alt vas, astfel ca, valoarea estimata o va depasi pe cea reala de cele mai multe ori.

Pe configuratia din 4_lung.txt va intoarce un drum care nu este de cost minim pe A* optimizat.
Drumul de cost minim este 25, iar euristica neadimisibila pe A * optimizat va intoarce un drum de cost 37.

### Comparatii

![Analiza input scurt](https://github.com/DimaOanaTeodora/Homework-1-KR-AI/blob/main/Analiza_input_scurt.JPG)
![Analiza input lung](https://github.com/DimaOanaTeodora/Homework-1-KR-AI/blob/main/Analiza_input_lung.JPG)

#### Concluzii pe baza analizei:

- Euristica neadmisibila poate duce la solutii care nu sunt optime (prima solutie generata nu mai este drumul de cost minim)*
- Cea mai buna performanta obtinuta pe ambele teste este A* optimizat si cu euristica admisibila 1.
- Euristicile influenteaza foarte mult viteza algoritmilor.
- Algoritmul care are solutii pentru ambele fisiere este A* optimizat
- Datorita optimizarilor euristica neadmisibila este mai rapida, insa nu ofera o solutie optima
- Diferentele clare dintre algortimi se observa pe inputul care genreaza un arbore de succesori mai mare
- IDA* nu este atat de eficient (se observa ca depaseste timpul de timeout pe inputul mai lung, iar pe cel scurt are timp de executie de 2 ori mai mari ca A* si A* optimizat)
- A* optimizat este mai eficient din punct de vedere al memoriei utilizate
- UCS este mai eficient ca IDA*


### Calculare cost mutare:

- rezultatul este o culoare definita: L * cost_culoare
- rezultatul este o culoare nedefinita: L(de turnat) * cost_culoare_vas1 + L(aflat in vasul 2) * cost_culoare_vas2
- combin doua culori nedefinite: L * 1

