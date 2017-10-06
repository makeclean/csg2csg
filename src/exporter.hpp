

class Exporter {
  public:
  // Constructor
  Exporter(InputDeck deck, std::string output) {
    SetOutput(output);
    SetDeck(deck);
  }

  // Destructor
  virtual ~Exporter(){};

  virtual void Export(){};
  
  private:
  void SetOutput(std::string output) {
   outputfile = output;
  }
  void SetDeck(InputDeck deck) {
    this->deck = deck;
  }
   
  private:
    std::string outputfile;
    InputDeck deck;
};
