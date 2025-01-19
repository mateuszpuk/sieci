#include<sqlite3.h>
#include<stdio.h>
#include<stdlib.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<string.h>
#include <arpa/inet.h>
#include <fcntl.h> // for open
#include <unistd.h> // for close
#include<pthread.h>
#include <cjson/cJSON.h>

//do dodawania znaj
int are_friends(const char* name_db, const char* username1, const char* username2) {
    sqlite3 *db;
    sqlite3_stmt *stmt;
    int o = sqlite3_open(name_db, &db);

    if(o != SQLITE_OK) {
        printf("Błąd połączenia z bazą danych: %s\n", sqlite3_errmsg(db));
        return 0;
    }
    if (strcmp(username1, username2) == 0) {
    printf("Nie możesz dodać siebie jako znajomego\n");
    return 2; 
}

    char *sql = "SELECT * FROM FRIENDS WHERE (username1 = ? AND username2 = ?)";
    o = sqlite3_prepare_v2(db, sql, -1, &stmt, 0);
    if(o != SQLITE_OK) {
        printf("Błąd przygotowania zapytania: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 0;
    }

    sqlite3_bind_text(stmt, 1, username1, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, username2, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, username2, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 4, username1, -1, SQLITE_STATIC);

    o = sqlite3_step(stmt);
    if(o == SQLITE_ROW) {
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 1;  // Są już znajomymi
    } else {
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 0;  // Nie są jeszcze znajomymi
    }
}
//do dodawania user do tabeli
int add_user(const char* name_db,const char* username,const char* password){
    sqlite3 *db;
    sqlite3_stmt *stmt;
    int o = sqlite3_open(name_db, &db);
    
    if(o != SQLITE_OK) {
        printf("Błąd połączenia z bazą danych: %s\n", sqlite3_errmsg(db));
        return 0;
    }

    char *sql = "INSERT INTO USERS (username,password) VALUES(?, ?)";
    o = sqlite3_prepare_v2(db, sql, -1, &stmt, 0);
    if(o != SQLITE_OK) {
        printf("Błąd przygotowania zapytania: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 0;
    }

    sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, password, -1, SQLITE_STATIC);
    o = sqlite3_step(stmt);
    
    if(o == SQLITE_DONE) {
        printf("Dodano użytkownika: %s\n", username);
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 1;  
    } else {
        printf("Nie dodano użytkownika: %s\n", username);
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 0; 
    }
}
//do sprawdzania czy jest juz uzytkownik o takiej nazwie
int check_username(const char* name_db,const char* username){
    sqlite3 *db;
    sqlite3_stmt *stmt;
    int o = sqlite3_open(name_db, &db);
    
    if(o != SQLITE_OK) {
        printf("Błąd połączenia z bazą danych: %s\n", sqlite3_errmsg(db));
        return 0;
    }

    char *sql = "SELECT * FROM USERS WHERE username = ?";
    o = sqlite3_prepare_v2(db, sql, -1, &stmt, 0);
    if(o != SQLITE_OK) {
        printf("Błąd przygotowania zapytania: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 0;
    }

    sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);

    o = sqlite3_step(stmt);
    
    if(o == SQLITE_ROW) {
        printf("Znaleziono użytkownika: %s\n", username);
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 1;  
    } else {
        printf("Nie znaleziono użytkownika: %s\n", username);
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 0; 
    }
}
//sprawdzenie czy na podane dane sa w tabeli user
int check_user(const char* name_db,const char* username,const char* pwd){
    sqlite3 *db;
    sqlite3_stmt *stmt;
    int o = sqlite3_open(name_db, &db);
    
    if(o != SQLITE_OK) {
        printf("Błąd połączenia z bazą danych: %s\n", sqlite3_errmsg(db));
        return 0;
    }

    char *sql = "SELECT * FROM USERS WHERE username = ? AND password = ?";
    o = sqlite3_prepare_v2(db, sql, -1, &stmt, 0);
    if(o != SQLITE_OK) {
        printf("Błąd przygotowania zapytania: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 0;
    }

    sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, pwd, -1, SQLITE_STATIC);

    o = sqlite3_step(stmt);
    
    if(o == SQLITE_ROW) {
        printf("Znaleziono użytkownika: %s\n", username);
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 1;  
    } else {
        printf("Nie znaleziono użytkownika: %s\n", username);
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 0; 
    }
}
//do wysylania listy zanjomych 
char* check_friend(const char* name_db,const char* username1){
    sqlite3 *db;
    sqlite3_stmt *stmt;
    int o = sqlite3_open(name_db, &db);
    
    if(o != SQLITE_OK) {
        printf("Błąd połączenia z bazą danych: %s\n", sqlite3_errmsg(db));
        return 0;
    }

    char *sql = "SELECT username2 FROM FRIENDS WHERE username1 = ?";
    o = sqlite3_prepare_v2(db, sql, -1, &stmt, 0);
    if(o != SQLITE_OK) {
        printf("Błąd przygotowania zapytania: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 0;
    }

     sqlite3_bind_text(stmt, 1, username1, -1, SQLITE_STATIC);

    // Tworzenie obiektu JSON
    cJSON *friends_array = cJSON_CreateArray();

    while(sqlite3_step(stmt) == SQLITE_ROW) {
        const char* username2 = (const char*)sqlite3_column_text(stmt, 0);

        // Dodajemy znajomego do tablicy JSON
        cJSON_AddItemToArray(friends_array, cJSON_CreateString(username2));
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db);

    cJSON *response = cJSON_CreateObject();
    cJSON_AddItemToObject(response, "friends", friends_array);

    // Przekształcenie obiektu JSON na łańcuch znaków
    char *json_string = cJSON_Print(response);
    cJSON_Delete(response); 

    return json_string; 
}
 // do dodawania znajomosci
int add_friend(const char* name_db,const char* username1,const char* username2){
    sqlite3 *db;
    sqlite3_stmt *stmt;
    int o = sqlite3_open(name_db, &db);
    
    if(o != SQLITE_OK) {
        printf("Błąd połączenia z bazą danych: %s\n", sqlite3_errmsg(db));
        return 0;
    }
    
    char *sql = "INSERT INTO FRIENDS (username1, username2) VALUES(?, ?)";
    o = sqlite3_prepare_v2(db, sql, -1, &stmt, 0);
    if(o != SQLITE_OK) {
        printf("Błąd przygotowania zapytania: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 0;
    }

    sqlite3_bind_text(stmt, 1, username1, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, username2, -1, SQLITE_STATIC);

    o = sqlite3_step(stmt);
    if(o == SQLITE_DONE) {
        printf("Dodano znajomość: %s, %s\n", username1, username2);
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 1; 
    } else {
        printf("Błąd dodawania znajomości: %s\n", sqlite3_errmsg(db));
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 0;
    }
}

int add_message(const char* db_name, const char* sender, const char* receiver, const char* message) {
    sqlite3 *db;
    sqlite3_stmt *stmt;
    int o = sqlite3_open(db_name, &db);
    
    if (o != SQLITE_OK) {
        printf("Błąd połączenia z bazą danych: %s\n", sqlite3_errmsg(db));
        return 0;
    }

    const char *sql = "INSERT INTO MESSAGES (sender, receiver, message) VALUES (?, ?, ?)";
    o = sqlite3_prepare_v2(db, sql, -1, &stmt, 0);
    
    if (o != SQLITE_OK) {
        printf("Błąd przygotowania zapytania: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 0;
    }

    sqlite3_bind_text(stmt, 1, sender, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, receiver, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, message, -1, SQLITE_STATIC);
    
    o = sqlite3_step(stmt);
    if (o == SQLITE_DONE) {
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 1;
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db);
    return 0;
}

int create_group(const char* db_name, const char* group_name) {
    sqlite3 *db;
    sqlite3_stmt *stmt;
    int o = sqlite3_open(db_name, &db);

    if (o != SQLITE_OK) {
        printf("Błąd połączenia z bazą danych: %s\n", sqlite3_errmsg(db));
        return 0;
    }

    const char *sql = "INSERT INTO GROUPS (group_name) VALUES (?)";
    o = sqlite3_prepare_v2(db, sql, -1, &stmt, 0);
    
    if (o != SQLITE_OK) {
        printf("Błąd przygotowania zapytania: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 0;
    }

    sqlite3_bind_text(stmt, 1, group_name, -1, SQLITE_STATIC);
    
    o = sqlite3_step(stmt);
    if (o == SQLITE_DONE) {
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 1;
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db);
    return 0;
}

int add_member_to_group(const char* db_name, const char* group_name, const char* username) {
    sqlite3 *db;
    sqlite3_stmt *stmt;
    int o = sqlite3_open(db_name, &db);

    if (o != SQLITE_OK) {
        printf("Błąd połączenia z bazą danych: %s\n", sqlite3_errmsg(db));
        return 0;
    }

    // Znalezienie ID grupy po nazwie
    const char *group_sql = "SELECT id FROM GROUPS WHERE group_name = ?";
    o = sqlite3_prepare_v2(db, group_sql, -1, &stmt, 0);

    if (o != SQLITE_OK) {
        printf("Błąd przygotowania zapytania: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 0;
    }

    sqlite3_bind_text(stmt, 1, group_name, -1, SQLITE_STATIC);
    
    int group_id = -1;
    o = sqlite3_step(stmt);
    if (o == SQLITE_ROW) {
        group_id = sqlite3_column_int(stmt, 0);
    }
    
    sqlite3_finalize(stmt);

    if (group_id == -1) {
        printf("Nie znaleziono grupy o nazwie: %s\n", group_name);
        sqlite3_close(db);
        return 0;
    }

    // Dodanie użytkownika do grupy
    const char *insert_sql = "INSERT INTO GROUP_MEMBERS (group_id, username) VALUES (?, ?)";
    o = sqlite3_prepare_v2(db, insert_sql, -1, &stmt, 0);
    
    if (o != SQLITE_OK) {
        printf("Błąd przygotowania zapytania: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 0;
    }

    sqlite3_bind_int(stmt, 1, group_id);
    sqlite3_bind_text(stmt, 2, username, -1, SQLITE_STATIC);

    o = sqlite3_step(stmt);
    if (o == SQLITE_DONE) {
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 1;
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db);
    return 0;
}

int send_group_message(const char* db_name, const char* group_name, const char* sender, const char* message) {
    sqlite3 *db;
    sqlite3_stmt *stmt;
    int o = sqlite3_open(db_name, &db);

    if (o != SQLITE_OK) {
        printf("Błąd połączenia z bazą danych: %s\n", sqlite3_errmsg(db));
        return 0;
    }

    // Znalezienie ID grupy po nazwie
    const char *group_sql = "SELECT id FROM GROUPS WHERE group_name = ?";
    o = sqlite3_prepare_v2(db, group_sql, -1, &stmt, 0);

    if (o != SQLITE_OK) {
        printf("Błąd przygotowania zapytania: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 0;
    }

    sqlite3_bind_text(stmt, 1, group_name, -1, SQLITE_STATIC);
    
    int group_id = -1;
    o = sqlite3_step(stmt);
    if (o == SQLITE_ROW) {
        group_id = sqlite3_column_int(stmt, 0);
    }
    
    sqlite3_finalize(stmt);

    if (group_id == -1) {
        printf("Nie znaleziono grupy o nazwie: %s\n", group_name);
        sqlite3_close(db);
        return 0;
    }

    // Wysłanie wiadomości do grupy
    const char *insert_sql = "INSERT INTO GROUP_MESSAGES (group_id, sender, message) VALUES (?, ?, ?)";
    o = sqlite3_prepare_v2(db, insert_sql, -1, &stmt, 0);
    
    if (o != SQLITE_OK) {
        printf("Błąd przygotowania zapytania: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 0;
    }

    sqlite3_bind_int(stmt, 1, group_id);
    sqlite3_bind_text(stmt, 2, sender, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, message, -1, SQLITE_STATIC);

    o = sqlite3_step(stmt);
    if (o == SQLITE_DONE) {
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 1;
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db);
    return 0;
}


char client_message[2000];
char buffer[1024];

char ok[4]="ok\n";
char nie[5]="nie\n";
char dodano[7]="dodano\n";
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void * socketThread(void *arg)
{
  printf("new thread \n");
  int newSocket = *((int *)arg);
  int n;
  char username[30];
char password[30];
char username1[30];
bzero(username,30);
bzero(username1,30);
bzero(password,30);
  for(;;){
    n=recv(newSocket , client_message , 2000 , 0);
    printf("%s\n",client_message);
        if(n<1){
            break;
        }
        if (sscanf(client_message, "LOG;%30[^;];%30s", username, password) == 2) {// pobranie username i pwd 
            printf("%s\n", username);
            printf("%s\n", password);
            //czyszczenie
            char *message = malloc(sizeof(client_message));
            strcpy(message,client_message);
            sleep(1);
            memset(&client_message, 0, sizeof (client_message));

            int result = check_user("database.db", username, password);//sprawdzanie czy jest w bazi danych
            if (result == 1) {
                printf("zalogowałes sie\n");
                send(newSocket,ok,sizeof(ok),0);
                sleep(1);//uspienie by sie znajomi nie wysylali z wiadomoscia wyzej

                char* friends_json = check_friend("database.db", username);
    
                if (friends_json != NULL) {//sprawdzenie czy ma znajomych
                    // Wysyłanie listy znajomych w formacie JSON do klienta
                    send(newSocket, friends_json, strlen(friends_json), 0);
                    printf("Wysłano listę znajomych w formacie JSON: %s\n", friends_json);

                    // Zwolnienie pamięci po użyciu JSON
                    free(friends_json);
                }
            }
            else{
                send(newSocket,nie,sizeof(nie),0);
                
            }}
        else if (sscanf(client_message, "NEWF;%30[^;];%30s", username, username1) == 2) {//pobranie usernames
            printf("%s\n", username);
            printf("%s\n", username1);

            char *message = malloc(sizeof(client_message));
            strcpy(message,client_message);
            sleep(1);
            memset(&client_message, 0, sizeof (client_message));

            if (are_friends("database.db", username, username1)==1) {//sprawdzenie czy sa znajomymi
                send(newSocket, "Już jesteście znajomymi\n", 25, 0);
                printf("Wysłano wiadomość: Już jesteście znajomymi\n");
            } else if (are_friends("database.db", username, username1)==2){//sprawdzenie czy nie dodaje sei samego siebie do znaj
                send(newSocket, "Nie możesz dodać siebie do znajomych.\n", 39, 0);
                printf("Wysłano wiadomość: Nie możesz dodać siebie do znajomych.\n");
            }
            else if (check_username("database.db",username1)==0){//sprawdzenie czy dodawany uzytkownik istnieje
                send(newSocket,"Nie ma takiego użytkownika.",27,0);
                printf("Nie ma takiego użytkownika.");
            }
            else {
                int result1 = add_friend("database.db", username, username1);//jesli tamte nie spelnione to sie udaje dodac
                if (result1 == 1) {
                    send(newSocket, dodano, sizeof dodano, 0);
                    printf("Wysłano wiadomość: %s\n", dodano);
                } 
            }
        }
        else if (sscanf(client_message, "SIGN;%30[^;];%30s", username, password) == 2){//pobranie do rejestracji
            
            char *message = malloc(sizeof(client_message));
            strcpy(message,client_message);
            sleep(1);
            memset(&client_message, 0, sizeof (client_message));

            int result1 = check_username("database.db", username);//sprawdzenie czy juz nazwa zajeta
            if (result1 == 1) {
                printf("nazwa zajeta\n");
                
                send(newSocket,nie,sizeof(nie),0);
                printf("Wysłano wiadomość: %s\n", nie); 
                
            }
            else{
                if (add_user("database.db",username,password)==1){//jesli nie to sie rejestruje
                    send(newSocket,ok,sizeof(ok),0);
                    printf("rejestracja ok");}
            }
        }
            

    

    }
    printf("Exit socketThread \n");

    pthread_exit(NULL);
}

int main(){
  int serverSocket, newSocket;
  struct sockaddr_in serverAddr;
  struct sockaddr_storage serverStorage;
  socklen_t addr_size;

  //Create the socket. 
  serverSocket = socket(PF_INET, SOCK_STREAM, 0);

  // Configure settings of the server address struct
  // Address family = Internet 
  serverAddr.sin_family = AF_INET;

  //Set port number, using htons function to use proper byte order 
  serverAddr.sin_port = htons(1100);

  //Set IP address to localhost 
  serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);


  //Set all bits of the padding field to 0 
  memset(serverAddr.sin_zero, '\0', sizeof serverAddr.sin_zero);

  //Bind the address struct to the socket 
  bind(serverSocket, (struct sockaddr *) &serverAddr, sizeof(serverAddr));

  //Listen on the socket
  if(listen(serverSocket,50)==0)
    printf("Listening\n");
  else
    printf("Error\n");
    pthread_t thread_id;

    while(1)
    {
        //Accept call creates a new socket for the incoming connection
        addr_size = sizeof serverStorage;
        newSocket = accept(serverSocket, (struct sockaddr *) &serverStorage, &addr_size);

        if( pthread_create(&thread_id, NULL, socketThread, &newSocket) != 0 )
           printf("Failed to create thread\n");

        pthread_detach(thread_id);
        //pthread_join(thread_id,NULL);
    }
  return 0;
}
