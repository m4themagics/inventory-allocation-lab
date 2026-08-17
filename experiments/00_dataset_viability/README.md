# 00 — Dataset viability: can M5 support repeated allocation decisions?

**Status:** draft; pass criteria fixed, dataset slice and operational rules not yet
preregistered.

This experiment exists to kill the dataset or the proposed operational layer cheaply. It
runs before a full loader, forecast model or optimiser is written and before M5 is committed
to.

## Question

Does the M5 dataset contain enough repeated item-by-store demand, under a cohort selected
strictly from the past, to support 26 rolling inventory-allocation decisions whose scarcity
regimes are materially different?

## Why it must run first

The central question assumes a stable set of products is repeatedly allocated across stores,
with enough history to estimate uncertainty and enough resource pressure for the policies to
disagree. Those assumptions are about the data and the semi-synthetic operational layer, not
about Pyomo — and they are cheap to check before six months are spent.

Three traps:

**Future-selected winners.** Choosing the “top 50” products using the complete M5 history
uses test demand to decide which series deserve to exist. The cohort rule is fitted once on
the initial train window and frozen before validation.

**Sales masquerading as demand.** M5 has no source inventory or stockout flag. A zero may be
true zero demand or censored demand. This experiment describes intermittency; it does not
pretend to identify the two causes.

**Scarcity manufactured from the answer.** Defining weekly central supply as a fraction of
realised next-week sales would guarantee attractive binding constraints by leaking the
outcome. Supply and capacity rules may use train/validation statistics, never the demand of
the week being planned.

## Preregistered pass criteria

All three must hold. Thresholds are fixed now so the scope cannot be softened after the
numbers are seen.

**A — Temporal support.** After an initial **104 train weeks** and **13 validation weeks**,
the chosen slice retains at least **26 consecutive test weeks** with complete calendar dates.
*Without repeated future decisions there is no closed-loop experiment.*

**B — Stable allocation cohort.** The train-only rule yields at least **50 items**. Each item
has non-zero network sales in at least **60% of train weeks** and appears in at least **8 of
10 stores** during validation.
*A collection of one-off products is assortment selection, not repeated inventory
allocation.*

**C — Distinct constraint regimes.** On validation only, train-derived operational rules make
the `0.6` scarcity regime supply-binding in at least **80%** of weeks and the `1.2` regime
supply-binding in at most **20%**. The item cohort and demand forecasts are identical across
regimes.
*If tight and loose create the same feasible set, the main experimental axis is decoration.*

## Diagnostic that decides between two stories

The moving-block residual profile: zero share, variance-to-mean ratio and cross-store
correlation for whole weekly residual vectors.

High dispersion and dependence support the mechanism “joint scenarios may change the last
case-pack decisions”. Low dependence does not reject M5 — it predicts a smaller stochastic
gain and turns “deterministic is enough here” into the likely result.

Price coverage is reported beside this diagnostic. Missing price may remove a forecast
feature, but does not by itself invalidate the allocation question.

## Outcomes

| Result | Action |
|---|---|
| A, B, C pass | Commit to M5 and freeze the cohort/operational rules. |
| A or B fails | Reject this M5 scope before modelling; do not hand-pick an easier cohort. |
| C fails | Reject the operational-layer rule; revise it once on train/validation, preregister again, then rerun. |
| Diagnostics show weak dependence | Continue, but preregister the expectation that scenario MILP may not pay. |

## Run

The entry point is implemented in phase 0, not in this scaffold. Its fixed interface will be:

```bash
uv run python experiments/00_dataset_viability/run.py --config configs/m5.yaml
```

It will expect `calendar.csv`, `sales_train_evaluation.csv` and `sell_prices.csv` under
`data/raw/m5/` and write one JSON result plus a human-readable pass/fail report.
