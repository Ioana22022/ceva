struct x {
    int x1, x2;
    char x3;
};

__attribute__((stdcall))
int func(struct x a, float b, void* c, int d) {
    return 42;
}

int main() {
    struct x a;
    a.x3 = '$';
    func(a, 3.14, (void*)0xdeadbeef, 1);
    return 0;
}
