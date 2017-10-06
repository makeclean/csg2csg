#include "MCNPInput.hpp"
#include "geometry.hpp"
// #include "options.hpp"

#include <stdexcept>
#include <cassert>
#include <iostream>
#include <sstream>
#include <cstdlib>

/******************
 * IMPLEMENTATIONS OF DataRef
 ******************/

bool OPT_VERBOSE = true;
bool OPT_DEBUG = false;

template <class T> 
class CardRef : public DataRef<T>{
  
protected:
  InputDeck& deck;
  DataCard::id_t key;

public:
  CardRef( InputDeck& deck_p, DataCard::kind kind, int ident ) : 
    DataRef<T>(), deck(deck_p), key( std::make_pair( kind, ident ) )
  {}

  virtual const T& getData() const {
    DataCard* c = deck.lookup_data_card( key );
    const T& ref = dynamic_cast< DataRef<T>* >(c)->getData();
    return ref;
  }

  virtual CardRef<T> * clone(){
    return new CardRef<T>( *this );
  }

  const DataCard::id_t& getKey() const { return key; } 

};

/******************
 * HELPER FUNCTIONS
 ******************/

static void strlower( std::string& str ){
  // convert to lowercase
  for(size_t i = 0; i < str.length(); ++i){
    str[i] = tolower( str.at(i) );
  }
}

static int makeint( const std::string& token ){
  const char* str = token.c_str();
  char* end;
  int ret = strtol(str, &end, 10);
  if( end != str+token.length() ){
    std::cerr << "Warning: string [" << token << "] did not convert to int as expected." << std::endl;
  }
  return ret;
}

static std::vector<std::string> parseID( const token_list_t tokens ){
  //This function returns the first two or three arguments in token_list, which
  //name and define the type of surface.
  std::vector<std::string> identifier (3);
  identifier[0] = tokens.at(0);
  if(identifier[0].find_first_of("*+") != identifier[0].npos){
    std::cerr << "Warning: no special handling for reflecting or white-boundary surfaces" << std::endl;
    identifier[0][0] = ' ';
  } 
  
  if(tokens.at(1).find_first_of("1234567890-") != 0){
    identifier[1] = '0';
    identifier[2] = tokens.at(1);
  }
  else{
    identifier[1] = tokens.at(1);
    identifier[2] = tokens.at(2);
    if( makeint( identifier.at(1) ) == 0 ){
      std::cerr << "I don't think 0 is a valid surface transformation ID, so I'm ignoring it." << std::endl;
    }
  }
  return identifier;
}

static double makedouble( const std::string& token ){
  std::string tmp = token;

  // MCNP allows FORTRAN-style floating point values where the 'e' in the exponent is missing,
  // e.g. 1.23-45 means 1.23e-45.  The following check inserts such a missing 'e' to avoid 
  // confusing strtod().
  size_t s_idx = tmp.find_last_of("+-");
  if( s_idx != tmp.npos && s_idx > tmp.find_first_of("1234567890") && tmp.at(s_idx-1) != 'e' ){
    tmp.insert( tmp.find_last_of("+-"), "e" );
    if( OPT_DEBUG ) std::cout << "Formatting FORTRAN value: converted " << token << " to " << tmp << std::endl;
  }

  const char* str = tmp.c_str();
  char* end;
  double ret = strtod(str, &end);
  if( end != str+tmp.length() ){
    std::cerr << "Warning: string [" << tmp << "] did not convert to double as expected." << std::endl;
  }
  return ret;
}

/** parse the args of an MCNP geometry transform */
static std::vector<double> makeTransformArgs( const token_list_t tokens ){
  std::vector<double> args;
  for( token_list_t::const_iterator i = tokens.begin(); i!=tokens.end(); ++i){
    
    std::string token = *i;
    size_t idx;
    while( (idx = token.find_first_of("()")) != token.npos){
      token.replace( idx, 1, "" ); // remove parentheses
    }
    if( token.find_first_of( "1234567890" ) != token.npos){
      args.push_back( makedouble( token ) );
    }
    else if( token.length() > 0) {
      std::cerr << "Warning: makeTransformArgs ignoring unrecognized input token [" << token << "]" << std::endl;
    }
  }
  return args;
}

/**
 * Attempt to create a Transform object using the given numbers. Bounding parentheses are allowed
 * and will be removed.
 *
 * The returned object is allocated with new and becomes the property of the caller.
 */
static DataRef<Transform>* parseTransform( InputDeck& deck, const token_list_t tokens, bool degree_format = false ){

  std::vector<double> args = makeTransformArgs( tokens );
  if( args.size() == 1 ){
    return new CardRef<Transform>( deck, DataCard::TR, static_cast<int>(args[0]) );
  }
  else{
    return new ImmediateRef<Transform>( Transform( args, degree_format ) );
  }
}

static DataRef<Transform>* parseTransform( InputDeck& deck, token_list_t::iterator& i, bool degree_format = false ){
 
  token_list_t args;
  std::string next_token = *i;
  
  if( next_token.find("(") != next_token.npos ){
    do{
      args.push_back( next_token );
      next_token = *(++i);
    }
    while( next_token.find(")") == next_token.npos );
  }

  args.push_back( next_token );
  
  return parseTransform( deck, args, degree_format );
}

