import unittest

import mixed_interaction_audit as m


class MixedInteractionTests(unittest.TestCase):
    @staticmethod
    def config(a=0.3, b=0.2, ma=0, mb=0, eta=0):
        return {
            "alpha": a, "beta": b,
            "samples": {"f00": 0.0, "fa0": 0.0, "f0b": 0.0, "fab": 5 * a * b},
            "mixed_derivative_variation": {"alpha": ma, "beta": mb},
            "absolute_readout_error": {k: eta for k in m.KEYS},
        }

    def test_quadratic_exact_interaction(self):
        r = m.audit(self.config())["observation"]
        self.assertAlmostEqual(r["central_mixed_derivative_estimate"], 5)
        self.assertEqual(r["total_bound"], 0)
        self.assertTrue(r["zero_excluded"])

    def test_cubic_truncation_covers_known_bias(self):
        # F(alpha,beta) = 5 alpha beta + 2 alpha^2 beta - 3 alpha beta^2
        a, b = .4, .3
        r = self.config(a, b, ma=4, mb=6)
        r["samples"]["fab"] = a * b * (5 + 2*a - 3*b)
        out = m.audit(r)["observation"]
        self.assertLessEqual(abs(out["central_mixed_derivative_estimate"] - 5), out["truncation_bound"] + 1e-14)
        self.assertAlmostEqual(out["truncation_bound"], 2 * a + 3 * b)

    def test_noise_interval_can_be_inconclusive(self):
        r = self.config(a=0.1, b=0.1, eta=0.03)
        o = m.audit(r)["observation"]
        self.assertFalse(o["zero_excluded"])
        self.assertEqual(o["conditional_sign"], "INCONCLUSIVE")

    def test_negative_signed_amplitudes(self):
        r = self.config(a=-0.25, b=0.3, ma=2, mb=4)
        o = m.audit(r)["observation"]
        self.assertAlmostEqual(o["central_mixed_derivative_estimate"], 5.0)
        self.assertAlmostEqual(o["truncation_bound"], 0.25 + 0.6)

    def test_positive_unconstrained_optimum(self):
        r = self.config(a=1, b=1, ma=2, mb=2, eta=0.01)
        out = m.audit(r)
        h = (0.04)**(1/3)
        self.assertAlmostEqual(out["unconstrained_positive_optimum"]["abs_alpha"], h)
        self.assertAlmostEqual(out["unconstrained_positive_optimum"]["abs_beta"], h)
        self.assertAlmostEqual(out["unconstrained_positive_optimum"]["error_bound"], 3*h)

    def test_candidate_grid_selects_smallest_bound(self):
        r = self.config(a=.2,b=.2,ma=2,mb=2,eta=.01)
        r["candidate_amplitudes"] = {"alpha":[.1,.3,.8], "beta":[.1,.3,.8]}
        out=m.audit(r)["candidate_design"]
        self.assertAlmostEqual(out["best"]["alpha"], .3)
        self.assertAlmostEqual(out["best"]["beta"], .3)

    def test_fail_closed_invalid_arguments(self):
        r = self.config()
        r["alpha"] = 0.0
        with self.assertRaises(ValueError): m.audit(r)
        r = self.config()
        r["mixed_derivative_variation"]["beta"] = -0.1
        with self.assertRaises(ValueError): m.audit(r)
        r = self.config()
        r["absolute_readout_error"].pop("fab")
        with self.assertRaises(ValueError): m.audit(r)
        r = self.config()
        r["samples"].pop("fab")
        with self.assertRaises(ValueError): m.audit(r)


if __name__ == "__main__":
    unittest.main()
