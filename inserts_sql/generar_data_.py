"""
=============================================================================
PROYECTO 2 - GENERADOR DE DATOS (Faker + Firebird) - VERSIÓN INTEGRAL
Indicadores Sociales y Sanitarios de Guatemala
=============================================================================
"""
from __future__ import annotations

import argparse
import os
import random
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

from faker import Faker

# ---------------------------------------------------------------------------
# CONFIGURACION DE VOLUMEN (Modificado para consistencia)
# ---------------------------------------------------------------------------
N_PERSONAS = 10_000 # Base de IDs para evitar errores de llave foránea
N_HOGARES  = 3_500
N_HECHOS_DELICTIVOS = 15_000 
N_DENUNCIAS = 8_000
N_HVM = 4_500          
N_HVIF = 4_000         
N_HVI = 3_500          
N_HDISC = 2_500        
N_TRABAJO_INF = 2_500
N_FALTAS_JUD = 3_000
N_NECROPSIAS = 4_000
N_EXHUMACIONES = 800
N_SENTENCIAS = 5_000

N_REG_SALUD = 15_000
N_REG_DESNUT = 8_000
N_REG_CRONICA = 8_000
N_REG_VECTOR = 10_000
N_REG_MORBI = 5_000
N_EMBARAZO_ADO = 3_000
N_CONTROL_PREN = 4_000

OUTPUT_DIR = Path("inserts_sql")

