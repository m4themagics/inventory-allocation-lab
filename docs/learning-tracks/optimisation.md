# Optimisation learning track

Этот трек даёт mathematical и solver prerequisites для allocation policies. Он не является
отдельным research study: сначала здесь осваивается инструмент, затем с его помощью
проверяется гипотеза про value of the stochastic solution.

Не переходить к следующему модулю, пока текущий пример нельзя решить и объяснить без
подсказки. Готовой центральной MILP-реализации в репозитории намеренно нет.

## Module 0 — Notation and experiment discipline

Цель: отделить математическую постановку от синтаксиса Pyomo.

- [ ] Для каждого символа записать индекс, единицу измерения и момент доступности.
- [ ] На одном листе разделить parameters, variables и realised outcomes.
- [ ] Зафиксировать знак objective: cost minimisation.
- [ ] Записать, какие величины integer, а какие continuous.
- [ ] Для каждого solve сохранять solver/version/status/gap/time limit.

Gate: автор может рассказать задачу без слов “dataframe” и “библиотека”.

## Module 1 — Linear programming by hand

Темы:

- feasible region;
- linear objective и active constraints;
- slack;
- primal и dual;
- shadow price;
- infeasibility и unboundedness.

Упражнения:

1. Решить графически LP с двумя shipment variables.
2. Назвать active constraints в optimum.
3. Ослабить supply на одну единицу и сравнить изменение objective с dual value.
4. Создать infeasible instance и выписать конфликтующие constraints.
5. Создать unbounded formulation намеренной потерей ограничения.

Gate: до солвера автор предсказывает направление изменения optimum при ослаблении каждого
ресурса.

## Module 2 — Inventory balance and allocation formulation

Темы:

- on-hand, shipment, served demand, shortage, ending inventory;
- lost sales против backorder;
- case packs;
- supply, store volume и receiving capacity;
- shipment, holding и shortage cost.

Упражнения:

1. Выписать balance equation для одного item/store/week.
2. Провести руками две недели и перенести ending inventory.
3. Решить `2 items × 2 stores` полным перебором.
4. Проверить размерности каждого слагаемого objective.
5. Показать, почему replay прошлого allocation не является безопасным fallback.

Gate: inventory mass сходится поэлементно, а optimum маленького instance известен до запуска
кода.

## Module 3 — Integer decisions and MILP

Темы:

- integer variable количества case packs;
- LP relaxation;
- integrality gap;
- branch-and-bound;
- incumbent, bound и relative MIP gap;
- time limit.

Упражнения:

1. Найти instance, где LP relaxation даёт дробные packs.
2. Посчитать integrality gap руками.
3. Сравнить optimal plan с первым feasible incumbent.
4. Объяснить, что можно и нельзя утверждать после time limit.
5. Проверить, что ослабление supply не ухудшает optimal objective.

Gate: автор различает feasible, optimal и best-known решение и не называет time-limited
incumbent оптимумом.

## Module 4 — Pyomo and HiGHS

Темы:

- sets, parameters, variables;
- objective и constraint rules;
- domains и bounds;
- solver adapter;
- termination condition;
- extraction и independent validation решения.

Упражнения:

1. Перенести ровно hand-solved formulation без добавления features.
2. Сверить solver с полным перебором на нескольких tiny instances.
3. Отдельной функцией перепроверить packs, supply, volume и receiving capacity.
4. Прогнать optimal, infeasible и time-limit cases.
5. Зафиксировать solver options и версию в run manifest.

Gate: изменение одной строки математической модели предсказуемо меняет feasible set, а
independent checker ловит намеренно испорченный plan.

## Module 5 — Decisions under uncertainty

Темы:

- expected-value solution;
- two-stage stochastic program;
- shared first-stage allocation;
- scenario-specific recourse;
- Sample Average Approximation;
- VSS и EVPI;
- scenario count и stability.

Упражнения:

1. Построить two-scenario instance, где mean-demand plan проигрывает.
2. Построить другой instance, где deterministic и stochastic plans совпадают.
3. Показать one-scenario parity.
4. Посчитать VSS и EVPI руками.
5. Объяснить, почему независимое sampling item/store residuals меняет задачу.
6. Построить curve `scenario count → objective stability / solve time`.

Gate: автор может объяснить не только что stochastic policy выиграла, но и какое ограничение
и какой хвост спроса изменили allocation.

## Module 6 — Closed-loop readiness gate

До главного rolling experiment автор должен уметь:

- выписать deterministic и scenario formulations без кода;
- решить и защитить tiny instance;
- объяснить inventory state transition;
- интерпретировать status, incumbent, bound и gap;
- построить independently feasible fallback;
- посчитать state-matched oracle regret;
- объяснить VSS, EVPI и их отличие от realised cost delta;
- показать adversarial leakage test;
- назвать единицу bootstrap и почему ей является week.

После gate открывается главный scarcity × uncertainty experiment.

## Чего нет в этом треке

Не “никогда”, а “не до главного результата”:

- CVaR и distributionally robust optimisation;
- Benders decomposition;
- multi-echelon inventory;
- routing;
- custom solver callbacks;
- decision-focused learning.

Не приходит никогда в этот проект:

- реализация собственного MILP solver;
- Gurobi только ради строки в стеке;
- перебор solver technologies без измеренного bottleneck.

## Teach-back questions

1. Чем parameter отличается от decision variable?
2. Почему shortage и ending inventory не должны быть положительными одновременно при
   положительных costs?
3. Что означает active constraint и чем slack отличается от dual value?
4. Почему LP relaxation даёт lower bound для cost-minimisation MILP?
5. Что можно утверждать о plan после time limit?
6. Почему oracle решается из state каждой policy отдельно?
7. Чем VSS отличается от EVPI?
8. Почему lower WAPE не гарантирует lower realised cost?
9. Когда safety-stock heuristic может сделать scenario MILP ненужным?
10. Почему residual scenarios строятся out-of-fold и joint?
