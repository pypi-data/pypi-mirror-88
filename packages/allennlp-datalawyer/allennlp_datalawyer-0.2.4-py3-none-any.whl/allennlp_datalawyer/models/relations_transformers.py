from typing import Dict, Optional, List, Any

from overrides import overrides

import torch
from torch.nn.functional import softmax

import allennlp.nn.util as util

from allennlp.data import Vocabulary
from allennlp.modules import Seq2SeqEncoder, Seq2VecEncoder, TextFieldEmbedder
from allennlp.models.model import Model
from allennlp.nn.util import get_token_ids_from_text_field_tensors
from allennlp.training.metrics import CategoricalAccuracy, FBetaMeasure

from allennlp_datalawyer.models.spert import SpERTRelationClassifier


@Model.register('relations')
class RelationsModel(Model):

    def __init__(self,
                 vocab: Vocabulary,
                 embedder: TextFieldEmbedder,
                 seq2seq_encoder: Seq2SeqEncoder = None,
                 seq2vec_encoder: Seq2VecEncoder = None,
                 use_spert: bool = True,
                 mask_with_entities_spans: bool = True,
                 dropout: Optional[float] = None,
                 max_pairs: int = 100,
                 expanded_vocab_size: int = 1) -> None:
        super().__init__(vocab)

        self._embedder = embedder
        self._use_spert = use_spert
        self._mask_with_entities_spans = mask_with_entities_spans

        self.relations_size = vocab.get_vocab_size('labels')
        self.entities_size = vocab.get_vocab_size('entities_labels')

        if expanded_vocab_size > 0:
            default_vocab_size = self._embedder.token_embedder_tokens.config.vocab_size
            self._embedder.token_embedder_tokens.transformer_model.resize_token_embeddings(
                default_vocab_size + expanded_vocab_size)

        if use_spert:
            self._relations_classifier = SpERTRelationClassifier(vocab=vocab,
                                                                 embedder=self._embedder,
                                                                 relation_types=self.relations_size,
                                                                 entity_types=self.entities_size,
                                                                 dropout=dropout,
                                                                 max_pairs=max_pairs)
        else:
            self._seq2seq_encoder = seq2seq_encoder
            self._seq2vec_encoder = seq2vec_encoder
            seq2vec_output_dim = seq2vec_encoder.get_output_dim()
            encoding_size = seq2vec_output_dim * 2 if mask_with_entities_spans else seq2vec_output_dim
            self._classifier = torch.nn.Linear(in_features=encoding_size,
                                               out_features=self.relations_size)

        if dropout:
            self._dropout = torch.nn.Dropout(dropout)
        else:
            self._dropout = None

        self._loss = torch.nn.BCEWithLogitsLoss()

        labels = list(self.vocab.get_token_to_index_vocabulary('labels').values())[1:]

        self.metrics = {
            "accuracy": CategoricalAccuracy(),
            "fbeta-micro": FBetaMeasure(average='micro', labels=labels),
            "fbeta-weighted": FBetaMeasure(average='weighted', labels=labels)
        }

    def forward(  # type: ignore
            self,
            context: Dict[str, Dict[str, torch.LongTensor]],
            head: torch.IntTensor,
            head_entity: torch.LongTensor,
            tail: torch.IntTensor,
            tail_entity: torch.LongTensor,
            relation_label: torch.LongTensor = None,
            metadata: List[Dict[str, Any]] = None,
    ) -> Dict[str, torch.Tensor]:

        context_size = context['tokens']['mask'].shape[1]

        embedded_text_input = self._embedder(context)

        # if self._dropout:
        #     embedded_text_input = self._dropout(embedded_text_input)

        def create_entity_mask(start, end, context_size):
            mask = torch.zeros(context_size, dtype=torch.bool, device=head.device)
            mask[start:end] = 1
            return mask

        # Create a mask for the text to mask out tokens that are not entities.
        # shape: (batch_size, sequence_length)
        entities_masks = []
        relations_masks = torch.zeros_like(
            get_token_ids_from_text_field_tensors(context), dtype=torch.bool
        )
        for i, entity_mask in enumerate(relations_masks):
            entities_mask = []
            head_span = head[i]
            tail_span = tail[i]
            entity_mask[head_span[0]:head_span[1]] = 1
            entities_mask.append(create_entity_mask(head_span[0], head_span[1], context_size))
            entity_mask[tail_span[0]:tail_span[1]] = 1
            entities_mask.append(create_entity_mask(tail_span[0], tail_span[1], context_size))
            entities_masks.append(torch.stack(entities_mask))

        entities_masks = torch.stack(entities_masks)
        relations_masks = relations_masks.unsqueeze(1)

        if self._use_spert:

            logits = self._relations_classifier(context=context,
                                                embedded_context=embedded_text_input,
                                                entities_masks=entities_masks,
                                                relations_masks=relations_masks)

        else:

            mask = util.get_text_field_mask(context)

            embedded_text = self._seq2seq_encoder(embedded_text_input, mask)
            # if self._dropout:
            #     embedded_text = self._dropout(embedded_text)

            embedded_text = self._seq2vec_encoder(embedded_text, mask)
            # if self._dropout:
            #     embedded_text = self._dropout(embedded_text)

            if self._mask_with_entities_spans:
                entities_spans_mask = relations_masks.squeeze(1)
                entities_spans_mask[:, 0] = 1  # prevent pack empty tensors error

                encoded_entities_span = self._seq2seq_encoder(embedded_text_input, entities_spans_mask)
                # if self._dropout:
                #     encoded_entities_span = self._dropout(encoded_entities_span)

                encoded_entities_span = self._seq2vec_encoder(encoded_entities_span, entities_spans_mask)
                # if self._dropout:
                #     encoded_entities_span = self._dropout(encoded_entities_span)

                # encoded_text = encoded_text.unsqueeze(dim=-1)
                # encoded_entities_span = encoded_entities_span.unsqueeze(dim=-1)
                embedded_text = torch.cat([embedded_text, encoded_entities_span], dim=-1)
                # if self._dropout:
                #     embedded_text = self._dropout(embedded_text)

            if self._dropout:
                embedded_text = self._dropout(embedded_text)

            logits = self._classifier(embedded_text)
            logits = logits.unsqueeze(1)

        class_probabilities = softmax(logits, dim=-1)

        output_dict = {"logits": logits,
                       "probabilities": class_probabilities}

        if relation_label is not None:
            relation_labels = torch.zeros([relation_label.shape[0], self.relations_size], dtype=torch.float32,
                                          device=relation_label.device)
            relation_labels.scatter_(1, relation_label.unsqueeze(1), 1)
            # relation_labels = relation_labels[:, 1:]  # all zeros for 'none' relation
            relation_labels = relation_labels.unsqueeze(1)

            # loss = self._loss(logits, relation_label_onehot.long().view(-1))
            loss = self._loss(logits, relation_labels)
            output_dict["loss"] = loss
            self.metrics['accuracy'](logits.view(logits.shape[0], -1), relation_label)
            self.metrics['fbeta-micro'](class_probabilities.view(logits.shape[0], -1), relation_label)
            self.metrics['fbeta-weighted'](class_probabilities.view(logits.shape[0], -1), relation_label)

        return output_dict

    @overrides
    def get_metrics(self, reset: bool = False) -> Dict[str, float]:
        metrics_to_return = {'accuracy': self.metrics['accuracy'].get_metric(reset)}
        for metric in ['fbeta-micro', 'fbeta-weighted']:
            for name, value in self.metrics[metric].get_metric(reset).items():
                metrics_to_return[metric + '-' + name] = value
        return metrics_to_return

    @overrides
    def make_output_human_readable(
            self, output_dict: Dict[str, torch.Tensor]
    ) -> Dict[str, torch.Tensor]:
        """
        Does a simple argmax over the probabilities, converts index to string label, and
        add `"label"` key to the dictionary with the result.
        """
        predictions = output_dict["probabilities"]
        if predictions.dim() == 2:
            predictions_list = [predictions[i] for i in range(predictions.shape[0])]
        else:
            predictions_list = [predictions]
        classes = []
        for prediction in predictions_list:
            label_idx = prediction.argmax(dim=-1).item()
            label_str = self.vocab.get_index_to_token_vocabulary('labels').get(label_idx, str(label_idx))
            classes.append(label_str)
        output_dict["labels"] = classes
        return output_dict