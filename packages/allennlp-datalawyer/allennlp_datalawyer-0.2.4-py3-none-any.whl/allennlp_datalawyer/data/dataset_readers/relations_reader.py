import logging
import json
import random

from tqdm import tqdm
from itertools import combinations
from typing import Dict, List, Iterator, Any

from allennlp.common.file_utils import cached_path
from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.data.fields import TextField, SpanField, MetadataField, LabelField
from allennlp.data.instance import Instance
from allennlp.data.token_indexers import PretrainedTransformerIndexer
from allennlp.data.tokenizers import Token, PretrainedTransformerTokenizer

from allennlp_datalawyer.data.dataset_readers.relations import SingleToken, Sentence, Entity, Relation

logger = logging.getLogger(__name__)


@DatasetReader.register("relations_reader")
class RelationsDatasetReader(DatasetReader):

    def __init__(self,
                 max_negative_samples: int = 0,
                 transformer_model_name: str = "neuralmind/bert-base-portuguese-cased",
                 tokenizer_kwargs: Dict[str, Any] = None,
                 **kwargs) -> None:
        super().__init__(**kwargs)

        self.no_relation_label = 'NO_RELATION'
        self.max_negative_samples = max_negative_samples
        self._tokenizer = PretrainedTransformerTokenizer(
            model_name=transformer_model_name,
            tokenizer_kwargs=tokenizer_kwargs,
        )
        self._token_indexers = {
            "tokens": PretrainedTransformerIndexer(
                transformer_model_name, tokenizer_kwargs=tokenizer_kwargs
            )
        }

    def _read(self, file_path: str) -> Iterator[Instance]:

        file_path = cached_path(file_path)

        def get_relation_for_entities_pair(entity_1: Entity, entity_2: Entity, relations: List[Relation]) -> Relation:
            for _relation in relations:
                if _relation.matches_entities(entity_1, entity_2):
                    return _relation
            return None

        sentences = json.load(open(file_path, mode='r', encoding='utf-8'))
        for json_sentence in tqdm(sentences, desc="Parsing dataset '%s'" % file_path):
            if json_sentence:
                sentence = self._parse_sentence(json_sentence)
                context = [token.phrase for token in sentence.tokens]

                if self.max_negative_samples > 0 and all(
                        [suffix not in file_path for suffix in ['_dev.', '_test.', '_val.', '_valid.']]):

                    negative_tuples = [(entity_1, entity_2) for entity_1, entity_2 in combinations(sentence.entities, 2)
                                       if
                                       get_relation_for_entities_pair(entity_1, entity_2, sentence.relations) is None]
                    negative_tuples = random.sample(negative_tuples,
                                                    min(len(negative_tuples), self.max_negative_samples))

                    for idx, (entity_1, entity_2) in enumerate(negative_tuples):
                        sentence.relations.append(
                            Relation(rid=idx + len(sentence.relations),
                                     sentence_id=sentence.sentence_id,
                                     relation_type=self.no_relation_label,
                                     head_entity=entity_1, tail_entity=entity_2))

                for relation in sentence.relations:
                    yield self.text_to_instance(context=context, relation=relation)

    def _parse_sentence(self, sentence_json):
        sentence_id = sentence_json['orig_id']
        tokens_json = sentence_json['tokens']
        relations_json = sentence_json['relations']
        entities_json = sentence_json['entities']

        # parse tokens
        sentence_tokens, sentence_encoding = self._parse_tokens(tokens_json, sentence_id)

        # parse entity mentions
        entities = self._parse_entities(entities_json, sentence_tokens, sentence_id)

        # parse relations
        relations = self._parse_relations(relations_json, entities, sentence_id)

        return Sentence(sentence_id=sentence_id, tokens=sentence_tokens, entities=entities,
                        relations=relations, encoding=sentence_encoding)

    def _parse_tokens(self, tokens_json: List[str], sentence_id):
        sentence_tokens = []

        sentence_encoding = [self._tokenizer.tokenizer.convert_tokens_to_ids('[CLS]')]

        # parse tokens
        for token_idx, token_phrase in enumerate(tokens_json):
            token_encoding = self._tokenizer.tokenizer.encode(token_phrase, add_special_tokens=False)
            span_start, span_end = (len(sentence_encoding), len(sentence_encoding) + len(token_encoding))

            token = SingleToken(tid=token_idx, sentence_id=sentence_id, index=token_idx,
                                span_start=span_start, span_end=span_end, phrase=token_phrase)

            sentence_tokens.append(token)
            sentence_encoding += token_encoding

        sentence_encoding += [self._tokenizer.tokenizer.convert_tokens_to_ids('[SEP]')]

        return sentence_tokens, sentence_encoding

    @staticmethod
    def _parse_entities(entities_json: List[dict], sentence_tokens: List[SingleToken], sentence_id: str) -> \
            List[Entity]:
        entities = []

        for entity_idx, entity_json in enumerate(entities_json):
            entity_type = entity_json['type']
            start, end = entity_json['start'], entity_json['end']

            # create entity mention
            tokens = sentence_tokens[start:end]
            phrase = " ".join([t.phrase for t in tokens])
            entity = Entity(eid=entity_idx, sentence_id=sentence_id,
                            entity_type=entity_type, tokens=tokens, phrase=phrase)
            entities.append(entity)

        return entities

    @staticmethod
    def _parse_relations(relations_json: List[dict], entities: List[Entity], sentence_id: str) -> List[Relation]:
        relations = []

        for relation_idx, relation_json in enumerate(relations_json):
            relation_type = relation_json['type'] if 'type' in relation_json else None

            head_idx = relation_json['head']
            tail_idx = relation_json['tail']

            # create relation
            head = entities[head_idx]
            tail = entities[tail_idx]

            reverse = int(tail.tokens[0].index) < int(head.tokens[0].index)

            relation = Relation(rid=relation_idx, sentence_id=sentence_id, relation_type=relation_type,
                                head_entity=head, tail_entity=tail, reverse=reverse)
            relations.append(relation)

        return relations

    def text_to_instance(self,
                         context: List[str],
                         relation: Relation,
                         tokenized_context: List[Token] = None) -> Instance:
        fields = dict()

        if tokenized_context is None:
            tokenized_context = self._tokenizer.tokenize(' '.join(context))

        context_field = TextField(tokens=tokenized_context, token_indexers=self._token_indexers)
        fields["context"] = context_field

        fields["head"] = SpanField(span_start=relation.head_entity.span_start,
                                   span_end=relation.head_entity.span_end,
                                   sequence_field=context_field)
        fields["head_entity"] = LabelField(label=relation.head_entity.entity_type,
                                           label_namespace="entities_labels")

        fields["tail"] = SpanField(span_start=relation.tail_entity.span_start,
                                   span_end=relation.tail_entity.span_end,
                                   sequence_field=context_field)
        fields["tail_entity"] = LabelField(label=relation.tail_entity.entity_type,
                                           label_namespace="entities_labels")

        if relation.relation_type is not None:
            fields["relation_label"] = LabelField(label=relation.relation_type)

        # make the metadata
        fields["metadata"] = MetadataField(metadata={
            "relation": relation,
            "context": context,
            "context_tokens": tokenized_context
        })

        # fields["tokens"] = context_field
        #
        # fields["label"] = LabelField(label=relation.relation_type)

        return Instance(fields)
