# Create your views here.
from determine.web.models import *
from determine.web.forms import *
from determine.web.unique_slug import *

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect 

from django.template import loader, Context

from django.template.defaultfilters import slugify
from determine.web import libdetermine
from django.conf import settings
from django import forms
from django.http import HttpResponse



import datetime
from lxml import etree
import tempfile


def newSite(request):
    if request.method == 'POST': # If the form has been submitted...
        import os
        form = NewSignalSiteForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            title = form.cleaned_data['title']
            country = form.cleaned_data['country']
            siteRecord = SignalSite(title=title, country=country)
            siteRecord.save()
            unique_slugify(siteRecord, siteRecord.title)
            siteRecord.save()
            site = libdetermine.siteClass()
            site.address = title
            xmlFile = siteRecord.get_xml_filename_full()
            xmlDirs = siteRecord.get_xml_dirs_full()
            if not os.path.exists(xmlDirs):
                os.makedirs(xmlDirs)
            f=open(xmlFile, 'w')
            f.write(site.xml())
            f.close()
            next_url = siteRecord.get_absolute_url()
   
            # Step number 2..... better url than /thanks/
            return HttpResponseRedirect(next_url) # Redirect after POST
    else:
        form = NewSignalSiteForm() # An unbound form

    return render_to_response('forms/new-site.html', locals())


