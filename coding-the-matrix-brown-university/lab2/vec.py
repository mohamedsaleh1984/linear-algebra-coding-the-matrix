# Copyright 2013 Philip N. Klein
from typing import cast
def getitem(v,k):
    """
    Return the value of entry k in v.
    Be sure getitem(v,k) returns 0 if k is not represented in v.f.

    >>> v = Vec({'a','b','c', 'd'},{'a':2,'c':1,'d':3})
    >>> v['d']
    3
    >>> v['b']
    0
    """
    # assert k in v.D
    return v.f[k] if k in v.f else 0

def setitem(v,k,val):
    """
    Set the element of v with label d to be val.
    setitem(v,d,val) should set the value for key d even if d
    is not previously represented in v.f, and even if val is 0.

    >>> v = Vec({'a', 'b', 'c'}, {'b':0})
    >>> v['b'] = 5
    >>> v['b']
    5
    >>> v['a'] = 1
    >>> v['a']
    1
    >>> v['a'] = 0
    >>> v['a']
    0
    """
    #assert k in v.D
    v.f[k] = val
    pass

def equal(u,v):
    """
    Return true iff u is equal to v.
    Because of sparse representation, it is not enough to compare dictionaries

    Consider using brackets notation u[...] and v[...] in your procedure
    to access entries of the input vectors.  This avoids some sparsity bugs.

    >>> Vec({'a', 'b', 'c'}, {'a':0}) == Vec({'a', 'b', 'c'}, {'b':0})
    True
    >>> Vec({'a', 'b', 'c'}, {'a': 0}) == Vec({'a', 'b', 'c'}, {})
    True
    >>> Vec({'a', 'b', 'c'}, {}) == Vec({'a', 'b', 'c'}, {'a': 0})
    True

    Be sure that equal(u, v) checks equalities for all keys from u.f and v.f even if
    some keys in u.f do not exist in v.f (or vice versa)

    >>> Vec({'x','y','z'},{'y':1,'x':2}) == Vec({'x','y','z'},{'y':1,'z':0})
    False
    >>> Vec({'a','b','c'}, {'a':0,'c':1}) == Vec({'a','b','c'}, {'a':0,'c':1,'b':4})
    False
    >>> Vec({'a','b','c'}, {'a':0,'c':1,'b':4}) == Vec({'a','b','c'}, {'a':0,'c':1})
    False

    The keys matter:
    >>> Vec({'a','b'},{'a':1}) == Vec({'a','b'},{'b':1})
    False

    The values matter:
    >>> Vec({'a','b'},{'a':1}) == Vec({'a','b'},{'a':2})
    False
    """
    # check same domain set
    same_domain = set(u.D) == set(v.D)
    if same_domain:
        # check the same keys 
        if u.f.keys() == v.f.keys():
            # check the keys values 
            for k in u.f:
                if u.f[k] != v.f[k]:
                    return False
            return True
        elif u.f.keys() != v.f.keys():
            return False
        else:
            return False
    return False

def add(u,v):
    """
    Returns the sum of the two vectors.
    
    Consider using brackets notation u[...] and v[...] in your procedure
    to access entries of the input vectors.  This avoids some sparsity bugs.

    Do not seek to create more sparsity than exists in the two input vectors.
    Doing so will unnecessarily complicate your code and will hurt performance.

    Make sure to add together values for all keys from u.f and v.f even if some keys in u.f do not
    exist in v.f (or vice versa)

    >>> a = Vec({'a','e','i','o','u'}, {'a':0,'e':1,'i':2})
    >>> b = Vec({'a','e','i','o','u'}, {'o':4,'u':7})
    >>> c = Vec({'a','e','i','o','u'}, {'a':0,'e':1,'i':2,'o':4,'u':7})
    >>> a + b == c
    True
    >>> a == Vec({'a','e','i','o','u'}, {'a':0,'e':1,'i':2})
    True
    >>> b == Vec({'a','e','i','o','u'}, {'o':4,'u':7})
    True
    >>> d = Vec({'x','y','z'}, {'x':2,'y':1})
    >>> e = Vec({'x','y','z'}, {'z':4,'y':-1})
    >>> f = Vec({'x','y','z'}, {'x':2,'y':0,'z':4})
    >>> d + e == f
    True
    >>> d == Vec({'x','y','z'}, {'x':2,'y':1})
    True
    >>> e == Vec({'x','y','z'}, {'z':4,'y':-1})
    True
    >>> b + Vec({'a','e','i','o','u'}, {}) == b
    True
    """
    domain = set(u.D | v.D)
    result = {}
    # copy from u to result vector
    for k in u.f.keys():
        result[k] = u.f[k]
    # print('u.f ', result)
    for key in v.f.keys():
        # print(f'current key {key}')
        # print('changes ', result)

        if key in u.f:
            result[key] = v.f[key] + u.f[key]
            # addition
            # print(f'addition {v.f[key]}+{u.f[key]}={result[key]}' )
        else:
            result[key] = v.f[key]
            # print(f'inserted {key} => {result[key]}' )
            
    return Vec(domain,result)

