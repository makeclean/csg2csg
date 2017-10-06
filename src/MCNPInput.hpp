#ifndef MCNP_INPUT_FORMAT_H
#define MCNP_INPUT_FORMAT_H

#include <vector>
#include <map>
#include <iosfwd>
#include <string>

typedef std::vector< std::string > token_list_t;

#include "dataref.hpp"
#include "geometry.hpp"

class InputDeck;

/**
 * Superclass of all cards in the input deck
 */
class Card{
protected:
  InputDeck& parent_deck;

  Card( InputDeck& deck_p ):
    parent_deck(deck_p)
  {}

  virtual ~Card(){}

public:
  InputDeck& getDeck() { return parent_deck; }

};

// forward defs
class Transform;
class Fill;

/**
 * Cell card
 */
class CellCard : public Card {

public:
  enum geom_token_t {INTERSECT, UNION, COMPLEMENT, LPAREN, RPAREN, CELLNUM, SURFNUM, MBODYFACET};
  // for CELLNUM and SURFNUM the second item in the geom_list_entry is the given number 
  // (possibly negative for surfaces)
  // for MBODYFACET it is  (cell number*10 + facet number) * sense (where sense=1 or -1)
  typedef std::pair<enum geom_token_t, int> geom_list_entry_t;
  typedef std::vector<geom_list_entry_t> geom_list_t;

  enum lattice_type_t { NONE = 0, HEXAHEDRAL = 1, HEXAGONAL = 2 };

protected:
  
  CellCard( InputDeck& deck );

private: 
  // never defined and should never be called
  CellCard( const CellCard& c );
  CellCard& operator=( const CellCard& c );

public:
  
  virtual int getIdent() const = 0; 
  virtual const geom_list_t getGeom() const = 0; 

  virtual const DataRef<Transform>& getTrcl() const = 0; 

  virtual int getUniverse() const = 0;
  virtual bool hasFill() const = 0;
  virtual const Fill& getFill() const = 0;
  
  virtual bool isLattice() const = 0;
  virtual lattice_type_t getLatticeType() const = 0;
  virtual const Lattice& getLattice() const = 0;

  virtual int getMat() const = 0;
  virtual double getRho() const = 0;
  virtual const std::map<char,double>& getImportances() const = 0;

  virtual void print( std::ostream& s ) const = 0; 

};

std::ostream& operator<<(std::ostream& str, const CellCard::geom_list_entry_t& t );


/**
 * Surface Card
 */
class SurfaceCard : public Card {
protected:
  int ident, tx_id;
  DataRef<Transform> *coord_xform;
  std::string mnemonic;
  std::vector<double> args;

public:
  SurfaceCard( InputDeck& deck, const token_list_t tokens );
  SurfaceCard( InputDeck& deck, const SurfaceCard s, int facetNum );

  int getIdent() const { return ident; } 
  int getTxid() const { return tx_id; }
  void print( std::ostream& s ) const ;

  const DataRef<Transform>& getTransform() const ; 
  const std::string& getMnemonic() const { return mnemonic; }
  const std::vector<double>& getArgs() const { return args; }


  std::pair<Vector3d,double> getPlaneParams() const;
  std::vector< std::pair<Vector3d, double> > getMacrobodyPlaneParams() const;
};

/**
 * Data cards
 */

class DataCard : public Card {

public:
  typedef enum { TR, OTHER } kind;
  typedef std::pair< kind, int > id_t;

  DataCard( InputDeck& deck ) : Card( deck ) {}

  virtual void print( std::ostream& str ) = 0;
  virtual kind getKind(){ return OTHER; }

};


/**
 * Main interface to MCNP reader: the InputDeck 
 */
class InputDeck{

public:
  typedef std::vector< CellCard* > cell_card_list;
  typedef std::vector< SurfaceCard* > surface_card_list;
  typedef std::vector< DataCard* > data_card_list;

protected:
  class LineExtractor;

  cell_card_list cells;
  surface_card_list surfaces;
  data_card_list datacards;

  std::map<int, CellCard*> cell_map;
  std::map<int, SurfaceCard*> surface_map;
  std::map< DataCard::id_t, DataCard*> datacard_map;

  bool do_line_continuation( LineExtractor& lines, token_list_t& token_buffer );
  void parseTitle( LineExtractor& lines );
  void parseCells( LineExtractor& lines );
  void parseSurfaces( LineExtractor& lines );
  void parseDataCards( LineExtractor& lines );
  void copyMacrobodies();

public:

  ~InputDeck();

  cell_card_list& getCells() { return cells; }
  surface_card_list& getSurfaces() { return surfaces; } 
  data_card_list& getDataCards(){ return datacards; }

  cell_card_list getCellsOfUniverse( int universe );

  CellCard* lookup_cell_card(int ident);
  SurfaceCard* lookup_surface_card(int ident);
  DataCard* lookup_data_card( const DataCard::id_t& ident );

  DataCard* lookup_data_card( DataCard::kind k, int ident ){
    return lookup_data_card( std::make_pair( k, ident ) );
  }

  static InputDeck& build( std::istream& input );
  

};

template < class T >
std::ostream& operator<<( std::ostream& out, const std::vector<T>& list );

#endif /* MCNP_INPUT_FORMAT_H */
