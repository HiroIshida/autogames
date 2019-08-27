// if you cannot find json-c,
// sudo apt install libjson-c-dev
#include <stdio.h>
#include <iconv.h>
#include <json-c/json.h>

void read_message_json(int **field_data, char* string);
void create_message_json(struct json_object *json_obj, int *next_move);
void json_to_string(struct json_object *json_obj, char **json_str);
