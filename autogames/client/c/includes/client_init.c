// http://www.koikikukan.com/archives/2017/10/31-000300.php

#include "client_init.h"

int client_init ( char* port ) {
  struct sockaddr_in addr;

  // create socket
  if( (sockfd = socket( AF_INET, SOCK_STREAM, 0) ) < 0 ) {
    perror( "socket" );
  }

  // set server's address and port
  addr.sin_family = AF_INET;
  addr.sin_port = htons( atoi(port) );
  addr.sin_addr.s_addr = inet_addr( "127.0.0.1" );

  // connect to server
  connect( sockfd, (struct sockaddr *)&addr, sizeof( struct sockaddr_in ) );

  return 0;
}
