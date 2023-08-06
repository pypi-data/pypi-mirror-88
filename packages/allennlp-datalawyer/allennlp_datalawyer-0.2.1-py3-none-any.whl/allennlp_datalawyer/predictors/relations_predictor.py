from overrides import overrides

from sacremoses import MosesTokenizer

from allennlp.common.util import JsonDict
from allennlp.data import DatasetReader, Instance
from allennlp.models import Model
from allennlp.predictors.predictor import Predictor

from allennlp_datalawyer.data.dataset_readers.relations import Relation

@Predictor.register('relations_predictor')
class RelationsPredictor(Predictor):
    """
        Predictor for any model that takes in a sentence and returns
        a single set of tags for it.  In particular, it can be used with
        the [`CrfTagger`](https://docs.allennlp.org/models/master/models/tagging/models/crf_tagger/)
        model and also the [`SimpleTagger`](../models/simple_tagger.md) model.

        Registered as a `Predictor` with name "sentence_tagger".
        """

    def __init__(
            self,
            model: Model,
            dataset_reader: DatasetReader
    ) -> None:
        super().__init__(model, dataset_reader)
        self._tokenizer = MosesTokenizer()

    @overrides
    def _json_to_instance(self, json_dict: JsonDict) -> Instance:
        """
        Expects JSON that looks like `{"sentence": "..."}`.
        Runs the underlying model, and adds the `"words"` to the output.
        """
        sentence = json_dict["sentence"]
        tokens = self._tokenizer.tokenize(sentence)
        return self._dataset_reader.text_to_instance(tokens)
