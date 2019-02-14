int main() {
    int x = 1000, i, j;
    for (i = 1; i < 10; i++) {
        for (j = 1; j < 4; j++) {
            if (x == 42)
                break;
        }
        if (i == 3)
            continue;
    }
    return 0;
}
