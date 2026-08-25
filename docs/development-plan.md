# План разработки

> **Статус · 25.08.2026: ARCHIVED / HARD PAUSE, 0 ч/нед.** Технический план сохранён; возврат
> возможен только отдельным карьерным решением, а не по старому календарю.

Финальная редакция, 2026-08-17. Один флагман под профиль **Production Optimization /
Decision Systems Engineer**: реальный временной ряд → прогноз и сценарии → решение с
ограничениями → closed-loop оценка → эксплуатационный контракт.

## Бюджет

Около 6 часов в неделю на проект в течение шести месяцев: **~150 часов до законченного
результата**. Отклики и подготовка к собеседованиям в эти часы не входят.

| Блок | Часов |
|---|---:|
| M5, временной протокол, fingerprint | ~18 |
| Симулятор, метрики, эвристики | ~22 |
| Детерминированный MILP и корректность | ~30 |
| Прогноз и совместные сценарии | ~25 |
| Стохастический MILP, fallback, batch contract | ~28 |
| Главный rolling-эксперимент и текст | ~27 |
| **Итого** | **~150** |

Два правила удерживают бюджет.

**Оптимизация несжимаема.** До самостоятельно выписанной модели, ручного решения маленького
инстанса и понимания статусов солвера — не меньше 40–50 часов внутри месяцев 3 и 5. Pyomo,
который “вернул число”, не считается математической моделью.

**Forecasting сжимается.** Временные признаки, LightGBM и offline evaluation уже близки к
текущему опыту автора. Здесь запрещена гонка за M5 leaderboard: прогноз нужен как честный
вход в решение, а не как второй флагман внутри первого.

## Центральный вопрос

> В каких режимах дефицита и неопределённости scenario-based MILP снижает out-of-sample
> операционные затраты достаточно, чтобы окупить дополнительное время решения относительно
> point-forecast MILP?

Механизм:

```text
слабые ограничения
→ почти весь полезный запас можно отправить
→ форма распределения спроса мало меняет allocation
→ deterministic policy достаточно

жёсткие ограничения + асимметричная цена shortage
→ решают последние case packs у границы
→ коррелированные хвосты спроса меняют ценность размещения
→ point forecast становится хрупким
```

Стандартный OR-язык для этого разрыва — **Value of the Stochastic Solution**. Но headline
проекта не “посчитала VSS один раз”. Нужна карта:

```text
scarcity × forecast uncertainty × cost asymmetry
→ realised cost delta × solve-time delta × fallback rate
```

**Чем это отличается от соседей.** M5 оценивает вероятностный прогноз до decision layer.
Scenario Predict-then-Optimize решает более богатую inventory-routing задачу и предлагает
метод генерации сценариев. JD.com показывает production allocation на закрытых данных и
масштабе. Здесь не заявляется новый метод. Портфельный вклад — публичный воспроизводимый
ответ на вопрос выбора сложности: где сценарный оптимизатор нужен, а где эвристика или
детерминированная модель дают тот же бизнес-результат дешевле.

Основные ориентиры:

- M5 uncertainty: `10.1016/j.ijforecast.2021.10.009`;
- Scenario Predict-then-Optimize: `10.1287/trsc.2024.0613`;
- JD.com inventory allocation: `10.1287/inte.2025.0245`;
- demand censoring как отдельная статистическая проблема: `10.1287/opre.2019.1883`.

## Датасет

**M5 Forecasting** — кандидат, фиксируется только после недели 0. В нём есть реальные
ежедневные продажи Walmart по товарам и магазинам, календарные события и недельные цены.
Планируемый срез: один department, около 50 товаров, 10 магазинов, weekly aggregation,
26 rolling test weeks.

Именно M5 подходит лучше H&M для этой задачи: повторяющиеся store × item решения, цены и
длинная временная ось. Но он не является inventory dataset в полном смысле.

**Честная граница данных:** наблюдаются продажи, а не uncensored demand. Не наблюдаются
исходные stockouts, центральный запас, store inventory, case packs, capacity, shipment,
holding и shortage costs. Операционный слой строится semi-synthetically только по правилам,
зафиксированным на train window. Исправлять цензурирование “интуитивно” нельзя: выводы
относятся к sales-as-demand benchmark и sensitivity grid, а не к восстановленному истинному
спросу.

Второго полноценного датасета до главного результата не будет.

---

# Неделя 0 — kill-test датасета

[Эксперимент 00](../experiments/00_dataset_viability/README.md), один вечер после загрузки
исходных CSV. Критерии фиксируются до просмотра агрегатов.

**A — временная опора, blocking.** После 104 недель initial history и 13 недель validation
остаются минимум 26 последовательных test weeks без календарных дыр.

**B — повторяющийся allocation, blocking.** По train-only правилу находится когорта минимум
из 50 товаров: каждый имеет продажи минимум в 60% train weeks на уровне сети и наблюдается
минимум в 8 из 10 магазинов на validation. Когорта после этого замораживается.

**C — полнота известных признаков, blocking.** Для выбранной когорты price и calendar
покрывают не меньше заранее установленной доли decision rows. Порог записывается в protocol
до расчёта; пропуски не заполняются будущими значениями.

**D — структура неопределённости, diagnostic.** Seasonal-naive rolling residuals измеряются
как целые week × item × store vectors: доля нулей, dispersion, cross-store correlation и
ошибка по demand buckets. Низкая зависимость не отклоняет данные — она предсказывает меньшую
ценность joint scenarios и остаётся возможным отрицательным результатом.

