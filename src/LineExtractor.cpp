#include "LineExtractor.hpp"

LineExtractor::LineExtractor(std::string inputdeck) : 
    input_deck(inputdeck), next_line("*NO INPUT*"), has_next(true), 
    next_line_idx(0) {
  input_deck = inputdeck;
  input.open(input_deck,std::ios::in);
  get_next();
}

// get the next line set in the next_line variable
void LineExtractor::get_next() {
    bool comment; 
    do {
        if(!std::getline(input, next_line)) {
          has_next = false;
        } else { 

        comment = false;
        next_line_idx++;

        // strip trailing carriage return, if any
        if(next_line.length() > 0 && *(next_line.rbegin()) == '\r')
          next_line.resize(next_line.size()-1);
        
        // convert to lowercase
        strlower(next_line);

        // TODO this is MCNP specific, may need code specific thing to deal
        // with other codes comment lines

        // Append a space, to catch blank comment lines (e.g. "c\n") that would otherwise not meet
        // the MCNP comment card spec ("a C anywhere in columns 1-5 followed by at least one blank.")
        // I have seen lines like "c\n" or " c\n" as complete comment cards in practice, so MCNP must 
        // accept them.
        next_line.append(" ");

        // We want to find "c " within the first five
        // columns, but not if the c has anything other than a space before it.
        size_t idx = next_line.find("c ");
        if( idx < 5 ) {
          if( idx == 0 || next_line.at(idx-1) == ' ') {
            comment = true;
          }
        }

      }
    }
    while( has_next && comment );
    // iterate until next_line is not a comment line.
}

// return the next line
const std::string& LineExtractor::peekLine() {
    if( has_next ) return next_line;
    else throw std::runtime_error("LineExtractor out of lines, cannot peekLine().");
}

// return the next line and set the line number
const std::string& LineExtractor::peekLine( int& lineno ) {
    lineno = next_line_idx;
    return peekLine();
}

// get the next line and set the next line variable
std::string LineExtractor::takeLine() { 
    if( has_next ){
      std::string ret = next_line;
      get_next();
      return ret;
    }
    else throw std::runtime_error("LineExtractor out of lines, cannot takeLine().");
}

// take the next line and set the line number
std::string LineExtractor::takeLine( int& lineno ){
    lineno = next_line_idx;
    return takeLine();
}

// if we have the next line set or not
bool LineExtractor::hasLine() {
    return has_next;
}

/**
  * @return the file line number of the next line (as will be returned by either
  * peekLine or takeLine) 
  */
int LineExtractor::getLineCount() {
    return next_line_idx;
}

void LineExtractor::strlower( std::string& str ){
  // convert to lowercase
  for(size_t i = 0; i < str.length(); ++i){
    str[i] = tolower( str.at(i) );
  }
}