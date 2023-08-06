"""toc builder.

toc builder has business logic.

"""

import typing


class TOCBuilder:
    """TOC Builder class.

    TOCBuilder is a class for main process.

    """

    HEADER_CHAR = "#"
    ITEM_CHAR = "* "
    ITEM_INDENT = "  "
    SECTION_JOINT = "-"
    SECTION_PREFIX = "sec"
    CODE_BLOCK_CHAR = "```"

    def __init__(self, in_file: typing.TextIO, out_file: typing.TextIO,
                 level: int, to_embed: str, exclude_symbol: str) -> None:
        """Initialize TOCBuilder.

        constructor.

        """
        self.in_file = in_file
        self.out_file = out_file
        self.upper_level = level
        self.to_embed = to_embed
        self.exclude_symbol = exclude_symbol
        self.is_code_block = False
        self.section_counter_list = [0] * self.upper_level
        self.toc_item_list = []
        self.new_contents_list = []
        self.toc = ""
        self.new_contents = ""

    def build(self) -> None:
        """Build Table of Contents.

        build is a main function of this class to make TOC.

        """
        for line in self.in_file:
            if self._is_code_block(line):
                self.new_contents_list.append(line)
                continue

            if not self._is_header(line):
                self.new_contents_list.append(line)
                continue

            level = self._detect_level(line)
            if level > self.upper_level:
                self.new_contents_list.append(line)
                continue

            if self._has_exclude_comment(line):
                self.new_contents_list.append(line)
                continue

            section = self._build_section(level)
            title = self._extract_header_title(line, level)

            self.new_contents_list.append(self._make_section_tag(section))
            self.new_contents_list.append(line)

            self._append_toc_row(title, section, level)

        self.toc = "\n".join(self.toc_item_list) + "\n"
        self.new_contents = "".join(self.new_contents_list)

        self._embed_toc()

    def write(self) -> None:
        """Write a markdown.

        write a markdown file.

        """
        self.out_file.write(self.new_contents)

    def _is_code_block(self, line: str) -> bool:
        if self.CODE_BLOCK_CHAR in line:
            self.is_code_block = not self.is_code_block

        return self.is_code_block

    def _is_header(self, line: str) -> bool:
        return line.startswith(self.HEADER_CHAR)

    def _has_exclude_comment(self, line: str) -> bool:
        return self.exclude_symbol in line

    def _detect_level(self, line: str) -> int:
        level = 0
        for char in line:
            if char != self.HEADER_CHAR:
                break
            level += 1

        return level

    def _append_toc_row(self, title: str, section: str, level: int) -> None:
        indent = self.ITEM_INDENT * (level - 1)
        title = f"[{title}]"
        section = f"(#{section})"
        self.toc_item_list.append(indent + self.ITEM_CHAR + title + section)

    def _extract_header_title(self, line: str, level: int) -> str:
        title = line[level:]
        return title.strip()

    def _build_section(self, level: int) -> str:
        for i in range(len(self.section_counter_list)):
            if i < level - 1:
                continue
            elif i == level - 1:
                self.section_counter_list[i] += 1
            else:
                self.section_counter_list[i] = 0

        section_num = [str(s) for s in self.section_counter_list]

        return self.SECTION_PREFIX + self.SECTION_JOINT.join(section_num)

    def _make_section_tag(self, section: str) -> str:
        return f"<a id=\"{section}\"></a>\n"

    def _embed_toc(self) -> None:
        self.new_contents = self.new_contents.replace(self.to_embed, self.toc)
