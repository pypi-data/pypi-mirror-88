ChronoTCO
====
**Version**: Experimental 0.0.1  
This is an experimental decorator implementation of tail call optimization in Python3 via bytecode injection, reducing the space complexity of recursion to **O(1)** (rather than **O(n)**) by manipulating the function structure itself.  

If a function is tail-call recursive and you want to ensure you won't blow the stack, use chronotco!

Installation
----
    pip install chronotco  


Usage
----
Import the decorator:

    from chronotco import chronotco

And decorate your tail-recursive function!

    @chronotco
    def tail_factorial(n, accumulator=1):
    if n == 0: return accumulator
    else: return tail_factorial(n-1, accumulator * n)

Support
----
I do not provide any support, and I am not responsible for any melted faces from raw performance!

License
----
The license is copyleft, just keep it free forever and do what you will.