static FillNode parseFillNode( InputDeck& deck, token_list_t::iterator& i, const token_list_t::iterator& end, bool degree_format = false ){
  // simple fill. Format is n or n (transform). Transform may be either a TR card number
  // or an immediate transform 
  
  int n; // the filling universe
  DataRef<Transform>* t;
  bool has_transform = false;

  std::string first_token = *i;
  size_t paren_idx = first_token.find("(");

  std::string second_token;

  if( paren_idx != first_token.npos ){
    // first_token has an open paren
    std::string n_str(first_token, 0, paren_idx);
    n = makeint(n_str);

    second_token = first_token.substr(paren_idx,first_token.npos);
    has_transform = true;
  }
  else{
    n = makeint(first_token);

    if( ++i != end ){
      second_token = *i;
      if( second_token[0] == '(' ){
        has_transform = true;
      }
      else{
        // the next token didn't belong to this fill 
        i--;
      }
    }
    else{ i--; }
  }

  if( has_transform ){    
    token_list_t transform_tokens;
    std::string next_token = second_token;
    
    while( next_token.find(")") == next_token.npos ){
      transform_tokens.push_back(next_token);
      next_token = *(++i);
    }
    transform_tokens.push_back( next_token );

    t = parseTransform( deck, transform_tokens, degree_format );

  }
  else{
    t = new NullRef<Transform>();
  }


  if( n < 0 ){
    n = -n; // TODO: handle negative universe numbers specially
  }
  
  return FillNode (n, t );
}

static bool isblank( const std::string& line ){
  return (line=="" || line.find_first_not_of(" ") == line.npos );
}


template < class T >
std::ostream& operator<<( std::ostream& out, const std::vector<T>& list ){

  out << "[";

  for(typename std::vector<T>::const_iterator i = list.begin(); i!=list.end(); ++i){
    out << *i << "|";
  }

  if(list.size() > 0) 
    out << "\b"; // unless list was empty, backspace the last | character

  out << "]";
  return out;
}



/******************
 * CELL CARDS
 ******************/

class CellCardImpl : public CellCard { 
protected:
  static geom_list_entry_t make_geom_entry(geom_token_t t, int param = 0){
    return std::make_pair(t, param);
  }
  
  static bool is_num_token( geom_list_entry_t t ){
    return t.first == CELLNUM || t.first == SURFNUM || t.first == MBODYFACET;
  }
  
  static bool is_op_token( geom_list_entry_t t ){
    return t.first == COMPLEMENT || t.first == UNION || t.first == INTERSECT;
  }
  
  static int operator_priority( geom_list_entry_t t ){
    switch(t.first){
    case COMPLEMENT: return 3;
    case INTERSECT:  return 2;
    case UNION:      return 1;
    default:
      throw std::runtime_error("queried operator priority for a non-operator token");
    }
  }

  /**
   * Build the geom list as part of cell construction.
   * Each item in the list will be a string; either " ", ":", or "#", indicating
   * operators, or parentheses, or numbers indicating surface or cell identities.
   *
   * @param The list of geometry tokens in the input file, as a list of strings that were 
   *        separated by white space in the original file.
   */
  void retokenize_geometry( const token_list_t& tokens ){
    for(token_list_t::const_iterator i = tokens.begin(); i!=tokens.end(); ++i){
      const std::string& token = *i;
      
      size_t j = 0;
      while( j < token.length() ){

        char cj = token.at(j);

        switch(cj){
          
          // the following macro pushes an intersect token onto the geom list
          // if the end of that list indicates that one is needed
#define IMPLICIT_INTERSECT() do{                                \
            if(geom.size()){                                    \
              geom_list_entry_t &t = geom.at(geom.size()-1);    \
              if( is_num_token(t) || t.first == RPAREN ){       \
                geom.push_back( make_geom_entry( INTERSECT ) ); \
              }}} while(0) 
          
        case '(': 
          IMPLICIT_INTERSECT();
          geom.push_back(make_geom_entry(LPAREN)); j++;
          break;
          
        case ')':
          geom.push_back(make_geom_entry(RPAREN)); j++;
          break;
          
        case '#':
          IMPLICIT_INTERSECT();
          geom.push_back(make_geom_entry(COMPLEMENT)); j++; 
          break;
          
        case ':':
          geom.push_back(make_geom_entry(UNION)); j++; 
          break;
          
        default: // a number
          // the number refers to a cell if the previous token is a complement
          bool is_cell = geom.size() && ((geom.at(geom.size()-1)).first == COMPLEMENT);
          IMPLICIT_INTERSECT();
          assert(isdigit(cj) || cj == '+' || cj == '-' );
          size_t end = token.find_first_not_of("1234567890-+.",j);
          assert(j != end);

          std::string numstr( token, j, end-j );
          const char* numstr_c = numstr.c_str();
          char* p;
          int num = strtol( numstr_c, &p, 10 );

          if( *p == '.' ){
            // This is a macrobody facet
            assert( !is_cell );

            int facet = strtol( p+1, NULL, 10 );
            assert( facet > 0 && facet <= 8 );

            // storage of macrobody facets: multiply cell number by ten, add facet number
            num *= 10;
            // don't add a positive facet number to a negative cell numer
            num += (num > 0) ? facet : -facet;
            geom.push_back( make_geom_entry( MBODYFACET, num ) );
          }
          else{
            geom.push_back( make_geom_entry( is_cell ? CELLNUM : SURFNUM, num ));
          }

          j += (end-j);
          break;
#undef IMPLICIT_INTERSECT

        }
        
      } 
    }
    