# ---------------------------------------------------------------------------
# DATOS MAESTROS DE GUATEMALA
# ---------------------------------------------------------------------------
REGIONES_GT = [("Metropolitana", "I"), ("Norte", "II"), ("Nororiente", "III"), ("Suroriente", "IV"), ("Central", "V"), ("Suroccidente", "VI"), ("Noroccidente", "VII"), ("Petén", "VIII")]
DEPARTAMENTOS_GT = [("Guatemala", "01", "Guatemala", 1), ("Alta Verapaz", "16", "Cobán", 2), ("Baja Verapaz", "15", "Salamá", 2), ("Chiquimula", "20", "Chiquimula", 3), ("El Progreso", "02", "Guastatoya", 3), ("Izabal", "18", "Puerto Barrios", 3), ("Zacapa", "19", "Zacapa", 3), ("Jalapa", "21", "Jalapa", 4), ("Jutiapa", "22", "Jutiapa", 4), ("Santa Rosa", "06", "Cuilapa", 4), ("Chimaltenango", "04", "Chimaltenango", 5), ("Escuintla", "05", "Escuintla", 5), ("Sacatepéquez", "03", "Antigua Guatemala", 5), ("Quetzaltenango", "09", "Quetzaltenango", 6), ("Retalhuleu", "11", "Retalhuleu", 6), ("San Marcos", "12", "San Marcos", 6), ("Sololá", "07", "Sololá", 6), ("Suchitepéquez", "10", "Mazatenango", 6), ("Totonicapán", "08", "Totonicapán", 6), ("Huehuetenango", "13", "Huehuetenango", 7), ("Quiché", "14", "Santa Cruz del Quiché", 7), ("Petén", "17", "Flores", 8)]
MUNICIPIOS_GT = [(1,"Guatemala","0101"),(1,"Mixco","0108"),(1,"Villa Nueva","0110"),(1,"San Miguel Petapa","0114"),(1,"Amatitlán","0117"),(1,"Chinautla","0107"),(1,"Villa Canales","0115"),(1,"San José Pinula","0103"),(1,"Santa Catarina Pinula","0102"),(1,"San Pedro Ayampuc","0106"),(1,"Fraijanes","0116"),(1,"Palencia","0105"),(1,"San Juan Sacatepéquez","0111"),(1,"San Pedro Sacatepéquez","0112"),(1,"San Raymundo","0113"),(1,"Chuarrancho","0109"),(1,"San José del Golfo","0104"),(2,"Cobán","1601"),(2,"San Pedro Carchá","1602"),(2,"San Juan Chamelco","1603"),(2,"Tactic","1604"),(2,"San Cristóbal Verapaz","1605"),(2,"Tucurú","1606"),(2,"Panzós","1607"),(2,"Senahú","1608"),(2,"Cahabón","1609"),(2,"Lanquín","1610"),(2,"Chahal","1611"),(2,"Fray Bartolomé de las Casas","1612"),(2,"Chisec","1613"),(2,"Santa Cruz Verapaz","1614"),(2,"Tamahú","1615"),(2,"Santa Catalina La Tinta","1616"),(2,"Raxruhá","1617"),(3,"Salamá","1501"),(3,"San Miguel Chicaj","1502"),(3,"Rabinal","1503"),(3,"Cubulco","1504"),(3,"Granados","1505"),(3,"El Chol","1506"),(3,"San Jerónimo","1507"),(3,"Purulhá","1508"),(4,"Chiquimula","2001"),(4,"San José La Arada","2002"),(4,"San Juan Ermita","2003"),(4,"Jocotán","2004"),(4,"Camotán","2005"),(4,"Olopa","2006"),(4,"Esquipulas","2007"),(4,"Concepción Las Minas","2008"),(4,"Quezaltepeque","2009"),(4,"San Jacinto","2010"),(4,"Ipala","2011"),(5,"Guastatoya","0201"),(5,"Morazán","0202"),(5,"San Agustín Acasaguastlán","0203"),(5,"San Cristóbal Acasaguastlán","0204"),(5,"El Jícaro","0205"),(5,"Sansare","0206"),(5,"Sanarate","0207"),(5,"San Antonio La Paz","0208"),(6,"Puerto Barrios","1801"),(6,"Livingston","1802"),(6,"El Estor","1803"),(6,"Morales","1804"),(6,"Los Amates","1805"),(7,"Zacapa","1901"),(7,"Estanzuela","1902"),(7,"Río Hondo","1903"),(7,"Gualán","1904"),(7,"Teculután","1905"),(7,"Usumatlán","1906"),(7,"Cabañas","1907"),(7,"San Diego","1908"),(7,"La Unión","1909"),(7,"Huité","1910"),(8,"Jalapa","2101"),(8,"San Pedro Pinula","2102"),(8,"San Luis Jilotepeque","2103"),(8,"San Manuel Chaparrón","2104"),(8,"San Carlos Alzatate","2105"),(8,"Monjas","2106"),(8,"Mataquescuintla","2107"),(9,"Jutiapa","2201"),(9,"El Progreso","2202"),(9,"Santa Catarina Mita","2203"),(9,"Agua Blanca","2204"),(9,"Asunción Mita","2205"),(9,"Yupiltepeque","2206"),(9,"Atescatempa","2207"),(9,"Jerez","2208"),(9,"El Adelanto","2209"),(9,"Zapotitlán","2210"),(9,"Comapa","2211"),(9,"Jalpatagua","2212"),(9,"Conguaco","2213"),(9,"Moyuta","2214"),(9,"Pasaco","2215"),(9,"San José Acatempa","2216"),(9,"Quesada","2217"),(10,"Cuilapa","0601"),(10,"Barberena","0602"),(10,"Santa Rosa de Lima","0603"),(10,"Casillas","0604"),(10,"San Rafael Las Flores","0605"),(10,"Oratorio","0606"),(10,"San Juan Tecuaco","0607"),(10,"Chiquimulilla","0608"),(10,"Taxisco","0609"),(10,"Santa María Ixhuatán","0610"),(10,"Guazacapán","0611"),(10,"Santa Cruz Naranjo","0612"),(10,"Pueblo Nuevo Viñas","0613"),(10,"Nueva Santa Rosa","0614"),(11,"Chimaltenango","0401"),(11,"San José Poaquil","0402"),(11,"San Martín Jilotepeque","0403"),(11,"Comalapa","0404"),(11,"Santa Apolonia","0405"),(11,"Tecpán Guatemala","0406"),(11,"Patzún","0407"),(11,"Pochuta","0408"),(11,"Patzicía","0409"),(11,"Santa Cruz Balanyá","0410"),(11,"Acatenango","0411"),(11,"Yepocapa","0412"),(11,"San Andrés Itzapa","0413"),(11,"Parramos","0414"),(11,"Zaragoza","0415"),(11,"El Tejar","0416"),(12,"Escuintla","0501"),(12,"Santa Lucía Cotzumalguapa","0502"),(12,"La Democracia","0503"),(12,"Siquinalá","0504"),(12,"Masagua","0505"),(12,"Tiquisate","0506"),(12,"La Gomera","0507"),(12,"Guanagazapa","0508"),(12,"San José","0509"),(12,"Iztapa","0510"),(12,"Palín","0511"),(12,"San Vicente Pacaya","0512"),(12,"Nueva Concepción","0513"),(12,"Sipacate","0514"),(13,"Antigua Guatemala","0301"),(13,"Jocotenango","0302"),(13,"Pastores","0303"),(13,"Sumpango","0304"),(13,"Santo Domingo Xenacoj","0305"),(13,"Santiago Sacatepéquez","0306"),(13,"San Bartolomé Milpas Altas","0307"),(13,"San Lucas Sacatepéquez","0308"),(13,"Santa Lucía Milpas Altas","0309"),(13,"Magdalena Milpas Altas","0310"),(13,"Santa María de Jesús","0311"),(13,"Ciudad Vieja","0312"),(13,"San Miguel Dueñas","0313"),(13,"Alotenango","0314"),(13,"San Antonio Aguas Calientes","0315"),(13,"Santa Catarina Barahona","0316"),(14,"Quetzaltenango","0901"),(14,"Salcajá","0902"),(14,"Olintepeque","0903"),(14,"San Carlos Sija","0904"),(14,"Sibilia","0905"),(14,"Cabricán","0906"),(14,"Cajolá","0907"),(14,"San Miguel Sigüilá","0908"),(14,"Ostuncalco","0909"),(14,"San Mateo","0910"),(14,"Concepción Chiquirichapa","0911"),(14,"San Martín Sacatepéquez","0912"),(14,"Almolonga","0913"),(14,"Cantel","0914"),(14,"Huitán","0915"),(14,"Zunil","0916"),(14,"Colomba","0917"),(14,"San Francisco La Unión","0918"),(14,"El Palmar","0919"),(14,"Coatepeque","0920"),(14,"Génova","0921"),(14,"Flores Costa Cuca","0922"),(14,"La Esperanza","0923"),(14,"Palestina de los Altos","0924"),(15,"Retalhuleu","1101"),(15,"San Sebastián","1102"),(15,"Santa Cruz Muluá","1103"),(15,"San Martín Zapotitlán","1104"),(15,"San Felipe","1105"),(15,"San Andrés Villa Seca","1106"),(15,"Champerico","1107"),(15,"Nuevo San Carlos","1108"),(15,"El Asintal","1109"),(16,"San Marcos","1201"),(16,"San Pedro Sacatepéquez","1202"),(16,"San Antonio Sacatepéquez","1203"),(16,"Comitancillo","1204"),(16,"San Miguel Ixtahuacán","1205"),(16,"Concepción Tutuapa","1206"),(16,"Tacaná","1207"),(16,"Sibinal","1208"),(16,"Tajumulco","1209"),(16,"Tejutla","1210"),(16,"San Rafael Pie de la Cuesta","1211"),(16,"Nuevo Progreso","1212"),(16,"El Tumbador","1213"),(16,"El Rodeo","1214"),(16,"Malacatán","1215"),(16,"Catarina","1216"),(16,"Ayutla","1217"),(16,"Ocós","1218"),(16,"San Pablo","1219"),(16,"El Quetzal","1220"),(16,"La Reforma","1221"),(16,"Pajapita","1222"),(16,"Ixchiguán","1223"),(16,"San José Ojetenam","1224"),(16,"San Cristóbal Cucho","1225"),(16,"Sipacapa","1226"),(16,"Esquipulas Palo Gordo","1227"),(16,"Río Blanco","1228"),(16,"San Lorenzo","1229"),(16,"La Blanca","1230"),(17,"Sololá","0701"),(17,"San José Chacayá","0702"),(17,"Santa María Visitación","0703"),(17,"Santa Lucía Utatlán","0704"),(17,"Nahualá","0705"),(17,"Santa Catarina Ixtahuacán","0706"),(17,"Santa Clara La Laguna","0707"),(17,"Concepción","0708"),(17,"San Andrés Semetabaj","0709"),(17,"Panajachel","0710"),(17,"Santa Catarina Palopó","0711"),(17,"San Antonio Palopó","0712"),(17,"San Lucas Tolimán","0713"),(17,"Santa Cruz La Laguna","0714"),(17,"San Pablo La Laguna","0715"),(17,"San Marcos La Laguna","0716"),(17,"San Juan La Laguna","0717"),(17,"San Pedro La Laguna","0718"),(17,"Santiago Atitlán","0719"),(18,"Mazatenango","1001"),(18,"Cuyotenango","1002"),(18,"San Francisco Zapotitlán","1003"),(18,"San Bernardino","1004"),(18,"San José El Idolo","1005"),(18,"Santo Domingo Suchitepéquez","1006"),(18,"San Lorenzo","1007"),(18,"Samayac","1008"),(18,"San Pablo Jocopilas","1009"),(18,"San Antonio Suchitepéquez","1010"),(18,"San Miguel Panán","1011"),(18,"San Gabriel","1012"),(18,"Chicacao","1013"),(18,"Patulul","1014"),(18,"Santa Bárbara","1015"),(18,"San Juan Bautista","1016"),(18,"Santo Tomás La Unión","1017"),(18,"Zunilito","1018"),(18,"Pueblo Nuevo","1019"),(18,"Río Bravo","1020"),(18,"San José La Máquina","1021"),(19,"Totonicapán","0801"),(19,"San Cristóbal Totonicapán","0802"),(19,"San Francisco El Alto","0803"),(19,"San Andrés Xecul","0804"),(19,"Momostenango","0805"),(19,"Santa María Chiquimula","0806"),(19,"Santa Lucía La Reforma","0807"),(19,"San Bartolo","0808"),(20,"Huehuetenango","1301"),(20,"Chiantla","1302"),(20,"Malacatancito","1303"),(20,"Cuilco","1304"),(20,"Nentón","1305"),(20,"San Pedro Necta","1306"),(20,"Jacaltenango","1307"),(20,"Soloma","1308"),(20,"Ixtahuacán","1309"),(20,"Santa Bárbara","1310"),(20,"La Libertad","1311"),(20,"La Democracia","1312"),(20,"San Miguel Acatán","1313"),(20,"San Rafael La Independencia","1314"),(20,"Todos Santos Cuchumatán","1315"),(20,"San Juan Atitán","1316"),(20,"Santa Eulalia","1317"),(20,"San Mateo Ixtatán","1318"),(20,"Colotenango","1319"),(20,"San Sebastián Huehuetenango","1320"),(20,"Tectitán","1321"),(20,"Concepción Huista","1322"),(20,"San Juan Ixcoy","1323"),(20,"San Antonio Huista","1324"),(20,"San Sebastián Coatán","1325"),(20,"Santa Cruz Barillas","1326"),(20,"Aguacatán","1327"),(20,"San Rafael Pétzal","1328"),(20,"San Gaspar Ixchil","1329"),(20,"Santiago Chimaltenango","1330"),(20,"Santa Ana Huista","1331"),(20,"Unión Cantinil","1332"),(20,"Petatán","1333"),(21,"Santa Cruz del Quiché","1401"),(21,"Chiché","1402"),(21,"Chinique","1403"),(21,"Zacualpa","1404"),(21,"Chajul","1405"),(21,"Chichicastenango","1406"),(21,"Patzité","1407"),(21,"San Antonio Ilotenango","1408"),(21,"San Pedro Jocopilas","1409"),(21,"Cunén","1410"),(21,"San Juan Cotzal","1411"),(21,"Joyabaj","1412"),(21,"Nebaj","1413"),(21,"San Andrés Sajcabajá","1414"),(21,"Uspantán","1415"),(21,"Sacapulas","1416"),(21,"San Bartolomé Jocotenango","1417"),(21,"Canillá","1418"),(21,"Chicamán","1419"),(21,"Ixcán","1420"),(21,"Pachalum","1421"),(22,"Flores","1701"),(22,"San José","1702"),(22,"San Benito","1703"),(22,"San Andrés","1704"),(22,"La Libertad","1705"),(22,"San Francisco","1706"),(22,"Santa Ana","1707"),(22,"Dolores","1708"),(22,"San Luis","1709"),(22,"Sayaxché","1710"),(22,"Melchor de Mencos","1711"),(22,"Poptún","1712"),(22,"Las Cruces","1713"),(22,"El Chal","1714")]

