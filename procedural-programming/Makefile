CC = gcc
CFLAGS = -Wall -g -Iinclude
TARGET = manuWash

SRC = src/main.c src/core/queue.c src/core/reservations.c src/core/time.c src/ui/menu.c src/utils/file.c src/utils/io.c
OBJ = $(patsubst src/%, build/%, $(SRC:.c=.o))

.PHONY: all run clean

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $(TARGET)

build/%.o: src/%.c
	@mkdir -p $(dir $@)   # cria diretório se não existir
	$(CC) $(CFLAGS) -c $< -o $@

run: $(TARGET)
	./$(TARGET)

clean:
	rm -rf build $(TARGET)
