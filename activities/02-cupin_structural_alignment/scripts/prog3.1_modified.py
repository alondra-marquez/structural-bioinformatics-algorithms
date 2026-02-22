

#!/usr/bin/env python

from __future__ import print_function
from math import sqrt
import re
import SVD
import argparse


"""

Script modificado 

prog3.1 Calcula la superposicion en 3D equivalente a un alineamiento de 
secuencia de dos proteinas del PDB. Genera un fichero PDB con la superposicion 
obtenida. 

Ejemplo de uso:

python prog3_1_modified.py \
  --fasta foldmason_aa.fa \
  --pdb foldmason.pdb \
  --pair 3ZPOcif_A,3ZPOcif_B \
  --pair 2XUEcif_A,2XUEcif_B \
  --out results.tsv

"""

__author__  = 'Bruno Contreras-Moreira (modified)' 

# 1) subrutinas

def foldmason_multimodel_coords(filename):
	"""
	Lee un PDB de FoldMason con múltiples bloques MODEL/ENDMDL y líneas:
	REMARK    Name: <ID>
	Devuelve:
	coords_by_model[ID] = model_coords
	donde model_coords es una lista de residuos (strings con líneas ATOM),
	igual que lee_coordenadas_PDB() para un PDB normal.
	"""

	name_pattern = re.compile(r"^REMARK\s+Name:\s*(\S+)")

	coords_by_model = {}
	in_model = False
	current_model_id = None

	model_coords = []
	residue_block = ''
	previous_res_id = ''

	with open(filename, 'r') as pdbfile:
		for line in pdbfile:

			# inicia modelo nuevo
			if line.startswith("MODEL"):
				in_model = True
				current_model_id = None
				model_coords = []
				residue_block = ''
				previous_res_id = ''
				continue

			# termina el modelo 
			if line.startswith("ENDMDL"):
				if residue_block != '':
					model_coords.append(residue_block)

				if current_model_id is not None:
					coords_by_model[current_model_id] = model_coords

				in_model = False
				current_model_id = None
				continue

			if not in_model:
				continue

			# captura el ID del modelo
			match = name_pattern.match(line)
			if match:
				current_model_id = match.group(1)
				continue

			if not line.startswith("ATOM"):
				continue

			# agrupa por residuo (mismo criterio que el script original)
			residue_id = line[17:26]

			if residue_id != previous_res_id:
				if residue_block != '':
					model_coords.append(residue_block)
				residue_block = line
			else:
				residue_block += line

			previous_res_id = residue_id

	if not coords_by_model:
		raise ValueError("No se detectaron modelos (MODEL/ENDMDL + REMARK Name) en el PDB.")

	return coords_by_model


def aligned_fasta(filename):
	"""Lee un FASTA alineado (con '-') y devuelve dict[id] = secuencia_alineada."""

	aligned_sequences = {}
	current_seq_id = None

	with open(filename, "r") as fasta_file:
		for f_line in fasta_file:
			line = f_line.strip()
			if not line:
				continue

			if line.startswith(">"):
				current_seq_id = line[1:].strip()
				if current_seq_id in aligned_sequences:
					raise ValueError("ID duplicado en FASTA: %s" % current_seq_id)
				aligned_sequences[current_seq_id] = ""
			else:
				if current_seq_id is None:
					raise ValueError("FASTA no inicia con header '>'")
				aligned_sequences[current_seq_id] += line

	# todas las secuencias deben tener la misma longitud
	alignment_lengths = set(len(seq) for seq in aligned_sequences.values())

	if len(alignment_lengths) != 1:
		raise ValueError( "Las secuencias del FASTA alineado no tienen la misma longitud s: %s"
			% sorted(alignment_lengths)
		)

	return aligned_sequences

def coords_alineadas(align1,coords1,align2,coords2):
	""" Devuelve dos listas de igual longitud con las coordenadas de los atomos CA 
	de los residuos alineados en align1 y align2."""
	
	total1,total2 = -1,-1
	align_coords1,align_coords2 = [],[]
	length = len(align1)
	
	if(length != len(align2)): 
		print("# coords_alineadas: alineamientos tienen != longitud")
		return ([],[])
	
	for r in range(0, length):
		res1 = align1[r:r+1]
		res2 = align2[r:r+1]
		if(res1 != '-'): total1+=1
		if(res2 != '-'): total2+=1
		if(res1 == '-' or res2 == '-'): continue #solo  interesan pares alineados
		align_coords1.append( extrae_coords_atomo(coords1[total1],' CA ') )
		align_coords2.append( extrae_coords_atomo(coords2[total2],' CA ') )
	return (align_coords1,align_coords2)
	