    if( OPT_DEBUG ) std::cout << tokens << " -> " << geom << std::endl;
    
  }


  /**
   * The final step of geometry parsing: convert the geometry list to RPN, which
   * greatly simplifies the process of evaluating the geometry later.  This function
   * uses the shunting yard algorithm.  For more info consult
   * http://en.wikipedia.org/wiki/Shunting_yard_algorithm
   */
  void shunt_geometry( ){
    geom_list_t geom_copy( geom );
    geom.clear();

    geom_list_t stack;
    for(geom_list_t::iterator i = geom_copy.begin(); i!=geom_copy.end(); ++i){
      geom_list_entry_t token = *i;
      if( is_num_token(token) ){
        geom.push_back(token);
      }
      else if( is_op_token(token) ){

        while(stack.size()){
          geom_list_entry_t& stack_top = stack.back();
          if( is_op_token(stack_top) && operator_priority(stack_top) > operator_priority(token) ){
            geom.push_back(stack_top);
            stack.pop_back();
          }
          else{
            break;
          }
        }
        stack.push_back(token);
      }
      else if( token.first == LPAREN ){
        stack.push_back(token);
      }
      else if( token.first == RPAREN ){
        while( stack.back().first != LPAREN ){
          geom.push_back( stack.back() );
          stack.pop_back();
        }
        stack.pop_back(); // remove the LPAREN
      }
    }
    while( stack.size() ){
      geom.push_back( stack.back() );
      stack.pop_back();
    }
  }

  Vector3d latticeVectorHelper( Vector3d difference_along_normal, Vector3d v_dir ){
    double length = difference_along_normal.length() / (difference_along_normal.normalize().dot(v_dir));
    return v_dir * length;
  }

  void setupLattice(){

    if( OPT_DEBUG ) std::cout << "Setting up lattice for cell " << ident << std::endl;

    std::vector< std::pair<SurfaceCard*,bool> > surfaceCards;
    
    for( geom_list_t::iterator i = geom.begin(); i!=geom.end(); ++i){
      geom_list_entry_t entry = *i;
      if( entry.first == SURFNUM ){
        SurfaceCard* surf = parent_deck.lookup_surface_card( std::abs(entry.second) );
        assert(surf);
        surfaceCards.push_back( std::make_pair(surf, (entry.second>0) ) );
      }
    }

    int num_finite_dims = 0;
    Vector3d v1, v2, v3;

    std::vector< std::pair<Vector3d, double> > planes;

    if( surfaceCards.size() == 1 ){ 
      planes = surfaceCards.at(0).first->getMacrobodyPlaneParams();
      if( surfaceCards.at(0).second != false ){
        std::cerr << "Warning: macrobody lattice with positive sense, will proceed as if it was negative.";
      }
    }
    else{
      for( unsigned int i = 0; i < surfaceCards.size(); ++i){
        planes.push_back( surfaceCards.at(i).first->getPlaneParams() );
        if( surfaceCards.at(i).second == true ){ planes[i].first = -planes[i].first; }
      }
    }

    if( OPT_DEBUG ){
      for( unsigned int i = 0; i < planes.size(); ++i){
        std::cout << " plane " << i << " normal = " << planes[i].first << " d = " << planes[i].second  << std::endl;
      }
    }
    if( lat_type == HEXAHEDRAL ){
      assert( planes.size() == 2 || planes.size() == 4 || planes.size() == 6 );
      if( planes.size() == 2 ){

        num_finite_dims = 1;
        v1 = planes[0].first.normalize() * std::fabs( planes[0].second - planes[1].second ); 

      }
      else if( planes.size() == 4 ){
        num_finite_dims = 2;
        
        Vector3d v3 = planes[0].first.cross( planes[2].first ).normalize(); // infer a third (infinite) direction
        
        // vector from planes[1] to planes[0]
        Vector3d xv = planes[0].first.normalize() * std::fabs( planes[0].second - planes[1].second );

        // direction of l.v1: cross product of normals planes[2] and v3
        Vector3d xv2 = planes[2].first.normalize().cross( v3 ).normalize();
        v1 = latticeVectorHelper( xv, xv2 );

        Vector3d yv = planes[2].first.normalize() * std::fabs( planes[2].second - planes[3].second );
        Vector3d yv2 = planes[0].first.normalize().cross( v3 ).normalize();
        v2 = latticeVectorHelper( yv, yv2 );


      }
      else{ // planes.size() == 6 
        num_finite_dims = 3;

        // vector from planes[1] to planes[0]
        Vector3d xv = planes[0].first.normalize() * std::fabs( planes[0].second - planes[1].second );

        // direction of v1: cross product of normals planes[2] and planes[4]
        Vector3d xv2 = planes[2].first.normalize().cross( planes[4].first.normalize() ).normalize();
        v1 = latticeVectorHelper( xv, xv2 );

        Vector3d yv = planes[2].first.normalize() * std::fabs( planes[2].second - planes[3].second );
        Vector3d yv2 = planes[0].first.normalize().cross( planes[4].first.normalize() ).normalize();
        v2 = latticeVectorHelper( yv, yv2 );

        Vector3d zv = planes[4].first.normalize() * std::fabs( planes[4].second - planes[5].second );
        Vector3d zv2 = planes[0].first.normalize().cross( planes[2].first.normalize() ).normalize();
        v3 = latticeVectorHelper( zv, zv2 );
        
      }
      
    }
    else if( lat_type == HEXAGONAL ){
      assert( planes.size() == 6 || planes.size() == 8 );

      v3 = planes[0].first.cross( planes[2].first ).normalize(); // prism's primary axis

      // vector from planes[1] to planes[0]
      Vector3d xv = planes[0].first.normalize() * std::fabs( planes[0].second - planes[1].second );
      
      // direction of l.v1: cross product of normals average(planes[2]+planes[4]) and v3
      // TODO: this averaging trick only works with regular hexagons...
      Vector3d xv2 = (planes[2].first.normalize()+planes[4].first.normalize()).normalize().cross( v3 ).normalize();
      v1 = latticeVectorHelper( xv, xv2 );
      
      Vector3d yv = planes[2].first.normalize() * std::fabs( planes[2].second - planes[3].second );
      Vector3d yv2 = (planes[1].first.normalize()+planes[4].first.normalize()).normalize().cross( v3 ).normalize();
      v2 = latticeVectorHelper( yv, yv2 );
      

      if( planes.size() == 6 ){
        num_finite_dims = 2;
        
      }
      else{ // planes.size() == 8
        num_finite_dims = 3;

        Vector3d zv = planes[6].first.normalize() * std::fabs( planes[6].second - planes[7].second );
        Vector3d zv2 = v3;
        v3 = latticeVectorHelper( zv, zv2 );
      }
    }

    if( OPT_DEBUG )std::cout << " dims " << num_finite_dims << " vectors " << v1 << v2 << v3 << std::endl;
    
    Lattice l;
    if( fill->hasData() ){
      l = Lattice( num_finite_dims, v1, v2, v3, fill->getData() );
    }
    else{
      FillNode n( this->universe );
      l = Lattice( num_finite_dims, v1, v2, v3,  n );
    }

    lattice = new ImmediateRef<Lattice>( l );

    
  }

  void makeData(){

    for( token_list_t::iterator i = data.begin(); i!=data.end(); ++i ){

      std::string token = *i;

      if( token == "trcl" || token == "*trcl" ){
        bool degree_format = (token[0] == '*');

        i++;
        trcl = parseTransform( parent_deck, i, degree_format );

      } // token == {*}trcl

      else if( token == "u" ){
        universe = makeint(*(++i));
      } // token == "u"
      else if ( token == "lat" ){
        int lat_designator = makeint(*(++i));
        assert( lat_designator >= 0 && lat_designator <= 2 );
        lat_type = static_cast<lattice_type_t>(lat_designator);
        if( OPT_DEBUG ) std::cout << "cell " << ident << " is lattice type " << lat_type << std::endl;
      }
      else if ( token == "mat" ){
        material = makeint(*(++i));
      }
      else if ( token == "rho" ){
        rho = makedouble(*(++i));
      }
      else if ( token.length() == 5 && token.substr(0,4) == "imp:" ){
        double imp = makedouble(*(++i));
        importances[token[4]] = imp;
      }
      else if( token == "fill" || token == "*fill" ){

        bool degree_format = (token[0] == '*');

        std::string next_token = *(++i);

        // an explicit lattice grid exists if 
        // * the next token contains a colon, or
        // * the token after it exists and starts with a colon
        bool explicit_grid = next_token.find(":") != next_token.npos; 
        explicit_grid = explicit_grid || (i+1 != data.end() && (*(i+1)).at(0) == ':' );

        if( explicit_grid ){

          // convert the grid specifiers (x1:x2, y1:y2, z1:z2) into three spaceless strings for easier parsing
          std::string gridspec[3];
          for( int dim = 0; dim < 3; ++dim ){

            std::string spec;

            // add tokens to the spec string until it contains a colon but does not end with one
            do{
              spec += *i;
              i++;
            }
            while( spec.find(":") == spec.npos || spec.at(spec.length()-1) == ':' );
            
            if(OPT_DEBUG) std::cout << "gridspec[" << dim << "]: " << spec << std::endl;
            gridspec[dim] = spec;

          }

          irange ranges[3];
          const char* range_str;
          char *p;
          
          int num_elements = 1;
          for( int dim = 0; dim < 3; ++dim ){
            range_str = gridspec[dim].c_str();
            ranges[dim].first  = strtol(range_str, &p, 10);
            ranges[dim].second = strtol(p+1, NULL, 10); 
            
            if( ranges[dim].second != ranges[dim].first ){
              num_elements *= ( ranges[dim].second - ranges[dim].first )+1;
            }

          }

          std::vector<FillNode> elements;
          for( int j = 0; j < num_elements; ++j ){
            elements.push_back( parseFillNode( parent_deck, i, data.end(), degree_format )  );
            i++;
          }
          i--;

          fill = new ImmediateRef< Fill >( Fill( ranges[0], ranges[1], ranges[2], elements) );

        }
        else{ // no explicit grid; fill card is a single fill node
          FillNode filler = parseFillNode( parent_deck, i, data.end(), degree_format );
          fill = new ImmediateRef< Fill >( Fill(filler) );
          
        }
      } // token == {*}fill
    }

    // ensure data pointers are valid
    if( !trcl ) {
      trcl = new NullRef< Transform >();
    }

    if( !fill ){
      fill = new NullRef< Fill > ();
    }

  }

  int ident;
  int material;
  double rho; // material density
  std::map<char, double> importances;

  geom_list_t geom;
  token_list_t data;
  DataRef<Transform>* trcl;
  DataRef<Fill>* fill;
  int universe;

  bool likenbut;
  int likeness_cell_n;

  lattice_type_t lat_type;
  DataRef<Lattice> *lattice;

