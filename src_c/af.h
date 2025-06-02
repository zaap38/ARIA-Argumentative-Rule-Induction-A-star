#pragma once
#include "argument.h"
#include <vector>
#include <tuple>
#include <string>
#include "snippets.h"
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <chrono>


typedef std::tuple<Argument*, Argument*> AttackPtr;
typedef std::tuple<Argument, Argument> Attack;
typedef std::string Fact;


class AF {

    public:
        AF();
        ~AF();

        std::vector<Argument> getArguments() const;
        Argument * getArgument(int i);
        Argument * getArgumentByName(const std::string & name);
        std::vector<AttackPtr> getAttacks() const;
        std::vector<AttackPtr> getSupports() const;
        std::vector<Argument*> getInAttackers(const Argument & a);
        std::vector<Argument*> getInSupporters(const Argument & a);
        std::vector<Argument*> getOutAttackers(const Argument & a);
        std::vector<Argument*> getOutSupporters(const Argument & a);
        void setArguments(const std::vector<Argument> & a);
        void addArgument(const Argument & a);
        void addAttack(const std::string & name1, const std::string & name2);
        void addSupport(const std::string & name1, const std::string & name2);
        void addAttack(const Argument & a1, const Argument & a2);
        void addSupport(const Argument & a1, const Argument & a2);
        void updateAliveness(const std::vector<Fact> & facts);
        bool predict(const std::vector<Fact> & facts, const std::string & target);
        void printAttacks() const;
        void printArguments() const;

    private:
        std::vector<Argument> _a;
        std::vector<AttackPtr> _r;  // attack relation
        std::vector<AttackPtr> _s;  // support relation

        void computeExtension(const Fact & target = "");
        void computeBipolarExtension(const Fact & target = "");
        Argument * getRootArgument();
        bool isRoot(const Argument & a);
        bool targetAlive(const std::string & target) const;
        void addAttack(const AttackPtr & r);
        void addSupport(const AttackPtr & r);

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
        void addAttack(const Attack & r, int type = 1);
        void removeAttack(const Attack & r);
        std::vector<Argument> getArguments() const;
        std::vector<std::vector<int>> getAttacks() const;
        std::vector<Attack> getAttackTuples() const;
        std::vector<Attack> getPossibleAddons() const;
        std::tuple<int, int> getAttackIndex(const Attack & r) const;
        void print() const;
        void printMatrix() const;
        bool isInAttack(const Argument & a) const;
        bool isInSupport(const Argument & a) const;
        bool isInAttackOrSupport(const Argument & a) const;
        int getAttackSize() const;
        std::string getHash(const std::string & callFrom = "") const;

    private:
        std::vector<Argument> _a;  // argument list
        std::vector<std::vector<int>> _r;  // 2D array of ints: encoded attack relation; 1: attack; 0: no attack; -1: invalid
};
