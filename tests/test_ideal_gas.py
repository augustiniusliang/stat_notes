"""Run: python -m unittest discover -s tests -v (requires sympy, mpmath)."""
import unittest
from pathlib import Path
import sympy as s
import mpmath as mp

class IdealGas(unittest.TestCase):
    def test_density_and_thermal_normalization(self):
        e,m,V,h,b=s.symbols('e m V h b', positive=True)
        p=s.sqrt(2*m*e)
        D=4*s.pi*V/h**3*p**2*s.diff(p,e)
        self.assertEqual(s.simplify(D-2*s.pi*V/h**3*(2*m)**s.Rational(3,2)*s.sqrt(e)),0)
        Z1=s.integrate(D*s.exp(-b*e),(e,0,s.oo))
        self.assertEqual(s.simplify(Z1-V*(2*s.pi*m/b)**s.Rational(3,2)/h**3),0)

    def test_integrals_and_derivatives(self):
        mp.mp.dps=35
        for g,z in [(1,mp.mpf('.2')),(1,mp.mpf('3')),(-1,mp.mpf('.2')),(-1,mp.mpf('.9'))]:
            b=mp.mpf('1.7')
            # Set the DOS prefactor to 1; retain beta and z independently.
            L=lambda b,z:g*mp.quad(lambda e:mp.sqrt(e)*mp.log(1+g*z*mp.exp(-b*e)),[0,mp.inf])
            N=mp.quad(lambda e:mp.sqrt(e)/(mp.exp(b*e)/z+g),[0,mp.inf])
            U=mp.quad(lambda e:e**mp.mpf('1.5')/(mp.exp(b*e)/z+g),[0,mp.inf])
            for a,c in [(z*mp.diff(lambda zz:L(b,zz),z),N),(-mp.diff(lambda bb:L(bb,z),b),U),(L(b,z)/b,2*U/3)]:
                self.assertTrue(mp.almosteq(a,c))
            for q in [mp.mpf('1.5'),mp.mpf('2.5')]:
                I=mp.quad(lambda e:e**(q-1)/(mp.exp(b*e)/z+g),[0,mp.inf])
                F=-mp.polylog(q,-g*z)/g
                self.assertTrue(mp.almosteq(I,mp.gamma(q)*b**(-q)*F))

    def test_virial_and_sommerfeld_coefficients(self):
        x=s.symbols('x')
        for g in [-1,1]:
            z=x+g*x**2/2**s.Rational(3,2)+(s.Rational(1,4)-3**(-s.Rational(3,2)))*x**3
            F=lambda q:z-g*z**2/2**q+z**3/3**q
            self.assertEqual(s.simplify(s.series(F(s.Rational(3,2)),x,0,4).removeO()-x),0)
            ratio=s.series(F(s.Rational(5,2))/x,x,0,3).removeO()
            self.assertEqual(s.simplify(ratio-1-g*x/2**s.Rational(5,2)-(s.Rational(1,8)-2/3**s.Rational(5,2))*x**2),0)
        E,N=s.symbols('E N',positive=True)
        D=3*N*s.sqrt(x)/(2*E**s.Rational(3,2))
        self.assertEqual(s.integrate(D,(x,0,E)),N)
        delta=-s.pi**2/6*s.diff(D,x).subs(x,E)/D.subs(x,E)
        self.assertEqual(s.simplify(delta+s.pi**2/(12*E)),0)
        u2=E*D.subs(x,E)*delta+s.pi**2/6*s.diff(x*D,x).subs(x,E)
        self.assertEqual(s.simplify(u2-s.pi**2*N/(4*E)),0)

    def test_source_regressions(self):
        text=(Path(__file__).resolve().parents[1]/'chaps/ideal_gas.tex').read_text()
        self.assertIn(r'\beta^{-3/2}\Gamma',text)
        self.assertIn(r'\beta^{-5/2}\Gamma',text)
        self.assertNotIn(r'4\pi (2m)^{\frac32}',text)
        self.assertIn(r'\mu = \frac{\hbar^2}{2m}',text)
        self.assertIn(r'p = \frac{2U}{3V}',text)

if __name__=='__main__': unittest.main()