public:
  CellCardImpl( InputDeck& deck, const token_list_t& tokens ) : 
    CellCard( deck ), trcl(NULL), fill(NULL), universe(0), likenbut(false), likeness_cell_n(0), 
    lat_type(NONE), lattice(NULL)
  {
    
    unsigned int idx = 0;

    ident = makeint(tokens.at(idx++));
    
    if(tokens.at(idx) == "like"){

      idx++;
      likenbut = true;
      likeness_cell_n = makeint(tokens.at(idx++));
      idx++; // skip the "but" token
      while(idx < tokens.size()){
        data.push_back(tokens[idx++]);
      }
      return;
    }

    material = makeint(tokens.at(idx++));
    rho = 0.0;
    if(material != 0){
      rho = makedouble(tokens.at(idx++)); // material density
    }

    token_list_t temp_geom;
    
    // while the tokens appear in geometry-specification syntax, store them into temporary list
    while(idx < tokens.size() && tokens.at(idx).find_first_of("1234567890:#-+()") == 0){
      temp_geom.push_back(tokens[idx++]);
    }

    // retokenize the geometry list, which follows a specialized syntax.
    retokenize_geometry( temp_geom );
    shunt_geometry();

    // store the rest of the tokens into the data list
    while(idx < tokens.size()){
      data.push_back(tokens[idx++]);
    }

    makeData();

  }

  ~CellCardImpl(){
    if(trcl)
      delete trcl;
    if(fill)
      delete fill;
    if(lattice)
      delete lattice;
  }

  virtual int getIdent() const{ return ident; }
  virtual const geom_list_t getGeom() const { return geom; }

  virtual const DataRef<Transform>& getTrcl() const { return *trcl; }
  virtual int getUniverse() const { return universe; }

  virtual bool hasFill() const { return fill && fill->hasData(); }
  virtual const Fill& getFill() const { 
    if( fill && fill->hasData() ){
      return fill->getData();
    }
    throw std::runtime_error( "Called getFill() on an unfilled cell");
  }

  virtual bool isLattice() const {
    return lat_type != NONE;
  }

  virtual lattice_type_t getLatticeType() const {
    return lat_type;
  }

  virtual const Lattice& getLattice() const {
    if( lattice && lattice->hasData() ){
      return lattice->getData();
    }
    throw std::runtime_error( "Called getLattice() on a cell that hasn't got one" );
  }

  virtual int getMat() const { return material; }
  virtual double getRho() const { return rho; }
  virtual const std::map<char,double>& getImportances() const { return importances; }

  virtual void print( std::ostream& s ) const{
    s << "Cell " << ident << " geom " << geom << std::endl;
  }

