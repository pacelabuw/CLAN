from .constants import (
    EXPLANATION_TAG,
    IGNORE_STARTS_WITH,
    INPUT_DIR,
    LANGUAGE_TAG,
    MEDIA_TAG,
    OUTPUT_DIR,
)


def swap_file(file: str) -> None:
    """Take a file and perform the swaps, output to a new file."""
    print(F"Swapping file {file}")
    swapped_output = []
    with open(f"{INPUT_DIR}/{file}") as f:
        lines = f.readlines()

    language_lines = [s for s in lines if s.startswith(LANGUAGE_TAG)]
    if len(language_lines) == 1:
        primary_language, secondary_language = get_languages(language_lines[0])
        print(primary_language, secondary_language)
    elif len(language_lines) > 1:
        raise Exception(
            "Found multiple language headers, "
            f"please ensure only 1 {LANGUAGE_TAG} is in headers."
        )
    else:
        raise Exception(
            "Could not find language header, "
            f"please ensure {LANGUAGE_TAG} is in headers."
        )
    
    for line in lines:
        if line.startswith("@"):
            swapped_output.append(swap_header(line, secondary_language))
        elif line.startswith(EXPLANATION_TAG):
            swapped_output.append(line)
        else:
            swapped_output.append(
                swap_utterance(
                    line,
                    primary_language=primary_language,
                    secondary_language=secondary_language,
                )
            )

    print(f"Found primary language {primary_language} and secondary language {secondary_language}")
    output_filename = f"{file.lower().split('.cha')[0]}_{secondary_language}.cha"
    print(f"Writing output file: {output_filename}")

    with open(f"{OUTPUT_DIR}/{output_filename}", "w") as f:
        f.writelines(swapped_output)


def get_languages(line: str) -> list[str]:
    """Retrieve languages from a comma separated string.
    
    Assume they are either tab separated from beginning of string or by themselves. 
    """
    if "\t" in line:
        _, languages_str = line.split("\t")
    else:
        languages_str = line
    languages = [l.strip() for l in languages_str.split(",")]

    if len(languages) > 2 or len(languages) < 2:
        raise Exception(f"Expected 2 languages in file but found {len(languages)}")
    
    return languages


def swap_header(line: str, secondary_language: str) -> str:
    """Swaps languages in headers, otherwise passes back the original header."""
    if line.startswith("@ID"):
        tag, data = line.split("\t")
        split_data = data.split("|")
        primary_language, secondary_language = [l.strip() for l in split_data[0].split(",")]
        split_data[0] = f"{secondary_language}, {primary_language}"
        return f"{tag}\t{'|'.join(split_data)}"
    elif line.startswith(LANGUAGE_TAG):
        tag = line.split("\t")[0]
        primary_language, secondary_language = get_languages(line)
        return f"{tag}\t{secondary_language}, {primary_language}\n"
    elif line.startswith(MEDIA_TAG):
        tag, data = line.split("\t")
        filename, filetype = [d.strip() for d in data.split(",")]
        return f"{tag}\t{filename}_{secondary_language}, {filetype}\n"
    return line


def swap_utterance(line: str, primary_language: str, secondary_language: str) -> str:
    """Breaks apart the utterance and performs the marking swaps needed.
    
    Rules:
        - Swap words with code switches (@s). If word has @s it will be removed, otherwise add @s
            ignoring punctuation.
        - Remove secondary tag. If a tag (ex: [-eng]) is found then it is removed.
        - Add secondary tag. When no tag or code switching is found then the primary language will
            be added as a tag at the beginning of utterance.
        - Lines with only symbols or special tags will be ignored.
    """
    speaker, utterances_str = line.split("\t")
    utterances = utterances_str.split(" ")
    swapped_utterances = []
    is_code_switched = False
    is_secondary = False
    is_all_ignored_symbols = True

    # If we find the secondary language tag, remove it.
    if utterances[1] == f"{secondary_language}]":
        utterances.pop(0)
        utterances.pop(0)
        is_secondary = True
    
    # Determine if any words are marked as code switched.
    for utterance in utterances[:-1]:   
        if utterance.endswith("@s"):
            is_code_switched = True

    # Ignore timestamp at end.
    for utterance in utterances[:-1]:
        is_utterance_ignored = False

        # Check if we should ignore this for code switching
        for ignored_symbol in IGNORE_STARTS_WITH:
            if not utterance or utterance.startswith(ignored_symbol):
                is_utterance_ignored = True
                break

        # Used to ensure no secondary tag gets added to a line we should ignore.
        is_all_ignored_symbols = is_all_ignored_symbols & is_utterance_ignored
        
        # Handle code switching cases.
        if is_code_switched and not is_utterance_ignored:
            if utterance.endswith("@s"):
                swapped_utterances.append(utterance.split("@")[0])
            elif utterance.endswith("@s>"):
                swapped_utterances.append(f"{utterance.split('@')[0]}>")
            elif utterance.endswith(">"):
                swapped_utterances.append(f"{utterance[:-1]}@s>")
            else:
                swapped_utterances.append(f"{utterance}@s")
        else:
            swapped_utterances.append(utterance)

    # Add secondary tag if needed.
    if not (is_code_switched or is_secondary or is_all_ignored_symbols):
        swapped_utterances.insert(0, f"[- {primary_language}]")

    # Rebuild the utterance
    return f"{speaker}\t{' '.join(swapped_utterances)} {utterances[-1]}"