def siteRecordFilter(year, month, day, slug):
    MONTHS = ['dummy', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    startOfDay = datetime.datetime(int(year), MONTHS.index(month), int(day))
    endOfDay = startOfDay + datetime.timedelta(1)
    try:
        siteRecord = SignalSite.objects.filter(slug=slug)
        siteRecord = siteRecord.filter(publish_date__gte=startOfDay)
        siteRecord = siteRecord.filter(publish_date__lte=endOfDay)
        siteRecord = siteRecord.order_by('-publish_date')[0]
        if siteRecord:
            return siteRecord
    except:
        return False

def getSiteObject(siteRecord):
    xmlFile = siteRecord.get_xml_filename_full()
    country = siteRecord.get_country_config_xml_full()
    countryConfig = libdetermine.parseCountryConfig(country)
    siteObject = libdetermine.parseSiteConfig(xmlFile, countryConfig)
    return siteObject, countryConfig

def writeBackSiteToXml(siteRecord, siteObject):
    xmlFile = siteRecord.get_xml_filename_full()
    f=open(xmlFile, 'w')
    f.write(siteObject.xml())
    f.close()
    

def getSiteHtml(siteRecord):
    xmlFile = siteRecord.get_xml_filename_full()
    siteTransform = siteRecord.get_site_xslt_full()
    # From http://www.rexx.com/~dkuhlman/pyxmlfaq.html#id9
    xslt_doc = etree.parse(siteTransform)
    transform = etree.XSLT(xslt_doc)
    indoc = etree.parse(xmlFile)
    paramdict = {'param1': 'value1', 'param2': 'value2'}
    outdoc = transform(indoc, **paramdict)
    return etree.tostring(outdoc, pretty_print=True)

def listToTupleChoices(l):
    newList = []
    for item in l:
        t = (item, item)
        newList.append(t)
    return tuple(newList)

def home(request):
    latestSites =  SignalSite.objects.all()[:5]
    return render_to_response('home.html', locals())

def allSites(request):
    latestSites =  SignalSite.objects.all()
    return render_to_response('all-sites.html', locals())


def start(request, year, month, day, slug):
    siteRecord = siteRecordFilter(year, month, day, slug)
    if siteRecord is False:
        return HttpResponseRedirect('/sites/error/')
    if siteRecord.locked:
        return HttpResponseRedirect(siteRecord.get_absolute_url_report())        
    siteObject, countryObject = getSiteObject(siteRecord)

    siteHtml = getSiteHtml(siteRecord)
    nextUrl = './phases/'
    nextName = 'Phases'
    return render_to_response('forms/start.html', locals())


def phases(request, year, month, day, slug):
    siteRecord = siteRecordFilter(year, month, day, slug)
    if siteRecord is False:
        return HttpResponseRedirect('/sites/error/')
    if siteRecord.locked:
        return HttpResponseRedirect(siteRecord.get_absolute_url_report())        
    siteObject, countryObject = getSiteObject(siteRecord)
    deletePhaseText = 'Delete Phase '
    addPhaseText = 'Add Phase'

    if request.method == 'POST':
        if request.POST.has_key(deletePhaseText):
#            return HttpResponseRedirect('delete/')
            phase_remove_letter = request.POST[deletePhaseText].lstrip(deletePhaseText)
            phase_remove = siteObject.phases.phase(phase_remove_letter)
            siteObject.phases.phases.remove(phase_remove)
            writeBackSiteToXml(siteRecord, siteObject) 
        if request.POST.has_key(addPhaseText):
            add_phase_letter = request.POST['add_phase_letter']
            phase_type = request.POST['phase_type']
            if add_phase_letter:
                next_url = siteRecord.get_absolute_url() + 'phases/add/' + add_phase_letter + '/' + phase_type
                return HttpResponseRedirect(next_url) # Redirect after POST
    currentPhases = siteObject.phases.phaseListLetters()
    phaseTypesChoices = listToTupleChoices(countryObject.listNames())
    class newPhaseForm(forms.Form):
        add_phase_letter = forms.CharField(max_length=2, help_text='(e.g. A)')
        phase_type = forms.ChoiceField(choices=phaseTypesChoices)
    form = newPhaseForm() # An unbound form
    siteHtml = getSiteHtml(siteRecord)
    nextUrl = '../stages/'
    nextName = 'Stages'
    return render_to_response('forms/phases.html', locals())


def stages(request, year, month, day, slug):
    siteRecord = siteRecordFilter(year, month, day, slug)
    if siteRecord is False:
        return HttpResponseRedirect('/sites/error/')
    if siteRecord.locked:
        return HttpResponseRedirect(siteRecord.get_absolute_url_report())        
    siteObject, countryObject = getSiteObject(siteRecord)
    addStageText = 'Add Stage'
    deleteStageText = 'Delete Stage '
    editStageText = 'Edit Stage '
    
    if request.method == 'POST':
        if request.POST.has_key(deleteStageText):
            stage_number = request.POST[deleteStageText].lstrip(deleteStageText)
            stage_selected = siteObject.stages.stage(stage_number)
            siteObject.stages.stages.remove(stage_selected)
            writeBackSiteToXml(siteRecord, siteObject) 
        if request.POST.has_key(addStageText):
            stageName = request.POST['stageName']
        if request.POST.has_key(editStageText):
            stageName = request.POST[editStageText].lstrip(editStageText)
        if request.POST.has_key(addStageText) or request.POST.has_key(editStageText):
            next_url = siteRecord.get_absolute_url() + 'stages/' + stageName + '/' 
            return HttpResponseRedirect(next_url) # Redirect after POST

    currentStages = siteObject.stages.listStageNames()
    currentStagesText = siteObject.stages.html()

    class newStageForm(forms.Form):
        stageName = forms.IntegerField(label="Stage :")
    form = newStageForm() # An unbound form
    siteHtml = getSiteHtml(siteRecord)
    nextUrl = '../intergreens/'
    nextName = 'Intergreens'
    previousUrl = '../phases/'
    previousName = 'Phases'
    return render_to_response('forms/stages.html', locals())

def intergreens(request, year, month, day, slug):
    siteRecord = siteRecordFilter(year, month, day, slug)
    if siteRecord is False:
        return HttpResponseRedirect('/sites/error/')
    if siteRecord.locked:
        return HttpResponseRedirect(siteRecord.get_absolute_url_report())        
    siteObject, countryObject = getSiteObject(siteRecord)
    currentPhases = siteObject.phases.phaseListLetters()
    intergreenHtml = ""
    _and_ = "_intergreen_"
    totalPhases = len(currentPhases)
    rangePhases = range(0, totalPhases+1)
    if request.method == 'POST':
        for k in request.POST:
            try:
                new_intergreen = int(request.POST[k])
                i = k.index(_and_)
                fromPhaseLetter = k[:i]
                toPhaseLetter = k[2:].lstrip(_and_)
                toPhase = siteObject.phases.phase(toPhaseLetter)
                old_intergreen = toPhase.intergreenFrom(fromPhaseLetter)
                if new_intergreen != old_intergreen:
                    try:
                        toPhase.setIntergreenFrom(fromPhaseLetter,new_intergreen)
                    except:
                        pass
            except:
                pass
        writeBackSiteToXml(siteRecord, siteObject) 
        
    if totalPhases >0:
        intergreenHtml = intergreenHtml + '<table  class="ig">'
        for row in range(0, totalPhases +1):
            intergreenHtml = intergreenHtml + "<tr>"
            for col in range(0, totalPhases +1):
                intergreenHtml = intergreenHtml + "<td>"
                intergreenHtml = intergreenHtml + '<div class="cell">'
                if row==0 and col==0:
                    intergreenHtml = intergreenHtml + "&nbsp;"
                elif row==0:
                    intergreenHtml = intergreenHtml + siteObject.phases.phases[col-1].letter
                elif col==0:
                    intergreenHtml = intergreenHtml + siteObject.phases.phases[row-1].letter
                elif col==row:
                    intergreenHtml = intergreenHtml + " X "
                else:
                    from_phase = siteObject.phases.phases[col-1]
                    from_phase_letter = siteObject.phases.phases[row-1].letter
                    intergreen_value = from_phase.intergreenFrom(from_phase_letter)
#                    intergreenHtml = intergreenHtml + str(intergreen_value)
                    inputName = siteObject.phases.phases[row-1].letter + _and_ + siteObject.phases.phases[col-1].letter
                    if intergreen_value == 0:
                        strIntergreen = ""
                    else:
                        strIntergreen = str(intergreen_value)
                    intergreenHtml = intergreenHtml + '<input type="text" name="' + inputName + '" id="ig" value="' + strIntergreen + '" class="ig"/>'
                intergreenHtml = intergreenHtml + '</div>'
                intergreenHtml = intergreenHtml + "</td>"
            intergreenHtml = intergreenHtml + "</tr>"
        intergreenHtml = intergreenHtml + "</table>"


    siteHtml = getSiteHtml(siteRecord)
    nextUrl = '../delays/'
    nextName = 'Delays'
    previousUrl = '../stages/'
    previousName = 'Stages'
    return render_to_response('forms/intergreens.html', locals())

def delays(request, year, month, day, slug):
    siteRecord = siteRecordFilter(year, month, day, slug)
    if siteRecord is False:
        return HttpResponseRedirect('/sites/error/')
    if siteRecord.locked:
        return HttpResponseRedirect(siteRecord.get_absolute_url_report())        
    siteObject, countryObject = getSiteObject(siteRecord)
    currentPhases = siteObject.phases.phaseListLetters()
    currentStages = siteObject.stages.listStageNames()
    
    addDelayText = 'Add Delay'
    deleteDelayText = 'Delete '
        
    
    phaseChoices = listToTupleChoices(currentPhases)
    stageChoices = listToTupleChoices(currentStages)
    class newDelayForm(forms.Form):
        phase = forms.ChoiceField(choices=phaseChoices)
        stageFrom = forms.ChoiceField(choices=stageChoices, label="Moving from stage:")
        stageTo = forms.ChoiceField(choices=stageChoices, label="Moving to stage:")
        delay_by = forms.IntegerField(label="Is delayed by:") 

    if request.method == 'POST':
        if request.POST.has_key(deleteDelayText):
            delayText = request.POST[deleteDelayText].lstrip(deleteDelayText)
            siteObject.phases.phaseDelayDelete(delayText)
            tmp = delayText
            writeBackSiteToXml(siteRecord, siteObject) 
            form = newDelayForm() # An unbound form
        if request.POST.has_key(addDelayText):
            form = newDelayForm(request.POST) # A bound form
            if form.is_valid(): # All validation rules pass
                try:
                    phase = form.cleaned_data['phase']
                    stageFrom = form.cleaned_data['stageFrom']
                    stageTo = form.cleaned_data['stageTo']
                    delay_by = form.cleaned_data['delay_by']
                    siteObject.phases.phase(str(phase)).setPhaseDelay(stageFrom, stageTo, str(delay_by))
                    writeBackSiteToXml(siteRecord, siteObject)
                except:
                    pass

    else:
        form = newDelayForm() # An unbound form
        
    currentDelays = siteObject.phases.phaseDelayList()
    currentDelaysText = siteObject.phases.phaseDelayHtml()
    siteHtml = getSiteHtml(siteRecord)
    nextUrl = '../diagrams/'
    nextName = 'Diagrams'
    previousUrl = '../intergreens/'
    previousName = 'Intergreens'
    return render_to_response('forms/delays.html', locals())

def lock(request, year, month, day, slug):
    siteRecord = siteRecordFilter(year, month, day, slug)
    if siteRecord is False:
        return HttpResponseRedirect('/sites/error/')
    if siteRecord.locked:
        return HttpResponseRedirect(siteRecord.get_absolute_url_report())        
    siteObject, countryObject = getSiteObject(siteRecord)

    if request.method == 'POST':
        if request.POST.has_key('True'):
            siteRecord.locked = True
            siteRecord.save()
        else:
            siteRecord.locked = False
            siteRecord.save()
        next_url = siteRecord.get_absolute_url() + 'report/'
        return HttpResponseRedirect(next_url)

    currentDiagramText = siteObject.diagramsHtml()
    siteHtml = getSiteHtml(siteRecord)
    previousUrl = '../report/'
    previousName = 'Report'
    return render_to_response('forms/lock.html', locals())

    

def diagrams(request, year, month, day, slug):
    siteRecord = siteRecordFilter(year, month, day, slug)
    if siteRecord is False:
        return HttpResponseRedirect('/sites/error/')
    if siteRecord.locked:
        return HttpResponseRedirect(siteRecord.get_absolute_url_report())        
    siteObject, countryObject = getSiteObject(siteRecord)    
    currentDiagrams = siteObject.listDiagrams()
    
    addDiagramText = 'Add Diagram'
    deleteDiagramText = 'Delete Diagram '
    editDiagramText = 'Edit Diagram '

    class newDiagramform(forms.Form):
        diagram_title = forms.CharField(max_length=200)
        cycle_time = forms.IntegerField(initial = 60)
    if request.method == 'POST':
        i = None
        if request.POST.has_key(deleteDiagramText):
            diagramText = request.POST[deleteDiagramText].lstrip(deleteDiagramText)
            try:
                removeDiagram = siteObject.diagram(str(diagramText))
                siteObject.requiredDiagrams.remove(removeDiagram)
                currentDiagrams = siteObject.listDiagrams()
                writeBackSiteToXml(siteRecord, siteObject)
                form = newDiagramform() # An unbound form
            except:
                pass
        if request.POST.has_key(editDiagramText):
            try:
                diagramText = request.POST[editDiagramText].lstrip(editDiagramText)
                i = currentDiagrams.index(str(diagramText))
            except:
                pass
        if request.POST.has_key(addDiagramText):
            form = newDiagramform(request.POST)
            if form.is_valid():
                diagram_title = form.cleaned_data['diagram_title']
                cycle_time = form.cleaned_data['cycle_time']
                newDiagram = libdetermine.requiredDiagramClass(str(diagram_title), cycle_time, 
                siteObject.stages.stages[0].stageName, 1)
                siteObject.requiredDiagrams.append(newDiagram)

                writeBackSiteToXml(siteRecord, siteObject)
                currentDiagrams = siteObject.listDiagrams()
                i = currentDiagrams.index(str(diagram_title))
        if i is not None:
            # diagrams/edit/(?P<diagramNumber>\d{1,2})$'
            next_url = siteRecord.get_absolute_url() + 'diagrams/edit/' + str(i) + '/'
            return HttpResponseRedirect(next_url)
    else:
        form = newDiagramform() # An unbound form
        
    currentDiagramText = siteObject.diagramsHtml()
    siteHtml = getSiteHtml(siteRecord)
    nextUrl = '../report/'
    nextName = 'Report'
    previousUrl = '../delays/'
    previousName = 'Delays'
    return render_to_response('forms/diagrams.html', locals())



# phasesAdd
def phasesAdd(request, year, month, day, slug, letter, phaseType):
    siteRecord = siteRecordFilter(year, month, day, slug)
    if siteRecord is False:
        return HttpResponseRedirect('/sites/error/')
    if siteRecord.locked:
        return HttpResponseRedirect(siteRecord.get_absolute_url_report())        
    siteObject, countryObject = getSiteObject(siteRecord)
    phaseTypeObject = countryObject.phaseType(str(phaseType))
    fixedItems =[]
    class phaseDetailsForm(forms.Form):
        description = forms.CharField(label='Optional description:', max_length=255, help_text='(e.g. Southbound)', required=False)
        if not phaseTypeObject.preGreenTimeConfigurable:
            hidden = forms.HiddenInput
            if phaseTypeObject.preGreenTime > 0:
                fixedItems.append((phaseTypeObject.preGreenName, phaseTypeObject.preGreenTime))
        else:
            hidden = None
        preGreen = forms.IntegerField(label=phaseTypeObject.preGreenName, initial = phaseTypeObject.preGreenTime, widget=hidden)

        if not phaseTypeObject.greenConfigurable:
            hidden = forms.HiddenInput
            if phaseTypeObject.greenMin > 0:
                fixedItems.append((phaseTypeObject.greenName, phaseTypeObject.greenMin))            
        else:
            hidden = None
        green = forms.IntegerField(label='Min ' + phaseTypeObject.greenName, initial = phaseTypeObject.greenMin, widget=hidden)
        
        if not phaseTypeObject.postGreenConfigurable:
            hidden = forms.HiddenInput
            if phaseTypeObject.postGreenTime > 0:
                fixedItems.append((phaseTypeObject.postGreenName, phaseTypeObject.postGreenTime))
        else:
            hidden = None
        postGreen = forms.IntegerField(label=phaseTypeObject.postGreenName, initial = phaseTypeObject.postGreenTime, widget=hidden)

    if request.method == 'POST':
        form = phaseDetailsForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            preGreen = form.cleaned_data['preGreen']
            green = form.cleaned_data['green']
            postGreen = form.cleaned_data['postGreen']
            siteObject.phases.newPhase(letter, countryObject.phaseType(phaseType), greenMin=green, 
            postGreenTime=postGreen, preGreenTime=preGreen, description=description)
            writeBackSiteToXml(siteRecord, siteObject) 
            next_url = siteRecord.get_absolute_url() + 'phases/'
            return HttpResponseRedirect(next_url)
    else:
        form = phaseDetailsForm() # An unbound form
    siteHtml = getSiteHtml(siteRecord)
    return render_to_response('forms/add-phases.html', locals())

def stagesAdd(request, year, month, day, slug, stageName):
    siteRecord = siteRecordFilter(year, month, day, slug)
    if siteRecord is False:
        return HttpResponseRedirect('/sites/error/')
    if siteRecord.locked:
        return HttpResponseRedirect(siteRecord.get_absolute_url_report())        
    siteObject, countryObject = getSiteObject(siteRecord)
    currentPhases = listToTupleChoices(siteObject.phases.phaseListLetters())
    stageObject = siteObject.stages.stage(stageName)
    if not stageObject:
        currentPhasesInStage = []
    else:
        currentPhasesInStage =  stageObject.listPhaseNames()
    class stageDetailsForm(forms.Form):
        phasesInStage = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, 
                                                  label="", choices=currentPhases, 
                                                  initial = currentPhasesInStage)
    if request.method == 'POST':
        form = stageDetailsForm(request.POST)
        if form.is_valid():
            phasesInStage = form.cleaned_data['phasesInStage']
            if not stageObject:
                stageObject = siteObject.stages.newStage(stageName)
            phases = []
            for phaseLetter in phasesInStage:
                phases.append(siteObject.phases.phase(phaseLetter))
            stageObject.phases = phases
            writeBackSiteToXml(siteRecord, siteObject) 
            next_url = siteRecord.get_absolute_url() + 'stages/'
            return HttpResponseRedirect(next_url)
    else:
        form = stageDetailsForm()
    siteHtml = getSiteHtml(siteRecord)
    return render_to_response('forms/add-stages.html', locals())

