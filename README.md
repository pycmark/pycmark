# pycmark

A [CommonMark](https://commonmark.org/) parser for docutils.

## Features

* Provides `md2html` command
* Provides `pycmark.CommonMarkParser` component for docutils
* Customizable parser
  * All syntax are implemented as module
  * Developers can customize syntax via adding/removing the modules
* Compatibility
  * Passed all spec of CommonMark.
  * But docutils can't represent following document structure. Therefor they are disabled by default
    * Hard line break
    * deeper headings appeared before shallow one