def dot(u,v):
    """
    Returns the dot product of the two vectors.

    Consider using brackets notation u[...] and v[...] in your procedure
    to access entries of the input vectors.  This avoids some sparsity bugs.

    >>> u1 = Vec({'a','b'}, {'a':1, 'b':2})
    >>> u2 = Vec({'a','b'}, {'b':2, 'a':1})
    >>> u1*u2
    5
    >>> u1 == Vec({'a','b'}, {'a':1, 'b':2})
    True
    >>> u2 == Vec({'a','b'}, {'b':2, 'a':1})
    True
    >>> v1 = Vec({'p','q','r','s'}, {'p':2,'s':3,'q':-1,'r':0})
    >>> v2 = Vec({'p','q','r','s'}, {'p':-2,'r':5})
    >>> v1*v2
    -4
    >>> w1 = Vec({'a','b','c'}, {'a':2,'b':3,'c':4})
    >>> w2 = Vec({'a','b','c'}, {'a':12,'b':8,'c':6})
    >>> w1*w2
    72

    The pairwise products should not be collected in a set before summing
    because a set eliminates duplicates
    >>> v1 = Vec({1, 2}, {1 : 3, 2 : 6})
    >>> v2 = Vec({1, 2}, {1 : 2, 2 : 1})
    >>> v1 * v2
    12
    """
    dot = 0
    for k in u.f.keys():
        if k in v.f.keys():
            dot = dot + (u.f[k]*v.f[k])
    return dot

def scalar_mul(v, alpha):
    """
    Returns the scalar-vector product alpha times v.

    Consider using brackets notation v[...] in your procedure
    to access entries of the input vector.  This avoids some sparsity bugs.

    >>> zero = Vec({'x','y','z','w'}, {})
    >>> u = Vec({'x','y','z','w'},{'x':1,'y':2,'z':3,'w':4})
    >>> 0*u == zero
    True
    >>> 1*u == u
    True
    >>> 0.5*u == Vec({'x','y','z','w'},{'x':0.5,'y':1,'z':1.5,'w':2})
    True
    >>> u == Vec({'x','y','z','w'},{'x':1,'y':2,'z':3,'w':4})
    True
    """
    if alpha == 0:
        return Vec(v.D,{})
    negated_f = {k: alpha*v[k] for k in v.f}
    return Vec(v.D, negated_f)
    
def neg(v):
    """
    Returns the negation of a vector.

    Consider using brackets notation v[...] in your procedure
    to access entries of the input vector.  This avoids some sparsity bugs.

    >>> u = Vec({1,3,5,7},{1:1,3:2,5:3,7:4})
    >>> -u
    Vec({1, 3, 5, 7},{1: -1, 3: -2, 5: -3, 7: -4})
    >>> u == Vec({1,3,5,7},{1:1,3:2,5:3,7:4})
    True
    >>> -Vec({'a','b','c'}, {'a':1}) == Vec({'a','b','c'}, {'a':-1})
    True
    """
    #print("========================================")
    negated_f = {k: -v[k] for k in v.f}
    return Vec(v.D, negated_f)

