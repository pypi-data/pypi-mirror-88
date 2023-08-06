from xgboost.compat import *
from xgboost.core import Booster, DMatrix, XGBoostError
from xgboost.training import train
from xgboost.sklearn import XGBModel
class XGBC(XGBModel, XGBClassifierBase):
    # pylint: disable=missing-docstring,invalid-name,too-many-instance-attributes
    def __init__(self, objective="binary:logistic", **kwargs):
        super().__init__(objective=objective, **kwargs)

    def fit(self, X, y, sample_weight=None, base_margin=None,
            eval_set=None, eval_metric=None,
            early_stopping_rounds=None, verbose=True, xgb_model=None,
            sample_weight_eval_set=None, callbacks=None):
        # pylint: disable = attribute-defined-outside-init,arguments-differ

        evals_result = {}
        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)

        xgb_options = self.get_xgb_params()

        if callable(self.objective):
            obj = _objective_decorator(self.objective)
            # Use default value. Is it really not used ?
            xgb_options["objective"] = "binary:logistic"
        else:
            obj = None

        if self.n_classes_ > 2:
            # Switch to using a multiclass objective in the underlying
            # XGB instance
            xgb_options['objective'] = 'multi:softprob'
            xgb_options['num_class'] = self.n_classes_

        feval = eval_metric if callable(eval_metric) else None
        if eval_metric is not None:
            if callable(eval_metric):
                eval_metric = None
            else:
                xgb_options.update({"eval_metric": eval_metric})

        self._le = XGBoostLabelEncoder().fit(y)
        training_labels = self._le.transform(y)

        if eval_set is not None:
            if sample_weight_eval_set is None:
                sample_weight_eval_set = [None] * len(eval_set)
            else:
                assert len(sample_weight_eval_set) == len(eval_set)
            evals = list(
                DMatrix(eval_set[i][0],
                        label=self._le.transform(eval_set[i][1]),
                        missing=self.missing, weight=sample_weight_eval_set[i],
                        nthread=self.n_jobs)
                for i in range(len(eval_set))
            )
            nevals = len(evals)
            eval_names = ["validation_{}".format(i) for i in range(nevals)]
            evals = list(zip(evals, eval_names))
        else:
            evals = ()

        if len(X.shape) != 2:
            # Simply raise an error here since there might be many
            # different ways of reshaping
            raise ValueError(
                'Please reshape the input data X into 2-dimensional matrix.')
        self._features_count = X.shape[1]
        train_dmatrix = DMatrix(X, label=training_labels, weight=sample_weight,
                                base_margin=base_margin,
                                missing=self.missing, nthread=self.n_jobs)

        self._Booster = train(xgb_options, train_dmatrix,
                              self.get_num_boosting_rounds(),
                              evals=evals,
                              early_stopping_rounds=early_stopping_rounds,
                              evals_result=evals_result, obj=obj, feval=feval,
                              verbose_eval=verbose, xgb_model=xgb_model,
                              callbacks=callbacks)

        self.objective = xgb_options["objective"]
        if evals_result:
            for val in evals_result.items():
                evals_result_key = list(val[1].keys())[0]
                evals_result[val[0]][
                    evals_result_key] = val[1][evals_result_key]
            self.evals_result_ = evals_result

        if early_stopping_rounds is not None:
            self.best_score = self._Booster.best_score
            self.best_iteration = self._Booster.best_iteration
            self.best_ntree_limit = self._Booster.best_ntree_limit

        return self

    fit.__doc__ = XGBModel.fit.__doc__.replace(
        'Fit gradient boosting model',
        'Fit gradient boosting classifier', 1)

    def predict(self, data, output_margin=False, ntree_limit=None,
                validate_features=True, base_margin=None, prob_threshold=0.5):
        """
        Predict with `data`.

        .. note:: This function is not thread safe.

          For each booster object, predict can only be called from one thread.
          If you want to run prediction using multiple thread, call
          ``xgb.copy()`` to make copies of model object and then call
          ``predict()``.

          .. code-block:: python

            preds = bst.predict(dtest, ntree_limit=num_round)

        Parameters
        ----------
        data : array_like
            The dmatrix storing the input.
        output_margin : bool
            Whether to output the raw untransformed margin value.
        ntree_limit : int
            Limit number of trees in the prediction; defaults to
            best_ntree_limit if defined (i.e. it has been trained with early
            stopping), otherwise 0 (use all trees).
        validate_features : bool
            When this is True, validate that the Booster's and data's
            feature_names are identical.  Otherwise, it is assumed that the
            feature_names are the same.

        Returns
        -------
        prediction : numpy array
        """
        test_dmatrix = DMatrix(data, base_margin=base_margin,
                               missing=self.missing, nthread=self.n_jobs)
        if ntree_limit is None:
            ntree_limit = getattr(self, "best_ntree_limit", 0)
        class_probs = self.get_booster().predict(
            test_dmatrix,
            output_margin=output_margin,
            ntree_limit=ntree_limit,
            validate_features=validate_features)
        if output_margin:
            # If output_margin is active, simply return the scores
            return class_probs

        if len(class_probs.shape) > 1:
            column_indexes = np.argmax(class_probs, axis=1)
        else:
            column_indexes = np.repeat(0, class_probs.shape[0])
            column_indexes[class_probs > prob_threshold] = 1

        if hasattr(self, '_le'):
            return self._le.inverse_transform(column_indexes)
        warnings.warn(
            'Label encoder is not defined.  Returning class probability.')
        return class_probs

    def predict_proba(self, data, ntree_limit=None, validate_features=True,
                      base_margin=None):
        """
        Predict the probability of each `data` example being of a given class.

        .. note:: This function is not thread safe

            For each booster object, predict can only be called from one
            thread.  If you want to run prediction using multiple thread, call
            ``xgb.copy()`` to make copies of model object and then call predict

        Parameters
        ----------
        data : DMatrix
            The dmatrix storing the input.
        ntree_limit : int
            Limit number of trees in the prediction; defaults to best_ntree_limit if defined
            (i.e. it has been trained with early stopping), otherwise 0 (use all trees).
        validate_features : bool
            When this is True, validate that the Booster's and data's feature_names are identical.
            Otherwise, it is assumed that the feature_names are the same.

        Returns
        -------
        prediction : numpy array
            a numpy array with the probability of each data example being of a given class.
        """
        test_dmatrix = DMatrix(data, base_margin=base_margin,
                               missing=self.missing, nthread=self.n_jobs)
        if ntree_limit is None:
            ntree_limit = getattr(self, "best_ntree_limit", 0)
        class_probs = self.get_booster().predict(test_dmatrix,
                                                 ntree_limit=ntree_limit,
                                                 validate_features=validate_features)
        if self.objective == "multi:softprob":
            return class_probs
        classone_probs = class_probs
        classzero_probs = 1.0 - classone_probs
        return np.vstack((classzero_probs, classone_probs)).transpose()

    def evals_result(self):
        """Return the evaluation results.

        If **eval_set** is passed to the `fit` function, you can call
        ``evals_result()`` to get evaluation results for all passed **eval_sets**.
        When **eval_metric** is also passed to the `fit` function, the
        **evals_result** will contain the **eval_metrics** passed to the `fit` function.

        Returns
        -------
        evals_result : dictionary

        Example
        -------

        .. code-block:: python

            param_dist = {'objective':'binary:logistic', 'n_estimators':2}

            clf = xgb.XGBClassifier(**param_dist)

            clf.fit(X_train, y_train,
                    eval_set=[(X_train, y_train), (X_test, y_test)],
                    eval_metric='logloss',
                    verbose=True)

            evals_result = clf.evals_result()

        The variable **evals_result** will contain

        .. code-block:: python

            {'validation_0': {'logloss': ['0.604835', '0.531479']},
            'validation_1': {'logloss': ['0.41965', '0.17686']}}
        """
        if self.evals_result_:
            evals_result = self.evals_result_
        else:
            raise XGBoostError('No results.')

        return evals_result