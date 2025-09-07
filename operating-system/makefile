FLAGS = -g -pthread -lrt -Wall
OBJS = src/functions.c
SYSTEM_MANEGER = src/system_manager.c
MOBILE_USER = src/mobile_user.c
BACKOFFICE_USER = src/backoffice_user.c
TARGET = 5g_auth_platform
TARGET2 = mobile_user
TARGET3 = backoffice_user

all: $(TARGET) $(TARGET2) $(TARGET3)

$(TARGET): $(SYSTEM_MANEGER) $(OBJS)
				$(CC) $(FLAGS) $(SYSTEM_MANEGER) $(OBJS) -o $(TARGET)

$(TARGET2): $(MOBILE_USER) $(OBJS)
				$(CC) $(FLAGS) $(MOBILE_USER) -o $(TARGET2)

$(TARGET3): $(BACKOFFICE_USER) $(OBJS)
				$(CC) $(FLAGS) $(BACKOFFICE_USER) -o $(TARGET3)

clean:
				rm -f $(TARGET) $(TARGET2) $(TARGET3)
