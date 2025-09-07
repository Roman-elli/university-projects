CC = gcc
FLAGS = -g -pthread -lrt -Wall -Iinclude

OBJ_DIR = obj
DATA_DIR = data
OBJS = $(OBJ_DIR)/functions.o
SYSTEM_MANAGER = src/system_manager.c
MOBILE_USER = src/mobile_user.c
BACKOFFICE_USER = src/backoffice_user.c
CONFIG_5G_FILE = config/config5g.txt
CONFIG_MOBILE_FILE = config/configMobile.txt

BIN_DIR = bin
TARGET = $(BIN_DIR)/5g_auth_platform
TARGET2 = $(BIN_DIR)/mobile_user
TARGET3 = $(BIN_DIR)/backoffice_user

all: $(BIN_DIR) $(OBJ_DIR) $(TARGET) $(TARGET2) $(TARGET3)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

$(OBJ_DIR)/functions.o: src/functions.c | $(OBJ_DIR)
	$(CC) $(FLAGS) -c src/functions.c -o $(OBJ_DIR)/functions.o

$(TARGET): $(SYSTEM_MANAGER) $(OBJS)
	$(CC) $(FLAGS) $(SYSTEM_MANAGER) $(OBJS) -o $(TARGET)

$(TARGET2): $(MOBILE_USER) $(OBJS)
	$(CC) $(FLAGS) $(MOBILE_USER) $(OBJS) -o $(TARGET2)

$(TARGET3): $(BACKOFFICE_USER) $(OBJS)
	$(CC) $(FLAGS) $(BACKOFFICE_USER) $(OBJS) -o $(TARGET3)

clean:
	rm -rf $(BIN_DIR) $(OBJ_DIR) $(DATA_DIR)

run_5g:
	./$(TARGET) $(CONFIG_5G_FILE)

run_mobile:
	./$(TARGET2) $(CONFIG_MOBILE_FILE)

run_back:
	./$(TARGET3)
