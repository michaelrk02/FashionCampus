.PHONY : reload
reload:
	docker-compose rm -sf fashion-campus-api
	docker-compose build fashion-campus-api
	docker-compose up -d fashion-campus-api

.PHONY : reload-app
reload-app:
	docker-compose rm -sf fashion-campus-app
	docker-compose build fashion-campus-app
	docker-compose up -d fashion-campus-app

.PHONY : seed
seed:
	docker-compose exec fashion-campus-api python -m FashionCampus.database.seeder

.PHONY : logs
logs:
	docker-compose logs fashion-campus-api

.PHONY : test
test:
	docker-compose exec fashion-campus-api python -m FashionCampus.nn.test
