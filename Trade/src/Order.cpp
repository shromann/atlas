#include <iostream>
#include "Order.h"

Order::Order(float price, int size) : trade(false) {
    orderPrice = price;
    orderSize  = size;
    if (orderPrice > 0 & orderSize > 0){
        trade = true;
    }
}

void Order::send(){
    std::cout << "order sent!" << std::endl;
}
