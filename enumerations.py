from enum import Enum

class GradDidactic(str, Enum):
    asis='asist'
    sef_lucr='sef lucr'
    conf='conf'
    prof='prof'

class TipAsociere(str, Enum):
    titular='titular'
    asociat='asociat'
    extern='extern'

class CicluStudii(str, Enum):
    licenta='licenta'
    master='master'

class TipDisciplina(str, Enum):
    impusa='impusa'
    optionala='optionala'
    liber_aleasa='liber aleasa'

class CategorieDisciplina(str, Enum):
    domeniu='domeniu'
    specialitate='specialitate'
    adiacenta='adiacenta'

class TipExaminare(str, Enum):
    examen='examen'
    colocviu='colocviu'