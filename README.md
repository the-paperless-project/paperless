[ en | [de](README-de.md) | [el](README-el.md) ]

![Paperless](https://raw.githubusercontent.com/the-paperless-project/paperless/master/src/paperless/static/paperless/img/logo-dark.png)

> ## Important news about the future of this project
> 
> It's been more than 5 years since I started this project on a whim as an effort to try to get a handle on the massive amount of paper I was dealing with in relation to various visa applications (expat life is complicated!)  Since then, the project has *exploded* in popularity, so much so that it overwhelmed me and working on it stopped being "fun" and started becoming a serious source of stress.
> 
> In an effort to fix this, I created the Paperless GitHub [organisation](https://github.com/the-paperless-project), and brought on a few people to manage the issue and pull request load.  Unfortunately, that model has proven to be unworkable too.  With 23 pull requests waiting and 157 issues slowly filling up with confused/annoyed people wanting to get their contributions in, my whole "appoint a few strangers and hope they've got time" idea is showing my lack of foresight and organisational skill.
> 
> In the shadow of these difficulties, a fork called [Paperless-ng](https://github.com/jonaswinkler/paperless-ng) written by [Jonas Winkler](https://github.com/jonaswinkler) has cropped up.  It's *really* good, and unlike this project, it's actively maintained (at the time of this writing anyway).  With 564 forks currently tracked by GitHub, I suspect there are a few more forks worth looking into out there as well.
> 
> So, with all of the above in mind, I've decided to archive this project as read-only and suggest that those interested in new updates or submitting patches have a look at Paperless-ng.  If you really like "Old Paperless", that's ok too!  The project is [GPL licensed](https://github.com/the-paperless-project/paperless/blob/master/LICENSE), so you can fork it and run it on whatever you like so long as you respect the terms of said license.
>
> In time, I may transfer ownership of this organisation to Jonas if he's interested in taking that on, but for the moment, he's happy to run Paperless-ng out of its [current repo](https://github.com/jonaswinkler/paperless-ng).  Regardless, if we do decide to make the transfer, I'll post a notification here a few months in advance so that people won't be surprised by new code at this location.
> 
> For my part, I'm really happy & proud to have been part of this project, and I'm sorry I've been unable to commit more time to it for everyone.  I hope you all understand, and I'm really pleased that this work has been able to continue to live and be useful in a new project.  Thank you to everyone who contributed, and for making Free software awesome.
> 
> Sincerely,
> [Daniel Quinn](https://github.com/danielquinn)


[![Documentation](https://readthedocs.org/projects/paperless/badge/?version=latest)](https://paperless.readthedocs.org/)
[![Chat](https://badges.gitter.im/the-paperless-project/paperless.svg)](https://gitter.im/danielquinn/paperless)
[![Travis](https://travis-ci.org/the-paperless-project/paperless.svg?branch=master)](https://travis-ci.org/the-paperless-project/paperless)
[![Coverage Status](https://coveralls.io/repos/github/the-paperless-project/paperless/badge.svg?branch=master)](https://coveralls.io/github/the-paperless-project/paperless?branch=master)
[![StackShare](https://img.shields.io/badge/tech-stack-0690fa.svg?style=flat)](https://stackshare.io/the-paperless-project/the-paperless-project)
[![Thanks](https://img.shields.io/badge/THANKS-md-ff69b4.svg)](https://github.com/the-paperless-project/paperless/blob/master/THANKS.md)

Index and archive all of your scanned paper documents

I hate paper.  Environmental issues aside, it's a tech person's nightmare:

* There's no search feature
* It takes up physical space
* Backups mean more paper

In the past few months I've been bitten more than a few times by the problem of not having the right document around.  Sometimes I recycled a document I needed (who keeps water bills for two years?) and other times I just lost it... because paper.  I wrote this to make my life easier.


## How it Works

Paperless does not control your scanner, it only helps you deal with what your scanner produces

1. Buy a document scanner that can write to a place on your network.  If you need some inspiration, have a look at the [scanner recommendations](https://paperless.readthedocs.io/en/latest/scanners.html) page.
2. Set it up to "scan to FTP" or something similar. It should be able to push scanned images to a server without you having to do anything.  Of course if your scanner doesn't know how to automatically upload the file somewhere, you can always do that manually.  Paperless doesn't care how the documents get into its local consumption directory.
3. Have the target server run the Paperless consumption script to OCR the file and index it into a local database.
4. Use the web frontend to sift through the database and find what you want.
5. Download the PDF you need/want via the web interface and do whatever you like with it.  You can even print it and send it as if it's the original. In most cases, no one will care or notice.

Here's what you get:

![The before and after](https://raw.githubusercontent.com/the-paperless-project/paperless/master/docs/_static/screenshot.png)


## Documentation

It's all available on [ReadTheDocs](https://paperless.readthedocs.io/).


## Requirements

This is all really a quite simple, shiny, user-friendly wrapper around some very powerful tools.

* [ImageMagick](http://imagemagick.org/) converts the images between colour and greyscale.
* [Tesseract](https://github.com/tesseract-ocr) does the character recognition.
* [Unpaper](https://github.com/unpaper/unpaper) despeckles and deskews the scanned image.
* [GNU Privacy Guard](https://gnupg.org/) is used as the encryption backend.
* [Python 3](https://python.org/) is the language of the project.
  * [Pillow](https://pypi.python.org/pypi/pillowfight/) loads the image data as a python object to be used with PyOCR.
  * [PyOCR](https://github.com/jflesch/pyocr) is a slick programmatic wrapper around tesseract.
  * [Django](https://www.djangoproject.com/) is the framework this project is written against.
  * [Python-GNUPG](http://pythonhosted.org/python-gnupg/) decrypts the PDFs on-the-fly to allow you to download unencrypted files, leaving the encrypted ones on-disk.


## Project Status

This project has been around since 2015, and there's lots of people using it.  For some reason, it's really popular in Germany -- maybe someone over there can clue me in as to why?

I am no longer doing new development on Paperless as it does exactly what I need it to and have since turned my attention to my latest project, [Aletheia](https://github.com/danielquinn/aletheia).  However, I'm not abandoning this project.  I am happy to field pull requests and answer questions in the issue queue.  If you're a developer yourself and want a new feature, float it in the issue queue and/or send me a pull request!  I'm happy to add new stuff, but I just don't have the time to do that work myself.


## Affiliated Projects

Paperless has been around a while now, and people are starting to build stuff on top of it.  If you're one of those people, we can add your project to this list:

* [Paperless App](https://github.com/bauerj/paperless_app): An Android/iOS app for Paperless.
* [Paperless Desktop](https://github.com/thomasbrueggemann/paperless-desktop): A desktop UI for your Paperless installation.  Runs on Mac, Linux, and Windows.
* [ansible-role-paperless](https://github.com/ovv/ansible-role-paperless): An easy way to get Paperless running via Ansible.
* [paperless-cli](https://github.com/stgarf/paperless-cli): A golang command line binary to interact with a Paperless instance.

## Similar Projects

There's another project out there called [Mayan EDMS](https://www.mayan-edms.com/) that has a surprising amount of technical overlap with Paperless.  Also based on Django and using a consumer model with Tesseract and Unpaper, Mayan EDMS is *much* more featureful and comes with a slick UI as well, but still in Python 2. It may be that Paperless consumes fewer resources, but to be honest, this is just a guess as I haven't tested this myself.  One thing's for certain though, *Paperless* is a **way** better name.


## Important Note

Document scanners are typically used to scan sensitive documents.  Things like your social insurance number, tax records, invoices, etc.  While Paperless encrypts the original files via the consumption script, the OCR'd text is *not* encrypted and is therefore stored in the clear (it needs to be searchable, so if someone has ideas on how to do that on encrypted data, I'm all ears).  This means that Paperless should never be run on an untrusted host.  Instead, I recommend that if you do want to use it, run it locally on a server in your own home.


## Donations

As with all Free software, the power is less in the finances and more in the collective efforts.  I really appreciate every pull request and bug report offered up by Paperless' users, so please keep that stuff coming.  If however, you're not one for coding/design/documentation, and would like to contribute financially, I won't say no ;-)

The thing is, I'm doing ok for money, so I would instead ask you to donate to the [United Nations High Commissioner for Refugees](https://donate.unhcr.org/int-en/general). They're doing important work and they need the money a lot more than I do.
