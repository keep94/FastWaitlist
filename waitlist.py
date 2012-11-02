"""
Implements a waitlist. Operations:

- Add entity O(1)
- Remove entity O(log n)
- Get entity's position O(log n)
- Traverse waitlist in order O(n)
"""
class WaitList(object):

  _none = object()

  def __init__(self):
    self._keydict = {}
    self._reversedict = {}
    self._positdict = {}
    self._nextId = 1

  def Add(self, key):
    """ Add Entity."""
    if key in self._keydict:
      return
    self._keydict[key] = self._nextId
    self._reversedict[self._nextId] = key
    self._positdict[self._nextId] = self._Get(
        self._nextId - 1, self._nextId) + 1
    self._nextId += 1

  def Contains(self, key):
    """See if entity is in the list."""
    return key in self._keydict

  def Remove(self, key):
    """Remove entity from list. Raises KeyError if not found."""
    self._Remove(self._keydict.pop(key))

  def Discard(self, key):
    """Like Remove except a no-op if not found."""
    keyid = self._keydict.pop(key, self._none)
    if keyid is self._none:
      return
    self._Remove(keyid)

  def Get(self, key):
    """Returns 1-based position of entity in list.
    Raises KeyError if not found."""
    return self._Get(self._keydict[key], 0)

  def Find(self, key):
    """Like Get but returns 0 if not found."""
    keyid = self._keydict.get(key, self._none)
    if keyid is self._none:
      return 0
    return self._Get(keyid, 0)

  def IList(self):
    """Returns iterator emitting tuples of 1-based position and
     entity in order."""
    return self._IList(0, 0, self._nextId - 1, len(self._keydict))

  def __len__(self):
    return len(self._keydict)

  def _IList(self, start, sp, end, ep):
    if sp == ep:
      return
    if end - start == 1:
      yield ep, self._reversedict[end]
      return
    nend, nep = start, sp
    incr = 1
    while nend < end:
      nstart, nsp =  nend, nep
      nend = start + incr
      nep = self._ComputePosit(sp, nend, end, ep)
      for x in self._IList(nstart, nsp, nend, nep):
        yield x
      incr <<= 1

  def _ComputePosit(self, sp, posit, end, ep):
    if posit >= min(self._nextId, end):
      return ep
    return sp + self._positdict.get(posit, 0)
    
  def _Get(self, posit, end):
    return sum(self._positdict.get(id, 0) for id in self._GoDown(posit, end))

  def _GoUp(self, posit):
    span = 1
    while posit < self._nextId:
      yield posit
      while not posit & span:
        span <<= 1
      posit += span
      span <<= 1

  def _GoDown(self, posit, end):
    span = 1
    while posit | end != end:
      yield posit
      while not posit & span:
        span <<= 1
      posit -= span
      span <<= 1

  def _Remove(self, keyid):
    self._reversedict.pop(keyid)
    for id in self._GoUp(keyid):
      count = self._positdict.pop(id) - 1
      if count:
        self._positdict[id] = count
