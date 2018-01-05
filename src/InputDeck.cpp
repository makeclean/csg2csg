#include "InputDeck.hpp"

/******************
 * INPUT DECK Class
 ******************/

#define OPT_VERBOSE true

// Constructor 
InputDeck::InputDeck(std::string filename) {  
    fileName = filename;
}

InputDeck::~InputDeck(){
}

// open the input deck for reading and set the line extractor to 
// the correct stream
void InputDeck::OpenFile() {
  //std::ifstream input_deck(filenName);
  lines = new LineExtractor(fileName);
}

// build the input deck
InputDeck* InputDeck::build() {

  parseTitle();
  parseCells();
  parseSurfaces();
  parseDataCards();
  copyMacrobodies();

  while ( lines->hasLine()){ lines->takeLine(); }
  if( OPT_VERBOSE ) { std::cout << "Total lines read: " << lines->getLineCount()  <<  std::endl; }

  return this;
}

/* handle line continuations: return true if the next line should be treated as part of 
 * the current line */
bool InputDeck::do_line_continuation( token_list_t& token_buffer, char continuation_char ){

  /* check for final character being & */
  std::string last_token = token_buffer.at(token_buffer.size()-1);
  if( last_token.at(last_token.length()-1) == continuation_char ){

    if( last_token.length() == 1 ){
      token_buffer.pop_back();
    }
    else{
      last_token.resize(last_token.length()-1);
      token_buffer.at(token_buffer.size()-1).swap( last_token );
    }
    
    return true;
  } 
  /* check for next line beginning with five spaces */
  else if( lines->hasLine() && lines->peekLine().find("     ") == 0){
      /* but don't count it as a continuation if the line is entirely blank */
      if( lines->peekLine().find_first_not_of(" \t\n") != std::string::npos ){
          return true;
      }
  }
  
  return false;
}






InputDeck::cell_card_list InputDeck::getCellsOfUniverse( int universe ){

  cell_card_list ret;
  for( cell_card_list::iterator i = cells.begin(); i!=cells.end(); ++i){
    CellCard* c = *i;
    if( std::abs(c->getUniverse()) == universe ){
      ret.push_back( *i );
    }
  }
  return ret;

}


CellCard* InputDeck::lookup_cell_card(int ident){
  assert( cell_map.find(ident) != cell_map.end() );
  return (*cell_map.find(ident)).second;
}

SurfaceCard* InputDeck::lookup_surface_card(int ident){
  assert( surface_map.find(ident) != surface_map.end() );
  return (*surface_map.find(ident)).second;
}

DataCard* InputDeck::lookup_data_card( const DataCard::id_t& ident ){
  assert( datacard_map.find(ident) != datacard_map.end() );
  return (*datacard_map.find(ident)).second;
}

 /******************
 * PARSING UTILITIES 
 ******************/

class InputDeck::LineExtractor{

protected:
  std::istream& input;
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

  void get_next(){

    bool comment; 
    do{
      
      if(!std::getline(input, next_line)){
        has_next = false;
      }
      else{

        comment = false;
        next_line_idx++;

        // strip trailing carriage return, if any
        if(next_line.length() > 0 && *(next_line.rbegin()) == '\r')
          next_line.resize(next_line.size()-1);
        
        // convert to lowercase
        strlower(next_line);

        // Append a space, to catch blank comment lines (e.g. "c\n") that would otherwise not meet
        // the MCNP comment card spec ("a C anywhere in columns 1-5 followed by at least one blank.")
        // I have seen lines like "c\n" or " c\n" as complete comment cards in practice, so MCNP must 
        // accept them.
        next_line.append(" ");

        // We want to find "c " within the first five
        // columns, but not if the c has anything other than a space before it.
        size_t idx = next_line.find("c ");
        if( idx < 5 ){
          if( idx == 0 || next_line.at(idx-1) == ' '){
            comment = true;
          }
        }
      }
    }
    while( has_next && comment );
    // iterate until next_line is not a comment line.

  }

public:
  LineExtractor( std::istream& input_p ) : 
    input(input_p), next_line("*NO INPUT*"), has_next(true), next_line_idx(0)
  {
    get_next();
  }
  
  const std::string& peekLine() const {
    if( has_next ) return next_line;
    else throw std::runtime_error("LineExtractor out of lines, cannot peekLine().");
  }

  const std::string& peekLine( int& lineno ) const {
    lineno = next_line_idx;
    return peekLine();
  }

  std::string takeLine() { 
    if( has_next ){
      std::string ret = next_line;
      get_next();
      return ret;
    }
    else throw std::runtime_error("LineExtractor out of lines, cannot takeLine().");
  }

  std::string takeLine( int& lineno ){
    lineno = next_line_idx;
    return takeLine();
  }

  bool hasLine() const{
    return has_next;
  }

  /**
   * @return the file line number of the next line (as will be returned by either
   * peekLine or takeLine) 
   */
  int getLineCount() const{
    return next_line_idx;
  }

}; 