# ---------------------------------------------------------------------------
# UTILIDADES SQL Y CATÁLOGOS
# ---------------------------------------------------------------------------
AREAS_GEO = ["Urbana", "Rural", "Periurbana"]
SEXOS = [("Femenino",), ("Masculino",), ("Otro",)]
ETNIAS = [("Maya K'iche'", "Maya"), ("Maya Q'eqchi'", "Maya"), ("Maya Kaqchikel", "Maya"), ("Maya Mam", "Maya"), ("Maya Q'anjob'al", "Maya"), ("Maya Poqomchi'", "Maya"), ("Maya Achi'", "Maya"), ("Maya Ixil", "Maya"), ("Maya Tz'utujil", "Maya"), ("Maya Chuj", "Maya"), ("Maya Jakalteko", "Maya"), ("Garífuna", "Afro"), ("Xinca", "Indigena"), ("Ladino", "Mestizo"), ("Otro", "Otro")]
IDIOMAS = [("Español", 1), ("K'iche'", 1), ("Q'eqchi'", 1), ("Kaqchikel", 1), ("Mam", 1), ("Q'anjob'al", 1), ("Poqomchi'", 1), ("Achi'", 1), ("Ixil", 1), ("Tz'utujil", 1), ("Chuj", 1), ("Jakalteko", 1), ("Garífuna", 1), ("Xinca", 1), ("Inglés", 0), ("Francés", 0)]
ESTADOS_CIVIL = ["Soltero/a", "Casado/a", "Unido/a", "Divorciado/a", "Viudo/a", "Separado/a"]
RELIGIONES = ["Católica", "Evangélica", "Mormona", "Testigo de Jehová", "Maya", "Sin religión", "Otra"]
DISCAPACIDADES = [("Visual", "Vista"), ("Auditiva", "Oído"), ("Motora", "Movilidad"), ("Intelectual", "Cognitiva"), ("Mental", "Psicosocial"), ("Múltiple", "Varios")]
GRUPOS_ETARIOS = [("0-4", 0, 4), ("5-9", 5, 9), ("10-14", 10, 14), ("15-19", 15, 19), ("20-29", 20, 29), ("30-39", 30, 39), ("40-49", 40, 49), ("50-59", 50, 59), ("60-69", 60, 69), ("70+", 70, 120)]
NIVELES_EDU = [("Ninguno", 1, "Sin estudios"), ("Preprimaria", 2, "Inicial"), ("Primaria", 3, "1-6"), ("Básico", 4, "Secundaria"), ("Diversificado", 5, "Media"), ("Universitario", 6, "Superior"), ("Postgrado", 7, "Maestría")]
TIPOS_VIVIENDA = ["Propia", "Alquilada", "Prestada", "Cedida", "Invasión", "Otra"]
NIVELES_SOCIO = [("Extremo", 0, 2000), ("Bajo", 2000, 4500), ("Medio Bajo", 4500, 8000), ("Medio", 8000, 15000), ("Medio Alto", 15000, 30000), ("Alto", 30000, 999999)]
SECTORES_ECON = [("Agro", "A"), ("Manufactura", "C"), ("Construcción", "F"), ("Comercio", "G"), ("Transporte", "H"), ("Turismo", "I"), ("TIC", "J"), ("Finanzas", "K"), ("Servicios", "M"), ("Educación", "P"), ("Salud", "Q"), ("Gobierno", "O"), ("Doméstico", "T"), ("Otros", "S")]
OCUPACIONES = [("Agricultor","6111"),("Albañil","7112"),("Comerciante","5221"),("Conductor","8322"),("Docente","2330"),("Médico","2211"),("Enfermero","2221"),("Doméstica","9111"),("Carpintero","7522"),("Mecánico","7231"),("Vendedor","9520"),("Costurera","7531"),("Policía","5412"),("Militar","0110"),("Estudiante","9999"),("Ama de casa","9998"),("Profesional","2421"),("Obrero","9329"),("Pescador","6222"),("Cocinero","5120")]
TIPOS_EMPLEO = ["Asalariado","Cuenta propia","Empleador","Familiar","Doméstico","Aprendiz","Jubilado","Desempleado"]
COND_LABORAL = [("Formal", 1),("Informal", 0),("Subempleado", 0),("Desocupado", 0),("Inactivo", 0)]

