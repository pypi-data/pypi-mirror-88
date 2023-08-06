from abc import ABC
from typing import List, Union

import numpy as np
import pandas as pd

from baseten.common.core import (ExplainerInvalidConfigrationError,
                                 ExplainerNotSupportedError)

FRAMEWORK_TO_SHAP_TREE_MODELS_MAP = {
    'sklearn': {
        'RandomForestRegressor',
        'IsolationForest',
        'ExtraTreesRegressor',
        'DecisionTreeRegressor',
        'DecisionTreeClassifier',
        'RandomForestClassifier',
        'ExtraTreesClassifier',
        'GradientBoostingRegressor',
        'MeanEstimator',
        'QuantileEstimator',
        'DummyRegressor',
        'GradientBoostingClassifier',
        'LogOddsEstimator',
        'DummyClassifier'
    }
}

FRAMEWORK_TO_SHAP_LINEAR_MODELS_MAP = {
    'sklearn': {
        'LinearRegression',
        'Ridge',
        'RidgeClassifier',
        'RidgeCV',
        'Lasso',
        'MultiTaskLasso',
        'ElasticNet',
        'ElasticNetCV',
        'MultiTaskElasticNet',
        'LassoLars',
        'OrthogonalMatchingPursuit',
        'OrthogonalMatchingPursuitCV',
        'BayesianRidge',
        'ARDRegression',
        'LogisticRegression',
        'SGDClassifier',
        'SGDRegressor',
        'Perceptron',
        'PassiveAggressiveClassifier',
        'PassiveAggressiveRegressor',
        'TheilSenRegressor',
        'RANSACRegressor',
        'HuberRegressor',
    }
}

BLACKBOX_FRAMEWORKS_MODELS_MAP = {
    'sklearn': {
        'RandomForestRegressor',
        'IsolationForest',
        'ExtraTreesRegressor',
        'DecisionTreeRegressor',
        'DecisionTreeClassifier',
        'RandomForestClassifier',
        'ExtraTreesClassifier',
        'GradientBoostingRegressor',
        'MeanEstimator',
        'QuantileEstimator',
        'DummyRegressor',
        'GradientBoostingClassifier',
        'LogOddsEstimator',
        'DummyClassifier',
        'LinearRegression',
        'Ridge',
        'RidgeClassifier',
        'RidgeCV',
        'Lasso',
        'MultiTaskLasso',
        'ElasticNet',
        'ElasticNetCV',
        'MultiTaskElasticNet',
        'LassoLars',
        'OrthogonalMatchingPursuit',
        'OrthogonalMatchingPursuitCV',
        'BayesianRidge',
        'ARDRegression',
        'LogisticRegression',
        'SGDClassifier',
        'SGDRegressor',
        'Perceptron',
        'PassiveAggressiveClassifier',
        'PassiveAggressiveRegressor',
        'TheilSenRegressor',
        'RANSACRegressor',
        'HuberRegressor',
    }
}


class CustomFrameworkSupport:
    def __contains__(self, key):
        return True

    def get(self, key, *args):
        return self


CUSTOM_FRAMEWORKS_MODELS_MAP = CustomFrameworkSupport()


class BaseModelExplainer(ABC):
    name = 'BaseExplainer'
    requires_background_data = False
    requires_features_names = False


class TreeExplainer(BaseModelExplainer):
    name = 'ShapTreeExplainer'
    requires_background_data = False
    description = 'Uses Tree SHAP algorithms to explain the output of ensemble tree models.'
    framework_model_support = FRAMEWORK_TO_SHAP_TREE_MODELS_MAP


class LinearExplainer(BaseModelExplainer):
    name = 'ShapLinearExplainer'
    requires_background_data = True
    description = 'Computes SHAP values for a linear model.'
    framework_model_support = FRAMEWORK_TO_SHAP_LINEAR_MODELS_MAP


class KernelExplainer(BaseModelExplainer):
    name = 'ShapKernelExplainer'
    requires_background_data = True
    description = 'Uses the Kernel SHAP method to explain the output of any function.'
    framework_model_support = BLACKBOX_FRAMEWORKS_MODELS_MAP


class AnchorTabular(BaseModelExplainer):
    name = 'AlibiAnchorTabular'
    requires_background_data = True
    requires_features_names = True
    description = 'Uses the Alibi Anchor method to explain the output of tabular data.'
    framework_model_support = BLACKBOX_FRAMEWORKS_MODELS_MAP


class AnchorCounterFactual(BaseModelExplainer):
    name = 'AlibiCounterFactual'
    requires_background_data = False
    description = 'Uses the Alibi Anchor method to explain the output of tabular data.'
    framework_model_support = BLACKBOX_FRAMEWORKS_MODELS_MAP


class CustomExplainer(BaseModelExplainer):
    name = 'CustomExplainer'
    description = 'Uses the custom method to explain the output of a model.'
    framework_model_support = CUSTOM_FRAMEWORKS_MODELS_MAP


NAME_TO_EXPLAINER_MAP = {
    'BaseModelExplainer': BaseModelExplainer,
    'ShapTreeExplainer': TreeExplainer,
    'ShapLinearExplainer': LinearExplainer,
    'ShapKernelExplainer': KernelExplainer,
    'AlibiAnchorTabular': AnchorTabular,
    'AlibiCounterFactual': AnchorCounterFactual,
    'CustomExplainer': CustomExplainer,
}


def raises_invalid_explainer_configuration(
    explainer_name: str,
    model_framework: str,
    model_type: str,
    feature_data: Union[np.ndarray, pd.DataFrame, List] = None,
    feature_names=None,
    custom_explainer_file: str = None,
) -> None:
    if explainer_name not in NAME_TO_EXPLAINER_MAP:
        raise ExplainerNotSupportedError(f'Explainer: {explainer_name} is not known to BaseTen.')
    elif model_type not in NAME_TO_EXPLAINER_MAP[explainer_name].framework_model_support.get(model_framework, {}):
        raise ExplainerNotSupportedError(
            f'Explainer: {explainer_name} is not compatible for {model_framework}:{model_type}.')
    elif NAME_TO_EXPLAINER_MAP[explainer_name].requires_background_data and feature_data is None:
        raise ExplainerInvalidConfigrationError(
            f'Explainer: {explainer_name} requires background data for explanation.')
    elif NAME_TO_EXPLAINER_MAP[explainer_name].requires_features_names and feature_names is None:
        raise ExplainerInvalidConfigrationError(f'Explainer: {explainer_name} requires feature names for explanation.')
    elif explainer_name == 'CustomExplainer' and not custom_explainer_file:
        raise ExplainerInvalidConfigrationError(
            f'Explainer: {explainer_name} requires a file defining the CustomExplainer class object.'
        )
