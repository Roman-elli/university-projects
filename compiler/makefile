CC = gcc
CFLAGS = -Wall -Wextra -Wno-unused-function -g -I./include -I./build

SRC_DIR = src
BUILD_DIR = build
OBJ_DIR = obj

SRC = $(SRC_DIR)/utils/functions.c \
      $(SRC_DIR)/semantic/semantic.c \
      $(SRC_DIR)/codegen/codegen.c \
      $(SRC_DIR)/main.c

PARSER = $(BUILD_DIR)/parser.tab.c
LEXER  = $(BUILD_DIR)/lexer.yy.c
PARSER_HEADER = $(BUILD_DIR)/parser.tab.h

EXEC = go_compiler

OBJ = $(patsubst $(SRC_DIR)/%.c,$(OBJ_DIR)/%.o,$(SRC))

all: $(EXEC)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)
	mkdir -p $(OBJ_DIR)/utils
	mkdir -p $(OBJ_DIR)/semantic
	mkdir -p $(OBJ_DIR)/codegen

$(PARSER) $(PARSER_HEADER): $(SRC_DIR)/parser/parser.y | $(BUILD_DIR)
	bison -d -o $(PARSER) $(SRC_DIR)/parser/parser.y

$(LEXER): $(SRC_DIR)/lexer/lexer.l $(PARSER_HEADER) | $(BUILD_DIR)
	flex -o $(LEXER) $(SRC_DIR)/lexer/lexer.l

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c $(PARSER_HEADER) | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(EXEC): $(OBJ) $(PARSER) $(LEXER)
	$(CC) $(CFLAGS) $(OBJ) $(PARSER) $(LEXER) -o $(EXEC)

clean:
	rm -rf $(OBJ_DIR) $(BUILD_DIR) $(EXEC)

fclean: clean

re: fclean all

.PHONY: all clean fclean re