def diagramEdit(request, year, month, day, slug, diagramIndex):
    siteRecord = siteRecordFilter(year, month, day, slug)
    if siteRecord is False:
        return HttpResponseRedirect('/sites/error/')
    if siteRecord.locked:
        return HttpResponseRedirect(siteRecord.get_absolute_url_report())        
    siteObject, countryObject = getSiteObject(siteRecord)    
    currentDiagrams = siteObject.listDiagrams()
    
    addDiagramText = 'Add Movement'
    deleteDiagramText = 'Delete Movement '
    doneDiagramText = 'Finish Editing Diagram'

    try:
        diagram = siteObject.requiredDiagrams[int(diagramIndex)]
    except:
        return HttpResponseRedirect('../../')

    currentStages = siteObject.stages.listStageNames()
    stageChoices = listToTupleChoices(currentStages)
    if diagram.cycleTime >0:
        timeChoices = listToTupleChoices(range(0,diagram.cycleTime))
        currentMovements = diagram.movementsList()
    else:
        timeChoices = listToTupleChoices(["0"])

    class newMovementForm(forms.Form):
        timeSeconds = forms.ChoiceField(choices=timeChoices, label="At time:") 
        toStageName = forms.ChoiceField(choices=stageChoices, label="Move to stage:")
    
    if request.method == 'POST':
        if request.POST.has_key(doneDiagramText):
            next_url =  '../../'
            return HttpResponseRedirect(next_url)
        if request.POST.has_key(deleteDiagramText):
            movementText = request.POST[deleteDiagramText].lstrip(deleteDiagramText)
            diagram.movementsDelete(str(movementText))
            # Set start stage
            diagram.startEqualLastMovement()
            writeBackSiteToXml(siteRecord, siteObject) 
            form = newMovementForm() # An unbound form
        if request.POST.has_key(addDiagramText):
            form = newMovementForm(request.POST) # A bound form
            if form.is_valid(): # All validation rules pass
                try:
