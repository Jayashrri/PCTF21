image = pctf21_bluewhale_lvl1:latest
container = bluewhale

.PHONY: build start stop

all: start

build:
	@chmod +x level_1/startup.sh
	@chmod +x level_1/level_2/startup.sh
	@chmod +x level_1/level_2/level_3/startup.sh
	@chmod +x level_1/level_2/level_3/jail/keys
	@docker-compose --file level_1/docker-compose.yml build

start: $(if $(strip $(shell docker images -q $(image) 2>/dev/null)),,build)
	@docker-compose --file level_1/docker-compose.yml up --detach

stop:
	@docker-compose --file level_1/docker-compose.yml down
	@chattr -R -i level_1/level_2/level_3/jail
	@chattr -i level_1/level_2/algorithm.py
	-@rm level_1/level_2/bashrc/jail.bashrc
	-@rm level_1/level_2/level_3/app/modules/algorithm.py
	-@rm level_1/level_2/level_3/jail/algorithm.py
	-@rm level_1/level_2/level_3/algorithm.py
	-@rm level_1/level_2/app/modules/algorithm.py
	@chmod -x level_1/startup.sh
	@chmod -x level_1/level_2/startup.sh
	@chmod -x level_1/level_2/level_3/startup.sh
	@chmod -x level_1/level_2/level_3/jail/keys

clean: $(if $(strip $(shell docker ps -aqf 'name=$(container)')),,stop)
	@docker image rm $(image) --force
