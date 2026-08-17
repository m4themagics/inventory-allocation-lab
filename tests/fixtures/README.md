# Hand-checkable fixtures

Здесь появятся только маленькие данные, которые можно проверить на бумаге и коммитить.

Первая fixture — `2 items × 2 stores × 3 weeks`:

- integer demand и on-hand inventory;
- разные case-pack sizes;
- один binding supply constraint;
- один binding store-capacity constraint;
- известный deterministic optimum полным перебором;
- два demand scenarios, для которых stochastic plan отличается от mean-demand plan;
- один намеренно infeasible plan для independent checker.

Большой synthetic benchmark сюда не входит. Fixture существует ради correctness, а не ради
реалистичных метрик.
