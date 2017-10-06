#include "geometry.hpp"
#include <cfloat>
#include <iostream>
#include <cassert>

// #include "options.hpp"

//bool OPT_DEBUG = false;
extern bool OPT_DEBUG;

std::ostream& operator<<(std::ostream& str, const Vector3d& v ){
  str << "(" << v.v[0] << ", " << v.v[1] << ", " << v.v[2] << ")";
  return str;
}

double matrix_det( double mat[9] ){
  return (mat[0]*mat[4]*mat[8] -
          mat[0]*mat[5]*mat[7] -
          mat[1]*mat[3]*mat[8] +
          mat[1]*mat[5]*mat[6] +
          mat[2]*mat[3]*mat[7] -
          mat[2]*mat[4]*mat[6]);
}

/**
 * Compute Euler axis/angle, given a rotation matix.
 * See en.wikipedia.org/wiki/Rotation_representation_(mathematics) 
 */
void Transform::set_rots_from_matrix( double raw_matrix[9], enum mat_format f ){
    
  double mat[3][3]  = {{ raw_matrix[0], raw_matrix[3], raw_matrix[6] },
                       { raw_matrix[1], raw_matrix[4], raw_matrix[7] },
                       { raw_matrix[2], raw_matrix[5], raw_matrix[8] } };


  if( f == C_STYLE ){

    /* row-major ordering: rewrite mat as
       mat = { { raw_matrix[0], raw_matrix[1], raw_matrix[2] }; 
               { raw_matrix[3], raw_matrix[4], raw_matrix[5] },
               { raw_matrix[6], raw_matrix[7], raw_matrix[8] } };
    */

    mat[0][1] = raw_matrix [1];
    mat[0][2] = raw_matrix [2];
    mat[1][0] = raw_matrix [3];
    mat[1][2] = raw_matrix [5];
    mat[2][0] = raw_matrix [6];
    mat[2][1] = raw_matrix [7];

  }

  double det = matrix_det(raw_matrix); // determinant is the same regardless of ordering

  if( OPT_DEBUG ){
    std::cout << "Constructing rotation: " << std::endl;
    for( int i = 0; i < 3; i++ ){
      std::cout << "  [ ";
      for ( int j = 0; j < 3; j++ ){
        std::cout << mat[i][j] << " ";
      }
      std::cout << "]" << std::endl;
    }
    std::cout << "  det = " << det << std::endl;
  }

  if( det < 0.0 ){
    // negative determinant-> this transformation contains a reflection.
    invert = true;
    det *= -1;
    for( int i = 0; i < 9; i++){  mat[i/3][i%3] = -mat[i/3][i%3]; } 
    if( OPT_DEBUG ) std::cout << "  negative determinant => improper rotation (adding inversion)" << std::endl;
  }
  
  if( fabs( det - 1.0 ) > DBL_EPSILON ){
    std::cout << "Warning: determinant of rotation matrix " << det << " != +-1" << std::endl;
  }

  /* Older, more straightforward approach:
    theta = acos( (mat[0][0] + mat[1][1] + mat[2][2] - 1) / 2 );
    double twoSinTheta = 2 * sin(theta);
    axis.v[0] = ( mat[2][1]-mat[1][2]) / twoSinTheta;
    axis.v[1] = ( mat[0][2]-mat[2][0]) / twoSinTheta;
    axis.v[2] = ( mat[1][0]-mat[0][1]) / twoSinTheta;
  */

  /* I have switched from the simple implementation above to the more robust and complex
   * approach below.  It has better numerical stability and (what is more important)
   * handles correctly the cases where theta is a multiple of 180 degrees.
   * See also
   * en.wikipedia.org/wiki/Rotation_matrix#Axis_and_angle (for why to use atan2 instead of acos)
   * www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToAngle/index.htm (for handling 180-degree case)
   */

  double x = mat[2][1]-mat[1][2];
  double y = mat[0][2]-mat[2][0];
  double z = mat[1][0]-mat[0][1];
  double r = hypot( x, hypot( y,z ));
  double t = mat[0][0] + mat[1][1] + mat[2][2];
  theta = atan2(r,t-1);
  
  if( OPT_DEBUG ){
    std:: cout << "  r = " << r << " t = " << t << " theta = " << theta << std::endl;
    std:: cout << "  x = " << x << " y = " << y << " z = " << z << std::endl;
  }

  if( std::fabs(theta) <= DBL_EPSILON ){ 
    // theta is 0 or extremely close to it, so let's say there's no rotation after all.
    has_rot = false; 
    axis = Vector3d(); // zero vector
    if( OPT_DEBUG ) std::cout << "  (0) "; // std::endl comes below
  }
  else if( std::fabs( theta - M_PI ) <= DBL_EPSILON ){
    // theta is pi (180 degrees) or extremely close to it
    // find the column of mat with the largest diagonal
    int col = 0;
    if( mat[1][1] > mat[col][col] ){ col = 1; }
    if( mat[2][2] > mat[col][col] ){ col = 2; }

    axis.v[col] = sqrt( (mat[col][col]+1)/2 ); 
    double denom = 2*axis.v[col];
    axis.v[(col+1)%3] = mat[col][(col+1)%3] / denom;
    axis.v[(col+2)%3] = mat[col][(col+2)%3] / denom;

    if( OPT_DEBUG ) std::cout << "  (180) "; // std::endl comes below

  }
  else{ 
    // standard case: theta isn't 0 or 180
    axis.v[0] = x / r;
    axis.v[1] = y / r;
    axis.v[2] = z / r;
  }


  // convert theta back to degrees, as used by iGeom
  theta *= 180.0 / M_PI;
  
  if( OPT_DEBUG ) std::cerr << "computed rotation: " << *this << std::endl;

}

