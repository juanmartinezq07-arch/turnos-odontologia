# Reflexión escrita — TurnosAR (borrador para completar con tus palabras)

> Borrador semi-armado: está escrito en tono tranqui para que lo expliques
> con tus palabras en la defensa, pero ya mete los conceptos de la materia
> (Discovery, harness/fundación, knowledge-base, roadmap, protocolo de
> inspección Continuar/Ajustar, ciclo OPSX, spec como contrato, Engram).
> Donde veas [COMPLETAR] poné tu experiencia real. 1-2 páginas al final.

## 1. Qué del Discovery estaba mal o no se pudo verificar (y cómo lo detectamos)

La consigna ya avisaba que un agente "no deja huecos sin resolver" y tiende
a inventar antes que decir "no sé". Nos pasó tal cual: el primer relevamiento
traía datos que sonaban re convincentes pero sin respaldo público.

Lo detectamos con la verificación de fuentes por fetch directo (8 URLs).
Los 5 errores que encontramos están en `docs/discovery/_verificacion-fuentes.md`,
por ejemplo:

- [COMPLETAR con 1-2 ejemplos tuyos, ej: la URL `/precios` de DentalSoft que en realidad redirigía al demo, o la reserva "sin login" de AgendaPro que no aparecía en la página citada].

La regla que nos quedó: toda celda sin respaldo público dice "No evidenciado",
no se completa por deducción. Y distinguir siempre entre funcionalidad
comprobada (se ve en docs/demo/video oficial) y afirmación comercial
(lo dice el proveedor sin mostrarlo).

## 2. Dónde usamos Ajustar, qué estaba mal y qué pasaba si poníamos Continuar

El protocolo de inspección (Continuar / Ajustar / Parar acá) lo usamos en
serio al menos en [COMPLETAR: ej. "la revisión de la knowledge-base" o "el Propose del change"].

Lo que estaba mal era [COMPLETAR: ej. "el spec cubría de más / de menos / inventaba alcance que el Discovery había dejado para etapas posteriores"].
Lo corregimos con Ajustar y [COMPLETAR qué cambió].

Si en ese momento apretábamos Continuar de una, [COMPLETAR la consecuencia:
ej. "implementábamos algo que el MVP no pedía / arrastrábamos un dato falso del Discovery hasta el código"].
La lección: corregir temprano es barato, corregir en Apply es carísimo.

## 3. Implementar con spec aprobada vs. pedir código con un prompt suelto

La diferencia se nota en una cosa: con la spec aprobada (proposal + design +
specs con escenarios dado/cuando/entonces) el Apply fue casi mecánico, porque
el contrato ya decía qué tenía que pasar en el caso feliz, en el error de
negocio y en el borde (el turno que empieza justo cuando termina otro).

[COMPLETAR con tu comparación: ej. "antes le pedía código al agente y cada respuesta venía distinta / mezclaba lógica en los routers / había que re-explicar todo"].

Acá, si algo no estaba en el spec, no se inventaba en Apply: se volvía a
Propose. Eso al principio parece lento, pero te ahorra discutir con código
ya escrito.

## 4. Qué parte de la fundación aportó más y cuál menos al ciclo OPSX

- **Lo que más sumó:** [COMPLETAR, ej. "las reglas de negocio RN01–RN05 y el modelo de datos, porque el change era básicamente llevar RN02 a la base con el doble EXCLUDE" / "las reglas del AGENTS.md, porque mantuvieron el layout y los errores 409/422 consistentes"].
- **Lo que menos usamos:** [COMPLETAR con honestidad, ej. "el roadmap, porque con un solo change no había mucho que planificar" / "los flujos principales, porque el change era chico"].

[COMPLETAR una línea de por qué: qué habrías extrañado si faltaba lo primero].

## 5. Reparto del trabajo

[COMPLETAR: quién hizo qué etapa. Ej: "Trabajo individual: llevé Discovery, KB + roadmap y el ciclo OPSX completo." O en grupo: "X llevó Discovery, Y KB + roadmap, Z el change; cada uno con sus commits"].

---

*Checklist antes de entregar: que tenga 1-2 páginas, que cada afirmación
fuerte cite su evidencia (informe, verificación, spec), y que se note que
leyeron lo que el agente generó en vez de aprobar en automático.*
