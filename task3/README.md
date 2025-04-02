## Task3: Askona parser

Программа для парсинга интеренет магазина Askona. Парсит указанную страницу и сохраняет результаты в csv файл.

## Зависимости

Программа использует библиотеку `selenium`.  
````
pip install selenium
````

## Использование

```python <link> --count=<count> --output=<output.csv>```
- link — ссылка на страницу с товарами
- count — количество товаров, которое мы хотим сохранить (по умолчанию 5)
- output.csv — файл c результатом работы программы (по умолчанию askona_products.csv)

## Пример использования

````
python main.py https://www.askona.ru/podushki/? --count=5 --output=res.scv
````

## output.csv

На выходе получается один CSV файл, который содержит поля `["Name", "Type", "Price", "Rating", "Reviews", "Link"]`
Пример:  

| Name                       | Type                  | Price | Rating    | Reviews | Link                                                                                                                       |
| -------------------------- | --------------------- | ----- | --------- | ------- | -------------------------------------------------------------------------------------------------------------------------- |
| Alpha Technology 2.0       | Анатомическая подушка | 6290  | 4.9       | 59      | https://www.askona.ru/podushki/alpha-technology-2.htm?SELECTED_HASH_SIZE=14-949c364bc5a9c58b3890a731dfb1688d               |
| Immuno Technology 2.0      | Анатомическая подушка | 7390  | 5         | 53      | https://www.askona.ru/podushki/immuno-technology-2-0.htm?SELECTED_HASH_SIZE=9-50cc4e3b66ea5c4084650af82e8ee63f             |
| Amma                       | Анатомическая подушка | 3190  | 5         | 12      | https://www.askona.ru/podushki/podushka-amma.htm?SELECTED_HASH_SIZE=60x40-992ec5c1c1b553c7a5d1e195eb53693f                 |
| Balance Basic              | Набивная подушка      | 2190  | 4.9       | 179     | https://www.askona.ru/podushki/balance-basic.htm?SELECTED_HASH_SIZE=70x50-a4b2635c44dc0d09c7b8a26c3bbfaca2                 |
| Omega серия Technology 2.0 |Анатомическая подушка  | 11990 | No rating | 0       | https://www.askona.ru/podushki/podushka-omega-technology-2-0.htm?SELECTED_HASH_SIZE=64x42-b938183c75de78232af997ab9ab77ec0 |
