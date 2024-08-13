PROJECT_NAME := $(shell basename ${PWD})
PROJECT_HOME_DIR := $(shell echo "${PROJECT_NAME}/app")

LOCAL_EXEC := /bin/bash -c
$(info PROJECT_NAME: ${PROJECT_NAME})
$(info PROJECT_HOME_DIR: ${PROJECT_HOME_DIR})

start:
	@$(LOCAL_EXEC) "./bin/docker $@"

stop:
	@$(LOCAL_EXEC) "./bin/docker $@"

local:
	@$(LOCAL_EXEC) "./bin/docker $@"
