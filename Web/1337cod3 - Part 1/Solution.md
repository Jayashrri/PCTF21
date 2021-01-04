If we see the file `problems/testcase.gen.js`, it's apparent that the default generators for input and output are left as it is mistakenly. So random input and output files are generated every time a compilation is done and there is no correlation between the input and output. So an output file that matches the randomly generated output file must be created. 

Unfortunately WebAssembly only has a restricted set of libraries and functions available to use. However, the functionality to create symlinks is still available. So a relative symlink can be created to the generated output file, so that when the output file is evaluated, node follows the symlink and ends up comparing the generated output file to itself.

### Exploit:

```c
#include <stdio.h>
#include <unistd.h>

int main() {
    symlink("../../../problems/output.txt", "output.txt");
    return 0;
}
```