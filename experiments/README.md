# Experiments

Один каталог — один исследовательский вопрос, а не одна policy. Модель без вопроса живёт в
`src/ial/`, а сюда попадает только то, что что-то проверяет.

```text
experiments/<nn>_<slug>/
  README.md          вопрос, гипотеза, механизм, критерий успеха
  protocol.md        заполненный research protocol — до прогона
  run.py             или Makefile-цель; ровно одна команда запуска
  results/           числа, графики, per-week outcomes, run manifest
```

Запланированные вопросы по фазам:

| # | Вопрос | Фаза |
|---|---|---|
| 00 | Достаточно ли в M5 повторяющегося item × store спроса для честных rolling allocation decisions? | 0 |
| 01 | Где proportional и greedy теряют cost относительно perfect-information bound? | 2 |
| 02 | Совпадает ли детерминированный MILP с brute force и как растёт solve time? | 3 |
| 03 | Что LightGBM даёт сверх seasonal naive и калиброваны ли residual scenarios? | 4 |
| 04 | Как число scenarios меняет VSS, gap и solve latency? | 5 |
| 05 | В каких scarcity × uncertainty regimes scenario MILP бьёт deterministic policy? | 6 |
| 06 | Забирает ли safety-stock baseline тот же эффект дешевле? | 6 |

Нумерация закрепляется в момент старта эксперимента, а не заранее: список выше — намерение.
Он меняется, если предыдущий результат делает следующий вопрос бессмысленным.
