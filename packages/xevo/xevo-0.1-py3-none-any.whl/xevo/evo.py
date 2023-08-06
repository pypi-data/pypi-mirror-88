from abc import ABCMeta,abstractmethod

from time import time
import numpy as np

class evo(object):
  """
  any evo class contains at least
  def generation(s)->None:
  def _copy(s) -> "subclass of evo":
  
  """
  __metaclass__=ABCMeta
  
  def initial(s):
    s.q=[]
    s.i=0
  def __init__(s):
    s.initial()
  
  def populate(s,person,n=10)->None:
    s.q.append(person)
    while len(s.q)<n:
      s.q.append(person.randomize())

  
  @abstractmethod
  def generation(s)->None:
    """runs one update step"""
    pass
  
  def winner(s)->int:
    """finds the winner of the current batch"""
    val=[qq.strength() for qq in s.q]
    if s.q[0].shallmaximize():
      return np.argmax(val)
    else:
      return np.argmin(val)
  def topn(s,n=3)->"[int]":
    """finds n top players of the current batch"""
    if s.q[0].shallmaximize():
      val=[qq.strength() for qq in s.q]
    else:
      val=[-qq.strength() for qq in s.q]
    val=np.array(val)

    return val.argsort()[-n:][::-1]
  
  def average(s)->"float,float":
    """finds the average strength and its standard deviation"""
    val=[qq.strength() for qq in s.q]
    return np.mean(val),np.std(val)

  
  def logeneration(s,show=True)->"max,mean,std strength":
    """same as generation, but prints some stuff about the current gen"""
    t0=time()
    s.generation()
    t1=time()
    dt=int(t1-t0)
    index=s.winner()
    win=s[index]
    strength=win.strength()
    s.i+=1
    mm,ss=s.average()

    if show:
      print(f"-----generation {s.i} needed {dt}s-----")
      print(f"best object {index} reached strength {strength}")
      print(f"mean strength {mm} +- {ss}")
      print("")
    
    return strength,mm,ss
    
    
  
  def __getitem__(s, key):
    return s.q[key]
  
  def __setitem__(s,key,obj):
    s.q[key]=obj

  @abstractmethod
  def _copy(s) -> "subclass of evo":
    """copies everything used in the current object"""
    pass
  def copy(s) -> "subclass of evo":
    ret=s._copy()
    ret.i=s.i
    ret.q=[]
    for qq in s.q:
      ret.q.append(qq.copy())
    return ret
  
  def getwinner(s)->"eobj":
    return s[s.winner()]
  def gettopn(s,n=3)->"[eobj]":
    return [s[q] for q in s.topn(n=n)]
  