create_test_db_query = 'create database postgres_test'


run_dev:
	docker-compose up

init_db:
	docker exec -it time_backend flask init-db

drop_db:
	sudo rm -rf postgres_data/

psql:
	docker exec -it time_db psql -U postgres

test:
	pytest -s src

create_test_database:
	docker exec -it time_db psql -U postgres -c $(create_test_db_query)
