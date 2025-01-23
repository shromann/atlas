#include <iostream>
#include "Order.h"
#include "Strategy.h"

int main(int argc, char const *argv[])
{
    std::cout << "********* Atlas Trading *********\n";

    Strategy atlas = Strategy();
    if (Order order = atlas.createOrder(5); order.trade){
        order.send();
    }
    return 0;
}
