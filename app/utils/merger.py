from typing import List

def merge_words_kj(results, threshold=45):
    merged_lines = []
    current_line = []
    last_y = None
    for result in results:
        bbox, text, _ = result
        if bbox is None or text is None:
            continue
        y = bbox[0][1]
        if last_y is None or abs(y - last_y) <= threshold:
            current_line.append(text)
        else:
            merged_lines.append(" ".join(current_line))
            current_line = [text]
        last_y = y
    if current_line:
        merged_lines.append(" ".join(current_line))
    return merged_lines

def merge_words_scoring(results, threshold_y=55):
    merged_lines = []
    lines = {}
    for result in results:
        bbox, text, conf = result
        if bbox is None or text is None:
            continue
        y = bbox[0][1]
        x = bbox[0][0]
        found_line = None
        for line_y in lines:
            if abs(y - line_y) <= threshold_y:
                found_line = line_y
                break
        if found_line is None:
            lines[y] = []
            found_line = y
        lines[found_line].append((x, text, conf))
    for y in sorted(lines.keys()):
        sorted_words = sorted(lines[y], key=lambda item: item[0])
        line_text = " ".join(text for _, text, _ in sorted_words)
        avg_conf = sum(conf for _, _, conf in sorted_words) / len(sorted_words)
        merged_lines.append((line_text, avg_conf))
    return merged_lines