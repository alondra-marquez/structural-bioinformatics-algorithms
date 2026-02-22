# Actividad 7.7.2 – Modelado de complejo proteína–ADN con AlphaFold3 y evaluación estructural

### Objetivo

Modelar la estructura cuaternaria de un complejo proteína–ADN mediante AlphaFold3 y evaluar su calidad utilizando métricas internas de confianza y validación independiente en SwissModel Assess.

### Sistema estudiado

- Proteína: POU5F1 (OCT4)
- Organismo: Homo sapiens
- UniProt: Q01860
- Dominio modelado: 138–289 (dominio POU)
- ADN: Dúplex de 28 pb con motivo 5’-ATGCAAAT-3’

### Metodología

1) Modelado estructural (AlphaFold3)

Se utilizó AlphaFold3 para modelar el complejo proteína–ADN.
- Cadena A: dominio POU.
- Cadenas B y C: ADN de doble cadena.
- Parámetros por defecto.

Se generaron múltiples modelos y se seleccionó el mejor según el ipTM (confianza en la interfaz).

Archivos principales generados:
- Modelo final: [Modelo](results/fold_2026_02_22_14_19_model_0.cif)
- Resultados guardados en: [Resultados](results/)

2) Métricas internas de confianza (AF3)

Se interpretaron:
- ipTM: confianza en la interfaz proteína–ADN.
- pTM: confianza en el plegamiento global.
- PAE: incertidumbre relativa entre cadenas y regiones.

3) Validación (SwissModel Assess)

El modelo fue evaluado para obtener:
- MolProbity: calidad estereoquímica global.
- Ramachandran plot: conformación del backbone.
- Clashscore: contactos estéricos.
- QMEANDisCo: calidad estructural global y local.

Resultados guardados en: [Resultados](results/)

### Resultados e interpretación general

El reporte del análisis detallado se encuentra en:
- [Reporte](docs/Reporte_act4.md)