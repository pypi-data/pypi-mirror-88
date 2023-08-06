# LbAPLocal

LbAPLocal is the python library for running offline tests for the LHCb AnalysisProductions framework.


## Usage

After installing, LbAPLocal can be run from the command line with the following options:

```
Usage: lb-ap [OPTIONS] COMMAND [ARGS]...

  Command line tool for the LHCb AnalysisProductions

Options:
  --help  Show this message and exit.

Commands:
  list       List the available production folders by running lb-ap list...
  render     Render the info.yaml for a given production
  test       Execute a job locally
  debug      Start an interactive session inside the job's environment
  reproduce  Reproduce an existing online test locally
```

To see which productions are available:
```bash
$ lb-ap list
The available productions are:
* MyAnalysis
```

To see which jobs are available for a given production:
```bash
$ lb-ap list MyAnalysis
The available jobs for MyAnalysis are:
* My2016MagDownJob
* My2016MagUpJob
```

To render the templating in `info.yaml` for a given production:
```bash
$ lb-ap render MyAnalysis
```

To run a test of a job interactively:
```bash
$ lb-ap debug MyAnalysis My2016MagDownJob

Welcome to analysis productions debug mode:

The production can be tested by running:

gaudirun.py -T '$ANALYSIS_PRODUCTIONS_DYNAMIC/Lb2Lll/MC_2017_MagDown_Lb2PsiL_mm_strip_autoconf.py' '$ANALYSIS_PRODUCTIONS_BASE/Lb2Lll/stripping_seq.py' prodConf_DaVinci_00012345_00006789_1.py

[DaVinci v45r5] output $
```

To test a job non-interactively:
```bash
$ lb-ap test MyAnalysis My2016MagDownJob
Success! Output can be found in xxxxxxxxxxxx
```
