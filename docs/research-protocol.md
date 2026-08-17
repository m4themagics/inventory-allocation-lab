# Research protocol

Правила, которым должен удовлетворять результат, чтобы попасть в README или в `reports/`.
Один эксперимент из `experiments/` — одно заполнение этого checklist. Пустые поля
заполняются **до** итогового прогона, а не после того, как число уже увидено.

## Preregistration

```text
Research question:
Expected mechanism:
Population and unit of observation:
Decision problem and information timestamp:
Baseline:
Treatment:
Primary forecast metric:
Primary decision metric:
Correctness gates:
Expected failure modes:
Stopping rule:
```

## Data contract

- У каждого allocation есть `as_of_week`; прогноз и operational state используют только
  информацию, известную строго до этого момента.
- Cohort товаров фиксируется на initial train window, а не на всей истории.
- Train/validation/test разделяются до выбора модели, scenario rule и baseline.
- Dataset revision, sampling rule, seed и fingerprint сохраняются.
- Пропуски и исключённые недели считаются и публикуются.
- M5 sales явно называются proxy спроса; stockouts и substitution не восстанавливаются
  молча.
- Central supply, inventory, capacity, case packs и costs генерируются только из
  train/validation по заранее записанным правилам. Test outcome их не меняет.

## Evaluation contract

- Forecast quality и decision quality оцениваются отдельно.
- Policies получают одинаковые realised demand и inbound supply, но каждая ведёт собственную
  inventory trajectory.
- Oracle решает ту же задачу из pre-decision state конкретной policy, а не из общего удобного
  состояния.
- Hand-solvable `2 × 2` instance совпадает с полным перебором и солвером.
- Inventory balance и hard constraints перепроверяются вне Pyomo.
- One-scenario stochastic model совпадает с deterministic model.
- Solver status, gap, time limit, runtime и fallback сохраняются; неуспешные решения не
  исчезают из denominator.
- Per-week outcomes сохраняются для paired analysis.

## Uncertainty

До прогона выбрать block-bootstrap unit, длину блока, число repetitions и seed. Публиковать
effect size и interval для paired cost difference. Если interval включает ноль, результат не
называется улучшением или ухудшением.

Отдельные item × store rows не считаются независимыми наблюдениями. Основная единица — неделя
решения; временная зависимость сохраняется moving blocks.

## Reproducibility

Каждый run сохраняет commit, environment/lock revision, config snapshot, exact command,
seed, data fingerprint, solver version/settings и output paths. Clean-checkout smoke run —
обязательный gate.

## Publication gate

Finding появляется в README только когда:

- correctness tests проходят, включая ручной MILP и adversarial leakage test;
- protocol не был молча изменён после просмотра числа;
- uncertainty рассчитана;
- timeouts, infeasibility и fallback опубликованы рядом с cost;
- sensitivity к semi-synthetic operational layer показана;
- автор может провести teach-back без чтения кода: выписать objective/constraints, объяснить
  active constraint и вручную восстановить одну неделю решения.
