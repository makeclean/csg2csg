#include <fstream>
#include <string>

class LineExtractor {
  public:
  // Constructor
  LineExtractor(std::string inputdeck);
  // Destructor
  ~LineExtractor();

  public:
  //
  void get_next();
  const std::string& peekLine();
  const std::string& peekLine(int& lineno);
  std::string takeLine();
  std::string takeLine(int& lineno);
  bool hasLine();
  int getLineCount();
  static void strlower(std::string& string);

  private:
  char comment_char;
  std::string input_deck;
  std::ifstream input;
  std::string next_line;
  bool has_next;
  int next_line_idx;

  /* 
   * Take note of the following, from mcnp5 manual page 1-3:
   * Tab characters in the input file are converted to one or more blanks, such that the character
   * following the tab will be positioned at the next tab stop. Tab stops are set every 8 characters,
   * i.e., 9, 17, 25, etc. The limit of input lines to 80 columns applies after tabs are expanded into blank
   * spaces. </snip>
   * I don't know whether this needs to be addressed to handle corner cases for line continuation, etc.
   * currently, it is not addressed.
   */

};