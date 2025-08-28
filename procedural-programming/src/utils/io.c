
int checkint() {
    int x;
    while (scanf("%d", &x) != 1 || getchar() != '\n') {
        printf("Option does not exist. Please re-enter the option you want.\n>>> ");
        while (getchar() != '\n');
    }
    return x;
}