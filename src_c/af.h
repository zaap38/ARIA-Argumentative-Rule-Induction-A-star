#pragma once
#include "argument.h"
#include <vector>
#include <tuple>
#include <string>
#include "snippets.h"
#include <algorithm>
#include <cmath>


typedef std::tuple<Argument, Argument> Attack;
typedef std::string Fact;


class AF {

    public:
        AF();
        ~AF();

        std::vector<Argument> getArguments() const;
        Argument * getArgument(int i);
        Argument * getArgumentByName(const std::string & name);
        std::vector<Attack> getAttacks() const;
        std::vector<Argument*> getInAttackers(const Argument & a);
        std::vector<Argument*> getOutAttackers(const Argument & a);
        void setArguments(const std::vector<Argument> & a);
        void addArgument(const Argument & a);
        void addAttack(const Attack & r);
        void updateAliveness(const std::vector<Fact> & facts);
        bool predict(const std::vector<Fact> & facts, const std::string & target);
        void printAttacks() const;
        void printArguments() const;

    private:
        std::vector<Argument> _a;
        std::vector<Attack> _r;

        void computeExtension(const Fact & target = "");
        Argument * getRootArgument();
        bool isRoot(const Argument & a);
        bool targetAlive(const std::string & target) const;

};


class EncodedAF {

    public:
        EncodedAF();
        EncodedAF(const EncodedAF & af);
        EncodedAF(const std::vector<Argument> & arguments);
        ~EncodedAF();
        AF * convertToAF() const;
        void addArgument(Argument a);
        void addArguments(const std::vector<Argument> & a);
        void initAttackRelation();
        void addAttack(const Attack & r);
        void removeAttack(const Attack & r);
        std::vector<Argument> getArguments() const;
        std::vector<std::vector<int>> getAttacks() const;
        std::vector<Attack> getAttackTuples() const;
        std::vector<Attack> getPossibleAddons() const;
        std::tuple<int, int> getAttackIndex(const Attack & r) const;
        void print() const;
        void printMatrix() const;
        bool isInAttack(const Argument & a) const;
        int getAttackSize() const;
        std::string getHash() const;

    private:
        std::vector<Argument> _a;  // argument list
        std::vector<std::vector<int>> _r;  // 2D array of ints: encoded attack relation; 1: attack; 0: no attack; -1: invalid
};
