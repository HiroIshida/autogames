AGENT_FILE = agent.c # main agent program
AGENT_DIR = agents/ # main agent program is in this directory
INCLUDE_DIR = includes/ # include files are in this directory
LDFLAGS = -L/usr/lib/i386-linux-gnu # dynamic library
LSFLAGS = -ljson-c # static library
CFLAGS = -Wall -g -O2 # gcc options

client_c: client.c $(AGENT_DIR:=${AGENT_FLIE}) $(INCLUDE_DIR:=client_init.h) $(INCLUDE_DIR:=client_init.c) $(INCLUDE_DIR:=json_utils.h) $(INCLUDE_DIR:=json_utils.c)
	gcc -o client_c client.c $(AGENT_DIR:=${AGENT_FILE}) $(INCLUDE_DIR:=client_init.c) $(INCLUDE_DIR:=json_utils.c) $(LDFLAGS) $(LSFLAGS) $(CFLAGS)