def extrae_coords_atomo(res,atomo_seleccion):
	""" De todas las coordenadas atomicas de un residuo, extrae las de un atomo particular 
	y devuelve una lista con las X, Y y Z de ese atomo."""
	
	atom_coords = []
	for atomo in res.split("\n"):
		if(atomo[12:16] == atomo_seleccion):
			atom_coords = [ float(atomo[30:38]), float(atomo[38:46]), float(atomo[46:54]) ]
	return atom_coords


def calcula_superposicion_SVD(pdbh1,pdbh2,originalPDBname,fittedPDBname,test=False):
    """ Calcula matriz de rotacion que aplicada sobre coords1 minimiza RMSD respecto a coords2
    y crea archivo con formato PDB con la superposicion resultante.
    Emplea el algoritmo de 'Single Value Decomposition' del paquete SVD. """
	
    def calcula_centro(coords):
        centro = [0,0,0]
        for coord in (coords): 
            for dim in range(0,3): centro[dim] += coord[dim]
        for dim in range(0,3): centro[dim] /= len(coords)
        return centro
   
    def calcula_coordenadas_centradas(coords,centro):
        ccoords,total = [],0
        for coord in (coords): 
            ccoords.append(coord)
            for dim in range(0,3): ccoords[total][dim] -= centro[dim]
            total+=1
        return ccoords
		
    def calcula_coordenadas_rotadas(coords,rotacion):
        rcoords = [0,0,0]            
        for i in range(0,3):               
            tmp = 0.0
            for j in range(0,3): tmp += coords[j] * rotacion[i][j]
            rcoords[i] = tmp
        return rcoords			
   
    # escribe fichero PDB con coordenadas originales
    pdbfile = open(originalPDBname, 'w')
    print("HEADER %s\n" % pdbh1['file'], file=pdbfile)
    for res in (pdbh1['coords']): 
        print(res, file=pdbfile)
    print("TER\n", file=pdbfile)
    print("HEADER %s\n" % pdbh2['file'], file=pdbfile)
    for res in (pdbh2['coords']): 
        print(res, file=pdbfile)
    print("TER\n", file=pdbfile)
    pdbfile.close()	
	
    ## prepara coordenadas de atomos CA alineados (equivalentes)
    coords1,coords2 = pdbh1['align_coords'],pdbh2['align_coords']
    centro1 = calcula_centro(coords1) 
    centro2 = calcula_centro(coords2) 
    ccoords1 = calcula_coordenadas_centradas(coords1,centro1) 
    ccoords2 = calcula_coordenadas_centradas(coords2,centro2) 
	
    ## prepara matriz producto para descomposicion matricial SVD matriz = U.Sigma.V
    matriz = [[0,0,0],[0,0,0],[0,0,0]]
    peso = 1.0/len(ccoords1) # todos los residuos cuentan igual
    for i in range(0,3):
        for j in range(0,3):
            tmp = 0.0
            for k in range(0,len(ccoords1)): tmp += ccoords1[k][i] * ccoords2[k][j] * peso
            matriz[i][j]=tmp;
    if(test == True): 
        for i in range(0,3): 
            print("mat %f %f %f\n" % (matriz[i][0],matriz[i][1],matriz[i][2]))		
   			
    ## invoca descomposicion en valores singulares y comprueba matrix/determinante
    [U, Sigma, V] = SVD.svd( matriz )
    if(test==True): 
        for i in range(0,3): print("U %f %f %f\n" % (U[i][0],U[i][1],U[i][2]))
        for i in range(0,3): print("Vt %f %f %f\n" % (V[i][0],V[i][1],V[i][2]))
	
    rotacion = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(0,3):
        for j in range(0,3):
            rotacion[i][j]= U[j][0]*V[i][0] + U[j][1]*V[i][1] + U[j][2]*V[i][2]
				
    ## evalua error de la superposicion
    rmsd = 0.0
    for n in range(0,len(coords1)):
        coords1_rot = calcula_coordenadas_rotadas(ccoords1[n],rotacion)
        for i in range(0,3):
            desv = ccoords2[n][i]-coords1_rot[i]
            rmsd += desv*desv
    rmsd /= len(coords1)
	
    ## imprime superposicion de todos los atomos en formato PDB
    pdbfile = open(fittedPDBname, 'w')
	
    # pdb superpuesto, coordenadas rotadas (1)
    print("HEADER %s (rotated)\n" % pdbh1['file'], file=pdbfile)
    print("REMARK Rotation matrix:\n", file=pdbfile)
    for i in range(0,3): print("REMARK %f %f %f\n" % \
				(rotacion[i][0],rotacion[i][1],rotacion[i][2]), file=pdbfile)
    print("REMARK centroid: %f %f %f\n" % (centro1[0],centro1[1],centro1[2]), file=pdbfile)
    print("REMARK partner centroid: %f %f %f\n" % \
		(centro2[0],centro2[1],centro2[2]), file=pdbfile)
    for res in (pdbh1['coords']): 
        for atomo in res.split("\n"):
            if(atomo == ''): break
            atcoords = extrae_coords_atomo(res,atomo[12:16]) 
			
            atcoords[0] -= centro1[0] # centralo
            atcoords[1] -= centro1[1]
            atcoords[2] -= centro1[2]
			
            coords_rot = calcula_coordenadas_rotadas(atcoords,rotacion)
			
            # trasladalo al pdb referencia
            atcoords[0] = centro2[0] + coords_rot[0] 
            atcoords[1] = centro2[1] + coords_rot[1]
            atcoords[2] = centro2[2] + coords_rot[2]
					
            print("%s%8.3f%8.3f%8.3f%s" % \
                (atomo[0:30],atcoords[0],atcoords[1],atcoords[2],atomo[54:]), file=pdbfile)	
    print("TER\n", file=pdbfile)
	
    # pdb de referencia, coordenadas originales (2)
    print("HEADER %s\n" % pdbh2['file'], file=pdbfile)
    for res in (pdbh2['coords']): print(res, file=pdbfile)
    print("TER\n", file=pdbfile)
	
    pdbfile.close()	
	
    return sqrt(rmsd)
	
