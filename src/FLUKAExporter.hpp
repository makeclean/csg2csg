#include "MCNPInput.cpp"
#include "Exporter.hpp"

class FLUKAExporter : public Exporter {
  public:
  FLUKAExporter(InputDeck deck,std::string output);
  ~FLUKAExporter();
  public:
  void Export();
};
