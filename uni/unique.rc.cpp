#include <iostream>
using namespace std;
  int main(int *a,  bool*  b  ,  HELLO* h)
{
   int x = 2 * sizeof(int)  // sizeof(a[2]);
   int y = 3 * sizeof(bool)  // sizeof(b[3]);
   int z = 4 * sizeof(HELLO)  // sizeof(h[4]); 
   return 0;
}
