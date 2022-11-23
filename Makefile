.PHONY : reload
reload:
	docker-compose rm -sf fashion-campus-api
	docker-compose build fashion-campus-api
	docker-compose up -d fashion-campus-api

.PHONY : seed
seed:
	docker-compose exec fashion-campus-api python -m FashionCampus.database.seeder

.PHONY : logs
logs:
	docker-compose logs fashion-campus-api