#                if True:
                    timeSeconds = form.cleaned_data['timeSeconds']
                    toStageName = form.cleaned_data['toStageName']
                    movementObject = libdetermine.requiredDiagramMovementClass(timeSeconds, toStageName)
                    diagram.movements.append(movementObject)
                    # Set start stage
                    diagram.startEqualLastMovement()
                    writeBackSiteToXml(siteRecord, siteObject)
                except:
                    pass
        currentMovements = diagram.movementsList()
    else:
        form = newMovementForm() # An unbound form

    diagramHtml = diagram.diagramsHtml()    
    siteHtml = getSiteHtml(siteRecord)
    return render_to_response('forms/diagram-edit.html', locals())

def report(request, year, month, day, slug):
    siteRecord = siteRecordFilter(year, month, day, slug)
    if not siteRecord:
        return HttpResponseRedirect('/sites/error/')
    siteObject, countryObject = getSiteObject(siteRecord)

    siteHtml = getSiteHtml(siteRecord)
    previousUrl = '../diagrams/'
    previousName = 'Diagrams'
    return render_to_response('forms/report.html', locals())


def reportPdf(request, year, month, day, slug, pdfType):
    siteRecord = siteRecordFilter(year, month, day, slug)
    if siteRecord is False:
        return HttpResponseRedirect('/sites/error/')
    
    from subprocess import *
    
