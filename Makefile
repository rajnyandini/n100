load:
	python src/etl/loader.py

test:
	pytest tests/

report:
	python src/etl/validator.py

clean:
	del /q output\*.csv

dashboard:
	jupyter notebook

api:
	python main.py

ratios:
	python src/etl/calculate_ratios.py