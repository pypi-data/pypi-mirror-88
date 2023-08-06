#include "dreal/smt2/term.h"

#include <stdexcept>
#include <utility>

#include "fmt/format.h"
#include "fmt/ostream.h"

#include "dreal/util/exception.h"

namespace dreal {

using std::ostream;
using std::runtime_error;

Term::Term() : Term{Formula::False()} {}
Term::Term(Expression e) : type_{Term::Type::EXPRESSION}, e_{std::move(e)} {}
Term::Term(Formula f) : type_{Term::Type::FORMULA}, f_{std::move(f)} {}

Term::Type Term::type() const { return type_; }

const Expression& Term::expression() const {
  if (type() != Term::Type::EXPRESSION) {
    throw runtime_error("This term is not an expression.");
  }
  return e_;
}

Expression& Term::mutable_expression() {
  return const_cast<Expression&>(expression());
}

const Formula& Term::formula() const {
  if (type() != Term::Type::FORMULA) {
    throw runtime_error("This term is not a formula.");
  }
  return f_;
}

Term& Term::operator=(Expression e) { return *this = Term{std::move(e)}; }

Term& Term::operator=(Formula f) { return *this = Term{std::move(f)}; }

Formula& Term::mutable_formula() { return const_cast<Formula&>(formula()); }

Term Term::Substitute(const Variable& v, const Term& t) {
  switch (type_) {
    case Type::FORMULA:
      return Term{f_.Substitute(v, t.f_)};
    case Type::EXPRESSION:
      return Term{e_.Substitute(v, t.e_)};
  }
  DREAL_UNREACHABLE();
}

void Term::Check(Sort s) const {
  switch (type()) {
    case Term::Type::EXPRESSION:
      if (s == Sort::Int || s == Sort::Real || s == Sort::Binary) {
        return;  // OK
      }
      break;

    case Term::Type::FORMULA:
      if (s == Sort::Bool) {
        return;  // OK
      }
      break;
  }
  throw runtime_error{fmt::format(
      "Term {} is an expression but it is checked against sort {}.", *this)};
}

void Term::Check(Variable::Type t) const {
  switch (t) {
    case Variable::Type::BOOLEAN:
      if (type_ == Type::FORMULA) {
        return;  // OK
      }
      break;

    case Variable::Type::BINARY:
    case Variable::Type::INTEGER:
    case Variable::Type::CONTINUOUS:
      if (type_ == Type::EXPRESSION) {
        return;  // OK
      }
      break;
  }
  throw runtime_error{fmt::format(
      "Term {} is an expression but it is checked against type {}.", *this, t)};
}

ostream& operator<<(ostream& os, const Term& t) {
  switch (t.type()) {
    case Term::Type::EXPRESSION:
      return os << t.expression();
    case Term::Type::FORMULA:
      return os << t.formula();
  }
  DREAL_UNREACHABLE();
}

}  // namespace dreal
