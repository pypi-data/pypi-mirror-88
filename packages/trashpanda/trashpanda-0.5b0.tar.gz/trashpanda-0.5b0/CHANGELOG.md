# Changelog
This changelog is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.5b0] - 2020-12-17
### Changed
- *cut_after* now keeps first line if equal.

### Removed
- *add_blank_rows_to_dataframe* is replaced by *add_blank_rows*
- *cut_dataframe_after* is replaced by *cut_after*

## [0.4b0.post1] - 2020-12-01
### Fixed
- readthedocs issue

## [0.4b0] - 2020-12-01
### Fixed
- Results of *add_blank_rows_to_dataframe* and *cut_dataframe_after* keep the
  index name.
- Wrong definitions within the documentation.

### Added
- Methods *cut_dataframe_after_max*, *cut_series_after_max*, *cut_after*,
  *add_blank_rows*

### Deprecated
- Methods *cut_dataframe_after* and *add_blank_rows_to_dataframe* are replaced
  by *cut_after* and *add_blank_rows*

## [0.3b0] - 2020-11-25
### Added
- Method *cut_dataframe_after* which returns a cut DataFrame with interpolated values
  at the cutting index.

### Changed
- Changed structure of sphinx documentation.

### Removed
- Method *get_intersection_of_series* was removed and replaced by *get_intersection*,
  which works for *pandas.Series* and *pandas.DataFrame*.


## [0.2b0] - 2020-11-22
### Added
- Method *add_blank_rows_to_dataframe* for adding blank rows into a DataFrame.

## [0.1b0.post1] - 2020-11-15
### Added
- Link to the documentation.

### Deprecated
- Method *get_intersection_for_series* will be removed in the next release.

## [0.1b0] - 2020-11-15
### Added
- Method *get_intersection* as a replacement for *get_intersection_of_series*

### Deprecated
- Method *get_intersection_for_series* will be removed in the next release.

## [0.0b1.post1] - 2020-11-13
### Added
- Link to Read-the-Docs documentation in README.md and setup.py

## [0.0b1] - 2020-11-13
First release of trashpanda.

