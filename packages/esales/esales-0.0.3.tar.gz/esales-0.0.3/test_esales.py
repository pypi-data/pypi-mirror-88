import unittest
import esales

class test_esales(unittest.TestCase):

    def test_allenamen(self):
        a = esales.esales[0]
        b = "Marlijn"
        self.assertEqual(a,b)
        a = esales.esales[1]
        b = "Ilona"
        self.assertEqual(a,b)
        a = esales.esales[2]
        b = "Godelieve"
        self.assertEqual(a,b)
        a = esales.esales[3]
        b = "Jelmer"
        self.assertEqual(a,b)
        a = esales.esales[4]
        b = "Hok"
        self.assertEqual(a,b)
        a = esales.esales[5]
        b = "Angelique"
        self.assertEqual(a,b)
        a = esales.esales[6]
        b = "Twan"
        self.assertEqual(a,b, msg="Hee ouwe dibbes! Stel die deployment maar uit! Want we hebben een fout! Want " + esales.esales[6] + "... Who the f*ck is" + esales.esales[6] +"? Geef ons ouwe Twannes terug en je mag gaan deploymen, zoniet, dan sodemieter je maar op!")

if __name__ == '__main__':
    unittest.main()
