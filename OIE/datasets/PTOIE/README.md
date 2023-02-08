# Squadie (pt-br)
A library to generate OpenIE tuples in pt-br from a QA dataset (SQuAD) through spacy dependency analysis and a set of handcrafted algorithms.

## Why?

As in other areas of NLP, we expect neural networks to improve over the state-of-the-art rule-based systems in OpenIE. However, the extraction of neural open information was hampered by the lack of training data, especially in data that differs from the English language.

Large QA datasets such as SQuAD are available and contain *almost* the correct schema for an extract. An extensive set of rules (based on dependency analysis) can successfully convert QA pairs into OpenIE tuples. This is an easier problem than OpenIE itself because the answer is guaranteed to be an element in the tuple. The remaining problem is:
* (1) extract the other two elements
* (2) determine what the subject/relation/object is.

## Examples

```
A CBS transmitiu o Super Bowl 50 nos EUA e cobrou uma média de US $ 5 milhões por um comercial de 30 segundos durante o jogo.
<Cbs  |||   transmitiu  |||  o Super Bowl 50>

Nenhum plano foi anunciado sobre o reconhecimento de Harvey Martin, co-MVP do Super Bowl XII, que morreu em 2001.
<Harvey martin  |||   morreu  |||  em 2001>

Varsóvia (polonês: Warszawa [varˈʂava] (ouça); veja também outros nomes) é a capital e a maior cidade da Polônia.
<A maior cidade da polônia  |||   é  |||  Varsóvia>

No início de 2012, o comissário da NFL Roger Goodell afirmou que a liga planejava tornar o 50º Super Bowl "espetacular" e que seria "um jogo importante para nós como liga".
Goodell  |||   foi o comissário  |||  da NFL no início de 2012

Os Panteras terminaram a temporada regular com um recorde de 15 a 1, e o quarterback Cam Newton foi nomeado o Jogador Mais Valioso da NFL (MVP).
<Cam newton  |||   nomeado  |||  Jogador Mais Valioso>

O comitê anfitrião já levantou mais de US $ 40 milhões por meio de patrocinadores, incluindo Apple, Google, Yahoo !, Intel, Gap, Chevron e Dignity Health.
<O comitê  |||   levantou  |||  o dinheiro por meio de patrocinadores>
```

The parse algorithms cannot handle every type of question. In most cases when this happens parse() will return None. However, in some cases, malformed tuples may be returned.


## Overview

The main library is in vis.py in src. This file contains the algorithms that takes a QA pair and creates a logical 3-tuple. 

## Dependencies 

* spacy
* python 3
* nltk