# if site.xml is newer than report.xml
    siteObject, countryObject = getSiteObject(siteRecord)    
    report = libdetermine.generateReport(countryObject, siteObject)
    reportXML = siteRecord.get_report_xml_filename_full()
    xsl = siteRecord.get_site_xslt_report_full()
    pdf = siteRecord.get_report_pdf_filename_full()

    f=open(reportXML, 'w')
    f.write(report.xml())
    f.close()


    if pdfType == 'full':
        # Ugly code - Do something about it!
        tmpReport = tempfile.NamedTemporaryFile(suffix='dj-dt-')
        tmpXMLps = tempfile.NamedTemporaryFile(suffix='-dj-dt.ps')
        tmpXMLpdf = tempfile.NamedTemporaryFile(suffix='-dj-dt.pdf')
        tmpReportPdf = tempfile.NamedTemporaryFile(suffix='dj-dt.pdf')
        tmpSiteHtml = tempfile.NamedTemporaryFile(suffix='dj-dt.html')
                
        c = ["enscript", "-5", "-p", tmpXMLps.name, "-b", siteRecord.title, '--font=Courier6', "--highlight=html", 
        '--landscape', '--color', '--borders', '--media=A3',  '--title="XML"', 
        "--header='$n||Page $% of $='", reportXML ]
        enscript = Popen(c, stdout=PIPE)
        enscript.wait()
        
        pstopdf = Popen(["ps2pdf", tmpXMLps.name, tmpXMLpdf.name], stdout=PIPE)
        pstopdf.wait()
        
