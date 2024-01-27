import pytest

from src.swapper import get_languages, swap_header, swap_utterance


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ("@UTF8", "@UTF8"),
        ("@Window:	0_0_0_0_0_0_280_0_280_0", "@Window:	0_0_0_0_0_0_280_0_280_0"),
        ("@Begin", "@Begin"),
        ("@Languages:	spa, eng", "@Languages:	eng, spa\n"),
        (
            "@Participants: CHI Target_Child, MOT Mother",
            "@Participants: CHI Target_Child, MOT Mother"
        ),
        (
            "@ID:	spa, eng|bwl|CHI|||3bagstask||Target_Child|||",
            "@ID:	eng, spa|bwl|CHI|||3bagstask||Target_Child|||"
        ),
        (
            "@ID:	spa, eng|bwl|MOT|||3bagstask||Mother|||",
            "@ID:	eng, spa|bwl|MOT|||3bagstask||Mother|||"
        ),
        ("@Media:	test, video", "@Media:	test_eng, video\n"),
        ("@Transcriber:	test", "@Transcriber:	test"),
    ],
)
def test_swap_header(input: str, expected_output: str):
    result = swap_header(input, "eng")

    assert result == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ("@Languages:	spa, eng", ["spa", "eng"]),
        ("spa, eng", ["spa", "eng"]),
    ],
)
def test_get_languages(input: str, expected_output: list[str]):
    result = get_languages(input)

    assert result == expected_output


@pytest.mark.parametrize(
    "input",
    [
        ("@Languages:	spa, eng, fr"),
        ("spa, eng, fr"),
        ("@Languages:	spa"),
        ("spa"),
    ],
)
def test_get_languages_with_error(input: str):
    with pytest.raises(Exception):
        get_languages(input)


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ("*MOT:	a ver dime que es . 0_2357", "*MOT:	[- spa] a ver dime que es . 0_2357"),
        (
            "*MOT:	[- eng] have you seen my duckling ? 7767_9766",
            "*MOT:	have you seen my duckling ? 7767_9766"
        ),
        ("*CHI:	xxx . 2357_4934", "*CHI:	xxx . 2357_4934"),
        (
            "*CHI:	hay [?] una butterfly@s .  23360_25615",
            "*CHI:	hay@s [?] una@s butterfly .  23360_25615"
        ),
        (
            "*CHI:	has visto mi patito ?  23360_25615",
            "*CHI:	[- spa] has visto mi patito ?  23360_25615"
        ),
        (
            "*MOT:	<have@s you@s seen@s my@s> [//] has visto mi patito ? 107473_111550",
            "*MOT:	<have you seen my> [//] has@s visto@s mi@s patito@s ? 107473_111550"
        ),
        (
            "*MOT:	<mira y aquí hay una> [//] quién esta acá ? 182095_182816",
            "*MOT:	[- spa] <mira y aquí hay una> [//] quién esta acá ? 182095_182816"
        ),
        (
            "*MOT:	<circle@s esta> [//] el círculo está arriba 382462_384617",
            "*MOT:	<circle esta@s> [//] el@s círculo@s está@s arriba@s 382462_384617"
        )
    ],
)
def test_swap_utterance(input: str, expected_output: str):
    result = swap_utterance(input, "spa", "eng")

    assert result == expected_output
