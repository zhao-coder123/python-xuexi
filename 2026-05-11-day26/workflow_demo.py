"""Day 26: Agent / 工作流视角理解示例。"""

from __future__ import annotations


def generate_summary(article: str) -> str:
    return f"摘要: {article[:40]}..."


def extract_keywords(article: str) -> list[str]:
    candidates = ["FastAPI", "Python", "API", "AI", "Workflow"]
    return [item for item in candidates if item.lower() in article.lower()] or [
        "内容",
        "摘要",
    ]


def generate_title(article: str, keywords: list[str]) -> str:
    joined = " / ".join(keywords[:3])
    return f"{joined} 实战指南"


def run_article_workflow(article: str) -> dict[str, object]:
    """把多个步骤串成一个简单工作流。"""

    summary = generate_summary(article)
    keywords = extract_keywords(article)
    title = generate_title(article, keywords)

    return {
        "summary": summary,
        "keywords": keywords,
        "title": title,
    }


def main() -> None:
    article = "FastAPI 可以快速构建 Python API，适合后台系统和 AI 工作流接入。"
    result = run_article_workflow(article)
    print(result)


if __name__ == "__main__":
    main()