#        siteHtml = getSiteHtml(siteRecord)
#        tmpSiteHtml.write(siteHtml)
        xmlstarlet = Popen(["xmlstarlet", "tr", siteRecord.get_site_xslt_full(), siteRecord.get_xml_filename_full()], stdout=tmpSiteHtml)
        print "hi"

        xmlstarlet = Popen(["xmlstarlet", "tr", xsl, reportXML], stdout=PIPE)
        wkhtmltopdf = Popen(["wkhtmltopdf", "--page-size", "A3", "--orientation", 
        "Landscape", "-", tmpSiteHtml.name, tmpReportPdf.name], stdin=xmlstarlet.stdout, stdout=PIPE)
        wkhtmltopdf.wait()
    
        final = Popen(["pdftk", tmpReportPdf.name, tmpXMLpdf.name, "cat", "output", pdf], stdout=PIPE)
        final.wait()
        pdf_data = open(pdf, "rb").read()
        response = HttpResponse(pdf_data, mimetype='application/pdf')
#    if pdfType == 'simple':
    else:
        xmlstarlet = Popen(["xmlstarlet", "tr", xsl, reportXML], stdout=PIPE)
        wkhtmltopdf = Popen(["wkhtmltopdf", "--page-size", "A3", "--orientation", 
        "Landscape", "-", "-"], stdin=xmlstarlet.stdout, stdout=PIPE)
        response = HttpResponse(wkhtmltopdf.stdout, mimetype='application/pdf')

    filename = 'attachment; filename=' + slug + '.pdf'
    response['Content-Disposition'] = filename

    return response

