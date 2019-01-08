#/usr/env/python3

from CellCard import CellCard
import xml.etree.ElementTree as ET

# turn the generic operation type into a mcnp relevant text string
def openmc_op_from_generic(Operation):
    # if we are not of type operator - we are string do nowt
    if not isinstance(Operation, CellCard.OperationType):
        return Operation
    else:
        # otherwise we need to do something
        if Operation is CellCard.OperationType["NOT"]:
            string = " ~ "
        elif Operation is CellCard.OperationType["AND"]:
            string = " "
        elif Operation is CellCard.OperationType["UNION"]:
            string = " | "
        else:
            string = "unknown operation"
    # return the operation
    return string

# generate the strings that define the xml version of the
# cell
def get_openmc_cell_info(cell):
    cell_id = str(cell.cell_id)
    material_number = str(cell.cell_material_number)

    if material_number == "0":
        material_number = "void"
        
    # make the string to define the cell    
    operation = ''.join(openmc_op_from_generic(e) for e in cell.cell_interpreted)
    operation = ''.join(str(e) for e in operation)
    operation = operation.replace("("," ( ")
    operation = operation.replace(")"," ) ")
    universe = cell.cell_universe
    fill = cell.cell_fill

    if cell.cell_universe_rotation != 0:
        rotation = ""
        rotation += str(cell.cell_universe_rotation[0]) + " "
        rotation += str(cell.cell_universe_rotation[4]) + " "
        rotation += str(cell.cell_universe_rotation[8])
    else:
        rotation = "0 0 0"

    if cell.cell_universe_offset != 0:
        translation = ""
        translation += str(cell.cell_universe_offset[0]) + " "
        translation += str(cell.cell_universe_offset[1]) + " "
        translation += str(cell.cell_universe_offset[2]) + " "
    else:
        translation = "0 0 0"

    return (cell_id, material_number, operation,universe,fill,rotation,translation)
    
    
def write_openmc_cell(cell, geometry_tree):

    (cell_id, material_number, description,
    universe,fill,rotation,translation) = get_openmc_cell_info(cell)
    
    if fill != 0:
        ET.SubElement(geometry_tree, "cell", id = str(cell_id),
                      region = str(description),
                      universe = str(universe),
                      fill = str(fill),
                      rotation = str(rotation),
                      translation = str(translation))
    else:
        ET.SubElement(geometry_tree, "cell", id = str(cell_id),
                      material=str(material_number),
                      region = str(description),
                      universe = str(universe))




#
class OpenMCCell(CellCard):
    def __init__(self, card_string):
        CellCard.__init__(self, card_string)
