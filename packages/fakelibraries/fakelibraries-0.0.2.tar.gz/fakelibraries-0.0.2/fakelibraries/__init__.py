import random
from datetime import datetime

# Patient ID
def patient_id():
    random_id = ' '.join([str(random.randint(0, 999)).zfill(3) for i in range(3)])
    return random_id

# pracID or patid or SYSTEM_ID_E
def prac_id():
    random_id = ' '.join([str(random.randint(0, 999)).zfill(2) for i in range(2)])
    return random_id

# e_cr_patid
def e_cr_patid():
    random_id = '_'.join([str(random.randint(0, 999)).zfill(2) for i in range(4)])
    return random_id

# RowID
def row_id():
    random_id = ''.join([str(random.randint(0, 999)).zfill(1) for i in range(3)])
    return random_id

# SourceItemID
def sourse_item_id():
    random_id = '-'.join([str(random.randint(999, 9999)).zfill(1) for i in range(3)])
    return random_id

# MHMDS Person ID
def mhmds_person_id():
    random_id = ' '.join([str(random.randint(1000, 9999)).zfill(1) for i in range(2)])
    return random_id

# MHMDS Spell ID
def mhmds_spell_id():
    random_id = ' '.join([str(random.randint(1000, 9999)).zfill(1) for i in range(3)])
    return random_id
