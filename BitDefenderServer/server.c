#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>       
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h>
#include <dirent.h>

#define PORT 12345
#define BCKLOG 5 //size of waiting connections queue


// thread function
void *conn_handler(void *);
// type of request function
int ret_choice(char *);
/* variables I need to access in thread function, so will declared them here instead of 
 creating a struct encapsulating them all so they could be sent as paramater. */
int socket_desc;
char quotes[50][1000];
int q_len; //number of quotes

int main(int argc, char* argv[]){

	struct sockaddr_in server_addr, client_addr;
	int newfd; // accept - return
	int *new_sock; //one for every thread
	FILE *fsrv; //read file from service
	char line[1000];

	// read all quotes of the day in **quotes
	fsrv = fopen("./service/quote_of_the_day", "r");
	if(!fsrv){
		perror("Missing file of quotes");
		exit(1);

	}
	while(fgets(line, 1000, fsrv)) strcpy(quotes[q_len++], line);

	//create socket and bind and listen
	socket_desc = socket(AF_INET, SOCK_STREAM, 0);
	if(socket_desc < 0)
	{
		perror("Cannot create socket\n");
		exit(1);
	}

	//set all values from buffer to 0
	memset((char*) &server_addr, 0, sizeof(server_addr));

	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(PORT);
	server_addr.sin_addr.s_addr = INADDR_ANY;

	if(bind(socket_desc, (struct sockaddr *) &server_addr, sizeof(server_addr)) < 0)
	{
		perror("bind err\n");
		exit(1);
	}
	

	listen(socket_desc, BCKLOG);
	int clen = sizeof(client_addr);
	while(1)

	{
		newfd = accept(socket_desc, (struct sockaddr *)&client_addr,(socklen_t*)&clen);
		if(newfd < 0)
		{
			perror("accept err\n");
			exit(1);
		}

		printf("Connection accepted\n");
		pthread_t tid;
		new_sock = malloc(1);
		*new_sock = newfd;
		if(pthread_create(&tid, NULL, conn_handler, (void*)new_sock) < 0)
		{
			perror("can't create thread\n");
			exit(1);
		
		}
		printf("added handler\n");

	}
	
	return 0;
}

int ret_choice(char *path) //return the type of request
{
	struct stat statbuf; //stat struct 
	if(stat(path, &statbuf) == 0)
	{
		if(S_ISDIR(statbuf.st_mode)) return 1; //directory
		if(S_ISREG(statbuf.st_mode)) //regular file
		{
			// hardcoded value :(
			if(strstr(path, "quote_of_the_day")) return 2; // quote thing
			return 0; //if is not service type, then it's a file
		}

	}
	return 3; // path not available, must display Error message
	
}

void *conn_handler(void *socket_desc_thread)
{
		
	
	int socket_d = *(int *)socket_desc_thread;
	int choice; //0 - file, 1 - dir, 2 - quote, 3 - error
	int n; //number of bytes read/written
	char buff[1024]; //server reads characters here from socket
	char *p; // get the path from request
	char path[100]; // path that will actually be tested, 100 is just a guess
	FILE *fp, *fpe;
	unsigned char *file_buff = malloc(256);
	unsigned char *err_buff = malloc(256);
	char *msg = malloc(1000); //for storing the quote

	//for the html file with directories 
	char webline[150]; //read line by line
	char dwebpage[4096]; //html file displaying directory contents

	//for directory
	DIR *dir;
	struct dirent *entry;

	//read from client
	memset(buff, 0, 1024);
	n = read(socket_d, buff, 1024);
	if(n < 0) 
	{
		perror("error at read");
		exit(1);
	}
	
	//obtain the path
	p = strtok(buff, " ");
	if(p)
	{
		p = strtok(NULL, " ");
		printf("%s\n", p);

	}
	printf("%s\n", p); //just to be  sure

	// path is relative to webroot
	strcpy(path, "./webroot");
	strcat(path, "/"); 

	//if command contains "repository" the search in webroot content
	if(strstr(p, "repository")){

		strcat(path, p + (sizeof("/repository")));
	}
	//otherwise just search the path relative to webroot
	else{
		strcat(path, "../");
		strcat(path, p);
	}
	choice = ret_choice(path); //type of request
	printf("choice: %d\n", choice); //just to be sure
	switch(choice)
	{
		case 0: //file
			fp = fopen(path, "rb");
			if(fp == NULL)
			{
				printf("File open error\n");
				exit(1);
			}
	
			memset(file_buff, 0, 256);
			int nread = fread(file_buff, 1, 256, fp);
			printf("%s %d\n", path, nread);
			if(!nread) 
			{
				printf("File is empty\n");
				exit(1);					
			}
			if(nread > 0) // read was success then write it to client fd
			{
				printf("Sending...\n");
				write(socket_d, file_buff, nread);
			}
			
			break;	
		case 1: // directory

			strcpy(dwebpage,
				"HTTP/1.1 200 OK\r\n"
				"Content-Type: text/html: charset=UTF-8\r\n\r\n"
				"<!DOCTYPE html>\r\n"
				"<html><body>");
			if((dir = opendir(path))!=NULL) //display dir contents
			{
				while((entry = readdir(dir))!=NULL)
				{

					//create the html body
					sprintf(webline, "<a href=%s>%s</a><br>", path, entry->d_name);
					strcat(dwebpage, webline);
				}
				strcat(dwebpage, "</body></html>"); // add final tags
				closedir(dir);
				write(socket_d, dwebpage, strlen(dwebpage));
			} 
			else 
			{
				perror("Cannot open directory");
				exit(1);

			}
			break;
		case 2: // quote
			printf("Sending...\n");
			//random quote by generating random index.. might have used some other random generating mechanism.. it oddly seems to reproduce the same result every time
			strcpy(msg, quotes[rand() % q_len]); 
			write(socket_d, msg, strlen(msg));
			break;
		case 3: // error; display error msg
			fpe = fopen("errormsg.bin", "rb"); //open the special error file 
			//might have simply wrote it in a string of char instead of reading the message from a file, this seemed to be the most convenient solution after several failures..
			if(fpe == NULL){
				printf("missing error file\n");
				exit(1);

			}
			memset(err_buff, 0, 256);
			int n = fread(err_buff, 1, 256, fpe);
			if(n > 0) //read was succesfull
			{
				printf("Sending...\n");
				write(socket_d, err_buff, n);
			}
			else {
				perror("Error at read error file");
				exit(1);
			}
			break;

	}
	// free all the buffers used... 
	// could have malloc'd/free'd all of them in the corresponding switch branch, but i didn't 
	// really wanted to risk other seg faults....
	free(file_buff);
	free(err_buff);
	free(msg);
	close(socket_d);
	free(socket_desc_thread);
}



