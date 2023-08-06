# SCRI_db

* ## Description

SCRI_db is a python based application to handle, store, and access data on projects, and associated samples, stored on AWS. Read the [***documentation***](https://awnimo.github.io/SCRI_db/). The application is split into two parts:

1. A *reporting interface*.
2. *Command line tools* to process and update the database registry.

* #### The Reporting Interface

This is a web based interactive R-shiny user friendly interface, to pull reports and summaries, on projects and samples, stored in our database. Once installed, the user can use the package associated notebook, to establish a connection to the database. Through the interface, the user can use the different selectors and filters, to view the desired results. It also allows downloading a `.csv` formatted image of the resulting table.

* #### The Command Line Tools

The ***Command Line Tools*** module has methods to parse ***iLabs*** `HTML` project initiation forms, and sample submission forms. It also has built in methods to collect meta data from these forms, and construct a `MySQL INSERT` statements to push the data to our database on AWS.

* ## System Requirements

1. Python >= 3.6
2. R 3.0.1+. If you don't already have R, download it <a href=http://cran.rstudio.com/>here</a>.
3. mysql-connector-python Version: 8.0.13, install 
        
        $> pip3 install mysql-connector-python
        
4. Jupyter and ipywidgets:
        
        $> pip3 install -U jupyter
        $> pip3 install ipywidgets
        $> jupyter nbextension enable --py widgetsnbextension

* ## Installation

If you are an authorized user with access privileges to update and write to the database, install the *Command Line Tools* from `PyPI`:

    $> pip install SCRIdb
    $> scridb -v

To install the `RShiny` package for the `The Reporting Interface`:

    $> git clone https://github.com/dpeerlab/SCRI_db.git
    $> cd SCRI_db
    $> python3 setup.py RShiny

If you are a front-end user that only needs access to the database to view reports, you can skip the previous step. The `RShiny` setup command assumes `R` platform is installed and exists in `$PATH`. For a customized path to `R`, provide the command line with `--R-path=<path/to/R>` (`python3 setup.py RShiny -h`).

Contact a database `admin` for a `username` and `password` before start using the new platform.

* ## Usage

* ### The Reporting Interface

Activate the notebook:

    $> cd notebook
    $> jupyter notebook samples_db.ipynb
    
From the main menu choose ***Run All*** from ***Cell***. A dual tab box will appear.

* #### Configuration File Setup

It is optional to setup a configuration file to easily connect to the database. Choose the ***configure*** tab if this is the first time you connect to the database. Check ***Create New Configuration***, and enter your ***New Username*** and ***New Password*** (the same ones provided by the database `admin`), then click ***Submit***. This action will create and store a configuration file for future connections to the databae.

If successful, uncheck the ***Create New Configuration***, and switch back to the ***connect*** tab and click the ***Connect to DB!*** button (no need to provide a ***username*** and ***password***).

* #### Establish Connection Without Configuration Setup

Use a ***username*** and ***password*** in the designated fields in the ***connect*** tab, if you want to skip creating a configuration file, to connect to the database.

Start using the web interface and pull your favotite reports.

* ***Important note:*** it is imperative to close the `Samples Dashbord` page by clicking `Close window` on the left side panel, to properly terminate `RShiny`, and prevent kernel hanging.

* ### The Command Line Tools

Detailed information on usage is on [Wiki](https://github.com/dpeerlab/Dana-Pe-er-Wiki/wiki/Command-Line-Tools).

Intended for users with privileged access to the database (with read/write/update access).

    $> scridb -h
     scridb [-h] [-c [CONFIG]] [-f [FILE]] [-o [RESULTS_OUTPUT]] [-j [JOBS]]
              [-e [EMAIL]] [-p [PEM]] [-dS [DOCKERIZEDSEQC]] [-sc [SCATA]]
              {data_submission,process,upload_stats,data_transfer,run} ...

The following will actually build an `HTML` overall report on projects to monitor ongoing projects and their status:

    $> projectsHTML_index

A new feature added to update metadata on samples submitted to *IGO* for sequencing:

    $> update_IGOdates -h
    update_IGOdates [-h] [-s [SEQUENCING_DATE]] [filename]

* ## Release Notes

  ### Version 1.2.1
    
  This new release supports Cite-seq, as well as many improvements to accommodate new changes made on the database side, that require recording records as IGO ids, run records, as well as Cromwell id run jobs. 
  
  Changes were also made to the HTML parser such that future changes to the iLabs HTML forms would require minimal updates to labels added or dropped from new designs. Additionally, the new HTML parser is less susceptible to changes to the HTML structured tables.
  
  ### Version 1.1.9
    
  New in this release `create-job` tool that attempts to regenerate processing jobs for samples with proper records in the database, and already on AWS S3. The tool can be called in command line as follows:
  
      create-job -h
  
  ### Version 1.1.4
    
  Added `Tags` to newly created AWS users, with keys `Name` and `email`.
  
  A minor fix to `upload_stats`.
  
  ### Version 1.1.3
    
  The `CLI` can be installed now from [`PyPI`](https://pypi.org/project/SCRIdb/), no need to clone or sync local repository with remote one.
  
  
