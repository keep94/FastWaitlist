import itertools
import unittest
import waitlist

class WaitlistTest(unittest.TestCase):

  def test_empty(self):
    w = waitlist.WaitList()
    self.assertEqual(0, len(w))
    self.assertFalse(w.Contains('NotInList'))
    self.assertEqual(0, w.Find('NotInList'))
    self.assertRaises(KeyError, w.Get, 'NotInList')
    w.Discard('NotInList')
    self.assertRaises(KeyError, w.Remove, 1)
    self.assertEquals([], list(w.IList()))

  def test_add_partial_remove_remove_all(self):
    w = waitlist.WaitList()
    r = xrange(1, 1001)
    for i in r:
      w.Add(i)
    self.AssertWaitList([(i, i) for i in r], w)
    for i in xrange(1, 900):
      w.Remove(i)
    r = xrange(900, 1001)
    self.AssertWaitList([(i - 899, i) for i in r], w)
    for i in r:
      if i % 16 != 1:
        w.Remove(i)
    self.AssertWaitList(
        [(1, 913), (2, 929), (3, 945), (4, 961), (5, 977), (6, 993)], w)
    notInList = 950
    self.assertFalse(w.Contains(notInList))
    self.assertEqual(0, w.Find(notInList))
    self.assertRaises(KeyError, w.Get, notInList)

    for i in xrange(1, 1001):
      w.Discard(i)
    self.AssertWaitList([], w)
    self.assertEqual(0, len(w._positdict))

  def test_add_remove_multiple_times(self):
    w = waitlist.WaitList()
    self.AddRemove(w, 51)
    self.AddRemove(w, 101)
    self.AddRemove(w, 151)
    self.AddRemove(w, 201)

  def test_normal_use(self):
    w = waitlist.WaitList()
    w.Add('Mike')
    w.Add('Jill')
    w.Add('Bill')
    w.Add('Mike')  # Duplicate add

    self.AssertWaitList(
        [(1, 'Mike'), (2, 'Jill'), (3, 'Bill')], w)

    w.Remove('Jill')
    w.Add('Raymond')
    w.Add('Jill')

    self.AssertWaitList(
        [(1, 'Mike'), (2, 'Bill'), (3, 'Raymond'), (4, 'Jill')], w)

    # Take first two off
    for _, k in list(itertools.islice(w.IList(), 2)):
      w.Remove(k)

    self.AssertWaitList(
        [(1, 'Raymond'), (2, 'Jill')], w)
 
  def AddRemove(self, w, x):
    r = xrange(x)
    for i in r:
      w.Add(i)
    self.AssertWaitList([(i + 1, i) for i in r], w)
    for i in r:
      w.Remove(i)
    for i in r:
      self.assertFalse(w.Contains(i))
      self.assertEqual(0, w.Find(i))
    self.AssertWaitList([], w)

  def AssertWaitList(self, l, w):
    self.assertEqual(len(l), len(w))
    self.assertEqual(l, list(w.IList()))
    for p, k in l:
      self.assertTrue(w.Contains(k))
      self.assertEqual(p, w.Get(k))
      self.assertEqual(p, w.Find(k))

if __name__ == '__main__':
  unittest.main()