EJES_VIOLENCIA = ["General", "Mujer", "Infantil", "VIF", "Estructural", "Faltas"]
TIPOS_DENUNCIA_POR_EJE = {
    "General": ["Robo","Extorsión","Amenazas"],
    "Mujer": ["Física VM","Psicológica VM","Femicidio"],
    "Infantil": ["Maltrato","Abandono","Explotación"],
    "VIF": ["VIF Física","VIF Psicológica"],
    "Estructural": ["Discriminación Étnica","Género"],
    "Faltas": ["Orden Público","Propiedad"]
}
INST_REPORTANTES = [("PNC","PNC"),("MP","MP"),("PDH","PDH"),("OJ","OJ")]
ESTADOS_DENUNCIA = ["Recibida","Investigación","Procesada","Cerrada"]
CLASIF_DELITO = ["Leve","Grave","Gravísimo"]
TIPOS_HECHO = [("Homicidio","Dolo",3),("Femicidio","Género",3),("Robo","Fuerza",2),("Lesiones","Daño",2),("Violación","Sexual",3)]
ARMAS = ["Fuego","Blanca","Contundente","Manos","Ninguna"]
MOVILES = ["Robo","Venganza","Pasional","Pandillas","Riña"]
LUGARES = ["Vía pública","Vivienda","Comercio","Transporte"]
PENAS = ["Prisión","Multa","Trabajo"]
TIPOS_DELITO_JUZ = [("Homicidio","123 CP"),("Femicidio","6 LCFEM"),("Robo","252 CP")]
TIPOS_VM = ["Física","Psicológica","Económica"]
CENTROS_AT_NOMBRES = ["CAIMUS","Hospital","DEMI"]
TIPOS_AT = ["Médica","Psicológica","Legal"]
TIPOS_VIF = ["Física","Psicológica"]
RELACIONES_AV = ["Cónyuge","Padre","Hijo","Hermano"]
TIPOS_VI = ["Maltrato","Abandono","Abuso"]
SECTORES_TI = ["Agro","Comercio","Servicios"]
TIPOS_TI = [("Asalariado",0),("Peligroso",1)]
JORNADAS_TI = [("Completa",40),("Parcial",20)]
TIPOS_DISC = ["Étnica","Género"]
GRUPOS_POB = ["Maya","LGBTIQ","Niñez"]
TIPOS_FALTA = [("Escándalo","489 CP"),("Riña","488 CP")]
SANCIONES = [("Multa",50,500),("Arresto",0,0)]

# Salud
CAPITULOS_CIE10 = [("A00-B99","Infecciosas"),("E00-E90","Metabólicas")]
CIE10_DETALLE = [(1,"A09","Diarrea"),(2,"E11","Diabetes"),(1,"A90","Dengue"),(2,"E44","Desnutrición")]
INDICADORES_SALUD = [(1,"Desnutrición Aguda","casos"),(2,"Diabetes","casos"),(1,"Dengue","casos")]
CATEGORIAS_INDIC = ["Nutrición","Crónicas","Vectores"]
TIPOS_CENTRO_SALUD = ["Hospital","Centro de Salud","Puesto"]
VECTORES = [("Aedes","Mosquito"),("Triatoma","Vinchuca")]
ENF_VECTOR_NOMBRES = ["Dengue","Malaria","Chagas"]
COMPLIC_EMB = [("Preeclampsia",None),("Hemorragia",None)]
TIPOS_ENCUESTA = ["ENCOVI","Censo"]
PARENTESCOS = ["Jefe","Cónyuge","Hijo"]

# ---------------------------------------------------------------------------
# UTILIDADES SQL
# ---------------------------------------------------------------------------
def sql_str(s) -> str:
    if s is None: return "NULL"
    return "'" + str(s).replace("'", "''") + "'"

def sql_date(d: Optional[date]) -> str:
    if d is None: return "NULL"
    return f"'{d.isoformat()}'"

def sql_time(t) -> str:
    if t is None: return "NULL"
    return f"'{t.strftime('%H:%M:%S')}'"

class SqlWriter:
    def __init__(self, outdir: Path):
        self.outdir = outdir
        outdir.mkdir(parents=True, exist_ok=True)
        self.files: dict[str, list[str]] = {}

    def add(self, modulo: str, sql: str):
        self.files.setdefault(modulo, []).append(sql)

    def add_cleanup(self, modulo: str, tables: list[str]):
        for t in reversed(tables):
            self.files.setdefault(modulo, []).insert(0, f"DELETE FROM {t};")
        self.files[modulo].insert(len(tables), "COMMIT;")

    def commit_module(self, modulo: str):
        self.files.setdefault(modulo, []).append("COMMIT;")

    def write_all(self):
        for modulo, lines in self.files.items():
            fname = self.outdir / f"{modulo}.sql"
            with open(fname, "w", encoding="utf-8") as f:
                f.write("SET NAMES UTF8;\nSET AUTODDL OFF;\n\n")
                f.write("\n".join(lines))
            print(f"  -> {fname.name} ({len(lines)} líneas)")

fake = Faker("es_MX")
class Ids: pass
ids = Ids()

