#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void setup_IO()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}

void shell()
{
    system("/bin/sh");
}

int main()
{
    int current_power = -9000;
    int power_up;

    setup_IO();

    puts(" _______  _     _  __    _  _______  __   __  _______  _______  ______   ");
    puts("|       || | _ | ||  |  | ||       ||  | |  ||       ||       ||    _ |  ");
    puts("|    _  || || || ||   |_| ||_     _||  | |  ||_     _||   _   ||   | ||  ");
    puts("|   |_| ||       ||       |  |   |  |  |_|  |  |   |  |  | |  ||   |_||_ ");
    puts("|    ___||       ||  _    |  |   |  |       |  |   |  |  |_|  ||    __  |");
    puts("|   |    |   _   || | |   |  |   |  |       |  |   |  |       ||   |  | |");
    puts("|___|    |__| |__||_|  |__|  |___|  |_______|  |___|  |_______||___|  |_|");
    puts("");
    puts("=========================================================================");
    puts("                         Stage 1: Over 9000");
    puts("=========================================================================");
    printf("Current Power Level: %d\n", current_power);
    printf("Power up => ");

    scanf("%d", &power_up);

    if (power_up > 9000)
    {
        puts("Sorry, you do not have that much potential :(");
        exit(0);
    }

    printf("Powering up.");
    sleep(1);
    printf(".");
    sleep(1);
    puts(".");
    sleep(1);
    puts("");

    current_power += power_up;

    printf("Your new power level is %d\n", current_power);

    if (current_power > 9000)
    {
        puts("IT'S OVER NINE THOUSAND!!!");

        shell();
    }
    else
    {
        puts("You're too weak to operate a shell!");
    }

    return 0;
}
