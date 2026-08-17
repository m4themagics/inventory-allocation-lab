# Data workspace

Данные в git не коммитятся — здесь будут жить только ingestion code, schema contracts и
fingerprints.

```text
data/
  raw/          # неизменяемый снимок исходных M5 CSV
  interim/      # daily long table и проверенные справочники
  processed/    # weekly point-in-time panel для решений
  fixtures/     # крошечные hand-checkable данные, их коммитить можно
```

## Датасет

[M5 Forecasting dataset](https://doi.org/10.5281/zenodo.10203108) — реальные ежедневные
unit sales Walmart по товарам и магазинам, календарные события и недельные sell prices.
Полный набор содержит иерархию item / department / category / store / state и почти пять с
половиной лет истории.

Планируемый первый срез: один department, около 50 товаров, все 10 магазинов, weekly
aggregation, 104 недели initial history, 13 validation weeks и 26 rolling test weeks. Cohort
выбирается только по initial train window и после этого не меняется.

## Заполнить до первой загрузки

```text
Источник и лицензия:
Ревизия / checksum исходных файлов:
Department и train-only правило выбора items:
Семантика as_of_week:
Какие calendar/price поля известны в момент решения:
Правило daily → weekly aggregation:
Train / validation / test cutoffs:
Правила semi-synthetic supply, inventory, packs, capacity и costs:
Ожидаемые риски утечки:
Метод fingerprint:
```

Пока эти поля не заполнены, M5 остаётся кандидатом, а не выбранным доказательством.

## Про честность спроса

M5 публикует **sales, не latent demand**. Нулевая продажа может означать нулевой спрос, а
может — stockout; исходной availability и потерянного спроса нет. Substitution между товарами
тоже не наблюдается.

Поэтому проект не “исправляет” продажи до вымышленного истинного спроса. Реализованный
benchmark прямо называется `sales-as-demand`. Central supply, on-hand inventory, case packs,
capacity и costs моделируются отдельно, детерминированно и только по train/validation. Все
выводы ограничены этой semi-synthetic постановкой и получают sensitivity analysis.

Работа о demand censoring показывает, что интуитивная предварительная коррекция censored
sales может давать несостоятельные оценки; это ещё одна причина не маскировать границу данных:
[Ban, 2020](https://doi.org/10.1287/opre.2019.1883).
