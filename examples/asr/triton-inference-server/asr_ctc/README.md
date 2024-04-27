
## Accuracy
|Dataset   | WER |
|----------|-----|
|dev-clean |     |
|dev-other |     |
|test-clean|2.05%|  # target 1.83%  to debug
|test-other|     |


## Performance

test-clean - 19452.28s

|concurrency | dtype | num instance| RTFx|duration|sorted|allow_ragged_batch|
|------------|-------|-------------|-----|--------|------|------------------|
|10          |float16| 1           |     | 77.86  | N    | T                |
|20          |float16| 1           |     | 50.16  | N    | T                |
|20          |float16| 1           |     | 26.58  | Y    | T                |
|30          |float16| 1           | 570 | 34.10  | N    | T                |
|40          |float16| 1           |     | 31.99  | N    | T                |
|50          |float16| 1           |     | 28.54  | N    | T                |
|50          |float16| 1           |     | 13.56  | Y    | T                |
|50          |float16| 1           |     | 144.87 | Y    | F                |
|60          |float16| 1           |     | 27.95  | N    | T                |
|70          |float16| 1           |     | 25.30  | N    | T                |
|80          |float16| 1           | 765 | 25.40  | N    | T                |
|80          |float16| 1           |     | 12.18  | Y    | T                |
|100         |float16| 1           |     | 12.14  | Y    | T                |
|10          |float16| 2           |     | 60.22  | N    | T                |
|50          |float16| 2           |     | 28.15  | N    | T                |
|100         |float16| 2           |     | 26.19  | N    | T                |
|20          |float16| 2           |     | 34.06  | Y    | T                |
|100         |float16| 2           |     | 13.61  | Y    | T                |
|150         |float16| 2           |     | 11.91  | Y    | T                |
|200         |float16| 2           | 1661| 11.71  | Y    | T                |