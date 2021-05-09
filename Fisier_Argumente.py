import argparse
import os
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

#creez fisiere de output pentru fiecare fisier de input

#verific daca nu există folderul folder_output, caz în care îl creez
if not os.path.exists(cale_folder_ouput):
	os.mkdir(cale_folder_ouput)

for numeFisierIntrare in listaFisiereIntrare:
    numeFisierOutput = "output_" + numeFisierIntrare

    Output = open(cale_folder_ouput+"\\" + numeFisierOutput, "w")

    # ----prelucrare fisier de input ---------#

    # închid fișierul
    Output.close()


