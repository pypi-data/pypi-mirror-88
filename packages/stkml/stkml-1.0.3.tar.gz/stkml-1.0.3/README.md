## Stkml-cli
![continuous_integration](https://github.com/Stackitect/stackml-cli/workflows/continuous_integration/badge.svg)
![publish_to_Pypi](https://github.com/Stackeo-io/stackml-cli/workflows/publish_to_Pypi/badge.svg)
[![PyPI package](https://badge.fury.io/py/stkml.svg)](https://pypi.python.org/pypi/stkml/)
[![downloads](https://img.shields.io/pypi/dm/stkml.svg)](https://pypistats.org/packages/stkml)
[![copyright](https://stkml.stackeo.io/_static/copyright.svg)](https://stkml.stackeo.io/_static/copyright.html)

STKML is an open-source IoT stack coding language developed by Stackeo and INRIA for both industry and academic research. STKML allows you to describe an IoT system globally and then to detail its different entities and their relationships in a simple way. Thus IoT teams can quickly visualize and verify the principles of the end-to-end architecture, create simulation or reproducible test scenarios for the sizing and forecasting of the non-functional properties of a connected system or an IoT solution. end to end before its large-scale deployment. STKML also allows vendors to create libraries of IoT product models and architecture patterns for integration into an architectural design.

A set of tools associated with STKML (enriched online editor, transpilators, diagramming tools, topology checking tools, model libraries) are being developed to support developers in assisted coding and compilation of their models. components and architecture in order to automatically generate models, their documentation or the associated simulation or deployment scenarios. The user can thus contribute to the Stacker community, by creating, reusing and manipulating frameworks and architectural templates and models of IoT system components.

The implementation is compatible with python3.6

## Usage

### Installation of application

```bash
pip install stkml
```

### Run the application

You can run the application with the following command

```bash
stkml

Usage: stkml [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  check           check a Stkml project
  check:package   check stkml package
  compile         compile a Stkml project using a specific backend
  create:package  create a stkml package
  init            initialize a Stkml project
  install         install a Stkml package from stackhub
  publish         publish a Stkml package to stackhub
  search          search for a Stkml package on stackhub

```
### Check
```bash
Usage: stkml check [OPTIONS] STKMLFOLDER

  check a Stkml project

Options:
  -d, --disable-syntax-verification
                                  ignore syntax verification
  -h, --help                      Show this message and exit.
```

###Compile

```bash
Usage: stkml compile [OPTIONS] STKMLPROJECT COMMAND [ARGS]...

  compile a Stkml project using a specific backend

Options:
  -d, --disable-syntax-verification
                                  ignore syntax verification
  -h, --help                      Show this message and exit.

Commands:
  diagram  compile a Stkml project for diagram
  drawio   compile a Stkml project for Drawio

```

#### Compile Diagram

```bash
Usage: stkml compile diagram [OPTIONS]

  compile stkml file for diagram

  Example:     stkml compile stkml_project diagram -t 1 -o img

Options:
  -t, --type [1|2|3]  the diagram type {Architecture ,Topology or Map}
                      [required]

  -o, --output TEXT   the output file  [required]
  -h, --help          Show this message and exit.

```

##### Diagram Examples

-   System Diagram
      ```
      stkml compile -i Examples/example.stkml diagram -t 1 -o Examples/results/diagram/Type1/level1 --icons Examples/icons/
      ```
      Result :
      ![](https://stkml.stackeo.io/_images/level1.png)

-   Deployment Topology Diagram
      ```
      stkml compile -i Examples/example.stkml diagram -t 2 -o Examples/results/Type2/diagram/level1 --icons Examples/icons/
      ```
      Result :
      ![](https://stkml.stackeo.io/_images/level11.png)

-   Deployment Map
      ```
      stkml compile -i Examples/example.stkml diagram -t 3 -o Examples/results/Type2/diagram/level2.html --icons Examples/icons/
      ```
      Result :

       [![](https://stkml.stackeo.io/_static/results/type3.png)](https://stkml.stackeo.io/_static/results/level2_2.html)

#### Compile Drawio

```bash

Usage: stkml compile drawio [OPTIONS]

  compile stkml file for Drawio

  Example:     stkml compile stkml_project Drawio -l 1 -o Drawio

Options:
  -l, --level [1|2]  the diagram view level {System View or Layer View}
                     [required]

  -o, --output TEXT  the output file  [required]
  -h, --help         Show this message and exit.

```
#####Drawio Examples

- level 1 :
  ```
  stkml compile -i Examples/example.stkml drawio -l 1 -o Examples/results/Type1/level1
  ```
  Result :
  [![](https://stkml.stackeo.io/_static/results/level1.png)](https://stkml.stackeo.io/_static/results/level1.html)

- level 2 :
  ```
  stkml compile -i Examples/example.stkml drawio -l 2 -o Examples/results/Type1/level2
  ```
  Result :
  [![](https://stkml.stackeo.io/_static/results/level2.png)](https://stkml.stackeo.io/_static/results/level2.html)

#### Init

```bash

Usage: stkml init [OPTIONS] STKMLDIR

  initialize a Stkml project

Options:
  -h, --help  Show this message and exit.

```
#### Check package
```bash

Usage: stkml check:package [OPTIONS] PACKAGE_PATH

  check a Stkml package

Options:
  -d, --disable-syntax-verification
                                  ignore syntax verification
  -m, --check-metadata            check the package metadata
  -h, --help                      Show this message and exit.
```

#### Create package

```bash
Usage: stkml create:package [OPTIONS] PACKAGE

  create a stkml package

Options:
  -h, --help  Show this message and exit.
```

#### Publish package
```bash
Usage: stkml publish [OPTIONS] PACKAGE

  publish a Stkml package to stackhub

Options:
  -h, --help  Show this message and exit.
```

#### Install package
```bash
Usage: stkml install [OPTIONS] NAME

Options:
  -v, --version TEXT  the version of the package
  -h, --help          Show this message and exit.
```

#### Search Package
```bash
Usage: stkml search [OPTIONS] PACKAGE

  search for a Stkml package on stackhub

Options:
  -h, --help  Show this message and exit.
```

##### Configure the Ide to make stkml code

- See the [stkml documentation](https://stkml.stackeo.io/rst/developer_guide/index.html#configure-the-ide)
