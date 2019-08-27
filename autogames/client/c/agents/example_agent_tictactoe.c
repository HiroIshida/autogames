#include "../includes/agent.h"

void think(int *move) {
  move[0] = rand() % 3;
  move[1] = rand() % 3;
}