**E — режимы ограничений, blocking для постановки, не для данных.** Semi-synthetic supply и
capacity, рассчитанные только по train, должны дать различимые validation-режимы: tight часто
binding, medium смешанный, loose преимущественно slack. Если этого нет, правила
перепараметризуются один раз по train/validation и замораживаются до test.

Провал A–C означает: M5 отклоняется до реализации моделей. Провал E означает: отклоняется
операционная постановка, а не подбирается удачный test-результат.

---

# Месяцы 1–6

Каждый месяц добавляет слой, но предыдущая версия уже должна быть законченной работой.

## Месяц 1 — данные и временной протокол (~18 ч)

- immutable raw snapshot и SHA-256 fingerprint;
- daily → weekly panel без выбора товаров по будущему;
- initial train / rolling validation / rolling test;
- цены и календарные признаки по семантике их доступности в момент решения;
- adversarial leakage test: изменение будущих продаж не меняет прошлый input;
- маленькая hand-checkable fixture.

Результат месяца: одна таблица решения `as_of_week × item × store`, которую одинаково читают
forecast, simulator и optimizer.

## Месяц 2 — симулятор, метрики и эвристики (~22 ч)

- inventory balance: `on_hand + shipment = served + ending_inventory`;
- lost-sales assumption без скрытого backorder;
- proportional allocation и feasible greedy;
- realised shipment / holding / shortage cost, fill rate, lost units;
- каждая policy ведёт собственную inventory trajectory;
- oracle из того же pre-decision state только для regret;
- paired per-week records, ничего не усредняется раньше времени.

В конце месяца уже существует законченный baseline-проект: две простые политики проходят
один closed-loop backtest. Если дальнейший MILP не случится, эти числа всё равно честны.

## Месяц 3 — детерминированный MILP (~30 ч)

- переменная — количество case packs `k[item, store] ∈ Z+`;
- ограничения supply, store volume, receiving capacity;
- point demand, shortage и ending inventory в objective;
- Pyomo + HiGHS, фиксированные time limit и relative gap;
- `2 item × 2 store` решён вручную и полным перебором;
- независимый feasibility checker;
- монотонность оптимума при ослаблении ресурса;
- LP relaxation, integrality gap и active constraints как диагностика.

Никакого scenario model, пока детерминированная программа не защищается на бумаге.

## Месяц 4 — forecast и сценарии (~25 ч)

- seasonal naive;
- один global LightGBM с lag/rolling/price/calendar features;
- WAPE, RMSSE, bias по rolling validation;
- residuals только из rolling out-of-fold прогнозов;
- moving-block sampling целых residual vectors, не независимых ячеек;
- calibration: coverage, dispersion и dependence diagnostics;
- safety-stock baseline как дешёвая альтернатива полной stochastic model.

LightGBM тюнится один раз на validation. Лучший forecast не выбирается по decision cost на
test — иначе comparison уже подогнан.

## Месяц 5 — scenario MILP и эксплуатационный контур (~28 ч)

- shared first-stage allocation, scenario-specific shortage/inventory;
- one-scenario parity с deterministic model;
- Expected Value solution, VSS и perfect-information bound;
- scenario-count × solve-time curve;
- solver status, incumbent, gap, time limit и версия рядом с каждым plan;
- feasible greedy fallback с независимой повторной проверкой;
- один batch contract и run manifest;
- мониторинг input / forecast / solver / decision без dashboard.

Повторять прошлый plan как fallback нельзя: inventory state уже другой.

## Месяц 6 — главный эксперимент (~27 ч)

Сетка:

```text
scarcity ratio: 0.6 / 0.8 / 1.0 / 1.2
× shortage / holding cost ratio
× forecast uncertainty bucket
```

На каждой ячейке:

- realised cost и fill rate;
- scenario MILP minus strongest deterministic baseline;
- state-matched oracle regret;
- solve p50/p95, gap, timeout и fallback rate;
- доля binding supply/capacity constraints;
- paired moving-block bootstrap interval by week.

Финальный график — не leaderboard политик, а **карта режимов**. Она должна показать, где
стохастическая сложность покупает бизнес-эффект, где не покупает, и какой operational budget
за это уплачен.

---

# Приоритеты

- **Must** — week 0, temporal panel, simulator, strong heuristics, checked deterministic and
  scenario MILP, rolling map, uncertainty.
- **Should** — safety-stock baseline, LP diagnostics, batch manifest, fallback drill.
- **Could** — CVaR, explicit lead time, thin FastAPI adapter after the finding.

## Чего в проекте нет

- **Multi-echelon optimisation** — превращает один защищаемый вопрос в дипломную работу;
- **Routing** — соседняя NP-hard задача со своим набором решений и метрик;
- **Substitution model** — M5 не даёт данных, чтобы оценить её честно;
- **Deep forecasting** — не усиливает OR-сигнал до проверки простого LightGBM;
- **Decision-focused learning** — новый estimator не нужен, чтобы ответить на вопрос VSS;
- **Kubernetes и feature store** — batch-контракт, manifest и failure semantics достаточны;
- **Dashboard** — результат проекта это карта и отчёт, не интерфейс.

# Месяцы 7–9 — только после результата

1. CVaR против expected-cost policy на тех же rolling states.
2. Lead time и pipeline inventory, если one-period модель упирается именно в эту границу.
3. Тонкий API с parity test против batch service.

Ни одно расширение не начинает жить, пока таблица месяца 6 пуста.
