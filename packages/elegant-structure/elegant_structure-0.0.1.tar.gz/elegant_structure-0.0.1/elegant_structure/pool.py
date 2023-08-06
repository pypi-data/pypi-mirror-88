class Pool:
  
  def __init__(self, Obj, verbose=False):
    self.Obj = Obj
    self.next_id = 0
    self.removed_ids = []
    self.items = []
    self.verbose = verbose
  
  def get_next_id(self):
    nid = self.next_id
    if self.removed_ids:
      nid = self.removed_ids.pop()
    else: 
      self.next_id += 1
    return nid
  
  def add(self, *argv, **kwargs):
    nid = self.get_next_id()
    assert nid <= len(self.items), f'Error happen when adding item to pool'
    if nid == len(self.items):
      self.items.append(self.Obj(*argv, **kwargs))
    else:
      self.items[nid].__init__(*argv, **kwargs)
    return nid
  
  def remove(self, nid):
    self.removed_ids.append(nid)
    
  def __getitem__(self, nid):
    if nid >= len(self.items) or nid in self.removed_ids:
      if self.verbose:
        print('the item is not exist in pool.')
      return None
    else:
      return self.items[nid]
    
  def all(self):
    return [self.items[i] for i in range(len(self.items)) if i not in self.removed_ids]
  
  def __repr__(self):
    return str(self.all())