###############################################################################################################################

class Vec:
    """
    A vector has two fields:
    D - the domain (a set)
    f - a dictionary mapping (some) domain elements to field elements
        elements of D not appearing in f are implicitly mapped to zero
    """
    def __init__(self, labels, function):
        assert isinstance(labels, set)
        assert isinstance(function, dict)
        self.D = labels
        self.f = function

    __getitem__ = getitem
    __setitem__ = setitem
    __neg__ = neg
    __rmul__ = scalar_mul #if left arg of * is primitive, assume it's a scalar

    def __mul__(self,other):
        #If other is a vector, returns the dot product of self and other
        if isinstance(other, Vec):
            return dot(self,other)
        else:
            return NotImplemented  #  Will cause other.__rmul__(self) to be invoked

    def __truediv__(self,other):  # Scalar division
        return (1/other)*self

    __add__ = add

    def __radd__(self, other):
        "Hack to allow sum(...) to work with vectors"
        if other == 0:
            return self

    def __sub__(a,b):
        "Returns a vector which is the difference of a and b."
        return a+(-b)

    __eq__ = equal

    def is_almost_zero(self):
        s = 0
        for x in self.f.values():
            if isinstance(x, int) or isinstance(x, float):
                s += x*x
            elif isinstance(x, complex):
                y = abs(x)
                s += y*y
            else: return False
        return s < 1e-20

    def __str__(v):
        "pretty-printing"
        D_list = sorted(v.D, key=repr)
        numdec = 3
        wd = dict([(k,(1+max(len(str(k)), len('{0:.{1}G}'.format(v[k], numdec))))) if isinstance(v[k], int) or isinstance(v[k], float) else (k,(1+max(len(str(k)), len(str(v[k]))))) for k in D_list])
        s1 = ''.join(['{0:>{1}}'.format(str(k),wd[k]) for k in D_list])
        s2 = ''.join(['{0:>{1}.{2}G}'.format(v[k],wd[k],numdec) if isinstance(v[k], int) or isinstance(v[k], float) else '{0:>{1}}'.format(v[k], wd[k]) for k in D_list])
        return "\n" + s1 + "\n" + '-'*sum(wd.values()) +"\n" + s2

    def __hash__(self):
        "Here we pretend Vecs are immutable so we can form sets of them"
        h = hash(frozenset(self.D))
        for k,v in sorted(self.f.items(), key = lambda x:repr(x[0])):
            if v != 0:
                h = hash((h, hash(v)))
        return h

    def __repr__(self):
        return "Vec(" + str(self.D) + "," + str(self.f) + ")"

    def copy(self):
        "Don't make a new copy of the domain D"
        return Vec(self.D, self.f.copy())

    def __iter__(self):
        raise TypeError('%r object is not iterable' % self.__class__.__name__)


def gf2_add(u,v):
    assert isinstance(u, GF2_Vec)
    assert isinstance(v, GF2_Vec)
    new_list = [x ^ y for (x,y) in zip(u.bits(),v.bits())]
    return new_list

def gf2_equal(u,v):
    assert isinstance(u, GF2_Vec)
    assert isinstance(v, GF2_Vec)
    return u.bits() == v.bits()

class GF2_Vec:
    """
    GF2_Vector 
    bit stream vector, assuming vectors are with same length
    """
    def __init__(self, bitStream):
        assert isinstance(bitStream, list)
        self.bitStream = bitStream

    def bits(self):
        return self.bitStream
    
    def sumOfBitStreams(self, vectors):
        assert isinstance(vectors, list)
        assert isinstance(vectors[0], GF2_Vec)
        # vector length
        result:GF2_Vec = GF2_Vec([0] * len(vectors[0].bits()))
        # length
        l = len(vectors)
        # TODO: Fix
        for i in range(l):
            exp_cast:GF2_Vec = cast(GF2_Vec,vectors[i])
            result =  result + exp_cast
        return result
        
    def revel(self):
        print(self.bitStream)
    
    def __str__(self):
        s1 = ''.join(self.bits())
        return s1

    __add__ = gf2_add
    __eq__ = gf2_equal