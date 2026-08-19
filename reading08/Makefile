# Compiler Settings

CC=	gcc
CFLAGS=	-Wall -g -std=gnu99
LIBS=

# Main Targets

test:
	@python3 ../.scripts/grade.py

program:    program.c
	@echo Building program...
	@$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

clean:
	@echo Cleaning up...
	@rm -f program test_program.sh

# Test Targets

test-quiz:	$(wildcard answers.json answers.yaml)
	@../.scripts/check.py

test-program: 	program
	@curl -sLO https://pnutz.h4x0r.space/courses/cse.30341.fa26/static/txt/reading08/test_program.sh
	@chmod +x test_program.sh
	@./test_program.sh
