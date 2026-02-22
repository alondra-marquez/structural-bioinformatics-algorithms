# Alineamiento estructural de dominios Cupin

**CATH 2.60.120.650**

## Descripción

Este repositorio contiene el análisis de alineamiento estructural múltiple de dominios pertenecientes a la superfamilia **Cupin** (CATH 2.60.120.650).

Se realizaron:

- Alineamiento estructural múltiple con FoldMason
- Búsqueda estructural con FoldSeek
- Cálculo de porcentaje de identidad y RMSD mediante un script modificado
    

El análisis  e interpretación se encuentran en el reporte incluido en la carpeta [Carpeta report](report/)


Estructura del repositorio

```
ACT2_structural_alignment/
│
├── README.md
├── report/
│   └── reporte_ACT2.pdf
│   ├──img/
│      └──dominio.jpeg
├── data/
│   ├── foldmason.pdb
│   ├── foldmason_aa.fa
│   └── foldmason_ss.fa
│
├── results/
│   ├── results_domains.tsv
│   ├── foldmason_alignment.png
│   └── superposition.png
│
├── scripts/
	└── prog3.1.py
	├── SVD.py
 └── prog3.1_modified.py

```

## Dominios analizados

- 2WWJ_A01
- 2XUE_A01  
- 4DIQ_B01
- 5FYV_A01
- 3ZPO_B01
- 3PU8_B01

## Ejecución

Ejemplo de ejecución del script modificado:

```python 
python3 scripts/prog3.1_modified.py \
  --pdb data/foldmason.pdb \
  --fasta data/foldmason_aa.fa \
  --pair 3ZPOcif_A,3ZPOcif_B \
  --pair 3ZPOcif_B,2XUEcif_A \
  --pair 3PU8cif_A,4DIQcif_B \
  --pair 2WWJcif_A,5FYVcif \
  --out results/results_domains.tsv
```

