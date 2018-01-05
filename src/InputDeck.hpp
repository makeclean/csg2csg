#include <ifstream>
// Virtual Class which all CSG Input operations should
// base off
class InputDeck {
  public:
    virtual void build(std::ifstream input);
    virtual void parseTitle();
    virtual void parseCells();
    virtual void parseSurfaces();
    virtual void parseDataCards();
    virtual void copyMacroBodies();
  private:
    virtual CellCard* lookup_cell_card(int index);
    virtual SurfaceCard* lookup_surface_card(int index);
    virtual DataCard* lookup_data_card(int index);
}

  
