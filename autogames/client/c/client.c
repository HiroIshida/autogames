#include "includes/json_utils.h"
#include "includes/client_init.h"
#include "includes/agent.h"

int main(int argc, char* argv[]) {
  if ( argc != 2) {
    printf("1 argument is expected.\n");
    exit(EXIT_FAILURE);
  }

  client_init(argv[1]);

  // NOTE: very big board is not assumued (max size: 100*100 board)
  int i;
  int size_x = 100;
  int size_y = 100;
  int **field; // field state of the game
  field = malloc(sizeof(int *) * size_x);
  for (i=0;i<size_x;i++) {
    field[i] = malloc(sizeof(int) * size_y);
  }

  // socket communication
  int rsize;
  while( 1 ) {
    // receive field information from server
    rsize = recv( sockfd, buf, sizeof( buf ), 0 );
    if ( rsize == 0 ) {
      printf("[C Client] Finished.\n");
      break;
    }
    usleep( 10 * 1000 ); // wait for 10[ms]
    read_message_json(field, buf);
    // think next move (main algorithm)
    think(next_move);
    struct json_object *new_obj = json_object_new_object();
    create_message_json(new_obj, next_move);
    char *json_string = (char *)malloc(sizeof(char) * 1024);
    json_to_string(new_obj, &json_string);
    // send next move to server
    send( sockfd, json_string, rsize, 0);
  }

  // close socket
  close( sockfd );
  // release memory
  free(field);

  return 0;
}
