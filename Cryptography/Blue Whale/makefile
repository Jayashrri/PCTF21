image = pctf21_bluewhale_lvl1:latest
container = bluewhale

.PHONY: build start stop

all: start

build:
	@chmod +x level_1/startup.sh
	@chmod +x level_1/level_2/startup.sh
	@chmod +x level_1/level_2/level_3/startup.sh
	@docker-compose --file level_1/docker-compose.yml build

start: $(if $(strip $(shell docker images -q $(image) 2>/dev/null)),,build)
	@chmod +x level_1/startup.sh
	@chmod +x level_1/level_2/startup.sh
	@chmod +x level_1/level_2/level_3/startup.sh
	@docker-compose --file level_1/docker-compose.yml up --detach

stop:
	@docker-compose --file level_1/docker-compose.yml down
	@-rm level_1/level_2/level_3/app/modules/algorithm.py
	@-rm level_1/level_2/level_3/algorithm.py
	@-rm level_1/level_2/app/modules/algorithm.py
	@-rm level_1/level_2/security/jail.bashrc
	@-rm level_1/level_2/security/.profile
	@chmod -x level_1/level_2/shell/main.py
	@chmod -x level_1/shell/main.py
	@chmod -x level_1/startup.sh
	@chmod -x level_1/level_2/startup.sh
	@chmod -x level_1/level_2/level_3/startup.sh

clean: $(if $(strip $(shell docker ps -aqf 'name=$(container)')),stop,)
	@docker image rm $(image)
