run_dev:
	flask --app src/app.py run --debug --host=0.0.0.0 --port=8000

init_db:
	flask --app src/app.py init-db

drop_db:
	sudo rm -rf postgres_data/

psql:
	docker exec -it time_db psql -U postgres