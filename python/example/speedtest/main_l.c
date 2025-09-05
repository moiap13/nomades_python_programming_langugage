#include <stdio.h>
#include <stdlib.h>

int main() 
{
  int *l = malloc(1000000000 * sizeof(int));
  for (int i = 0; i < 100; i++) {
    l[i] = 0;
  }
  for (int i = 0; i < 1000000000; i++) {
    l[i] = l[i] + 1;
  }
  printf("%d\n", l[0]);
  return 0;
}