protected:
  void finish(){
    if( likenbut ){
      CellCardImpl* host = dynamic_cast<CellCardImpl*>(parent_deck.lookup_cell_card( likeness_cell_n ));
      if(host->likenbut){
        host->finish(); // infinite recursion if cells are circularly defined... but our users wouldn't do that, right?
      }
      geom = host->geom;
      universe = host->universe;
      lat_type = host->lat_type;
      material = host->material;
      rho = host->rho;
      importances = host->importances;

      if( host->trcl->hasData()){
        trcl = host->trcl->clone();
      }
      if( host->hasFill()){
        fill = host->fill->clone();
      }
      if( host->isLattice()){
        lattice = host->lattice->clone();
      }
      makeData();

      likenbut = false;
    }

    if( lat_type != NONE && lattice == NULL ){
      setupLattice();
    }

  }

  friend class InputDeck;
};

CellCard::CellCard( InputDeck& deck ) :
  Card(deck)
{}

std::ostream& operator<<(std::ostream& str, const CellCard::geom_list_entry_t& t ){
  switch(t.first){
  case CellCard::LPAREN:     str << "("; break;
  case CellCard::RPAREN:     str << ")"; break;
  case CellCard::COMPLEMENT: str << "#"; break;
  case CellCard::UNION:      str << ":"; break;
  case CellCard::INTERSECT:  str << "*"; break;
  case CellCard::SURFNUM:    str << t.second; break;
  case CellCard::CELLNUM:    str << "c" << t.second; break;
  case CellCard::MBODYFACET: 
    int cell = t.second / 10;
    int facet = abs(t.second) - (abs(cell)*10);
    str << cell << "." << facet;
    break;
  }
  return str;
}



