#pragma once
#include "argument.h"
#include <vector>
#include <tuple>
#include <string>


typedef std::tuple<Argument, Argument> Attack;


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
        const std::string & predict() const;

    private:
        std::vector<Argument> _a;
        std::vector<Attack> _r;

};


class EncodedAF {

    public:
        EncodedAF();
        EncodedAF(const EncodedAF & af);
        ~EncodedAF();
        AF * convertToAF() const;
        void addArgument(Argument a);
        void addArguments(const std::vector<Argument> & a);
        void initAttackRelation();
        void addAttack(const Attack & r);
        void removeAttack(const Attack & r);
        std::vector<Argument> getArguments() const;
        std::vector<Attack> getAttacks() const;
        std::vector<Attack> getPossibleAddons() const;

    private:
        std::vector<Argument> _a;  // argument list
        std::vector<std::vector<int>> _r;  // encoded attack relation; 1: attack; 0: no attack; -1: invalid
};