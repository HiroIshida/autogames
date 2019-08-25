// Compile
// gcc -Wall -g -O2 -o agent-c agent.c -L /usr/lib/i386-linux-gnu -ljson-c; ./agent-c;
// Execution

#include "json_utils.h"
#include "client_init.h"
#include "agent.h"

int main(int argc, char* argv[]) {
  if ( argc != 2) {
    printf("1 argument is expected.\n");
    exit(EXIT_FAILURE);
  }

  client_init(argv[1]);

  // MEMO: do not forget to free(field)
  int i;
  int size_x = 3;
  int size_y = 3;
  // TODO: size_x and size_y should be set dynamically
  field = malloc(sizeof(int *) * size_x);
  for (i=0;i<size_x;i++) {
    field[i] = malloc(sizeof(int) * size_y);
  }

  // socket communication
  int rsize;
  while( 1 ) {
    // receive
    rsize = recv( sockfd, buf, sizeof( buf ), 0 );
    if ( rsize == 0 ) {
      printf("[C Client] Finished.\n");
      return 0;
    }
    usleep( 10 * 1000 ); // wait for 10[ms]
    read_message_json(field, buf);
    // response
    think(next_move);
    struct json_object *new_obj = json_object_new_object();
    create_message_json(new_obj, next_move);
    /* json_string = json_object_to_json_string(new_obj); */
    char *json_string = (char *)malloc(sizeof(char) * 1024);
    json_to_string(new_obj, &json_string);
    /* json_string = json_object_to_json_string(new_obj); */
    send( sockfd, json_string, rsize, 0);
  }

  // close socket
  close( sockfd );

  return 0;
}
