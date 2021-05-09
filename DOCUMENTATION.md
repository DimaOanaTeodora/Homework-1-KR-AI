# Problema vaselor cu apa

Link enunt: [Problema vaselor cu apa](http://irinaciocan.ro/inteligenta_artificiala/exemple-teme-a-star.php)

## Citire din linia de comanda
```
python main.py -i path_to_input_folder -o path_to_output_folder -n NSOL -t TIMEOUT
```
#### Exemple:
```
    Ex1: python main.py -i Input -o Output -n 4 -t 200
    Ex2: python main.py -i C:\Users\Lenovo\Desktop\Test" "Input -o C:\Users\Lenovo\Desktop\Test" "Output -n 4 -t 200
    PS:" "reprezinta spatiul din numele folderului: Test Input sau Test Output
```
### Format fisier de intrare:

- c1 c2 c3 reprezentand combinatiile de culori (c1 + c2 = c2 + c1 = c3)
- numele culorilor folosite si costul/litru : culoare cost
- stare_initiala
- capacitatea vasului, lichidul existent in el, culoarea lichidului
- stare_finala
- lichidul existent si culoarea lichidului

## Euristici folosite:

#### Euristica banala:
```python
* insert code here*
```
  Estimez costul ca fiind 1 daca nu am ajuns in starea scop, si 0 daca am ajuns.  
  Astfel, o data ce se gaseste o solutie, ea va fi pusa la inceputul cozii pentru a putea fi afisata.

#### Euristica Admisibila 1

#### Euristica Admisibila 2

#### Euristica Neadmisibila

