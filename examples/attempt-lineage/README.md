# Attempt and outcome lineage examples

These generic cases exercise the attempt outcome integrity contract without referring to a specific product or pilot.

| Case | Scenario | Expected interpretation |
|---|---|---|
| A | Product gate runs and fails | `product_failure` |
| B | Operator preparation fails first | Product `not_executed`; `operator_error` |
| C | Reusable orchestration fails first | Product `not_executed`; `orchestration_error` |
| D | Product gate starts but the environment prevents a conclusion | Product `inconclusive`; `environment_failure` |
| E | Authority declares the product gate not applicable | Product `not_applicable`; no failure class |
| F | Later evidence classifies an initially unknown failure | Append a classification; preserve the original bytes |
| G | A normative change affects prior proof | Record materiality and require a new attempt |
| H | A correction is applied but not checked | Keep it `applied_not_validated` |

All timestamps, actors, identifiers, and evidence references are synthetic. They demonstrate structure only and do not claim that a real command ran.
