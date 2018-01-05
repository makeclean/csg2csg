#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <fstream>

// Virtual Class which all CSG Input operations should
// base off

#ifndef INPUTDECK_HPP 
#define INPUTDECK_HPP 1

InputDeck {
  public:
  InputDeck(std::string filename);
  ~InputDeck();
  public:
  virtual void parseCells()

  private:
  std::map<int,CellCard*> cells; /// maps of cell cards by id
  std::map<int,SurfaceCard*> surfaces; /// maps of surface cards by id
  std::vector<DataCard*> datacards; /// collection fo datacards
  
  LineExtractor* lines; /// line extractor class
  std::string fileName; /// the filename to be input
};

#endif
  
