#include <stdio.h>

/*
 * Make a program that counts to 1'000'000'000 in C
 */
int	main(void)
{
	int	n;

	n = 0;
	while (n < 1000000000)
	{
		n++;
	}
	printf("%d\n", n);
}
