#/usr/env/python3

class InputDeck:
    """ InputDeck class from which other concrete examples
    should inherit, for example MCNPInputDeck will inhert
    from this class
    """
    filename = ""
    file_lines = ""
    title = ""
    total_num_lines = 0

    # if doing a direct tranlation store here
    # TODO maybe these should be dictionaries by index
    cell_list = []
    surface_list = []
    last_free_surface_index = 0
    importance_list = {} # dictionary of importances
    material_list = {}
    transform_list = {}
    
    # this calculates coordinates that bound the placement of
    # surfaces we do this by checking the manifold surfaces
    # for the their value and adding to the list
    bounding_coordinates = [0,0,0,0,0,0]
    
    # if doing a hierachy transform store here
    cell_card_collection = {}
    surface_card_collection = {}
    
    def __init__(self, filename):
        self.filename = filename

    # find the cell with a given id
    def find_cell(self, cell_id):
        for cell in self.cell_list:
            if str(cell.cell_id) == str(cell_id):
                return cell
        return None
        
    # read the whole file into a big list for further
    # procesing
    def read(self):
        with open(self.filename, 'rU', errors="replace") as f:
            self.file_lines = f.readlines()
            
        # sometimes truely monstrous people stuff weird
        # characters into textfiles
        self.file_lines = [x.lower() for x in self.file_lines]

        self.total_num_lines = len(self.file_lines)

    # access a surface with a particular id
    def get_surface_with_id(self, id):
        for surface in self.surface_list:
            if surface.surface_id == id :
                return surface
        return None 

    # access a cell with a particular id
    def get_cell_with_id(self, id):
        for cell in self.cell_list:
            if cell.cell_id == id :
                return cell
        return None 


    def from_input(self,InputDeckClass):
        InputDeck.filename = InputDeckClass.filename
        InputDeck.title = InputDeckClass.title
        InputDeck.cell_list = InputDeckClass.cell_list
        InputDeck.surfcace_list = InputDeckClass.surface_list
        InputDeck.material_list = InputDeckClass.material_list
        return

    # step through each cell and determine if the cell can 
    # be split into multiple simple subcells
    def split_unions(self):
        # update the cell definition - loop over all cells
        for idx, cell in enumerate(self.cell_list):
            # look through the interpreted cell and determine if we can pattern
            # match any splitable unions - this will look like (stuff):(stuff):(stuff)
            # so we could make 3 cells from that
            continue
