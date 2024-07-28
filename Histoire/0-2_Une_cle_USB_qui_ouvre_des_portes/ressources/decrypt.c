#include <stdio.h>
#include <stdlib.h>
#include <sys/random.h>
#include <string.h>
#include <unistd.h>

int main(void) {
	
	char list[101][30] = { "backflip2\0", "backflip17\0", "backflip16\0", "backflip15\0", "backflip147\0", "backflip123\0", "backflip12\0", "backflip101\0", "backflip060495!\0", "backflip0\0", "backflip.\0", "backfliplayout\0", "backflic\0", "backflex\0", "backflash\0", "backfl1p\0", "backfist1\0", "backfist\0", "backfire39\0", "backfire13117\0", "backfire07\0", "backfire!\0", "backfileedit\0", "backfighter\0", "backfield1\0", "backfeather\0", "backfat8\0", "backfat1\0", "backfat.\0", "backfat\0", "backetball1991\0", "backetball\0", "backet\0", "backerz\0", "backeryman\0", "backery\0", "backerstraat\0", "backers4009\0", "backers35\0", "backers23\0", "backerpumita.14\0", "backerij\0", "backer58\0", "backer49\0", "backer44\0", "backer41\0", "backer40\0", "backer34\0", "backer24\0", "backer1228\0", "backer1\0", "backer09\0", "backer07\0", "backer01\0", "backer&\0", "backenzie\0", "backenupp\0", "backend1\0", "backend08\0", "backen33\0", "backen1\0", "backelem\0", "backedu\0", "backedneans\0", "backed\0", "backeast\0", "backe123456789\0", "backe#41\0", "backdry\0", "backdrop\0", "backdrafts\0", "backdraft86\0", "backdraft3342\0", "backdraft06\0", "backdraft.\0", "backdown9\0", "backdown25\0", "backdown0\0", "backdor\0", "backdoorlover\0", "backdoor@#&*9\0", "backdoor912\0", "backdoor831\0", "backdoor82\0", "backdoor789\0", "backdoor76\0", "backdoor75\0", "backdoor66\0", "backdoor44\0", "backdoor1993\0", "backdoor11\0", "backdoor0\0", "backdoor.\0", "backdive\0", "backdeptrai\0", "backden1\0", "backden\0", "backdella\0", "backdeck\0", "backdeath\0", 0};

	unsigned char charset[63] = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
	charset[63] = 0;
	printf("charset %s\n", charset);
	unsigned char salt[17] = {0};
	salt[17] = 0;
	unsigned char token[9] = {0};
	token[9] = 0;
	unsigned char password[33] = {0};
	password[33] = 0;

	int secure_seed = 1719603762;
	int pos = 0;
	int password_index;
	getrandom(&password_index,1,2);
	

	printf("random index : %d\n", password_index);

	srand(secure_seed);

	for (int i = 0; i < 16; i++) {
		pos = rand();
		salt[i] = charset[pos % 62];
	}
	printf("salt : %s\n", salt);

	for (int i = 0; i < 8; i++) {
		pos = rand();
		token[i] = charset[pos % 62];
	}
	printf("token : %s\n", token);

	char *dest = NULL;
	char *final = NULL;
	char *final_salt = malloc(20);
	final_salt[0] = '$';
	final_salt[1] = '6';
	final_salt[2] = '$';

	for (int i = 0; i < 100; i++) {
			printf("%d : %s\n", i, list[i]);
			dest = strcat(list[i], token);
			printf("%d : %s\n", i, dest);
			final = crypt(dest, strcat(final_salt, (char *)salt));
			printf("%s\n", final);
	}
	
	return 0;
}
