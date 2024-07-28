# Build the docker images
build:
	docker-compose -f docker-compose.yml build

# Start the development environment
dev:
	docker-compose -f docker-compose.yml up

# Start the production environment
prod:
	docker-compose -f docker-compose.yml -f deploy/docker-compose.prod.yml up -d

# Run the test suite
test:
	docker-compose -f docker-compose.test.yml up --exit-code-from web

# shell
shell:
	docker-compose exec -it web /bin/bash

# Run the linters and static analysis tools
lint:
	docker-compose -f docker-compose.yml run --rm web flake8 .
	docker-compose -f docker-compose.yml run --rm web black --check .

# Format the code
format:
	docker-compose -f docker-compose.yml run --rm web black .

# Install dependencies
install:
	pip install --upgrade pip
	pip install -r dependencies/requirements.txt
	pip install -r dependencies/requirements-dev.txt
	pip install -r dependencies/requirements-test.txt

# Remove all the docker containers and volumes
clean:
	docker-compose -f docker-compose.yml down -v
	docker-compose -f docker-compose.test.yml down -v
	docker-compose -f docker-compose.prod.yml down -v
