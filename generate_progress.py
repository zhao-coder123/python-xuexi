"""
解析 PYTHON_30_DAY_BACKEND_AI_PLAN.md，生成 progress.json
用法: python generate_progress.py
"""

import json
import re
import os

MD_FILE = os.path.join(os.path.dirname(__file__), "PYTHON_30_DAY_BACKEND_AI_PLAN.md")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "progress.json")


def parse_markdown(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    result = {"title": "", "weeks": [], "extras": []}
    current_week = None
    current_day = None
    current_section = None
    current_extra = None  # 非 week/day 的独立区块
    item_counter = {}
    in_code_block = False

    def make_id(prefix: str) -> str:
        item_counter[prefix] = item_counter.get(prefix, 0) + 1
        return f"{prefix}_{item_counter[prefix]}"

    def week_prefix(week_num: int) -> str:
        return f"w{week_num}"

    def day_prefix(week_num: int, day_num: int) -> str:
        return f"w{week_num}d{day_num:02d}"

    for line in lines:
        stripped = line.strip()

        # 跟踪代码块
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # 文档标题
        if stripped.startswith("# ") and not result["title"]:
            result["title"] = stripped[2:].strip()
            continue

        # Week 标题
        week_match = re.match(r"^## Week (\d+)\s*\|\s*(.+)", stripped)
        if week_match:
            week_num = int(week_match.group(1))
            week_title = week_match.group(2).strip()
            current_week = {
                "id": f"week{week_num}",
                "week": week_num,
                "title": week_title,
                "deliverables": [],
                "days": [],
                "review": [],
            }
            result["weeks"].append(current_week)
            current_day = None
            current_section = None
            current_extra = None
            continue

        # Day 标题
        day_match = re.match(r"^### Day (\d+)\s*\|\s*(.+)", stripped)
        if day_match and current_week:
            day_num = int(day_match.group(1))
            day_title = day_match.group(2).strip()
            current_day = {
                "id": f"day{day_num:02d}",
                "day": day_num,
                "title": day_title,
                "sections": [],
            }
            current_week["days"].append(current_day)
            current_section = None
            continue

        # 本周交付 / Week N 自检 / 本日交付 等标题
        if stripped.startswith("### 本周交付") and current_week:
            current_section = {"title": "本周交付", "items": []}
            current_week["deliverables_section"] = current_section
            current_day = None
            continue
        if re.match(r"^### Week \d+ 收口", stripped) and current_week:
            current_day = {
                "id": f"day{current_week['week'] * 7:02d}_review",
                "day": current_week["week"] * 7,
                "title": stripped[4:].strip(),
                "sections": [],
            }
            current_week["days"].append(current_day)
            current_section = None
            continue

        # 加粗段标题 → section
        bold_match = re.match(r"^\*\*(.+?)\*\*$", stripped)
        if bold_match:
            section_title = bold_match.group(1).strip()
            new_section = {"title": section_title, "items": []}

            # 判断归属
            if section_title.startswith("Week") and "自检" in section_title and current_week:
                current_section = new_section
                current_week["_review_section"] = current_section
                current_day = None
            elif current_day:
                current_day["sections"].append(new_section)
                current_section = new_section
            elif current_week:
                # week 级别的 section（如本周交付）
                if "deliverables_section" not in current_week:
                    current_week["deliverables_section"] = new_section
                current_section = new_section
            continue

        # 独立 ## 区块（非 Week）
        h2_match = re.match(r"^## (.+)", stripped)
        if h2_match and not week_match:
            section_name = h2_match.group(1).strip()
            # 跳过非内容区块
            if section_name in ("Dashboard", "Stack Board", "Sprint Overview"):
                current_extra = {"id": section_name.lower().replace(" ", "_"), "title": section_name, "sections": []}
                current_week = None
                current_day = None
                current_section = None
                continue
            current_extra = {"id": re.sub(r"\W+", "_", section_name).strip("_").lower(), "title": section_name, "items": []}
            result["extras"].append(current_extra)
            current_week = None
            current_day = None
            current_section = None
            continue

        # 独立 ### 区块
        h3_match = re.match(r"^### (.+)", stripped)
        if h3_match and not current_week:
            sub_title = h3_match.group(1).strip()
            if current_extra is not None:
                sub_section = {"title": sub_title, "items": []}
                if "sections" not in current_extra:
                    current_extra["sections"] = []
                current_extra["sections"].append(sub_section)
                current_section = sub_section
            continue

        # Checkbox 项
        checkbox_match = re.match(r"^- \[([ xX])\]\s+(.+)", stripped)
        if checkbox_match:
            done = checkbox_match.group(1).lower() == "x"
            text = checkbox_match.group(2).strip()

            # 生成 ID
            if current_day and current_section:
                wn = current_week["week"] if current_week else 0
                dn = current_day["day"]
                sec_short = current_section["title"][:4]
                prefix = f"w{wn}d{dn:02d}_{sec_short}"
                item_id = make_id(prefix)
            elif current_week and current_section:
                prefix = f"w{current_week['week']}_{current_section['title'][:6]}"
                item_id = make_id(prefix)
            elif current_section:
                prefix = f"extra_{current_section['title'][:6]}"
                item_id = make_id(prefix)
            elif current_extra:
                prefix = f"extra_{current_extra['id'][:10]}"
                item_id = make_id(prefix)
            else:
                prefix = "misc"
                item_id = make_id(prefix)

            item = {"id": item_id, "text": text, "done": done}

            if current_section and "items" in current_section:
                current_section["items"].append(item)
            elif current_day:
                if not current_day["sections"]:
                    current_day["sections"].append({"title": "默认", "items": []})
                current_day["sections"][-1]["items"].append(item)
            elif current_week:
                current_week["deliverables"].append(item)
            elif current_extra and "items" in current_extra:
                current_extra["items"].append(item)

    # 整理：把 _review_section 合并到 review
    for week in result["weeks"]:
        if "_review_section" in week:
            week["review"] = week["_review_section"].get("items", [])
            del week["_review_section"]
        if "deliverables_section" in week:
            if not week["deliverables"]:
                week["deliverables"] = week["deliverables_section"].get("items", [])
            del week["deliverables_section"]

    return result


def main():
    data = parse_markdown(MD_FILE)

    # 统计
    total = 0
    done = 0
    for week in data["weeks"]:
        for d in week.get("deliverables", []):
            total += 1
            done += d["done"]
        for day in week.get("days", []):
            for sec in day.get("sections", []):
                for item in sec.get("items", []):
                    total += 1
                    done += item["done"]
        for r in week.get("review", []):
            total += 1
            done += r["done"]
    for extra in data.get("extras", []):
        for item in extra.get("items", []):
            total += 1
            done += item["done"]
        for sec in extra.get("sections", []):
            for item in sec.get("items", []):
                total += 1
                done += item["done"]

    data["stats"] = {"total": total, "done": done}

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Generated {OUTPUT_FILE}")
    print(f"Total items: {total}, Done: {done}")


if __name__ == "__main__":
    main()
