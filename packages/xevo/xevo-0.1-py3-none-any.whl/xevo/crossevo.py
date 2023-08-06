from xevo.evo import evo

import numpy as np
import time
    

class crossevo(evo):
  """similar to lineevo but no concept of neighbours"""
  
  def __init__(s,wsmerge=0.3):
    s.initial()
    s.wsmerge=wsmerge



  def generation(s)->None:
    i1=np.random.randint(len(s.q))
    i2=i1
    while i1==i2:
      i2=np.random.randint(len(s.q))
    i1won=s.q[i1].figth(s.q[i2])
    iwon=i1
    ilost=i2
    if not i1won:
      iwon=i2
      ilost=i1
    if np.random.random()<s.wsmerge:
      s.q[ilost]+=s.q[iwon]
    else:
      s.q[ilost]=s.q[iwon].mutate()
    
    


  def _copy(s):
    return crossevo(s.wsmerge)



