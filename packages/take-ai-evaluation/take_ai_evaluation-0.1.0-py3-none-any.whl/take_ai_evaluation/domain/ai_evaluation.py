__author__ = 'Cecilia Assis and Milo Utsch'
__version__ = '0.1.0'

import typing as tp

import pandas as pd
import matplotlib

from take_ai_evaluation.logic import KnowledgeBase, validate_dataframe, validate_parameters, validate_parameter
from take_ai_evaluation.persistence import read_dataframe
from take_ai_evaluation.presentation import plot_confusion_matrix, plot_text

DF = pd.DataFrame
StrOrDataframe = tp.Union[str, DF]
AX = matplotlib.axes.Axes
TupleOrAX = tp.Union[tp.Tuple, AX]


class AiEvaluation:
    """AiEvaluation

    Wraps methods for calling and using the package's visualizations.

    Attributes
    ----------
    intent_col : str
        Column containing the original intents in your knowledge base.
    predict_col: str
        Column containing the original intents in your knowledge base.
    analysed_base: pandas.DataFrame
        Dataframe object containing the knowledge base.
    knowledge_base: KnowledgeBase
        Object that wraps methods for calculating insights regarding the quality of the Knowledge Base.

    Methods
    -------
    get_all_vs_all_confusion_matrix(title, normalize=False)
        Provides the ALL vs ALL confusion matrix.
    get_one_vs_all_confusion_matrix(title, normalize=False)
        Provides the ONE vs ALL confusion matrix.
    get_best_intent(metric='accuracy', as_graph=False)
        Provides best intent based on a metric.
    get_worst_intent(metric='accuracy', as_graph=False)
        Provides worst intent based on a metric.

    Raises
    ------
    Exception
        If the after read `analysed_base` dataframe is empty.
    AttributeError
        If any of the expected columns is not present inside the knowledge base dataframe.
    """

    def __init__(self,
                 analysed_base: StrOrDataframe,
                 sentence_col: str,
                 intent_col: str,
                 predict_col: str,
                 analysed_base_sep: str = '|') -> None:
        """
        Parameters
        ----------
        analysed_base : str | pandas.DataFrame
            Dataframe object, can be a file to be read.
        sentence_col : str
            Column containing the original sentence in your knowledge base.
        intent_col : str
            Column containing the original intents in your knowledge base.
        predict_col : str
            Column containing the predicted intents in your knowledge base.
        analysed_base_sep : str, optional
            CSV separator (default is "|").
        """
        self.__validate_params(analysed_base=analysed_base,
                               sentence_col=sentence_col,
                               intent_col=intent_col,
                               predict_col=predict_col)

        self.intent_col = intent_col
        self.predict_col = predict_col

        self.__init_analysed_base(analysed_base=analysed_base,
                                  analysed_base_sep=analysed_base_sep,
                                  sentence_col=sentence_col)
        self.__init_knowledge_base()

    def __validate_params(self, analysed_base, sentence_col, intent_col, predict_col):
        """
        Validates parameters' types and values.

        Parameters
        ----------
        analysed_base : str | pandas.DataFrame
            Dataframe object, can be a file to be read.
        sentence_col : str
            Column containing the original sentence in your knowledge base.
        intent_col : str
            Column containing the original intents in your knowledge base.
        predict_col : str
            Column containing the predicted intents in your knowledge base.

        Raises
        ------
        TypeError
            If the parameter's type does not match the desired type.
        ValueError
            If the parameter is empty.
        """
        params = {'sentence_col': sentence_col,
                  'intent_col': intent_col,
                  'predict_col': predict_col}

        validate_parameter(param=analysed_base, param_name='analysed_base', target_type=(str, DF))
        validate_parameters(params=params.keys(), params_names=params.values(), target_type=str)

    def __init_analysed_base(self, analysed_base, analysed_base_sep: str, sentence_col: str):
        """
        Reads knowledge base's file dataframe.

        Parameters
        ----------
        analysed_base
            Dataframe object, can be a file to be read.
        analysed_base_sep : str, optional
            CSV separator (default is "|").
        sentence_col : str
            Column containing the original sentence in your knowledge base.
        """
        analysed_base = read_dataframe(analysed_base, analysed_base_sep)

        columns = [sentence_col, self.intent_col, self.predict_col]
        validate_dataframe(analysed_base, columns)

        self.analysed_base = analysed_base

    def __init_knowledge_base(self):
        """Initializes the knowledge base object after reading it's files.
        """
        self.knowledge_base = KnowledgeBase(analysed_base=self.analysed_base,
                                            intent_col=self.intent_col,
                                            predict_col=self.predict_col)

    def get_all_vs_all_confusion_matrix(self, title: str, normalize: bool = False) -> AX:
        """
        Provides the ALL vs ALL confusion matrix for a knowledge base.

        Parameters
        ----------
        title : str
            Wanted title for the output graph.
        normalize : bool, optional
            If True, return output normalized using L1 normalization (default is false).

        Returns
        -------
        matrix : matplotlib Axes
            Axes object with the confusion matrix.
        """
        return plot_confusion_matrix(confusion_matrix=self.knowledge_base.all_vs_all_confusion_matrix,
                                     title=title,
                                     xlabel='True label',
                                     ylabel='Predicted label',
                                     normalize=normalize)

    def get_one_vs_all_confusion_matrix(self, intent: str, title: str, normalize: bool = False) -> AX:
        """
        Provides the ONE vs ALL confusion matrix for a knowledge base and a given intent.

        Parameters
        ----------
        intent : str
            Label of the intent to be retrieved.
        title : str
            Wanted title for the output graph.
        normalize : bool, optional
            If True, return output normalized using L1 normalization (default is false).

        Returns
        -------
        matrix : matplotlib Axes
            Axes object with the confusion matrix.
        """
        intent = self.knowledge_base.get_intent(intent=intent)

        return plot_confusion_matrix(confusion_matrix=intent.one_vs_all_confusion_matrix,
                                     title=title,
                                     normalize=normalize)

    def get_worst_intent(self, metric: str = 'accuracy', as_graph: bool = False) -> TupleOrAX:
        """Provides worst intent based on a metric.

        Parameters
        ----------
        metric : str, optional
            Metric to be evaluated against (default is accuracy).
            Can be either of "accuracy", "precision", "recall" or "f1".
        as_graph : bool, optional
            If True, shows the result as a graph, i.e. image (default is false).

        Returns
        -------
        intent : tuple or matplotlib Axes
            Worst intent's name and value.

        Raises
        ------
        KeyError
            If `metric` is any of the expected ones.
        """
        intent, value = self.knowledge_base.get_worst_intent(metric)

        if as_graph:
            text = f'Intent: {intent}\n{metric.capitalize()}: {value:.2f}'
            return plot_text(text, 'Worst intent')

        return intent, value

    def get_best_intent(self, metric: str = 'accuracy', as_graph: bool = False) -> TupleOrAX:
        """Provides best intent based on a metric.

        Parameters
        ----------
        metric : str, optional
            Metric to be evaluated against (default is accuracy).
            Can be either of "accuracy", "precision", "recall" or "f1".
        as_graph : bool, optional
            If True, shows the result as a graph, i.e. image (default is false).

        Returns
        -------
        intent : tuple or matplotlib Axes
            Best intent's name and value.

        Raises
        ------
        KeyError
            If `metric` is any of the expected ones.
        """
        intent, value = self.knowledge_base.get_best_intent(metric)

        if as_graph:
            text = f'Intent: {intent}\n{metric.capitalize()}: {value:.2f}'
            return plot_text(text, 'Best intent')

        return intent, value
