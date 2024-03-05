#pragma once
#include "argument.h"

#typedef std::tuple<Argument, Argument> Attack;


class EncodedAF {

    public:
        EncodedGraph();
        EncodedAF(const EncodedAF & af);
        ~EncodedGraph();
        AF * convertToAF() const;
        void addArgument(Argument a);
        void addAttack(Attack r);
        std::vector<Argument> getArguments() const;
        std::vector<Attack> getAttacks() const;
        std::vector<Attack> getPossibleAddons() const;

    private:
        std::vector<Argument> _a;  // argument list
        std::vector<std::vector<int>> _r;  // encoded attack relation; 1: attack; 0: no attack; -1: invalid
};

class AF {

    public:
        AF();
        ~AF();

        std::vector<Argument> getArguments() const;
        std::vector<Attack> getAttacks() const;
        std::vector<Argument> getInAttacks(const Argument & a) const;
        std::vector<Argument> getOutAttacks(const Argument & a) const;
        void addArgument(const Argument & a);
        void addAttack(const Attack & r);
        void updateAliveness(const std::vector<std::string> & facts);

    private:
        std::vector<Argument> _a;
        std::vector<Attack> _r;

};