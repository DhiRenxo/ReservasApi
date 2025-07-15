from models.ambiente import Ambiente
from models.cursos import Curso
from models.docente import Docente
from fastapi import HTTPException
import re

def traducir_dia(abreviado: str) -> str:
    dias = {
        "Lun": "Lunes",
        "Mar": "Martes",
        "Mie": "Miércoles",
        "Jue": "Jueves",
        "Vie": "Viernes",
        "Sab": "Sábado",
        "Dom": "Domingo"
    }
    return dias.get(abreviado, abreviado)

def extraer_ambiente_id(texto: str, db) -> int:
    match = re.search(r"(?i)Asignaci[oó]n de Horas para el aula\s*:\s*(.+)", texto)
    if not match:
        raise HTTPException(status_code=400, detail="Nombre de aula no encontrado en el PDF")

    nombre_aula = match.group(1).strip()
    ambiente = db.query(Ambiente).filter(Ambiente.codigo.ilike(f"%{nombre_aula}%")).first()

    if not ambiente:
        raise HTTPException(status_code=404, detail=f"Aula '{nombre_aula}' no encontrada en la base de datos")

    return ambiente.id

def buscar_curso_id(codigo: str, db) -> int:
    curso = db.query(Curso).filter(Curso.codigo == codigo.strip()).first()
    if not curso:
        raise HTTPException(status_code=404, detail=f"Curso con código '{codigo}' no encontrado")
    return curso.id

def buscar_docente_id(sigla: str, db) -> int:
    docente = db.query(Docente).filter(Docente.codigo == sigla.strip()).first()
    if not docente:
        raise HTTPException(status_code=404, detail=f"Docente con sigla '{sigla}' no encontrado")
    return docente.id

def extraer_horarios_de_texto(texto: str, db) -> list[dict]:
    bloques = texto.splitlines()
    resultados = []

    ambienteid = extraer_ambiente_id(texto, db)
    dias_detectados = []
    matriz_horaria = []
    hora_pattern = r"^\d{2}:\d{2}$"

    for linea in bloques:
        if "Hora" in linea and any(d in linea for d in ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]):
            dias_detectados = re.findall(r"Lun|Mar|Mie|Jue|Vie|Sab|Dom", linea)
            continue

        celdas = re.split(r"\s{2,}", linea.strip())
        if len(celdas) >= 2 and re.match(hora_pattern, celdas[0]):
            matriz_horaria.append(celdas)

    for i in range(len(matriz_horaria) - 1):
        fila = matriz_horaria[i]
        hora_inicio = fila[0]
        hora_fin = matriz_horaria[i + 1][0]

        for j in range(1, len(fila)):
            if j-1 >= len(dias_detectados):
                continue
            diasemana = traducir_dia(dias_detectados[j - 1])
            celda = fila[j].strip()

            if len(celda.split()) >= 3:
                grupo, curso_cod, docente_sigla = celda.split()[:3]

                try:
                    cursoid = buscar_curso_id(curso_cod, db)
                    docenteid = buscar_docente_id(docente_sigla, db)
                except HTTPException as e:
                    continue  # Salta si no encuentra alguno

                resultados.append({
                    "ambienteid": ambienteid,
                    "cursoid": cursoid,
                    "docenteid": docenteid,
                    "diasemana": diasemana,
                    "horainicio": hora_inicio,
                    "horafin": hora_fin,
                    "grupo": grupo
                })

    return resultados
