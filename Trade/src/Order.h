#pragma once

class Order{
private:
    float orderPrice;
    int   orderSize;
public:
    Order(float price, int size);
    void send();
    bool trade;
};