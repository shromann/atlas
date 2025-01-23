#include "Strategy.h"

Strategy::Strategy(){
}

Order Strategy::createOrder(int x)
{
    Order order = Order(x, x);
    if (x % 2 == 0){
        order.trade = true;
    }
    return order;
}