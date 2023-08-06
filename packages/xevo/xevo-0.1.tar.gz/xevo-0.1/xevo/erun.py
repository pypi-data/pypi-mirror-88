import matplotlib.pyplot as plt
import numpy as np
import time

class erun:
  
  def __init__(s,vo,obj,population=10,show=True,delay=None):
    """vo: some evo
       obj: some eobj
       population=10: size of population
    
    """
    s.vo=vo
    s.obj=obj
    
    s.vo.populate(s.obj,population)
    
    s.shallmaximize=s.obj.shallmaximize()
    
    s.delay=delay
    
    s.show=show
    
    s.maxs=[]
    s.means=[]
    s.stds=[]
  def getwinner(s):
    return s.vo.getwinner()
  def gettopn(s,n=3):
    return s.vo.gettopn(n=n)
  
  def run(s,maxsteps=1000000,goalstrength=1000000.0):
    for i in range(maxsteps):
      mx,mm,ss=s.vo.logeneration(s.show)
      s.maxs.append(mx)
      s.means.append(mm)
      s.stds.append(ss)
      if s.shallmaximize:
        if mx>=goalstrength:return
      else:
        if mx<=goalstrength:return
      if not s.delay is None:
        time.sleep(s.delay)
  
  def show_history(s,log=False):
    i=np.arange(len(s.maxs))
    
    plt.close()
    
    lab="max"
    if not s.shallmaximize:lab="min"
    plt.plot(i,s.maxs,alpha=0.5,color="red",label=lab)
    
    plt.plot(i,s.means,alpha=0.5,color="black",label="mean")
    me=np.array(s.means)
    st=np.array(s.stds)
    plt.fill_between(i,me-st,me+st,color="gray",alpha=0.3)
    
    if log:plt.yscale("log",nonpositive="clip")
    
    plt.legend()
    
    plt.show()
      