/******************
 * SURFACE CARDS
 ******************/

SurfaceCard::SurfaceCard( InputDeck& deck, const token_list_t tokens ):
  Card(deck)
{
      std::vector<std::string> identifier = parseID( tokens );
      ident = makeint(identifier.at(0));
      tx_id = makeint(identifier.at(1));
      mnemonic = identifier.at(2);
      size_t idx = 2;
      if( tx_id == 0 ){
        coord_xform = new NullRef<Transform>();
      }
      else if ( tx_id < 0 ){
        // abs(tx_id) is the ID of surface with respect to which this surface is periodic.
        std::cerr << "Warning: surface " << ident << " periodic, but this program has no special handling for periodic surfaces";
      }
      else{ // tx_id is positive and nonzero
        coord_xform = new CardRef<Transform>( deck, DataCard::TR, tx_id );
      }
      if( tokens.at(2) == mnemonic ){
        idx++;
      }

      while( idx < tokens.size() ){
        args.push_back( makedouble(tokens[idx++]) );
      }
}

SurfaceCard::SurfaceCard( InputDeck& deck, const SurfaceCard s, int facetNum ):
  Card(deck)
{
  //This form of SurfaceCard makes a copy of a macrobody for use with one of its facets.
  ident = facetNum;
  mnemonic = s.getMnemonic();
  args = s.getArgs();
  tx_id = s.getTxid();
  if( tx_id == 0 ){
    coord_xform = new NullRef<Transform>();
  }
  else if ( tx_id < 0 ){
    // abs(tx_id) is the ID of surface with respect to which this surface is periodic.
    std::cerr << "Warning: surface " << ident << " periodic, but this program has no special handling for periodic surfaces";
  }
  else{ // tx_id is positive and nonzero
    coord_xform = new CardRef<Transform>( deck, DataCard::TR, tx_id );
  }
}

const DataRef<Transform>& SurfaceCard::getTransform() const {
  return *coord_xform;
}

void SurfaceCard::print( std::ostream& s ) const {
  s << "Surface " << ident << " " << mnemonic << args;
  if( coord_xform->hasData() ){
    // this ugly lookup returns the integer ID of the TR card
    s << " TR" << dynamic_cast<CardRef<Transform>*>(coord_xform)->getKey().second;
  }
  s << std::endl;
}

std::pair<Vector3d,double> SurfaceCard::getPlaneParams() const {
  if(mnemonic == "px"){
    return std::make_pair(Vector3d(1,0,0), args[0]);
  }
  else if(mnemonic == "py"){
    return std::make_pair(Vector3d(0,1,0), args[0]);
  }
  else if(mnemonic == "pz"){
    return std::make_pair(Vector3d(0,0,1), args[0]);
  }
  else if(mnemonic == "p"){
    return std::make_pair(Vector3d( args ), args[3]/Vector3d(args).length());
  }
  else{
    throw std::runtime_error("Tried to get plane normal of non-plane surface!");
  }
}

std::vector< std::pair<Vector3d, double> > SurfaceCard::getMacrobodyPlaneParams() const {
  
  std::vector< std::pair< Vector3d, double> > ret;
  if( mnemonic == "box" ){
    Vector3d corner( args );
    const Vector3d v[3] = {Vector3d(args,3), Vector3d(args,6), Vector3d(args,9)};

    // face order: v1 -v1 v2 -v2 v3 -v3
    for( int i = 0; i < 3; ++i ){
      Vector3d p = corner + v[i];
      ret.push_back( std::make_pair( v[i].normalize(), v[i].projection( p ).length() ) );
      ret.push_back( std::make_pair( -v[i].normalize(), v[i].projection( p ).length()-v[i].length() ) );
    }

  }
  else if( mnemonic == "rpp" ){
    Vector3d min( args.at(0), args.at(2), args.at(4) );
    Vector3d max( args.at(1), args.at(3), args.at(5) );

    for( int i = 0; i < 3; ++i ){
      Vector3d v; v.v[i] = 1;
      ret.push_back( std::make_pair( v.normalize(), max.v[i] ));
      ret.push_back( std::make_pair(-v.normalize(), min.v[i] ));
    }

  }
  else if( mnemonic == "hex" || mnemonic == "rhp" ){

    Vector3d vertex( args ), height( args,3 ), RV( args, 6 ), SV, TV;
    if( args.size() == 9 ){
      SV = RV.rotate_about(height, 60); TV = RV.rotate_about(height, 120);
    }
    else{
      SV = Vector3d( args, 9 ); TV = Vector3d( args, 12 );
    }
    
    double len = RV.projection( vertex+RV ).length();
    ret.push_back( std::make_pair( RV.normalize(), len ) );
    ret.push_back( std::make_pair(-RV.normalize(), len - 2.0 * RV.length() ));
    
    len = SV.projection( vertex+SV ).length();
    ret.push_back( std::make_pair( SV.normalize(), len ) );
    ret.push_back( std::make_pair(-SV.normalize(), len - 2.0 * SV.length() ));

    len = TV.projection( vertex+TV ).length();
    ret.push_back( std::make_pair( TV.normalize(), len ) );
    ret.push_back( std::make_pair(-TV.normalize(), len - 2.0 * TV.length() ));

    len = height.projection( vertex+height ).length();
    ret.push_back( std::make_pair( height.normalize(), len ) );
    ret.push_back( std::make_pair(-height.normalize(), len - height.length() ));

  }
  else{ 
    throw std::runtime_error("Tried to get macrobody plane normals of unsupported surface!" );
  }
  return ret;
}



