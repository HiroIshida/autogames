#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include "json_utils.h"

// int client_sockfd;
int sockfd;
char buf[1024];

int client_init ( char* port );
