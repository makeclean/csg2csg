#/usr/env/python3

from Input import InputDeck
from FLUKASurfaceCard import FLUKASurfaceCard, write_fluka_surface
from FLUKACellCard import FLUKACellCard, write_fluka_cell
#from FLUKAMaterialCard import FLUKAMaterialCard, write_fluka_material

zz_to_remove = [34000,37000,39000,44000,45000,59000,61000,63000,
                66000,67000,68000,69000,70000,76000,81000,84000,
                85000,86000,87000,88000,89000,91000,93000]

zz_to_collapse = [4000,6000,7000,8000,9000,10000,11000,12000,13000,
                  14000,15000,16000,17000,19000,20000,21000,22000,
                  23000,24000,25000,26000,27000,28000,29000,30000,
                  31000,32000,33000,35000,36000,52000,56000,57000,
                  58000,60000,62000,64000,65000,71000,72000,73000,
                  74000,75000,77000,78000,79000,80000,82000,83000,
                  94000,95000]

zz_to_fluka = {1000:"HYDROGEN",1001:"HYDROG-1",1002:"DEUTERIU", 
               1003:"TRITIUM",
               2000:"HELIUM", 2003:"HELIUM-3",2004:"HELIUM-4",
               3000:"LITHIUM", 3006:"LITHIU-6", 3007:"LITHIU-7",
               4000:"BERYLLIU",
               5000:"BORON", 5010:"BORON-10", 5011:"BORON-11",
               6000:"CARBON",
               7000:"NITROGEN",
               8000:"OXYGEN",
               9000:"FLUORINE",
               10000:"NEON",
               11000:"SODIUM",
               12000:"MAGNESIU",
               13000:"ALUMINUM",
               14000:"SILICON",
               15000:"PHOSPHO",
               16000:"SULFUR",
               17000:"CHLORINE",
               18000:"ARGON", 18040:"ARGON-40",
               19000:"POTASSIU",
               20000:"CALCIUM",
               21000:"SCANDIUM",
               22000:"TITANIUM",
               23000:"VANADIUM",
               24000:"CHROMIUM",
               25000:"MANGANES",
               26000:"IRON",
               27000:"COBALT",
               28000:"NICKEL",
               29000:"COPPER",
               30000:"ZINC",
               31000:"GALLIUM",
               32000:"GERMANIU",
               33000:"ARSENIC",
               35000:"BROMINE",
               36000:"KRYPTON",
               38000:"STRONTIU",38090:"90-SR",
               40000:"ZIRCONIU",
               41000:"NIOBIUM",
               42000:"MOLYBDEN",
               43000:"99-TC",
               46000:"PALLADIU",
               47000:"SILVER",
               48000:"CADMIUM",
               49000:"INDIUM",
               50000:"TIN",
               51000:"ANTIMONY",
               53000:"IODINE",53129:"129-I",
               54000:"XENON",54124:"124-XE",54126:"126-XE",54128:"128-XE", 54129:"129-XE", 54130:"130-XE", 54131:"131-XE", 54132:"132-XE", 54134:"134-XE",54135:"135-XE",54136:"136-XE",
               55000:"CESIUM",55135:"135-CS",55137:"137-CS",
               56000:"BARIUM",
               57000:"LANTHANU",
               58000:"CERIUM",
               60000:"NEODYMIU",
               62000:"SAMARIUM",
               64000:"GADOLINI",
               65000:"TERBIUM",
               71000:"LUTETIUM",
               72000:"HAFNIUM",
               73000:"TANTALUM",
               74000:"TUNGSTEN",
               75000:"RHENIUM",
               77000:"IRIDIUM",
               78000:"PLATINUM",
               79000:"GOLD",
               80000:"MERCURY",
               82000:"LEAD",
               83000:"BISMUTH",
               90230:"230-TH",90232:"232-TH",
               92233:"233-U",92234:"234-U",92235:"235-U",92238:"238-U",
               94239:"239-PU",
               95241:"241-AM"}


class FLUKAInput(InputDeck):
    """ FlukaInput class - does the actual processing
    """

    # constructor
    def __init__(self,filename = ""):
        InputDeck.__init__(self,filename)

    # write the fluka input deck ruler
    def __write_ruler(self, filestream):
        filestream.write("*...+....1....+....2....+....3....+....4" +
                         "....+....5....+....6....+....7....+....8\n")

        
    # Write the Serpent Cell definitions
    def __write_fluka_cells(self, filestream):
        filestream.write("* --- cell definitions --- *\n")
        for cell in self.cell_list:
            write_fluka_cell(filestream,cell)
        filestream.write("END\n")
        filestream.write("GEOEND\n")
        return
    
    # write the serpent surface definitions 
    def __write_fluka_surfaces(self, filestream):
        filestream.write("* --- surface definitions --- *\n")
        self.__write_ruler(filestream)
        filestream.write("GEOBEGIN                                                              COMBNAME\n")
        filestream.write("    0    0\n")
        for surface in self.surface_list:
            write_fluka_surface(filestream,surface)
        filestream.write("END\n")
        return

    # write the material assignments
    def __write_fluka_assignmats(self, filestream):
        self.__write_ruler(filestream)
        for cell in self.cell_list:
            # needs to be 10 chars
            filestream.write("ASSIGNMA C" + str(cell.cell_id) + " M" + str(cell.cell_material_number+ "\n")
        return

    # write the material compositions
    def __write_fluka_materials(self, filestream):
        filestream.write("* --- material definitions --- *\n")
        self.__write_ruler(filestream)

        # first loop through the materials and build the unqiue list
        # of fluka based materials

        for material in self.material_list:
            write_fluka_material(filestream, self.material_list[material])
            write_fluka_compound(filestream, self.material_list[material])
            write_fluka_lowmat(filestream, self.material_list[material])
        return

    # main write serpent method, depending upon where the geometry
    # came from 
    def write_fluka(self, filename, flat = True):
        f = open(filename,'w')
        self.__write_ruler(f)
        f.write("TITLE\n input deck automatically created by csg2csg\n")
        self.__write_ruler(f)
        self.__write_fluka_surfaces(f)
        self.__write_ruler(f)
        self.__write_fluka_cells(f)
        self.__write_ruler(f)
#        self.__write_fluka_materials(f)
        self.__write_ruler(f)
        f.write("STOP\n")
        f.close()
