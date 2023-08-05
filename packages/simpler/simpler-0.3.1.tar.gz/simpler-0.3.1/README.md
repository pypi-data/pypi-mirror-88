# Simpler

A library to make Python even simpler.

It contains an assorted selection of utils that I use on my projects.

## Installation

It is [available in PyPI](https://pypi.org/project/simpler/), just do `pip install simpler`.

## Usage

These are the methods currently available.

* **simpler.algorithms**
  * **DynamicProgramming:** abstract dynamic programming class. After implementing methods .alternatives(state), .is_final(state) and .penalty(state) you can run .solve, asking for one solution, one optimal solution, every solution or every optimal solution.
* **simpler.bioinformatics**
  * **codon_table:** dictionary of codon translations.
  * **monoisotopic_mass_table:** monoisotopic mass for every amino acid.
  * **monoisotopic_mass_water:** just that.
  * **parse_fasta:** given a fasta string, it returns every (or just the first) sequence found.
  * **dna_to_rna:** given a DNA string, returns its RNA version.
  * **rna_to_dna:** given a RNA string, returns its DNA version.
  * **rna_to_protein:** given a RNA string, returns its proteins.
  * **reverse_complement:** returns the reverse complement of a sequence, either DNA or RNA.
* **simpler.databases**
  * **MySQL:** this class provides a easy way to connect to a MySQL database and forget about implementation stuff. Methods find_many and find_one methods return {col_name: value} dicitonaries, find column returns just one value, insert returns the id of the inserted element, and apply returns the row count of deleted/updated rows.
* **simpler.files**
  * **cd:** changes working directory, base of relative routes, to the one where the script is located.
  * **read:** simplified read of a file with a single interface for string, bytes, json and pickle files.
  * **stream_lines:** same interface as read, just for string and bytes.
  * **write:** simplified write to a file with the same format as read.
  * **disk_cache:** this @annotation caches a file in the disk.
  * **size:** given a file, returns its size without loading it to memory.
  * **find_hidden_compressed:** given a file, finds if it contains the signature for any compressed format.
  * **tvshow_rename:** rename every TV show of a folder.
  * **directory_compare:** compares the changes in two directories recursively.
* **simpler.format**
  * **human_bytes:** transforms a size in bytes to a friendly amount.
  * **human_seconds:** transforms a number of seconds to a friendly format.
  * **human_date:** transforms a datetime to a relative friendly format.
  * **random_string:** returns a random string.
  * **print_matrix:** pretty-prints a 2D-array.
  * **safe_filename:** given a string name, returns its safe-to-save version.
* **simpler.mail**
  * **compose:** simplified interface to compose a mail message.
  * **send:** simplified interface to send a mail.
* **simpler.math**
  * **clamp:** returns a value clamped in an interval.
  * **snap:** returns a value snapped to a scale of a given size and offset.
  * **unique:** given a list, returns a list in the same order excluding repeated elements according to a uniqueness function.
  * **all_equal:** checks if every element of a sequence is the same.
  * **jaccard:** returns the Jaccard index of two sequences.
  * **levenshtein:** Returns the Levenshtein distance of two sequences.
  * **base_change:** changes the base of a number represented as a list of integers.
  * **prime_list:** returns the list of prime numbers from 2 to n.
  * **is_prime:** checks if a number is prime.
  * **fibonacci:** returns the n-th fibonacci number.
  * **lcm:** least common multiple of two numbers.
  * **gcd:** greatest common divisor of two numbers.
  * **factor:** returns the factors of a number and its exponents.
  * **palindrome_list:** returns every palindromic number with k digits.
  * **phi:** Euler's phi function.
* **simpler.sparql**
  * **dbpedia:** sends a query to DBPedia.
  * **types:** returns every entity type with values that contain a given string.
* **terminal**
  * **getch:** reads a sngle byte from the user input.
* **timing**
  * **tic:** adds the current time to a time stack.
  * **toc:** pops the last added time from a time stack and prints the difference. Can be used with tic to profile methods.
* **validation**
  * **assert_set:** asserts that a given value exists and returns it.
  * **assert_str:** asserts that a given value is a string and complies with some customisable checks, and returns it.
  * **assert_number:** asserts that a given value is a number and complies with some customisable checks, and returns it.
  * **assert_id:** asserts that a given value is a valid daabase id and returns it.
  * **assert_mail:** asserts that a given string is a valid mail and returns it.
  * **assert_exists:** asserts that the given path exists and returns it.
* **web**
  * **download_file:** stream a download a file from a URL while displaying the progress and ETA.
  * **DownloaderPool:** pool of workers that download a set of URLs simultaneously.