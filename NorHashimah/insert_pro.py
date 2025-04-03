# Skrip untuk menyisipkan tag anotasi ke dalam teks asal (menggunakan fail jsonl)

import json

def process_text(entry):
    text = entry["text"]
    labels = entry["label"]

    merged_labels = {}
    merged_labels2 = {}
    for start, end, tag in labels:
        if tag.endswith("2"):
            if start in merged_labels2:
                merged_labels2[start].append(tag[:-1])
            else:
                merged_labels2[start] = [tag[:-1]]
        else:
            if start in merged_labels:
                merged_labels[start].append(tag)
            else:
                merged_labels[start] = [tag]

    for start in sorted(merged_labels.keys(), reverse=True):
        tag_combination = "_".join(sorted(merged_labels[start]))
        if start in merged_labels2.keys():
            tag_combination2 = "_".join(sorted(merged_labels2[start]))
            text = text[:start] + f"*pro_{tag_combination2}* " + text[start:]
            if text[start][-1:] in [".",",","?","!"]:
                text = text[:start] + f" *pro_{tag_combination}* " + text[start:]
            else:
                text = text[:start] + f"*pro_{tag_combination}* " + text[start:]
        else:
            if text[start][-1:] in [".",",","?","!"]:
                text = text[:start] + f" *pro_{tag_combination}* " + text[start:]
            else:
                text = text[:start] + f"*pro_{tag_combination}* " + text[start:]

    return text

import glob

filepath = "./2003/"
files = glob.glob(filepath+"*-prodrop.jsonl")

for f in files:
    out_file = f.replace(".jsonl","_inserted.txt")
    inserted = []

    with open(f, "r", encoding="utf-8") as fh, open(out_file, "w", encoding="utf-8") as out:
        for l in fh:
            entry = json.loads(l.strip())
            inserted.append(process_text(entry))
        for i in inserted:
            print(i, file=out)
