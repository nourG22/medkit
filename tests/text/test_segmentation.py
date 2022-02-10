import pytest

from medkit.core.document import Collection
from medkit.core.text import TextDocument
from medkit.core.text.annotation import Entity
from medkit.core.text.span import Span
from medkit.text.segmentation import SentenceTokenizer


TEXT = (
    "Sentence testing the dot. We are testing the carriage return\rthis is the"
    " newline\n Test interrogation ? Now, testing semicolon;Exclamation! Several"
    " punctuation characters?!..."
)

TEST_CONFIG = [
    (
        SentenceTokenizer(input_label="RAW_TEXT"),
        [
            ("Sentence testing the dot", [Span(start=0, end=24)]),
            ("We are testing the carriage return", [Span(start=26, end=60)]),
            ("this is the newline", [Span(start=61, end=80)]),
            ("Test interrogation ", [Span(start=82, end=101)]),
            ("Now, testing semicolon", [Span(start=103, end=125)]),
            ("Exclamation", [Span(start=126, end=137)]),
            ("Several punctuation characters", [Span(start=139, end=169)]),
        ],
    ),
    (
        SentenceTokenizer(input_label="RAW_TEXT", keep_punct=True),
        [
            ("Sentence testing the dot.", [Span(start=0, end=25)]),
            ("We are testing the carriage return\r", [Span(start=26, end=61)]),
            ("this is the newline\n", [Span(start=61, end=81)]),
            ("Test interrogation ?", [Span(start=82, end=102)]),
            ("Now, testing semicolon;", [Span(start=103, end=126)]),
            ("Exclamation!", [Span(start=126, end=138)]),
            ("Several punctuation characters?!...", [Span(start=139, end=174)]),
        ],
    ),
]


@pytest.fixture
def collection():
    doc = TextDocument()
    raw_text = Entity(
        origin_id="", label="RAW_TEXT", spans=[Span(0, len(TEXT))], text=TEXT
    )
    doc.add_annotation(raw_text)
    return Collection([doc])


@pytest.mark.parametrize(
    "sentence_tokenizer,expected_sentences", TEST_CONFIG, ids=["default", "keep_punct"]
)
def test_annotate(collection, sentence_tokenizer, expected_sentences):
    assert sentence_tokenizer.input_label == "RAW_TEXT"
    sentence_tokenizer.annotate(collection)
    doc = collection.documents[0]
    assert isinstance(doc, TextDocument)
    sentences = [doc.get_annotation_by_id(ann) for ann in doc.entities.get("SENTENCE")]
    assert len(sentences) == 7
    for i, (text, spans) in enumerate(expected_sentences):
        assert sentences[i].text == text
        assert sentences[i].spans == spans
