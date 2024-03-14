#include "test.h"


void test() {

}

void testPredict() {
    AF af;
    Argument a1("a", "1");
    Argument a2("a", "2");
    Argument a3("a", "3");
    Argument a4("a", "4");
    Argument a5("a", "5");
    Argument a6("a", "6");
    Argument a7("a", "7");
    Argument label("label", "T");
    label.setIsLabel(true);
    af.addArgument(a1);
    af.addArgument(a2);
    af.addArgument(a3);
    af.addArgument(a4);
    af.addArgument(a5);
    af.addArgument(a6);
    af.addArgument(a7);
    af.addArgument(label);
    af.addAttack(std::make_tuple(a1, label));
}