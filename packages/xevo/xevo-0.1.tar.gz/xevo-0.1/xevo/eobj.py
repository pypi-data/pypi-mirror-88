from abc import ABCMeta,abstractmethod

import numpy as np


class eobj(object):
  """
  any eobj class contains at least
  def __add__(a,b):
  def randomize(s):
  def mutate(s):
  def calcstrength(s):
  def _copy(s):
  
  also __init__(s) should not contain any nonoptional parameters and call s.initial()
  """
  __metaclass__=ABCMeta
  
  def initial(s):
    s.stre=None
  
  def figth(a,b):
    """does a win against b"""
    sa=a.strength()
    sb=b.strength()
    
    if not a.shallmaximize():sa*=-1
    if not b.shallmaximize():sb*=-1
    if not sa==sb:return sa>sb
    return np.random.randint(2)==0
    
  
  def shallmaximize(s):
    """can be flipped to allow for minimization tasks"""
    return True
  
  @abstractmethod
  def __add__(a,b) -> "subclass of eobj":
    """define how to combine two objects"""
    pass
  
  @abstractmethod
  def randomize(s):
    """initialises a new object with initial random? parameters"""
    pass

  @abstractmethod
  def mutate(s) ->"subclass of eobj":
    """define how to mutate an object"""
    pass
  
  @abstractmethod
  def calcstrength(s) -> float:
    """calculate how strong the current object is"""
    return 0.0
  
  def strength(s) -> float:
    """define how strong the current object is"""
    if (not hasattr(s, 'stre')) or s.stre is None:
      s.stre=s.calcstrength()
    return s.stre
  

  @abstractmethod
  def _copy(s) -> "subclass of eobj":
    """copy the current object"""
  
  def copy(s) -> "subclass of eobj":
    """copy the current object"""
    ret=s._copy()
    return ret
  
  def __repr__(s):
    return str(s)