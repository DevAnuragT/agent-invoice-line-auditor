import math, unittest
from agent import analyze
def p(): return {"lines":[{"id":"L1","quantity":2,"unit_price":10,"tax_rate":.1}],"stated_total":22}
class Tests(unittest.TestCase):
    def test_match(self): self.assertEqual(analyze(p())["status"],"match")
    def test_subtotal(self): self.assertEqual(analyze(p())["calculated_subtotal"],20)
    def test_tax(self): self.assertEqual(analyze(p())["calculated_tax"],2)
    def test_mismatch(self):
        x=p(); x["stated_total"]=25; self.assertEqual(analyze(x)["status"],"mismatch")
    def test_tolerance(self):
        x=p(); x["stated_total"]=22.02; x["tolerance"]=.02; self.assertTrue(analyze(x)["within_tolerance"])
    def test_duplicate(self):
        x=p(); x["lines"]*=2
        with self.assertRaises(ValueError): analyze(x)
    def test_bool(self):
        x=p(); x["lines"][0]["quantity"]=True
        with self.assertRaises(ValueError): analyze(x)
    def test_nan(self):
        x=p(); x["stated_total"]=math.nan
        with self.assertRaises(ValueError): analyze(x)
    def test_tax_bounds(self):
        x=p(); x["lines"][0]["tax_rate"]=1.1
        with self.assertRaises(ValueError): analyze(x)
if __name__ == "__main__": unittest.main()
