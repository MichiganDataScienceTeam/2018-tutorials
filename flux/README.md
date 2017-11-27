# MDST Flux Tutorial

Jonathan Stroud

November 28, 2017

**Disclaimer:** This guide to Flux is meant as a brief tutorial, and
  intentionally leaves out some crucial information. For a
  comprehensive tutorial, see the [Flux User
  Guide](http://arc-ts.umich.edu/flux-user-guide/).

## What is Flux?

**Flux** is a shared computing cluster used by students and
  researchers at U of M. Flux is managed by Advanced Research
  Computing - Technology Services (ARC-TS).

Flux contains:
 - 1,372 compute nodes
 - 27,000 cores
 - Minimum 4GB RAM per core

There are several node types:
 - **CPU**
 - **GPU + CPU**
 - CPU + extra RAM
 - HIPAA-compliant CPU
 - Hadoop
 - Custom nodes
 - ... several others
 
Several storage options:
 - **Home directory** across Flux for permament small files
 - **Scratch space** across Flux for temporary large file storage
 - **Temp space** per node for temporary files during compute jobs
 - Long-term disk storage for permanent large files

For more information about Flux, refer to the [ARC-TS
website](http://arc-ts.umich.edu/resources/compute-resources/).

## Creating an Account

Before you join our MDST flux allocation, you need a general Flux
account. Fill out [**this form**](http://arc-ts.umich.edu/fluxform/)
to create an account.

To log in to flux, you will have to set up two-factor authentication.
Follow the instructions on the flux signup form for more information.

Once you have a flux account, you can join the MDST allocation
account. MDST does not add all members to our Flux allocation accounts
automatically. To be added, message Jonathan Stroud (@stroud).

## MDST Allocation Accounts

MDST has access to a CPU allocation and a GPU allocation. You should
use whichever is most appropriate for your work.

### `mdatascienceteam_flux`

This allocation account contains only CPUs, and is part of the regular
flux CPU cluster.

```
mdatascienceteam_flux
CPUs:           1000
Memory:         4TB
Queue:          preempt
Scratch space:  /scratch/mdatascienceteam_flux/
```

These cores are provided as part of the **preempt** queue. This means
that MDST does not own or rent a specific block of cores. Instead, we
have the ability to use any currently-unused cores for a short amount
of time. There is a small chance that, when using this queue, a job
will be cancelled because its cores are needed by another user. While
this does not seem to happen frequently, you should always
periodically save the progress of your job so that you can pick up on
it later if it is cancelled.

We graciously acknowledge free use of the Flux preempt queue from
ARC-TS.

### `mdstproject_fluxg`

In addition, we have two NVIDIA K40 GPUs available for special
projects that require additional computing resources. Access to GPU
resources is limited and granted as needed.

```
mdstproject_fluxg
GPUs:           2
CPUs:           4
Memory:         16GB
Queue:          fluxg
Scratch space:  /scratch/mdstproject_fluxg/
```

These GPUs are not part of the preempt queue, but you should still
periodically save the progress of your jobs when using the GPUs. This
will help you recover if your job ends due to an unexpected bug.

We graciously acknowledge donation of these GPUs by NVIDIA.

## Logging In & The Login Node

Most of the work you do on Flux will be on the **login node**. From
this machine, you can write code, launch jobs, and check on your
running jobs. You should not use this node to run code!

To enter the login node, open a terminal window and `ssh` in
(replacing `uniqname` with your uniqname):

```
$ ssh uniqname@flux-login.arc-ts.umich.edu
```

**Note:** you must be on the UofM network or VPN in order to use Flux.
  Otherwise, the above step will not work.

If you use a Windows machine, you can use
[putty](http://www.putty.org/) to SSH into flux.

You'll be prompted for both an MToken code and a password when you log
in.

### The `home` Directory

Once logged in, you'll be in your `home` directory.

This directory is intended for code and other small files that are
shared across your current jobs. It is not intended to for large
datasets or long-term storage.

Each user has a strict **80GB quota** in `/home/`. If you need more
storage space, use `/scratch/`.

### The `scratch` Directory

The `scratch` space is intended for temporary storage of large files.
For optimal performance, you should store your data as a few large
files rather than many small files. 

To navigate to your `scratch` directory:

```
$ cd /scratch/mdatascienceteam_flux/uniqname
```

In this directory, you have essentially unlimited temporary storage
space. **Any data that is stored here will be deleted after 90 days if
not in use.** We recommend periodically backing up your important
code and data to another location, such as MBox or Google Drive.

## PBS Jobs

To run compute jobs on Flux, you must first request nodes using the
`qsub` command. Typically, we use `qsub` by passing a PBS script,
which contains a request for resources and the job commands.

This repository contains a few examples of PBS scripts. To clone this
git repository to flux (and access the scripts), you'll first need to
set up an SSH key for use with Github. Refer to Github's tutorial on
the subject
[here](https://help.github.com/articles/generating-an-ssh-key/). Once
you've done that, you should be able to clone the directory as
follows:

```
$ cd ~
$ git clone git@github.com:MichiganDataScienceTeam/tutorials.git
$ cd tutorials/flux
```

### PBS scripts

Let's take a look at `flux_template.pbs`. This PBS script launches a
job on the `mdatascienceteam_flux` allocation account. Let's take a
look at a few important parts:

Here, you can replace `job_name` with whatever you want, like
`randomforest_train`. Pick something descriptive!

```
#PBS -N job_name
```

Here, make sure to replace `uniqname` with your actual uniqname:

```
#PBS -M uniqname@umich.edu
```

This line specifies how much computing power you want. Make sure to
request a little more than you think you need (but not too much!). As
is, we are requesting 2 CPUs on 1 node (each node has 16
CPUs) and 8GB of RAM, for 1 hour. If your job ends before
time is up, nothing bad will happen. However, if time is up before
your job ends, you might lose the results of your computation. It's
therefore good practice to save intermediate snapshots of your results
when running long jobs.

```
#PBS -l nodes=1:ppn=2,mem=8GB,walltime=01:00:00
```

At the end of the script, you can run whatever commands you want.
These commands will run on CPU nodes.

```
#  Put your job commands here:
echo "Hello, world"
```

Try modifying `flux_template.pbs` to make it load and run a python
script of your choosing, and save it as `myfirstpbs.pbs`. You can
submit the job to flux by entering the following:

```
$ qsub pbs/myfirstpbs.pbs
```

You'll receive an email when the job starts running, and an additional
email when it either aborts or completes. Once the job completes, it
will create a file called `<job_name>.o<job_id>` which contains the
job output. When I ran it, it looked like this:

```
$ cat job_name.o25820895
nyx6201
nyx6201
Hello, world
$
```

### Interactive Jobs

Often, you'll want to test things out interactively before submitting
big jobs. You can spawn an interactive session on Flux by including
the `#PBS -I` flag in your PBS scripts. For convenience, we've
included a script that will launch an interactive session. To launch,
simply run the script (no need to qsub, the script will qsub itself):

```
$ ./interactive_flux.sh
```

Make sure to edit the file to include your own uniqname first.

## Checking the Queue

TODO

## Modules

TODO

## Creating Modules

TODO

## Flux Policies and Best Practices

TODO
