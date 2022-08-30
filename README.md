# System Of Predictions On Real Estate

* Created a model for predict the price of real estates
* The data was scraped using scrapy on [imobiliariaativa](https://www.imobiliariaativa.com.br) website and saved using postgresql.
* A EDA was made using jupyter notebook for features selection.
* The mlflow was use for Linear Regression model witch reach a R2 of **0.86** and RMSE of **188252.95**.

## Requirements
```
seaborn==0.11.2
matplotlib==3.5.2
scikit-learn==1.1.1      
scipy==1.8.1
pandas==1.4.3
numpy==1.23.1
jupyterlab==3.4.4
mlflow==1.27.0
Scrapy==2.6.1
psycopg2-binary==2.9.3
```

## Running Files

  The files [ativa.py](https://github.com/RichardMan13/system_of_predictions_on_real_estate/blob/main/scrapy_real_estate/real_estate/spiders/ativa.py/) and [train.py](https://github.com/RichardMan13/system_of_predictions_on_real_estate/blob/main/mlflow/train.py/) are responsible to scrap and make the predictions respectively.

First run the file [ativa.py](https://github.com/RichardMan13/system_of_predictions_on_real_estate/blob/main/scrapy_real_estate/real_estate/spiders/ativa.py/) with the command line: 
`scrapy crawl ativa` 

Then run the file [train.py](https://github.com/RichardMan13/system_of_predictions_on_real_estate/blob/main/mlflow/train.py/) with the command line:
`python train.py`


