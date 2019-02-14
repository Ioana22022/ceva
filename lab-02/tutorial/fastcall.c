__attribute__((fastcall))
int func(int a, int b, int c, int d) {
    return 42;
}

int main() {
    func(1, 2, 3, 4);
    return 0;
}
