#pragma once

#include <memory>
#include <ostream>
#include <vector>

#include "dreal/solver/formula_evaluator.h"
#include "dreal/util/box.h"

namespace dreal {

/// Base type for evaluator cell types.
class FormulaEvaluatorCell {
 public:
  explicit FormulaEvaluatorCell(Formula f);

  /// Deleted copy-constructor.
  FormulaEvaluatorCell(const FormulaEvaluatorCell&) = delete;

  /// Deleted move-constructor.
  FormulaEvaluatorCell(FormulaEvaluatorCell&&) = default;

  /// Deleted copy-assignment operator.
  FormulaEvaluatorCell& operator=(const FormulaEvaluatorCell&) = delete;

  /// Deleted move-assignment operator.
  FormulaEvaluatorCell& operator=(FormulaEvaluatorCell&&) = delete;

  /// Default destructor.
  virtual ~FormulaEvaluatorCell() = default;

  const Formula& formula() const { return f_; }

  /// Returns true if the based formula is a simple relational formula which is
  /// in form of `constant relop variable` or `!(constant relop variable)`.
  bool is_simple_relational() const { return is_simple_relational_; }

  /// Returns true if the based formula is a not-equal formula which is
  /// in form of `e1 != e2` or `!(e1 == e2)`.
  bool is_neq() const { return is_neq_; }

  /// Evaluates the constraint/formula with @p box.
  virtual FormulaEvaluationResult operator()(const Box& box) const = 0;

  virtual const Variables& variables() const = 0;

  virtual std::ostream& Display(std::ostream& os) const = 0;

 private:
  const Formula f_;
  const bool is_simple_relational_{false};
  const bool is_neq_{false};
};

}  // namespace dreal
