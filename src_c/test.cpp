#include "test.h"


void test() {
    testPredict();
    std::cout << "All tests passed!" << std::endl;
}

void assertEqual(auto v1, auto v2) {
    if (v1 != v2) {
        throw std::runtime_error("Test failed: " + std::to_string(v1) + " != " + std::to_string(v2));
    }
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

    std::string targetName = "label";
    Argument label(targetName, "T");
    label.setIsLabel(true);

    af.addArgument(a1);
    af.addArgument(a2);
    af.addArgument(a3);
    af.addArgument(a4);
    af.addArgument(a5);
    af.addArgument(a6);
    af.addArgument(a7);
    af.addArgument(label);

    af.addAttack(a1, label);
    af.addAttack(a2, label);
    af.addAttack(a1, a2);
    af.addAttack(a3, a1);
    af.addAttack(a4, a3);
    af.addAttack(a4, a2);
    af.addAttack(a5, a3);
    af.addAttack(a6, a4);
    af.addAttack(a6, a5);
    af.addAttack(a6, a2);

    std::vector<Fact> f1 = {"a=1", "a=2"};
    assertEqual(af.predict(f1, targetName), false);

    std::vector<Fact> f2 = {"a=1", "a=2", "a=3", "a=4"};
    assertEqual(af.predict(f2, targetName), false);

    std::vector<Fact> f3 = {"a=1", "a=3", "a=4", "a=6"};
    assertEqual(af.predict(f3, targetName), true);

    std::vector<Fact> f4 = {"a=1", "a=2", "a=3", "a=5", "a=6"};
    assertEqual(af.predict(f4, targetName), true);

}