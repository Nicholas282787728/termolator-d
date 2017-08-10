
from typing import List, Dict
from DataDef import POSTag

#
#   Dedicated module for cross module dictionaries and other (static, read only) global vars
#   This fixes issues with these vars being reset bu @jep (likely due to realoding of modules after global vars have been initialized)
#
nom_dict: Dict[str, str] = {}
pos_dict: Dict[str, List[POSTag]] = {}
