struct json_object *message_json; // message in socket communication

void read_message_json(int **field_data, char* string);
void create_message_json(struct json_object *json_obj, int *next_move);
void json_to_string(struct json_object *json_obj, char **json_str);
