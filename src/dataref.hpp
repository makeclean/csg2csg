#ifndef MCNP2CAD_DATA_REF_H
#define MCNP2CAD_DATA_REF_H

// additional implemenentations of this class are defined in MCNPInput.cpp

template <class T> class DataRef{

public:
  virtual ~DataRef(){}

  virtual bool hasData() const { return true; }
  virtual const T& getData() const = 0;
  virtual DataRef<T>* clone() = 0;

};

/* Note about covariant return types:
 * DataRef<T> requires a clone() class that (polymorphically) copies the object; this allows any
 * DataRef object to be copied without reference to its implementing type.  This can be thought of
 * as a virtual constructor (see parashift.com/c++-faq-lite/virtual-functions.html#faq-20.8)
 * 
 * Note that on some older compilers, it may be necessary to change the return type of the clone()
 * method to be DataRef<T> for all classes.
 */


// a simple container around a given kind of data
template <class T>
class ImmediateRef : public DataRef<T>{
  
protected:
  T data;
 
public:
  ImmediateRef( const T& p ) :
    data(p) 
  {}

  virtual const T& getData() const { 
    return data;
  }

  // ImmediateRefs can have their data amended
  T& getData(){ return data; } 

  virtual ImmediateRef<T>* clone() {
    return new ImmediateRef<T>( *this );
  }

};

// a reference by pointer: use cautiously, as it assumes its data is always valid
template <class T>
class PointerRef : public DataRef<T>{

protected:
  const T* data;

public:
  PointerRef( const T* p ) : 
    data(p)
  {}

  virtual const T& getData() const {
    return *data;
  }

  virtual PointerRef<T>* clone() {
    return new PointerRef<T>( *this );
  }

};

#include <stdexcept>

// a class that has no data, and throws an exception if getData() is called.
template <class T>
class NullRef : public DataRef<T>{

public:
  NullRef() : 
    DataRef<T>()
  {}

  virtual bool hasData() const { return false; }

  virtual const T& getData() const {
    throw std::runtime_error("Attempting to pull data from a null reference!");
  }

  virtual NullRef<T> * clone(){
    return new NullRef<T>(*this);
  }

};




#endif /* MCNP2CAD_DATA_REF_H */
