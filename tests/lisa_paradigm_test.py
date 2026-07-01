"""Unit checks for the LISA v1.093 paradigm's math helpers.

Expected values are taken from the worked examples in the design post
(https://forum.nationstates.net/viewtopic.php?p=42898867#p42898867) and from
formulas read directly out of the mock spreadsheet's cells (confirmed via the
live sheet, not just the prose) at
https://docs.google.com/spreadsheets/d/1glbWWYG1yG8iRO-3f-ct6IfPGEW3l0BTo2-BoOqhUD0
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from xkoranate.paradigms.lisaparadigm import XkorLISAParadigm


def make_paradigm(**opts):
    p = XkorLISAParadigm()
    p.opt = opts
    p.userOpt = {}
    return p


def approx(a, b, tol=1e-3):
    return abs(a - b) < tol


# --- EAR / win probability formulas (unchanged from v1.0 to v1.093) ---

p = make_paradigm(powerScalar=1.984, refRank=10.93, REAR=300)
ear_at_ref_rank = p._ear(10.93)
assert approx(ear_at_ref_rank, 300, tol=1e-6), ear_at_ref_rank  # REAR is EAR at the reference rank, by construction

drawP, homeWinP, awayWinP = p._winDrawProbabilities(500, 500)
# equal teams: u = xW = 0.5, so DrawP = u-u^2 = 0.25 and each side splits the
# remaining 0.75 evenly (both are simultaneously "the underdog" at u=xW)
assert approx(drawP, 0.25), drawP
assert approx(homeWinP, 0.375) and approx(awayWinP, 0.375), (homeWinP, awayWinP)
assert approx(drawP + homeWinP + awayWinP, 1.0), (drawP, homeWinP, awayWinP)

# --- winning margin distribution (mean and P(margin=1), using the OLD
#     divisor of 500 for these specific worked examples, which predate the
#     v1.093 "margin divisor" concept) ---

p500 = make_paradigm(marginDivisor=500)


def zt_poisson_mean(lam):
    return lam / (1 - math.exp(-lam))


def zt_poisson_p1(lam):
    return lam / (math.exp(lam) - 1)


lam0 = p500._marginLambda(0)
assert approx(lam0, 1.093), lam0
assert approx(zt_poisson_mean(lam0), 1.644, tol=0.01), zt_poisson_mean(lam0)
assert approx(zt_poisson_p1(lam0), 0.551, tol=0.001), zt_poisson_p1(lam0)

lam350 = p500._marginLambda(350)  # favourite wins by a big EAR gap
assert approx(lam350, 2.201, tol=0.001), lam350
assert approx(zt_poisson_mean(lam350), 2.475, tol=0.01), zt_poisson_mean(lam350)
assert approx(zt_poisson_p1(lam350), 0.274, tol=0.001), zt_poisson_p1(lam350)

lamNeg350 = p500._marginLambda(-350)  # underdog wins by the same gap
# note: the forum post's prose actually mislabels P(margin=1) as "λ = 0.753"
# for this example; the real lambda (~0.543) is what reproduces its own
# stated mean (1.296) and P(margin=1) (75.3%) figures, checked below
assert approx(lamNeg350, 0.5427, tol=0.001), lamNeg350
assert approx(zt_poisson_mean(lamNeg350), 1.296, tol=0.01), zt_poisson_mean(lamNeg350)
assert approx(zt_poisson_p1(lamNeg350), 0.753, tol=0.001), zt_poisson_p1(lamNeg350)

# --- v1.093's revised losing-team-score lambda, checked against the mock
#     sheet's live cell CG5 (NetStyle=9.000, margin=2 -> lambda=0.690) ---

p750 = make_paradigm(marginDivisor=750)
assert approx(p750._losingScoreLambda(netStyle=9.0, margin=2), 0.690, tol=0.001)

# large margins should suppress the loser's expected goals more than small
# ones do, for the same style sum (the actual "Scorigami Mitigation" change)
lam_small_margin = p750._losingScoreLambda(netStyle=0, margin=1)
lam_large_margin = p750._losingScoreLambda(netStyle=0, margin=8)
assert lam_large_margin < lam_small_margin, (lam_small_margin, lam_large_margin)

print("ALL LISA PARADIGM TESTS PASSED")