# ---------------------------------------------------------------------------
# GENERADORES POR MODULO (01 - 15)
# ---------------------------------------------------------------------------
def generar_geografia(w: SqlWriter):
    mod = "01_geografia"
    w.add(mod, "INSERT INTO Pais(id_pais, nombre_pais, codigo_iso) VALUES (1, 'Guatemala', 'GTM');")
    for i, a in enumerate(AREAS_GEO, 1):
        w.add(mod, f"INSERT INTO Area_Geografica(id_area_geo, nombre_area) VALUES ({i}, {sql_str(a)});")
    ids.areas = list(range(1, len(AREAS_GEO)+1))
    for i, (nom, cod) in enumerate(REGIONES_GT, 1):
        w.add(mod, f"INSERT INTO Region(id_region, id_pais, nombre_region, codigo_region) VALUES ({i}, 1, {sql_str(nom)}, {sql_str(cod)});")
    for i, (nom, cod, cab, reg) in enumerate(DEPARTAMENTOS_GT, 1):
        w.add(mod, f"INSERT INTO Departamento(id_departamento, id_region, nombre_departamento, codigo_departamento, cabecera) VALUES ({i}, {reg}, {sql_str(nom)}, {sql_str(cod)}, {sql_str(cab)});")
    ids.departamentos = list(range(1, len(DEPARTAMENTOS_GT)+1))
    ids.municipios = []
    for i, (depto_idx, nom, cod) in enumerate(MUNICIPIOS_GT, 1):
        w.add(mod, f"INSERT INTO Municipio(id_municipio, id_departamento, id_area_geo, nombre_municipio, codigo_municipio, poblacion_estimada) VALUES ({i}, {depto_idx}, {random.choice(ids.areas)}, {sql_str(nom)}, {sql_str(cod)}, {random.randint(5000, 100000)});")
        ids.municipios.append(i)
    w.add_cleanup(mod, ["Municipio", "Departamento", "Region", "Area_Geografica", "Pais"])
    w.commit_module(mod)

def generar_catalogos(w: SqlWriter):
    mod = "02_catalogos"
    for i,(s,) in enumerate(SEXOS,1): w.add(mod, f"INSERT INTO Sexo(id_sexo, nombre_sexo) VALUES ({i}, {sql_str(s)});")
    ids.sexos = [1,2,3]
    for i,(e,d) in enumerate(ETNIAS,1): w.add(mod, f"INSERT INTO Etnia(id_etnia, nombre_etnia, descripcion) VALUES ({i}, {sql_str(e)}, {sql_str(d)});")
    ids.etnias = list(range(1,len(ETNIAS)+1))
    for i,(idi, ofi) in enumerate(IDIOMAS,1): w.add(mod, f"INSERT INTO Idioma(id_idioma, nombre_idioma, es_oficial) VALUES ({i}, {sql_str(idi)}, {ofi});")
    ids.idiomas = list(range(1,len(IDIOMAS)+1))
    for i,e in enumerate(ESTADOS_CIVIL,1): w.add(mod, f"INSERT INTO Estado_Civil(id_estado_civil, nombre_estado_civil) VALUES ({i}, {sql_str(e)});")
    ids.ec = list(range(1,len(ESTADOS_CIVIL)+1))
    for i,r in enumerate(RELIGIONES,1): w.add(mod, f"INSERT INTO Religion(id_religion, nombre_religion) VALUES ({i}, {sql_str(r)});")
    ids.religiones = list(range(1,len(RELIGIONES)+1))
    for i,(d,ds) in enumerate(DISCAPACIDADES,1): w.add(mod, f"INSERT INTO Discapacidad(id_discapacidad, nombre_discapacidad, descripcion) VALUES ({i}, {sql_str(d)}, {sql_str(ds)});")
    ids.discapacidades = list(range(1,len(DISCAPACIDADES)+1))
    for i,(g,mn,mx) in enumerate(GRUPOS_ETARIOS,1): w.add(mod, f"INSERT INTO Grupo_Etario(id_grupo_etario, nombre_grupo_etario, rango_edad_min, rango_edad_max) VALUES ({i}, {sql_str(g)}, {mn}, {mx});")
    ids.ge = list(range(1,len(GRUPOS_ETARIOS)+1))
    for i,(n,o,d) in enumerate(NIVELES_EDU,1): w.add(mod, f"INSERT INTO Nivel_Educativo(id_nivel_educativo, nombre_nivel, orden, descripcion) VALUES ({i}, {sql_str(n)}, {o}, {sql_str(d)});")
    ids.nivel_edu = list(range(1,len(NIVELES_EDU)+1))
    ids.instituciones_edu = []
    for i in range(1, 51):
        w.add(mod, f"INSERT INTO Institucion_Educativa(id_institucion_edu, id_municipio, nombre_institucion, sector) VALUES ({i}, {random.choice(ids.municipios)}, 'Escuela {i}', 'Público');")
        ids.instituciones_edu.append(i)
    for i,t in enumerate(TIPOS_VIVIENDA,1): w.add(mod, f"INSERT INTO Tipo_Vivienda(id_tipo_vivienda, nombre_tipo_vivienda) VALUES ({i}, {sql_str(t)});")
    ids.tipo_viv = list(range(1,len(TIPOS_VIVIENDA)+1))
    for i,(n,mn,mx) in enumerate(NIVELES_SOCIO,1): w.add(mod, f"INSERT INTO Nivel_Socioeconomico(id_nivel_socio, nombre_nivel, ingreso_min, ingreso_max) VALUES ({i}, {sql_str(n)}, {mn}, {mx});")
    ids.socio = list(range(1,len(NIVELES_SOCIO)+1))
    for i,(s,c) in enumerate(SECTORES_ECON,1): w.add(mod, f"INSERT INTO Sector_Economico(id_sector_econ, nombre_sector, codigo_ciiu) VALUES ({i}, {sql_str(s)}, {sql_str(c)});")
    ids.sec_econ = list(range(1,len(SECTORES_ECON)+1))
    w.add_cleanup(mod, ["Sector_Economico", "Nivel_Socioeconomico", "Tipo_Vivienda", "Institucion_Educativa", "Nivel_Educativo", "Grupo_Etario", "Discapacidad", "Religion", "Estado_Civil", "Idioma", "Etnia", "Sexo"])
    w.commit_module(mod)

