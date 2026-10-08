#include "smackdown.h"

char *ring[20];
FILE *save_file;

void play_match(){    
    int y, x;
    char buff[1024];
    uint8_t i = 0;
    char move_type;

    i = 0;
    while (i < 20){
        puts(ring[i]);
        i++;
    }
    puts("[PERFORM YOUR FINISHING MOVE]");

    printf("Target Row (Y-axis) >> ");
    scanf("%d", &y);
    getchar();
    printf("Target Col (X-axis) >> ");
    scanf("%d", &x);
    getchar();
    
    // VULNERABILITY: The bounds check warns the user, but doesn't exit!
    if (y >= 20 || x >= 0x80 || x < 0x0){
        puts("Ref: Hey! You can't do that, it's out of bounds!");
    }
    
    printf("Move Type (Char) >> ");
    scanf("%c", &move_type);
    getchar();
    
    puts("Climbing the top rope...");
    puts("BAH GAWD! HE JUMPS!!!");
    
    // Out-Of-Bounds Write occurs here if invalid coordinates were provided
    ring[y][x] = move_type;
    
    printf("Any last words for the camera? >> ");
    fgets(buff, 1000, stdin);
    printf("%s\n", buff);
    
    printf("\nCommentator: %s\n\n", commentary[rand() % NUM_COMMENTARY]);
}

void init_match(){
    uint8_t i = 0;
    uint8_t y = 0;

    puts(banner);
    puts("");
    srand(time(0));
    save_file = fopen("flag.txt", "r");
    
    while (i < 20){
        ring[i] = malloc(0x80);
        y = 0;
        while (y < 0x80){
            if (rand() % 10 == 3)
                ring[i][y] = '#';
            else 
                ring[i][y] = ' ';
            y++;
        }
        i++;
    }
}

void ignore_me(){
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);
    alarm(128);
}

int main(){
    ignore_me();
    init_match();
    while (true)
        play_match();
    return 0;
}