def percent_identity(alignmentA, alignmentB):
	"""% identidad usando solo columnas donde ambos != '-'."""

	if len(alignmentA) != len(alignmentB):
		raise ValueError("Alineamientos con distinta longitud")

	matches = 0
	pairs = 0
	for a, b in zip(alignmentA, alignmentB):
		if a == '-' or b == '-':
			continue
		pairs += 1
		if a == b:
			matches += 1

	if pairs == 0:
		return (0.0, 0, 0)

	return (100.0 * matches / pairs, matches, pairs)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Calcula %identidad y RMSD para pares de modelos en foldmason.pdb usando foldmason_aa.fa.")
	parser.add_argument("--pdb", required=True, help="PDB multi-model de FoldMason (foldmason.pdb)")
	parser.add_argument("--fasta", required=True, help="FASTA alineado de FoldMason (foldmason_aa.fa)")
	parser.add_argument("--pair", action="append", required=True,
						help="Par de IDs en formato ID1,ID2. Se puede repetir.")
	parser.add_argument("--out", default="results.tsv", help="Archivo de salida TSV (default: results.tsv)")
	args = parser.parse_args()

	# 1) Carga inputs
	coords_by_id = foldmason_multimodel_coords(args.pdb)
	fasta_by_id = aligned_fasta(args.fasta)

	# 2) Parsea pares
	pairs = []
	for p in args.pair:
		parts = p.split(",")
		if len(parts) != 2 or parts[0] == "" or parts[1] == "":
			raise SystemExit("Formato inválido para --pair. Usa: ID1,ID2")
		ida, idb = parts[0], parts[1]
		pairs.append((ida, idb))

	# 4) Escribe tabla
	with open(args.out, "w") as out:
		out.write("idA\tidB\tpairs\tmatches\tpid\tnCA\trmsd\n")
		out.flush()
		for ida, idb in pairs:
			# A) % identidad 
			alignmentA = fasta_by_id[ida]
			alignmentB = fasta_by_id[idb]
			pid, matches, pairs_no_gaps = percent_identity(alignmentA, alignmentB)

			# B) preparar dicts 
			pdbhA = {'file': ida, 'align': alignmentA, 'coords': coords_by_id[ida]}
			pdbhB = {'file': idb, 'align': alignmentB, 'coords': coords_by_id[idb]}

			# C) coords CA equivalentes
			(pdbhA['align_coords'], pdbhB['align_coords']) = coords_alineadas(
				pdbhA['align'], pdbhA['coords'],
				pdbhB['align'], pdbhB['coords']
			)

			n_ca = len(pdbhA['align_coords'])

			# D) RMSD por SVD (si no hay CA equivalentes, RMSD = nan)
			if n_ca == 0:
				rmsd = float("nan")
            
			else:
				orig_name = "original_tmp.pdb"
				fit_name  = "align_fit_tmp.pdb"
				rmsd = calcula_superposicion_SVD(pdbhA, pdbhB, orig_name, fit_name)
				
			# salida TSV
			out.write("%s\t%s\t%.2f\t%d\t%d\t%.3f\n" % (
				ida, idb, pid, pairs_no_gaps, n_ca, rmsd
			))
	print("Escribiendo en:", args.out)
	print(" Resultados en:", args.out)