def generar_personas(w: SqlWriter):
    mod = "03_personas"
    ids.personas = []
    for i in range(1, N_PERSONAS+1):
        sx = random.choice(ids.sexos)
        fn = fake.date_between(start_date="-80y", end_date="-1y")
        w.add(mod, f"INSERT INTO Persona(id_persona, nombres, apellidos, fecha_nacimiento, id_sexo, id_etnia, id_estado_civil, id_religion, numero_identificacion, es_anonimo) VALUES ({i}, {sql_str(fake.first_name())}, {sql_str(fake.last_name())}, {sql_date(fn)}, {sx}, {random.choice(ids.etnias)}, {random.choice(ids.ec)}, {random.choice(ids.religiones)}, '{random.randint(1000,9999)}', 0);")
        ids.personas.append((i, fn, sx))
        w.add(mod, f"INSERT INTO Domicilio(id_domicilio, id_persona, id_municipio, direccion, zona, es_actual) VALUES ({i}, {i}, {random.choice(ids.municipios)}, 'Calle {i}', '1', 1);")
    w.add_cleanup(mod, ["Domicilio", "Persona_Idioma", "Persona_Discapacidad", "Escolaridad_Persona", "Persona"])
    w.commit_module(mod)

def generar_empleo_hogar(w: SqlWriter):
    mod = "04_empleo_hogar"
    for i,(n,c) in enumerate(OCUPACIONES,1): w.add(mod, f"INSERT INTO Ocupacion(id_ocupacion, nombre_ocupacion, codigo_ciuo) VALUES ({i}, {sql_str(n)}, {sql_str(c)});")
    ids.ocupaciones = list(range(1,len(OCUPACIONES)+1))
    for i,t in enumerate(TIPOS_EMPLEO,1): w.add(mod, f"INSERT INTO Tipo_Empleo(id_tipo_empleo, nombre_tipo) VALUES ({i}, {sql_str(t)});")
    ids.tipo_empleo = list(range(1,len(TIPOS_EMPLEO)+1))
    for i,(n,f) in enumerate(COND_LABORAL,1): w.add(mod, f"INSERT INTO Condicion_Laboral(id_cond_laboral, nombre_cond_laboral, es_formal) VALUES ({i}, {sql_str(n)}, {f});")
    ids.cond_lab = list(range(1,len(COND_LABORAL)+1))
    ids.hogares = []
    for i in range(1, N_HOGARES+1):
        w.add(mod, f"INSERT INTO Hogar(id_hogar, id_municipio, id_tipo_vivienda, id_nivel_socio, numero_personas, ingreso_mensual_total) VALUES ({i}, {random.choice(ids.municipios)}, {random.choice(ids.tipo_viv)}, {random.choice(ids.socio)}, 4, 3000);")
        ids.hogares.append(i)
    w.add_cleanup(mod, ["Persona_Hogar", "Hogar", "Empleo_Persona", "Condicion_Laboral", "Tipo_Empleo", "Ocupacion"])
    w.commit_module(mod)

def generar_denuncias(w: SqlWriter):
    mod = "05_denuncias"
    for i,e in enumerate(EJES_VIOLENCIA,1): w.add(mod, f"INSERT INTO Eje_Violencia(id_eje_violencia, nombre_eje) VALUES ({i}, {sql_str(e)});")
    ids.tipos_den = []
    tid = 0
    for eje_idx, eje_nom in enumerate(EJES_VIOLENCIA, 1):
        for t_nom in TIPOS_DENUNCIA_POR_EJE.get(eje_nom, ["Otro"]):
            tid += 1
            w.add(mod, f"INSERT INTO Tipo_Denuncia(id_tipo_denuncia, id_eje_violencia, nombre_tipo) VALUES ({tid}, {eje_idx}, {sql_str(t_nom)});")
            ids.tipos_den.append((tid, eje_nom))
    for i,(n,s) in enumerate(INST_REPORTANTES,1): w.add(mod, f"INSERT INTO Institucion_Reportante(id_inst_reporte, nombre_institucion, siglas) VALUES ({i}, {sql_str(n)}, {sql_str(s)});")
    for i,e in enumerate(ESTADOS_DENUNCIA,1): w.add(mod, f"INSERT INTO Estado_Denuncia(id_estado_denuncia, nombre_estado) VALUES ({i}, {sql_str(e)});")
    ids.denuncias_list = []
    for i in range(1, N_DENUNCIAS+1):
        tden, eje_nom = random.choice(ids.tipos_den)
        fec = fake.date_between(start_date="-5y", end_date="today")
        w.add(mod, f"INSERT INTO Denuncia(id_denuncia, id_tipo_denuncia, id_municipio, id_inst_reporte, id_estado_denuncia, fecha_denuncia) VALUES ({i}, {tden}, {random.choice(ids.municipios)}, {random.randint(1,len(INST_REPORTANTES))}, 1, {sql_date(fec)});")
        ids.denuncias_list.append((i, eje_nom, fec))
    w.add_cleanup(mod, ["Seguimiento_Denuncia", "Persona_Denuncia", "Denuncia", "Estado_Denuncia", "Institucion_Reportante", "Tipo_Denuncia", "Eje_Violencia"])
    w.commit_module(mod)

def generar_hechos(w: SqlWriter):
    mod = "06_hechos"
    for i,c in enumerate(CLASIF_DELITO,1): w.add(mod, f"INSERT INTO Clasificacion_Delito(id_clasif_delito, nombre_clasif) VALUES ({i}, {sql_str(c)});")
    for i,(n,d,cl) in enumerate(TIPOS_HECHO,1): w.add(mod, f"INSERT INTO Tipo_Hecho_Delictivo(id_tipo_hecho, id_clasif_delito, nombre_tipo) VALUES ({i}, {cl}, {sql_str(n)});")
    for i,l in enumerate(LUGARES,1): w.add(mod, f"INSERT INTO Lugar_Ocurrencia(id_lugar_ocurr, nombre_lugar) VALUES ({i}, {sql_str(l)});")
    for i,a in enumerate(ARMAS,1): w.add(mod, f"INSERT INTO Arma_Utilizada(id_arma, nombre_arma) VALUES ({i}, {sql_str(a)});")
    for i,m in enumerate(MOVILES,1): w.add(mod, f"INSERT INTO Movil_Delito(id_movil, nombre_movil) VALUES ({i}, {sql_str(m)});")
    ids.hechos_list = []
    for i in range(1, N_HECHOS_DELICTIVOS+1):
        fec = fake.date_between(start_date="-5y", end_date="today")
        w.add(mod, f"INSERT INTO Hecho_Delictivo(id_hecho, id_tipo_hecho, id_municipio, id_lugar_ocurr, fecha_hecho, fue_resuelto) VALUES ({i}, {random.randint(1,len(TIPOS_HECHO))}, {random.choice(ids.municipios)}, {random.randint(1,len(LUGARES))}, {sql_date(fec)}, 0);")
        ids.hechos_list.append((i, fec))
    w.add_cleanup(mod, ["Agresor", "Victima", "Hecho_Movil", "Hecho_Arma", "Hecho_Delictivo", "Movil_Delito", "Arma_Utilizada", "Lugar_Ocurrencia", "Tipo_Hecho_Delictivo", "Clasificacion_Delito"])
    w.commit_module(mod)

