# Hash Code 2019 Score Calculator

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/72d31c842e3241a3ba15dd575f3ee6f4)](https://app.codacy.com/app/PicoJr/2019-hashcode-score?utm_source=github.com&utm_medium=referral&utm_content=PicoJr/2019-hashcode-score&utm_campaign=Badge_Grade_Dashboard)

**TL;DR** Compute score and check output for Hash Code 2019 Qualification Round.

## Usage

`python3 score.py res/a_example.txt res/a_example.out`

```
score: 2
```

### Check Output File

use `--check` option.

#### check images `id < maxid`

```bash
./score.py res/a_example.txt res/a_example_error_id_max.out --check
```

```
INFO:root:parsing res/a_example.txt
INFO:root:parsing res/a_example.txt done
INFO:root:4 images found (2 V,2 H)
INFO:root:parsing res/a_example_error_id_max.out
ERROR:root:image id: 4 > max id: 3, at line: 2
INFO:root:parsing res/a_example_error_id_max.out: done
ERROR:root:invalid output file: res/a_example_error_id_max.out
score : 0
```

#### check images `id` occur at most once

```bash
./score.py res/a_example.txt res/a_example_error_same_id_twice.out --check
```

```
INFO:root:parsing res/a_example.txt
INFO:root:parsing res/a_example.txt done
INFO:root:4 images found (2 V,2 H)
INFO:root:parsing res/a_example_error_same_id_twice.out
ERROR:root:image id: 3 found again at line: 4
INFO:root:parsing res/a_example_error_same_id_twice.out: done
ERROR:root:invalid output file: res/a_example_error_same_id_twice.out
score : 0
```

#### check images `orientation` is valid

```bash
./score.py res/a_example.txt res/a_example_error_orientation.out --check
```

```
INFO:root:parsing res/a_example.txt
INFO:root:parsing res/a_example.txt done
INFO:root:4 images found (2 V,2 H)
INFO:root:parsing res/a_example_error_orientation.out
ERROR:root:image id: 0 (V expected: H) at line: 1
ERROR:root:image id: 3 (V expected: H) at line: 1
INFO:root:parsing res/a_example_error_orientation.out: done
ERROR:root:invalid output file: res/a_example_error_orientation.out
score : 0
```

#### Check And Abort On 1st Error

`--check` reports all errors.

use `--abort` option to abort on 1st error.

```
./score.py res/a_example.txt res/a_example_error_all.out --check --abort
```

```
INFO:root:parsing res/a_example.txt
INFO:root:parsing res/a_example.txt done
INFO:root:4 images found (2 V,2 H)
INFO:root:parsing res/a_example_error_all.out
ERROR:root:image id: 3 found again at line: 4
INFO:root:aborting...
INFO:root:parsing res/a_example_error_all.out: done
ERROR:root:invalid output file: res/a_example_error_all.out
score : 0
```