/******************
 * DATA CARDS
 ******************/


class TransformCard : public DataCard, public DataRef<Transform> {

protected: 
  int ident;
  Transform trans;

public:
  TransformCard( InputDeck& deck, int ident_p, bool degree_format, const token_list_t& input );

  //  const Transform& getTransform() const{ return trans; } 
  const Transform& getData() const{ return trans; }
  TransformCard* clone(){ return new TransformCard(*this); }

  virtual void print( std::ostream& str );
  virtual kind getKind(){ return TR; }
  int getIdent() const{ return ident; }

};

TransformCard::TransformCard( InputDeck& deck, int ident_p, bool degree_format, const token_list_t& input ):
  DataCard(deck), ident(ident_p), trans( Transform( makeTransformArgs( input ), degree_format ) )
{}

void TransformCard::print( std::ostream& str ){
  str << "TR" << ident << ": ";
  trans.print(str);
  str << std::endl;
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

/** 
 * Append a single token to the given list of tokens.
 * The token is assumed to be lowercase, free of comments, and non-blank.  
 * This function is for handling shortcut
 * syntax, e.g. 1 4r, which should translate into four copies of the token 1
 */
void appendToTokenList( const std::string& token, token_list_t& tokens ){
  if( token.find_first_of("123456789") == 0 && token.at(token.length()-1) == 'r' ){
    // token starts with a number and ends with r: treat as repeat syntax.
    const char* string = token.c_str();
    char* p;
    int num = strtol( string, &p, 10 );
    if( (p - string) != static_cast<int>(token.length()) - 1 ){
      // oops, this isn't repeat format after all
      tokens.push_back(token);
      return;
    }

    if( OPT_DEBUG ) { std::cout << "Repeat syntax: " << token << " repeats " 
                                << tokens.back() << " " << num << " times." << std::endl; }

    for( int i = 0; i < num; ++i){
      const std::string& last_tok = tokens.back();
      tokens.push_back( last_tok );
    }
  }
  else{
    tokens.push_back(token);
  }
}

void tokenizeLine( std::string line, token_list_t& tokens, const char* extra_separators = "" ){
  
  // replace any occurances of the characters in extra_separators with spaces;
  // they will then act as token separators
  size_t found;
   
  found = line.find_first_of(extra_separators);
  while (found!= line.npos )
  {
    line[found] = ' ';
    found = line.find_first_of(extra_separators,found+1);
  }
  
  std::stringstream str(line);
  while(str){
    std::string t;
    str >> t;

    // skip over $-style inline comments
    size_t idx;
    if((idx = t.find("$")) != t.npos){
      if(idx > 0){
        // this token had some data before the $
        t.resize(idx);
        appendToTokenList( t, tokens );
      }
      break;
    }

    // if the token is nontrivial, save it
    // necessary because stringstream may return a "" at the end of lines.
    if(t.length() > 0)  appendToTokenList( t, tokens );
  }

}

/******************
 * INPUT DECK
 ******************/

InputDeck::~InputDeck(){
  std::cout << cells.size() << std::endl;
  for(cell_card_list::iterator i = cells.begin(); i!=cells.end(); ++i){
    delete *i;
  }
  cells.clear();
  for(surface_card_list::iterator i = surfaces.begin(); i!=surfaces.end(); ++i){
    delete *i;
  }
  surfaces.clear();
  for(data_card_list::iterator i = datacards.begin(); i!=datacards.end(); ++i){
    delete *i;
  }
  datacards.clear();
  
}

/* handle line continuations: return true if the next line should be treated as part of 
 * the current line */
bool InputDeck::do_line_continuation( LineExtractor& lines, token_list_t& token_buffer ){

  /* check for final character being & */
  std::string last_token = token_buffer.at(token_buffer.size()-1);
  if( last_token.at(last_token.length()-1) == '&' ){

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
  else if( lines.hasLine() && lines.peekLine().find("     ") == 0){
      /* but don't count it as a continuation if the line is entirely blank */
      if( lines.peekLine().find_first_not_of(" \t\n") != std::string::npos ){
          return true;
      }
  }
  
  return false;
}

void InputDeck::parseCells( LineExtractor& lines ){

  std::string line;
  token_list_t token_buffer;

  while( !isblank(line = lines.takeLine()) ){

    tokenizeLine(line, token_buffer, "=");
    
    if( do_line_continuation( lines, token_buffer ) ){
      continue;
    }

    if( OPT_DEBUG ) std::cout << "Creating cell with the following tokens:\n" << token_buffer << std::endl;
    CellCard* c = new CellCardImpl(*this, token_buffer);

    if( OPT_VERBOSE ) c->print(std::cout);

    this->cells.push_back(c);
    this->cell_map.insert( std::make_pair(c->getIdent(), c) );

    token_buffer.clear();

  }


}



void InputDeck::parseTitle( LineExtractor& lines ){
  
  // FIXME: will break if the title line looks like a comment card.

  int lineno;
  std::string topLine = lines.takeLine(lineno);
  if(topLine.find("message:") == 0){
    if( OPT_VERBOSE ) std::cout << "Skipping MCNP file message block..." << std::endl;
    do{
      // nothing
    }
    while( !isblank(lines.takeLine()) ) /*do nothing */;

    topLine = lines.takeLine(lineno);
  }

  if(topLine.find("continue") == 0){
    std::cerr << "Warning: this looks like it might be a `continue-run' input file." << std::endl;
    std::cerr << "  beware of trouble ahead!" << std::endl;
  }

  std::cout << "The MCNP title card is: " << topLine << std::endl;
  //std::cout << "    and occupies line " << lineno << std::endl;
}



void InputDeck::parseSurfaces( LineExtractor& lines ){
  std::string line;
  token_list_t token_buffer;
  while( !isblank(line = lines.takeLine()) ){

    tokenizeLine(line, token_buffer );

    if( do_line_continuation( lines, token_buffer ) ){
      continue;
    }
    //Create a surface card for each surface
    SurfaceCard* s = new SurfaceCard(*this, token_buffer);

    if( OPT_VERBOSE) s->print(std::cout);

    this->surfaces.push_back(s);
    this->surface_map.insert( std::make_pair(s->getIdent(), s) );
    
    token_buffer.clear();
  }
}

void InputDeck::parseDataCards( LineExtractor& lines ){
  std::string line;
  token_list_t token_buffer;

  while( lines.hasLine() && !isblank(line = lines.takeLine()) ){

    tokenizeLine(line, token_buffer );
    
    if( do_line_continuation( lines, token_buffer ) ){
      continue;
    }
    else if( token_buffer.at(0) == "#" ){
      std::cerr << "Vertical data card format not supported" << std::endl;
      std::cerr << "Data written in this format will be ignored." << std::endl;
    }

    DataCard* d = NULL;
    DataCard::kind t = DataCard::OTHER;
    int ident = 0;

    std::string cardname = token_buffer.at(0);
    token_buffer.erase( token_buffer.begin() );

    if( cardname.find("tr") == 0 || cardname.find("*tr") == 0 ){

      t = DataCard::TR;
      bool degree_format = false;
      if( cardname[0] == '*' ){
        degree_format = true;
        cardname = cardname.substr( 1 ); // remove leading * 
      }
      else if( cardname.find("*") == cardname.length()-1 ){
        // although it's undocumented, apparently TRn* is a synonym for *TRn
        // (the manual uses this undocumented form in chapter 4)
        degree_format = true;
        cardname.resize( cardname.length() -1 ); // remove trailing *
      }

      std::string id_string( cardname, 2 );

      // the id_string may be empty, indicating that n is missing from TRn.  
      // examples from the manual indicate it should be assumed to be 1
      if( id_string == "" ){
        ident = 1;
      }
      else{
        ident = makeint( id_string );
      }

      d = new TransformCard( *this, ident, degree_format, token_buffer);
    }
    
    if(d){
      if( OPT_VERBOSE ){ d->print( std::cout ); }
      this->datacards.push_back(d);
      this->datacard_map.insert( std::make_pair( std::make_pair(t,ident), d) );
    }

    token_buffer.clear();

  }

}

void InputDeck::copyMacrobodies(){
  //If a macrobody facet is used, this creates a copy of the surface card of the macrobody with a different id.
  for( cell_card_list::iterator k = cells.begin(); k!=cells.end(); ++k){
    CellCard* c = *k;
    const CellCard::geom_list_t& geom = c->getGeom();
    for(CellCard::geom_list_t::const_iterator i = geom.begin(); i!=geom.end(); ++i){
    
      const CellCard::geom_list_entry_t& token = (*i);
 
      if( token.first == 7 ){
        //this is a macrobody facet
        int ident = -std::abs( token.second );
        if( surface_map.find(ident) == surface_map.end() ){ 
          //It won't create multiple copies if a facet is used more than once.
          int surfaceNum = -ident/10;

          SurfaceCard* surface = this->lookup_surface_card( surfaceNum );
          SurfaceCard* s = new SurfaceCard( *this, *surface, ident );

          if( OPT_VERBOSE ) s->print(std::cout);

          this->surfaces.push_back(s);
          this->surface_map.insert( std::make_pair(s->getIdent(), s) );
        }
      }
    }
  }
}


InputDeck& InputDeck::build( std::istream& input){
 
  LineExtractor lines(input);

  InputDeck* deck = new InputDeck();

  deck->parseTitle(lines);
  deck->parseCells(lines);
  deck->parseSurfaces(lines);
  deck->parseDataCards(lines);
  deck->copyMacrobodies();


  for( std::vector<CellCard*>::iterator i = deck->cells.begin(); i!=deck->cells.end(); ++i){
    dynamic_cast<CellCardImpl*>(*i)->finish();
  }

  while(lines.hasLine()){ lines.takeLine(); }
  if( OPT_VERBOSE ) { std::cout << "Total lines read: " << lines.getLineCount()  <<  std::endl; }

  return *deck;
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
