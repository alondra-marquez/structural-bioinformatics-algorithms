# Actividad 7.7.1 – Modelado de estructura terciaria con AlphaFold2 (ColabFold) y evaluación de calidad

## Objetivo
Modelar la estructura tridimensional de una proteína individual mediante AlphaFold2 (vía ColabFold/OpenFold) y evaluar la calidad del modelo usando métricas internas de confianza y validación independiente en SwissModel Assess.

## Sistema estudiado
**Proteína:** Aquaporina 4 
**Organismo:** Homo sapiens 
**UniProt/Accesión:** P55087
**Longitud:** 323 aa  
**Secuencia empleada:** [AQP4.fa](data/AQP4.fa)

## Metodología

### 1) Modelado estructural (AF2 – ColabFold)

- Se utilizó ColabFold para predecir la estructura terciaria a partir de la secuencia aminoacídica.
- Se generaron múltiples modelos (n=<<<5>>>), seleccionando el mejor según el ranking interno.

**Archivos principales generados:**

- Modelo final: `results/colabfold/model_rank_001.pdb`


### 2) Métricas internas de confianza (AF2)
Se interpretaron:
- **pLDDT:** confianza local por residuo.
- **pTM** (si disponible): confianza en la topología global.
- **PAE:** error alineado esperado para evaluar incertidumbre relativa entre regiones/dominios.

Resultados guardados en: [resultados AF2](results/Colabfold/)


### 3) Validación (SwissModel Assess)
El modelo PDB fue evaluado en SwissModel Assess para obtener:

- **MolProbity:** Evaluación estereoquímica global.
- **Ramachandran plot:** Distribución conformacional del backbone.
- **Clashscore:** Contactos estéricos no optimizados.
- **QMEAN / QMEANDisCo:** Calidad estructural global y local comparada con estructuras experimentales.


Resultados guardados en: [resultados Swissmodel](results/swissmodel/)

## Resultados e interpretación general

El análisis detallado se encuentra en:
- [Reporte actividad](docs/reporte_act3.md)

