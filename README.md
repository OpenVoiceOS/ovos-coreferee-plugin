# ovos-coreferee-plugin

OVOS plugin for coreference resolution and semantic triple extraction. It rewrites text so pronouns point to their referents. For example, it turns "call Mom. tell her to buy eggs" into "call Mom. tell Mom to buy eggs". This helps intent parsers and knowledge-graph builders that read the resolved text. The plugin also extracts subject-verb-object triples from text.

The plugin uses [spaCy](https://spacy.io) and the [coreferee](https://github.com/msg-systems/coreferee) pipeline component.

## Install

```bash
pip install ovos-coreferee-plugin
```

The plugin downloads the spaCy model `en_core_web_trf` on first use. This model needs `en_core_web_lg` as a companion. Both models download automatically.

## Usage

### Coreference resolution

`CorefereeParser` loads the spaCy model, adds the `coreferee` pipe, and replaces pronouns with their referents.

```python
from ovos_coreferee.parser import CorefereeParser

coref = CorefereeParser(first_person_token="Miro")
text = "My name is Miro. I like beer"
print(coref.replace_corefs(text))
# Miro's name is Miro. Miro likes beer
```

`replace_corefs` walks the parsed text twice. First, it applies rules for first-person pronouns (`I`, `me`, `my`, `mine`), `who`, and plural `we`. It maps these to the `first_person_token` set at init time (the speaker identity). Then it reads the coreference chains from `coreferee` and picks the longest proper-noun (or noun) mention in each chain as the replacement for every other mention in that chain. It joins plural chains with "and".

More examples:

```
Barrack Obama was born in Hawaii. He was president of the United States and lived in the White House.
     Barrack Obama was born in Hawaii. Obama was president of the United States and lived in the White House.

London has been a major settlement for two millennia. It was founded by the Romans, who named it Londinium.
     London has been a major settlement for two millennia. settlement was founded by the Romans, Romans named settlement Londinium.

I have a dog, a cat and a bird. we are a happy family
     Miro has a dog, a cat and a bird. Miro, dog, cat and bird are a happy family

call Mom. tell her to buy eggs. tell her to buy coffee. tell her to buy milk
     call Mom. tell Mom to buy eggs. tell Mom to buy coffee. tell Mom to buy milk
```

### Semantic triple extraction

`SpacyTriplesExtractor` extracts subject-verb-object triples from text, for knowledge-graph construction. It can run coreference resolution first (`solve_coref=True`, the default), so pronouns resolve to their referents before extraction.

```python
from ovos_coreferee.triples import SpacyTriplesExtractor

extractor = SpacyTriplesExtractor({"first_person_token": "Miro"})
triples = extractor.extract_triples(["Barrack Obama was born in Hawaii."])
```

### OVOS plugin entry points

The package registers plugin classes under these entry points (see `setup.py`):

- `intentbox.coreference` -> `CorefereeSolver`, an `ovos-plugin-manager` `CoreferenceSolverEngine`
- `opm.triples` -> `SpacyTriplesExtractor`, an `ovos-plugin-manager` `TriplesExtractor`
- `neon.plugin.text` -> `CorefereeNormalizerPlugin`, an `UtteranceTransformer` that appends the coref-resolved variant of each utterance for intent parsers to consider

## Related projects

- [OpenVoiceOS/ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager) defines the `CoreferenceSolverEngine`, `UtteranceTransformer`, and `TriplesExtractor` templates this plugin implements.
- [msg-systems/coreferee](https://github.com/msg-systems/coreferee) is the spaCy coreference resolution component this plugin builds on.

## License

Apache-2.0
