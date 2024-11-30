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
char client_message[2000];
char buffer[1024];
char username[30];
char password[30];
char ok[2]="ok";
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void * socketThread(void *arg)
{
  printf("new thread \n");
  int newSocket = *((int *)arg);
  int n;
  for(;;){
    // sleep(20);
    n=recv(newSocket , client_message , 2000 , 0);
    printf("%s\n",client_message);
        if(n<1){
            break;
        }
        if (sscanf(client_message,"LOG;%30[^;];%30[^;]",username,password)==2){
            printf("%s\n",username);
            printf("%s\n",password);
            int result = check_user("database.db", username, password);
            if (result==1){
                printf("zalogowałes sie");
                //zrobic send, i rcv u klienta i wtedy okienko sie zamyka wiec w signup tez to poprawic
                //zrobie to jutro mati 
            }
            else{
                printf("dupa");
            }

        }
        printf("dziala");

    char *message = malloc(sizeof(client_message));
    strcpy(message,client_message);

    sleep(1);
    send(newSocket,message,sizeof(message),0);
    memset(&client_message, 0, sizeof (client_message));

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
