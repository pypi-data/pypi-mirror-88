from typing import Dict, Optional, List, Any

from allennlp.data import Vocabulary
from allennlp.models.model import Model
from allennlp.modules import TextFieldEmbedder

import torch
from torch import nn as nn


def get_token(h: torch.tensor, x: torch.tensor, token: int):
    """ Get specific token embedding (e.g. [CLS]) """
    emb_size = h.shape[-1]

    token_h = h.view(-1, emb_size)
    flat = x.contiguous().view(-1)

    # get contextualized embedding of given token
    token_h = token_h[flat == token, :]

    return token_h


def batch_index(tensor, index):
    if tensor.shape[0] != index.shape[0]:
        raise Exception('tensor and index shapes are not the same: %s and %s' % (tensor.shape[0], index.shape[0]))

    return torch.stack([tensor[i][index[i]] for i in range(index.shape[0])])


def get_entities_features(embedded_text, entity_masks):
    """
    O shape do embedded_text é: [batch_size, sequence_length, embeddings_size]
    O shape do entity_masks é: [batch_size, 2, sequence_length], sendo o 2 correspondente a uma máscara para cada span
    de entidade que forma a relação.
    Este método faz o unsqueeze criando uma última dimensão para as máscaras. Este unsqueeze transforma cada vetor de
    tamanho sequence_length em sequence_length vetores de tamanho 1, que são booleanos. Em seguida, onde aos vetores que
    possuem valores falsos (posições de tokens que não fazem parte do span de alguma entidade) são atribuídos valores
    extremamente negativos.
    Em seguida, cada um dos embeddings do embedded_text é replicado para cada span das entidades, de forma que é criado
    um vetor de shape [batch_size, 2, sequence_length, embeddings_size].
    Este vetor de valores extremamente negativos a partir das máscaras é somado ao tensor redimensionado.
    O retorno é feito a partir de um max pooling dos embeddings de cada token da sequência pra cada span. Então, para
    cada sentença do batch, para cada span da sentença, agrega-se o valor máximo para cada token do span, retornando
    um tensor de shape [batch_size, 2, embeddings_size], sendo este embedding o resultado desta agregação.
    """
    # max pool entity candidate spans
    m = (entity_masks.unsqueeze(-1) == 0).float() * (-1e30)
    entity_spans_pool = m + embedded_text.unsqueeze(1).repeat(1, entity_masks.shape[1], 1, 1)
    return entity_spans_pool.max(dim=2)[0]


class SpERTRelationClassifier(Model):
    """ Span-based model to extract relations """

    VERSION = '1.1'

    def __init__(self,
                 vocab: Vocabulary,
                 embedder: TextFieldEmbedder,
                 relation_types: int,
                 entity_types: int,
                 dropout: Optional[float] = None,
                 max_pairs: int = 100):
        super().__init__(vocab)

        self._embedder = embedder
        # layers
        self.rel_classifier = nn.Linear(embedder.token_embedder_tokens.config.hidden_size * 3, relation_types)
        self.dropout = nn.Dropout(dropout)

        self._relation_types = relation_types
        self._entity_types = entity_types
        self._max_pairs = max_pairs

    def forward(self,
                context: Dict[str, Dict[str, torch.LongTensor]],
                embedded_context: torch.tensor,
                entities_masks: torch.tensor,
                relations_masks: torch.tensor):
        # get contextualized token embeddings from last transformer layer
        # batch_size = entities_masks.shape[0]

        # classify entities
        entity_spans_pool = get_entities_features(embedded_context, entities_masks)

        # classify relations
        h_large = embedded_context.unsqueeze(1).repeat(1, relations_masks.shape[1], 1, 1)

        # obtain relation logits
        # classify relation candidates
        rel_clf_logits = self._classify_relations(entity_spans_pool, relations_masks, h_large)

        return rel_clf_logits

    def _classify_relations(self, entity_spans, relations_masks, h):
        """
        O shape de entity_spans é [batch_size, 2, embeddings_size], sendo o 2 correspondente a um embedding para cada
        span de entidade que forma a relação.
        O shape de relations_masks é [batch_size, 1, sequence_length]
        O shape de h é [batch_size, 1, sequence_length, embeddings_size], sendo o 1 correspondente a uma representação
        para a relação.
        Primeiro, este método reorganiza o entity_spans para produzir uma representação de shape [batch_size, 1,
        embeddings_size * 2], colocando em um vetor só as representações de cada span.
        Em seguida, faz-se o unsqueeze criando uma última dimensão para as máscaras. Este unsqueeze transforma cada
        vetor de tamanho sequence_length em sequence_length vetores de tamanho 1, que são booleanos. Em seguida, onde
        aos vetores que possuem valores falsos (posições de tokens que não fazem parte do span de alguma entidade) são
        atribuídos valores extremamente negativos.
        Este vetor de valores extremamente negativos a partir das máscaras é somado ao tensor h, criando uma nova
        representação reforçada a partir da máscara.
        Nesta nova representação é feito um max pooling dos embeddings de cada token da sequência da relação. Então,
        para cada sentença do batch, para a relação em questão da sentença, agrega-se o valor máximo para cada token dos
        spans, resultando em um tensor de shape [batch_size, 1, embeddings_size], sendo este embedding o resultado desta
        agregação.
        Em seguida, é feita uma concatenação entre as representações por pares de entidades (entity_pairs) e as
        relações, resultando em um embedding de shape [batch_size, 1, embeddings_size * 3], no qual é aplicado dropout.
        Esta última representação é aplicada em um classificador e os logits são retornados.
        """
        batch_size = relations_masks.shape[0]
        # get pairs of entity candidate representations
        entity_pairs = entity_spans.view(batch_size, relations_masks.shape[1], -1)

        # relation context (context between entity candidate pair)
        # mask non entity candidate tokens
        m = ((relations_masks == 0).float() * (-1e30)).unsqueeze(-1)
        rel_ctx = m + h
        # max pooling
        rel_ctx = rel_ctx.max(dim=2)[0]
        # set the context vector of neighboring or adjacent entity candidates to zero
        # Zera os embeddings de qualquer relação que não tenha nenhum span, de acordo com a máscara
        rel_ctx[relations_masks.to(torch.uint8).any(-1) == 0] = 0

        # create relation candidate representations including context, max pooled entity candidate pairs
        # and corresponding size embeddings
        rel_repr = torch.cat([rel_ctx, entity_pairs], dim=2)
        rel_repr = self.dropout(rel_repr)

        # classify relation candidates
        chunk_rel_logits = self.rel_classifier(rel_repr)
        return chunk_rel_logits
