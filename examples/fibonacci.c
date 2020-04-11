/* File: fibonacci.c
 * Example in Cminus to compute fibonacci (n) 
 */

int fibonacci(int n) {
	int x += contador + indice;
	int y;
	if (n == 0) 
		return 0;
	else if (n  == 1)
		return 1;
	x = fibonacci(n-1);
	y = fibonacci(n-2);	
	return x + y;

}

int main() {
	
	int n;
	n = fibonacci(15);	
	return 0;
}