def generar_forense(w: SqlWriter):
    mod = "07_forense"
    for i in range(1, 11): w.add(mod, f"INSERT INTO Laboratorio_Forense(id_lab_forense, id_municipio, nombre_lab) VALUES ({i}, {random.choice(ids.municipios)}, 'Lab {i}');")
    for i in range(1, 21): w.add(mod, f"INSERT INTO Forense(id_forense, id_lab_forense, id_persona, numero_colegiado) VALUES ({i}, {random.randint(1,10)}, {random.choice(ids.personas)[0]}, 'COL-{i}');")
    for i in range(1, N_NECROPSIAS+1):
        hecho = random.choice(ids.hechos_list)
        w.add(mod, f"INSERT INTO Necropsia(id_necropsia, id_hecho, id_forense, id_lab_forense, fecha_necropsia, causa_muerte) VALUES ({i}, {hecho[0]}, {random.randint(1,20)}, {random.randint(1,10)}, {sql_date(hecho[1])}, 'Trauma');")
    w.add_cleanup(mod, ["Exhumacion", "Necropsia", "Forense", "Laboratorio_Forense"])
    w.commit_module(mod)

def generar_sentencias(w: SqlWriter):
    mod = "08_sentencias"
    for i in range(1, 11): w.add(mod, f"INSERT INTO Juzgado(id_juzgado, id_municipio, nombre_juzgado) VALUES ({i}, {random.choice(ids.municipios)}, 'Juzgado {i}');")
    for i,(n,a) in enumerate(TIPOS_DELITO_JUZ,1): w.add(mod, f"INSERT INTO Tipo_Delito_Juzgado(id_tipo_delito_jz, nombre_tipo, articulo_legal) VALUES ({i}, {sql_str(n)}, {sql_str(a)});")
    for i,p in enumerate(PENAS,1): w.add(mod, f"INSERT INTO Pena(id_pena, nombre_pena) VALUES ({i}, {sql_str(p)});")
    for i in range(1, N_SENTENCIAS+1):
        w.add(mod, f"INSERT INTO Sentencia(id_sentencia, id_juzgado, id_tipo_delito_jz, id_pena, fecha_sentencia, es_condenatoria) VALUES ({i}, {random.randint(1,10)}, {random.randint(1,len(TIPOS_DELITO_JUZ))}, {random.randint(1,len(PENAS))}, '2023-01-01', 1);")
    w.add_cleanup(mod, ["Detalle_Sentencia", "Persona_Sentenciada", "Sentencia", "Pena", "Tipo_Delito_Juzgado", "Juzgado"])
    w.commit_module(mod)

def generar_violencia_mujer(w: SqlWriter):
    mod = "09_violencia_mujer"
    for i,t in enumerate(TIPOS_VM,1): w.add(mod, f"INSERT INTO Tipo_Violencia_Mujer(id_tipo_vm, nombre_tipo_vm) VALUES ({i}, {sql_str(t)});")
    for i,n in enumerate(CENTROS_AT_NOMBRES,1): w.add(mod, f"INSERT INTO Centro_Atencion(id_centro_at, id_municipio, nombre_centro) VALUES ({i}, {random.choice(ids.municipios)}, {sql_str(n)});")
    for i,t in enumerate(TIPOS_AT,1): w.add(mod, f"INSERT INTO Tipo_Atencion(id_tipo_at, nombre_tipo_at) VALUES ({i}, {sql_str(t)});")
    
    # Filtrar solo personas de sexo femenino (id_sexo = 1)
    pers_fem = [p[0] for p in ids.personas if p[2] == 1]
    
    for i in range(1, N_HVM+1):
        # Aseguramos que la víctima exista y preferiblemente sea mujer
        vic = random.choice(pers_fem) if pers_fem else random.choice(ids.personas)[0]
        
        w.add(mod, f"INSERT INTO Hecho_Violencia_Mujer(id_hecho_vm, id_tipo_vm, id_municipio, id_victima_pers, fecha_hecho) VALUES ({i}, {random.randint(1,len(TIPOS_VM))}, {random.choice(ids.municipios)}, {vic}, '2023-05-10');")
    w.add_cleanup(mod, ["Atencion_Mujer", "Hecho_Violencia_Mujer", "Tipo_Atencion", "Centro_Atencion", "Tipo_Violencia_Mujer"])
    w.commit_module(mod)

def generar_vif(w: SqlWriter):
    mod = "10_vif"
    for i,t in enumerate(TIPOS_VIF,1): w.add(mod, f"INSERT INTO Tipo_VIF(id_tipo_vif, nombre_tipo_vif) VALUES ({i}, {sql_str(t)});")
    for i,r in enumerate(RELACIONES_AV,1): w.add(mod, f"INSERT INTO Relacion_Agresor_Victima(id_rel_agr_vict, nombre_relacion) VALUES ({i}, {sql_str(r)});")
    for i in range(1, N_HVIF+1):
        vic = random.choice(ids.personas)[0]
        w.add(mod, f"INSERT INTO Hecho_VIF(id_hecho_vif, id_tipo_vif, id_rel_agr_vict, id_municipio, id_victima_pers, fecha_hecho) VALUES ({i}, {random.randint(1,len(TIPOS_VIF))}, {random.randint(1,len(RELACIONES_AV))}, {random.choice(ids.municipios)}, {vic}, '2023-06-15');")
    w.add_cleanup(mod, ["Hecho_VIF", "Relacion_Agresor_Victima", "Tipo_VIF"])
    w.commit_module(mod)

def generar_violencia_infantil(w: SqlWriter):
    mod = "11_violencia_infantil"
    for i,t in enumerate(TIPOS_VI,1): w.add(mod, f"INSERT INTO Tipo_Violencia_Infantil(id_tipo_vi, nombre_tipo_vi) VALUES ({i}, {sql_str(t)});")
    for i in range(1, N_HVI+1):
        vic = random.choice(ids.personas)[0]
        w.add(mod, f"INSERT INTO Hecho_Violencia_Infantil(id_hecho_vi, id_tipo_vi, id_municipio, id_victima_pers, fecha_hecho) VALUES ({i}, {random.randint(1,len(TIPOS_VI))}, {random.choice(ids.municipios)}, {vic}, '2023-07-20');")
    w.add_cleanup(mod, ["Control_Prenatal", "Embarazo_Adolescente", "Trabajo_Infantil", "Hecho_Violencia_Infantil", "Jornada_Trabajo_Infantil", "Tipo_Trabajo_Infantil", "Sector_Trabajo_Infantil", "Tipo_Violencia_Infantil"])
    w.commit_module(mod)

