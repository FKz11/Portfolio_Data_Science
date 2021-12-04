Стек:

ML: sklearn, pandas, numpy, catboost, shap, xgboost  
API: flask
Данные: с kaggle - https://www.kaggle.com/adityadesai13/used-car-dataset-ford-and-mercedes

Задача: предсказать стоимость автомобилей марки Audi. Задача регрессии.

Используемые признаки:

- year (int)
- transmission (string)
- mileage (float)
- mpg (float)
- engineSize (float)

Преобразования признаков: 

- Сочитания признаков (*, +, -, /)
- Target Encoding
- Feature Selection (Auto) - самое интересное

Модель: XGBRegressor

Всё обёрнуто в Pipeline([preprocessing, model])

### Клонируем репозиторий и создаем образ
```
$ git clone https://github.com/fkz11/Portfolio_Data_Science.git
$ cd Portfolio_Data_Science/Audi_Car_Price_Prediction/api
$ docker build -t fkz11/api .
```

### Запускаем контейнер

Здесь Вам нужно создать каталог локально и сохранить туда предобученную модель (<your_local_path_to_pretrained_models> нужно заменить на полный путь к этому каталогу)
```
$ docker run -d -p 8180:8180 -p 8181:8181 -v <your_local_path_to_pretrained_models>:/app/app/models fkz11/api
```

### Переходим на http://0.0.0.0:8181/

### !!! Если ОС Windows, то после git clone нужно поменять окончания строк в файле docker-entrypoint.sh на Unix. Например через утилиту Sublime Text: view -> Line Endings -> Unix. Переходить нужно на http://localhost:8181/ !!!
