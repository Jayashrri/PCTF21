image = pctf21_bluewhale_lvl1:latest
target = $(shell docker images -q $(image) 2>/dev/null)
target := $(if $(strip $(target)),,build)

.PHONY: build start stop

all: start

build:
	@chmod +x level_1/startup.sh
	@chmod +x level_1/level_2/startup.sh
	@chmod +x level_1/level_2/level_3/startup.sh
	@chmod +x level_1/level_2/level_3/jail/keys
	@docker-compose --file level_1/docker-compose.yml build

start: $(target)
	@docker-compose --file level_1/docker-compose.yml up --detach 

stop:
	@docker-compose --file level_1/docker-compose.yml down
	@chattr -R -i level_1/level_2/level_3/jail
	@rm level_1/level_2/bashrc/jail.bashrc
	@rm level_1/level_2/level_3/app/modules/algorithm.py
	@rm level_1/level_2/level_3/jail/algorithm.py
	@rm level_1/level_2/level_3/algorithm.py
	@rm level_1/level_2/app/modules/algorithm.py
	@chmod -x level_1/startup.sh
	@chmod -x level_1/level_2/startup.sh
	@chmod -x level_1/level_2/level_3/startup.sh
	@chmod -x level_1/level_2/level_3/jail/keys

clean: stop
	@docker image rm $(image) --force
