#include "json_utils.h"

// See: https://qiita.com/koara-local/items/2d3220cd1e2fce8ff267
void read_message_json(int **field_data, char* string) {
  // create json from string
  struct json_object *json_obj = json_tokener_parse(string);
  // convert json data into int**
  json_object_object_foreach(json_obj, key, val) {
    if (json_object_is_type(val, json_type_array)) {
      if (strcmp(key, "field") == 0) {
        for (int i = 0; i < json_object_array_length(val); ++i) {
          struct json_object *arr = json_object_array_get_idx(val, i);
          for (int j = 0; j < json_object_array_length(arr); ++j) {
            struct json_object *element = json_object_array_get_idx(arr, j);
            field_data[i][j] = atoi(json_object_to_json_string(element));
          }
        }
      }
    }
  }
}

// https://linuxprograms.wordpress.com/2010/08/19/json_object_array_add/
void create_message_json(struct json_object *json_obj, int *next_move) {
  // create json array
  struct json_object *json_move = json_object_new_array();
  // create json integer
  struct json_object *j_x = json_object_new_int(next_move[0]);
  struct json_object *j_y = json_object_new_int(next_move[1]);
  // add json integers to array
  json_object_array_add(json_move, j_x);
  json_object_array_add(json_move, j_y);
  // add "move" key to the json
  json_object_object_add(json_obj, "move", json_move);
  // add "field" key to the json
  struct json_object *json_field = json_object_new_array();
  json_object_object_add(json_obj, "field", json_field);
}

void json_to_string(struct json_object *json_obj, char **json_str) {
  int buff_size = 1024;
  iconv_t ic;
  char    str_in[buff_size];
  char    str_out[buff_size];
  char    *ptr_in  = str_in;
  char    *ptr_out = str_out;
  size_t  mybufsz = (size_t) buff_size;

  strcpy(str_in, json_object_to_json_string(json_obj));
  ic = iconv_open("UTF-8", "SJIS");
  iconv(ic, &ptr_in, &mybufsz, &ptr_out, &mybufsz);
  iconv_close(ic);
  strcpy(*json_str, str_out);
}