Transform::Transform( double rot[9], const Vector3d& trans, enum mat_format f ) :
  translation(trans), has_rot(true), invert(false)
{
  set_rots_from_matrix( rot, f );
}

Transform::Transform( const std::vector< double >& inputs,  bool degree_format_p, enum mat_format f ) : 
  has_rot(false), invert(false)
{
  
  size_t num_inputs = inputs.size();
  
  // translation is always defined by first three inputs
  translation = Vector3d(inputs); 

  if( num_inputs == 9 ||                         // translation matrix with third vector missing
      num_inputs == 12 || num_inputs == 13 )  // translation matrix fully specified
    {
    
      has_rot = true;
      double raw_matrix[9];
    
    if( num_inputs == 9 ){
      for( int i = 3; i < 9; ++i){
        raw_matrix[i-3] = degree_format_p ? cos(inputs.at(i) * M_PI / 180.0 ) : inputs.at(i);
      }
      
      Vector3d v1( raw_matrix ); //v1 = v1.normalize();
      Vector3d v2( raw_matrix+3 ); //v2 = v2.normalize();
      Vector3d v3 = v1.cross(v2);//.normalize();
      raw_matrix[6] = v3.v[0];
      raw_matrix[7] = v3.v[1];
      raw_matrix[8] = v3.v[2];
    }
    else{
      for( int i = 3; i < 12; ++i){
        raw_matrix[i-3] = degree_format_p ? cos(inputs.at(i) * M_PI / 180.0 ) : inputs.at(i);
      }
      if( num_inputs == 13 && inputs.at(12) == -1.0 ){
        std::cout << "Notice: a transformation has M = -1.  Inverting the translation;" << std::endl;
        std::cout << " though this might not be what you wanted." << std::endl;
        translation = -translation;
      }
    }

    set_rots_from_matrix( raw_matrix, f );
    
  }
  else if( num_inputs != 3 ){
    // an unsupported number of transformation inputs
    std::cerr << "Warning: transformation with " << num_inputs << " input items is unsupported" << std::endl;
    std::cerr << "  (will pretend there's no rotation: expect incorrect geometry.)" << std::endl;
  }
  
}  

Transform Transform::reverse() const {
  Transform t;
  t.translation = -this->translation;
  t.has_rot = this->has_rot;
  t.invert = this->invert;
  t.axis = -this->axis;
  t.theta = this->theta;
  return t;
}

void Transform::print( std::ostream& str ) const{
  str << "[trans " << translation;
  if(has_rot){
    str << "(" << theta << ":" << axis << ")";
  }
  if(invert){
    str << "(I)";
  }
  str << "]";
}



std::ostream& operator<<( std::ostream& str, const Transform& t ){
  t.print(str);
  return str;
}

size_t Fill::indicesToSerialIndex( int x, int y, int z ) const {
  int grid_x = x - xrange.first;
  int grid_y = y - yrange.first;
  int grid_z = z - zrange.first;

  int dx = xrange.second - xrange.first + 1;
  int dy = yrange.second - yrange.first + 1;
  //  int dz = zrange.second - zrange.first;
  
  int index = grid_z * (dy*dx) + grid_y * dx + grid_x;

  assert( index >= 0 && (unsigned)(index) <= nodes.size() );
  return static_cast<size_t>( index );
}

const FillNode& Fill::getOriginNode() const { 
  if( !has_grid ){
    return nodes.at(0); 
  }
  else return nodes.at(indicesToSerialIndex( 0, 0, 0));
}

const FillNode& Fill::getNode( int x, int y, int z ) const {
  assert( has_grid );
  return nodes.at( indicesToSerialIndex(x, y, z) );
}






Lattice::Lattice( int dims, const Vector3d& v1_p, const Vector3d& v2_p, const Vector3d& v3_p, const FillNode& node ) : 
  num_finite_dims(dims), v1(v1_p), v2(v2_p), v3(v3_p), fill(new ImmediateRef<Fill>( Fill(node) ))
{}

Lattice::Lattice( int dims, const Vector3d& v1_p, const Vector3d& v2_p, const Vector3d& v3_p, const Fill& fill_p ) :
  num_finite_dims(dims), v1(v1_p), v2(v2_p), v3(v3_p), fill(new PointerRef<Fill>(&fill_p) )
{}


Lattice::Lattice( const Lattice& l ) :
  num_finite_dims( l.num_finite_dims ), v1( l.v1 ), v2( l.v2 ), v3( l.v3 ), fill( l.fill->clone() )
{}

Lattice& Lattice::operator=( const Lattice& l ){
  if( this != &l ){

    num_finite_dims = l.num_finite_dims;
    fill = l.fill->clone();
    v1 = l.v1;
    v2 = l.v2;
    v3 = l.v3;
    
  }
  return *this;
}


Transform Lattice::getTxForNode( int x, int y, int z ) const {

  Vector3d v;
  switch( num_finite_dims ){
  case 3:
    v = v3 * z; // fallthrough
  case 2:
    v = v + v2 * y; // fallthrough
  case 1:
    v = v + v1 * x;
  default:
    break;
  }

  return Transform(v);
}

const FillNode& Lattice::getFillForNode( int x, int y, int z ) const {
  if( fill->getData().has_grid ){
    return fill->getData().getNode( x, y, z );
  }
  else{
    return fill->getData().getOriginNode();
  }
}

  