#pdftk /tmp/report-test-simple-site-25.pdf dump_data output | grep "NumberOfPages" | cut -d\  -f 2


# endif
# from subprocess import *
#>>> p1 = Popen(["df"], stdout=PIPE)
#>>> p2 = Popen(["grep", "tmpfs"], stdin=p1.stdout, stdout=PIPE)
#>>> output = p2.communicate()[0]
#>>> print output

    # xmlstarlet report with stylesheet produing (html) to a PIPE
    # xmlstarlet tr  /home/bms/work/legal/digrams/traffic_signals_report.xsl /home/bms/work/legal/digrams/26-000146_corrected.xml.xml 
    # wkhtmltopdf to PIPE
    # wkhtmltopdf - - 2>/dev/null
    # return pip 
    
    
def form(request):
    context = dict(post=dict(), results=list())
# form.cleaned_data
    if request.POST:
        cleaned_data = []
        for k in request.POST: 
            cleaned_data.append(k)
            cleaned_data.append(request.POST[k])
            cleaned_data.append(dir(request.POST[k]))

        return render_to_response('forms.html', {'cleaned_data': cleaned_data,}) 


#        for name in ('save', 'id_save', 'Save', 'cancel', 'id_cancel','Cancel'):
#            context['results'].append("request.POST.has_key('%s') == %s" % (name,request.POST.has_key(name))) 
    return render_to_response('forms.html', context,) 
