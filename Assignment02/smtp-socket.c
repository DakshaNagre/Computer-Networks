#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <netdb.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define BUFFER_SIZE 1024

typedef struct addrinfo addr_t;

int generate_addr(const char* host, const char* port, addr_t** result) {
  addr_t hints;
  memset(&hints, 0, sizeof(addr_t));
  hints.ai_family = AF_INET;
  hints.ai_socktype = SOCK_STREAM;
  return getaddrinfo(host, port, &hints, result);
}

int open_socket(addr_t* i) {
  int sockid = socket(i->ai_family, i->ai_socktype, i->ai_protocol);
   if (sockid != -1) {
    if (connect(sockid, i->ai_addr, i->ai_addrlen) != -1) {
        return sockid;
    }
    close(sockid);
  }
  return -1;
}

int main(int argc, char** argv) {

  addr_t *results, *i;
  int sockid;
  char buffer[BUFFER_SIZE];
  char resp[BUFFER_SIZE];

  /* Build address information */
  if (generate_addr(argv[1], argv[2], &results) != 0) {
    fprintf(stderr, "Failed to get address information. Please pass the input parameters as host, port and the message. \n");
    exit(-1);
  }

  /* Iterating through the results from getaddrinfo()
  to  create socket and connect to remote server */
  for (i = results; i != NULL; i = i->ai_next) {
    if ((sockid = open_socket(i)) != -1) break;
  }

  //Results is null
  if (i == NULL) {
      fprintf(stderr, "Could not make connection\n");
    exit(-1);
  } 
  
  // Displaying all the ip address
  for (i = results; i != NULL; i = i->ai_next) {
     struct sockaddr_in *addr_in = (struct sockaddr_in *)i->ai_addr;
     char *ans = inet_ntoa(addr_in->sin_addr);
     printf("IP address: %s\n",ans);
  }  
  
  freeaddrinfo(results);
  
  memset(buffer, '\0', BUFFER_SIZE);
  memcpy(buffer, argv[3], strlen(argv[3]));
  
  /* Send message to remote server */
  if (send(sockid, buffer, BUFFER_SIZE, 0) != BUFFER_SIZE) {
    fprintf(stderr, "Failed to write entire buffer\n");
    exit(-1);
  } 
  
  /* Recieve echo from server */
  if (recv(sockid, resp, BUFFER_SIZE, 0) == -1) {
    perror("read error");
    exit(-1);
  } 
  
  printf("Response from server: %s\n", resp);
  return 0;
} 

         