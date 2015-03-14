### What is determine ###

<br />''[Generate traffic signal timing diagrams to determine green running times.](http://www.determine.org.uk/)'' Sometimes a picture (or even a diagram) is worth a thousand words, below an example report (pdf file) :-

**[Very basic example site - full report;](http://www.determine.org.uk/examples/simple-site.pdf)**

The main library [libdertermine](http://code.google.com/p/determine/source/browse/trunk/libdetermine/libdetermine.py) has all the logic needed for a traffic signal controller. Everything for determine is based around this library, xml and xml style sheets. The type of phases are defined in another [xml file](http://code.google.com/p/determine/source/browse/trunk/country-configs/uk.xml). The site (the actual set of traffic lights) is defined by another [xml file](http://code.google.com/p/determine/source/browse/trunk/examples/simplest.xml). The report is in a pdf, but in fact this is xml file with some formatting (see [example](http://www.determine.org.uk/examples/01234-a-nice-test-1.pdf)) <br /><br /> Determine is available as a local glade application - or using online using django at [determine.org.uk](http://www.determine.org.uk)