#!/usr/bin/env python3
"""檢查每個公開教學頁是否具備初學者所需的基本教學結構與有效本機連結。"""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


SITE_ROOT = Path(__file__).resolve().parent
TOPICS = ("ds", "dp", "greedy", "strings")
REQUIRED_TEXT = (
    "這頁要解決什麼問題",
    "核心直覺",
    "常見誤解",
    "複雜度與適用時機",
    "參考資料",
    "你現在應該記得什麼",
)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])


def generated_pages():
    for topic in TOPICS:
        topic_root = SITE_ROOT / "topics" / topic
        yield topic_root / "index.html"
        yield from sorted((topic_root / "pages").rglob("*.html"))


def main():
    errors = []
    pages = list(generated_pages())
    parsed = {}

    for page in pages:
        text = page.read_text(encoding="utf-8")
        for required in REQUIRED_TEXT:
            if required not in text:
                errors.append(f"{page.relative_to(SITE_ROOT)} 缺少「{required}」")

        if "problem" not in text and "predict-box" not in text:
            errors.append(f"{page.relative_to(SITE_ROOT)} 缺少題目情境或互動預測")
        if "<ol class=\"bug-list\">" not in text:
            errors.append(f"{page.relative_to(SITE_ROOT)} 缺少至少三項除錯清單")
        if text.count("<li>") < 3:
            errors.append(f"{page.relative_to(SITE_ROOT)} 的條列內容不足")
        if "strategies" in page.parts and not (
            "mini-trace" in text or "trace-viewer" in text
        ):
            errors.append(f"{page.relative_to(SITE_ROOT)} 缺少專屬最小手算 trace")

        parser = PageParser()
        parser.feed(text)
        parsed[page.resolve()] = parser

    for page, parser in parsed.items():
        for href in parser.links:
            parts = urlsplit(href)
            if parts.scheme or href.startswith("//") or parts.fragment.startswith("topic="):
                continue
            target = (
                (page.parent / (parts.path or page.name)).resolve()
                if parts.path
                else page
            )
            if not target.exists():
                errors.append(
                    f"{page.relative_to(SITE_ROOT)} 連到不存在的檔案：{href}"
                )
            elif (
                parts.fragment
                and target in parsed
                and parts.fragment not in parsed[target].ids
            ):
                errors.append(
                    f"{page.relative_to(SITE_ROOT)} 連到不存在的錨點：{href}"
                )

    if errors:
        print("\n".join(errors))
        raise SystemExit(1)

    print(f"checked {len(pages)} teaching pages: structure and local links passed")


if __name__ == "__main__":
    main()
