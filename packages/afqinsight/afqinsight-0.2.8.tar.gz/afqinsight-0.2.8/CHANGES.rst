v0.2.8 (December 10, 2020)
==========================
  * DEP: Bump groupyr version

v0.2.7 (December 09, 2020)
==========================
  * ENH: Add ensemble estimators to pipelines (#59)

v0.2.6 (October 28, 2020)
=========================
  * FIX: Add option to serialize cv execution (#57)


v0.2.5 (October 26, 2020)
=========================
  * ENH: Use joblib.Parallel instead of custom groupyr._ProgressParallel (#56)


v0.2.4 (October 26, 2020)
=========================
  * ENH: Add functions and test for outer cross-validation loop (#55)


v0.2.3 (October 22, 2020)
=========================
  * FIX: Use target transformer only if requested by user (#54)


v0.2.2 (October 15, 2020)
=========================
  * ENH: Bump groupyr version (#53)
  * ENH: Use sklearn LabelEncoder in load_afq_data and return classes (#52)
  * ENH: Increase flexibility of load_afq_data (#51)


v0.2.1 (October 14, 2020)
=========================

* Major refactoring after moving the sparse group lasso estimator functions into a new library (groupyr) and retaining only AFQ specific dataset transformers and pipelines in AFQ-Insight


v0.2.0 (October 14, 2020)
=========================

* Major refactoring after moving the sparse group lasso estimator functions into a new library (groupyr) and retaining only AFQ specific dataset transformers and pipelines in AFQ-Insight
