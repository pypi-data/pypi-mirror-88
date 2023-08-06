[![Python][python-test-image]][python-test-url]

[python-test-image]: https://github.com/dondakeshimo/tocot/workflows/Python%20poetry%20lint%20test%20build/badge.svg
[python-test-url]: https://github.com/dondakeshimo/tocot/actions?query=workflow%3A%22Python+poetry+lint+test+build%22

# tocot
Table Of Contents wO Tsukuru

This script build a TOC for markdown

# Required
Python >= 3.7

# Install
```
pip install tocot
```

# Usage
```
$ tocot --help
Usage: tocot [OPTIONS] IN_FILE OUT_FILE

Options:
  -l, --level INTEGER    [default: 2]
  -e, --to_embed TEXT    [default: [TOC]]
  --exclude_symbol TEXT  [default: exclude-toc]
  --help                 Show this message and exit.
```

### example
You have to write "[TOC]" in your markdown file, then run below command, "[TOC]" is replaced to Table of Contents.
```
$ tocot README.md new_README.md
```

##### README.md
```
# test
これはテスト

# 目次
[TOC]

# level1
## level2
### level3
#### level4
##### level5
###### level6

## 日本語のテスト

#### level3を飛ばす

# exclude <!-- exclude-toc -->
除外されるはず

\```
# exclude
code blockの中なので無視される
\```
```

##### new_README.md
```
<a id="sec1-0"></a>
# test
これはテスト

<a id="sec2-0"></a>
# 目次
* [test](#sec1-0)
* [目次](#sec2-0)
* [level1](#sec3-0)
  * [level2](#sec3-1)
  * [日本語のテスト](#sec3-2)


<a id="sec3-0"></a>
# level1
<a id="sec3-1"></a>
## level2
### level3
#### level4
##### level5
###### level6

<a id="sec3-2"></a>
## 日本語のテスト

#### level3を飛ばす

# exclude <!-- exclude-toc -->
除外される

\```
# exclude
code blockの中なので無視される
\```
```

If you want to change "[TOC]" to "table of contents template".
```
$ tocot -e "table of contents template" README.md new_README.md
```

You can select how deep include Table of contents.
Including title level is defined the number of "#".
```
$ tocot -l 4 README.md new_README.md
```

If you want to exclude title, you write comment "exclude-toc" next to the title.
```
$ tocot README.md new_README.md
```

You can change "exclude-toc" to "i hate this title".
```
$ tocot --exclude_symbol "i hate this title" README.md new_README.md
```

if you want to debug, you can write to stdout.
```
$ tocot README.md -
```
