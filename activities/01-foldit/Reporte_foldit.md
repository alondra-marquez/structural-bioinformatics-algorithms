# ACTIVIDAD 1. FOLDIT
---

Foldit es una plataforma interactiva basada en el motor Rosetta que permite explorar el proceso de plegamiento proteico mediante manipulación directa del esqueleto (backbone) y las cadenas laterales de una proteina.

Aunque se presenta como un juego, su funcionamiento se fundamenta en principios biofísicos reales y en funciones de energía similares a las empleadas en modelado estructural computacional.

El objetivo de esta actividad fue utilizar foldit como una herramienta didáctica para familiarizarse y explorar los conceptos vistos en clase, como: 

- Interacciones no covalentes
- Formación de estructura secundaria
- Eliminación de choques estéricos
- Optimización energética
- Relación secuencia–estructura

---
### Backbone y eliminación de choques

Durante los primeros niveles del modo *campaign*, como *One Small Clash, Swing It Around y Control Over Clashing* , el objetivo principal consistió en eliminar conflictos estéricos y optimizar la geometría del backbone.

En términos estructurales y retomando lo visto en clase :

- los choques estéricos corresponden a interacciones de van der Waals desfavorables, que aumentan significativamente la energía del sistema

- La rotación de enlaces del backbone permite modificar los ángulos diedros $\phi$ y $\psi$.

- Estas rotaciones deben respetar las regiones permitidas del diagrama de Ramachandran.

Las herramientas disponibles en el juego ilustran claramente distintos tipos de optimización:

- **Wiggle** realiza ajustes locales pequeños y progresivos, similares a una minimización por gradiente.

- **Shake** explora configuraciones alternativas de manera más global

Esto refleja directamente el concepto de:

> Minimización iterativa dentro de un paisaje energético con múltiples mínimos locales.


![[img/fig1_foldit.png]]
Figura 1. Eliminación de conflictos estéricos mediante ajuste del backbone en el nivel _Control Over Clashing_.

---
### Formación de láminas β y puentes de hidrógeno

En niveles como _Sheets Together_ y _Lonely Sheets_, se puede observa la alineación de segmentos extendidos formando láminas β.

Aquí se retoman varios conceptos fundamentales:

- Las láminas β se estabilizan por puentes de hidrógeno entre grupos NH y C=O del backbone.

- La orientación paralela o antiparalela afecta la geometría del contacto.

- La formación de contactos de largo alcance aumenta el orden de contactos (CO).

Durante la ejecución de estos niveles, la correcta alineación de las láminas β incrementó notablemente el puntaje al:

- Reducir la energía asociada a puentes H no satisfechos.
- Disminuir residuos hidrofóbicos expuestos.


Esto ejemplifica cómo la formación de estructuras secundarias es un paso limitante del plegamiento. 

![[img/fig2_foldit.png]]
Figura 2. Captura correpondiente al nivel 7, *sheets together*

![[img/fig3_foldit.png]]
Figura 3. Captura correspondiente al nivel 10 , *Lonely sheets*

---
### Efecto hidrofóbico y empaquetamiento

En el nivel _Hide the Hydrophobic_, se evidenció uno de los principios fundamentales del plegamiento proteico:

> Los residuos hidrofóbicos tienden a enterrarse en el interior del núcleo proteico.

Este comportamiento, es consecuencia del efecto hidrofóbico en solución acuosa, que contribuye significativamente a la estabilidad termodinámica del estado nativo. Cuando los residuos hidrofóbicos quedan expuestos al solvente, el sistema aumenta su energía y el puntaje disminuye en el juego.

Por el contrario, el empaquetamiento interno favorece interacciones de van der Waals y estabiliza el núcleo globular.

![[img/fig4_foldit.png]]
Figura 4. Captura correspondiente al nicel 5, *Hide the Hydrophobic*

---
### Minimización energética y embudo de plegamiento

Foldit modela el plegamiento como una búsqueda en un espacio conformacional altamente dimensional, esta representación se conecta directamente con la paradoja de Levinthal.

Teóricamente, acorde a lo visto en clase,  una proteína de 100 residuos podría adoptar un número astronómico de conformaciones. Si el proceso fuera completamente aleatorio, el tiempo necesario para explorarlas sería mayor que la edad del universo; sin embargo, en condiciones normales , el plegamiento ocurre en segundos.

La experiencia en Foldit muestra claramente que: 

- El proceso no es aleatorio.
- Existen trayectorias preferenciales.
- El sistema converge hacia mínimos energéticos específicos.

El uso repetido de Wiggle y Shake refleja la transición entre mínimos locales y una aproximación progresiva al mínimo global.

![[img/fig5_foldit.png]]
**Figura 5.** Optimización progresiva de la conformación hacia estados de menor energía.

---
### Relación secuencia–estructura

En niveles más avanzados (mutaciones y diseño), se observa que pequeñas modificaciones en la secuencia pueden alterar:

- Contactos estructurales
- Estabilidad energética
- Formación de elementos secundarios

Esto conecta con el principio de Anfinsen:

> La información necesaria para el plegamiento está contenida en la secuencia.

Sin embargo, también se evidencia que:

- Existen múltiples estados metaestables.
- No todas las conformaciones energéticamente favorables son funcionales.
---

### Conclusion 

En general, Foldit constituye una herramienta educativa muy util, que traduce principios biofísicos complejos en reglas computacionales simplificadas, permitiendo comprender conceptos clave de la estructura de las macromoléculas. 

Personalmente, la experiencia me permitió integrar los conceptos revisados en clase tanto de forma conceptual como visual. Poder manipular directamente una estructura y observar cómo pequeños cambios influyen en la energía del sistema resultó especialmente útil para comprender el plegamiento proteico

### Referencias

Cooper, S., Khatib, F., Treuille, A., et al. (2010). _Predicting protein structures with a multiplayer online game_. Science, 329(5999), 1244–1248.