def generar_discriminacion(w: SqlWriter):
    mod = "12_discriminacion"
    for i,t in enumerate(TIPOS_DISC,1): w.add(mod, f"INSERT INTO Tipo_Discriminacion(id_tipo_disc, nombre_tipo_disc) VALUES ({i}, {sql_str(t)});")
    for i,g in enumerate(GRUPOS_POB,1): w.add(mod, f"INSERT INTO Grupo_Poblacional(id_grupo_pob, nombre_grupo) VALUES ({i}, {sql_str(g)});")
    for i in range(1, N_HDISC+1):
        vic = random.choice(ids.personas)[0]
        w.add(mod, f"INSERT INTO Hecho_Discriminacion(id_hecho_disc, id_tipo_disc, id_grupo_pob, id_municipio, id_victima_pers, fecha_hecho) VALUES ({i}, {random.randint(1,len(TIPOS_DISC))}, {random.randint(1,len(GRUPOS_POB))}, {random.choice(ids.municipios)}, {vic}, '2023-08-25');")
    w.add_cleanup(mod, ["Hecho_Discriminacion", "Grupo_Poblacional", "Tipo_Discriminacion"])
    w.commit_module(mod)

def generar_faltas(w: SqlWriter):
    mod = "13_faltas"
    for i,(n,a) in enumerate(TIPOS_FALTA,1): w.add(mod, f"INSERT INTO Tipo_Falta_Judicial(id_tipo_falta, nombre_tipo_falta, articulo_legal) VALUES ({i}, {sql_str(n)}, {sql_str(a)});")
    for i,(n,mn,mx) in enumerate(SANCIONES,1): w.add(mod, f"INSERT INTO Sancion_Falta(id_sancion, nombre_sancion, monto_min, monto_max) VALUES ({i}, {sql_str(n)}, {mn}, {mx});")
    for i in range(1, N_FALTAS_JUD+1):
        per = random.choice(ids.personas)[0]
        w.add(mod, f"INSERT INTO Falta_Judicial(id_falta_jud, id_tipo_falta, id_sancion, id_municipio, id_persona, fecha_falta) VALUES ({i}, {random.randint(1,len(TIPOS_FALTA))}, {random.randint(1,len(SANCIONES))}, {random.choice(ids.municipios)}, {per}, '2023-09-30');")
    w.add_cleanup(mod, ["Falta_Judicial", "Sancion_Falta", "Tipo_Falta_Judicial"])
    w.commit_module(mod)

def generar_salud(w: SqlWriter):
    mod = "14_salud"
    for i,(c,n) in enumerate(CAPITULOS_CIE10,1): w.add(mod, f"INSERT INTO Capitulo_CIE10(id_cap_cie10, codigo_capitulo, nombre_capitulo) VALUES ({i}, {sql_str(c)}, {sql_str(n)});")
    for i,(cap,cod,nom) in enumerate(CIE10_DETALLE,1): w.add(mod, f"INSERT INTO CIE10(id_cie10, id_cap_cie10, codigo_cie10, nombre_diag) VALUES ({i}, {cap}, {sql_str(cod)}, {sql_str(nom)});")
    for i,c in enumerate(CATEGORIAS_INDIC,1): w.add(mod, f"INSERT INTO Categoria_Indicador(id_cat_indic, nombre_categoria) VALUES ({i}, {sql_str(c)});")
    for i,(cat,n,u) in enumerate(INDICADORES_SALUD,1): w.add(mod, f"INSERT INTO Indicador_Salud(id_indicador, id_cat_indic, nombre_indicador, unidad_medida) VALUES ({i}, {cat}, {sql_str(n)}, {sql_str(u)});")
    for i in range(1, N_REG_SALUD+1):
        w.add(mod, f"INSERT INTO Registro_Salud(id_reg_salud, id_indicador, id_municipio, id_grupo_etario, id_sexo, anio, cantidad_casos) VALUES ({i}, {random.randint(1,len(INDICADORES_SALUD))}, {random.choice(ids.municipios)}, 1, 1, 2023, 100);")
    w.add_cleanup(mod, ["Registro_Morbilidad_Materna", "Registro_Enfermedad_Vector", "Registro_Enfermedad_Cronica", "Registro_Desnutricion", "Registro_Salud", "Complicacion_Embarazo", "Vector_Enfermedad", "Centro_Salud", "Tipo_Centro_Salud", "Indicador_Salud", "Categoria_Indicador", "CIE10", "Capitulo_CIE10"])
    w.commit_module(mod)

def generar_encuestas(w: SqlWriter):
    mod = "15_encuestas"
    for i,t in enumerate(TIPOS_ENCUESTA,1): w.add(mod, f"INSERT INTO Tipo_Encuesta(id_tipo_enc, nombre_tipo_enc) VALUES ({i}, {sql_str(t)});")
    for i in range(1, 501):
        per = random.choice(ids.personas)[0]
        hog = random.choice(ids.hogares)
        w.add(mod, f"INSERT INTO Encuesta(id_encuesta, id_tipo_enc, id_persona, id_hogar, fecha_encuesta) VALUES ({i}, {random.randint(1,len(TIPOS_ENCUESTA))}, {per}, {hog}, '2023-11-15');")
    w.add_cleanup(mod, ["Respuesta_Encuesta", "Encuesta", "Tipo_Encuesta"])
    w.commit_module(mod)

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--outdir", default=str(OUTPUT_DIR))
    args = parser.parse_args()

    random.seed(args.seed)
    Faker.seed(args.seed)
    outdir = Path(args.outdir)

    print(f"=== GENERADOR DE DATOS INTEGRAL - PROYECTO 2 ===")
    w = SqlWriter(outdir)
    
    # Orden de ejecución para mantener integridad referencial
    generar_geografia(w)
    generar_catalogos(w)
    generar_personas(w)
    generar_empleo_hogar(w)
    generar_denuncias(w)
    generar_hechos(w)
    generar_forense(w)
    generar_sentencias(w)
    generar_violencia_mujer(w)
    generar_vif(w)
    generar_violencia_infantil(w)
    generar_discriminacion(w)
    generar_faltas(w)
    generar_salud(w)
    generar_encuestas(w)

    print("\n[Escribiendo archivos .sql con limpieza automática...]")
    w.write_all()
    print(f"\n[LISTO] Los archivos se encuentran en '{outdir.name}'")

if __name__ == "__main__":
    main()
