## Signal generation

### Info

The gridpack in `gridpacks/gridpack.tar.gz` produces ggH(125) to ZdZd to 2mu+2X. We run the GENSIM and PREMIXRAW steps, keeping
the scouting outputs, and subsequently run the slimmer from `../batch/Scouting/NtupleMaker/test/mcproducer.py` to embed L1 branches, while
keeping the EDM structure of the file. We will want to run the babymaker on the output of this submission.

### Submission

* Clone [ProjectMetis](https://github.com/aminnj/ProjectMetis/) and source its environment. You've probably already done this in the `../batch/` directory.
* Edit `submit_jobs.py` (`tag`, `total_events`, `events_per_job`, and the `mass`/`ctau` list)
* `./make_tar.sh` to make the tarball for the jobs
* Submit with `python submit_jobs.py` in a screen, so that resubmissions can happen in the background
* Visit the monitoring page and click on samples to see the output location.
