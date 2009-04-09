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

import datetime
from lxml import etree


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
            next_url = siteRecord.get_absolute_url() + "phases/"
   
            # Step number 2..... better url than /thanks/
            return HttpResponseRedirect(next_url) # Redirect after POST
    else:
        form = NewSignalSiteForm() # An unbound form

    return render_to_response('forms/new-site.html', locals())


def siteRecordFilter(year, month, day, slug):
    MONTHS = ['dummy', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    startOfDay = datetime.datetime(int(year), MONTHS.index(month), int(day))
    endOfDay = startOfDay + datetime.timedelta(1)
    siteRecord = SignalSite.objects.filter(slug=slug)
    siteRecord = siteRecord.filter(publish_date__gte=startOfDay)
    siteRecord = siteRecord.filter(publish_date__lte=endOfDay)
    siteRecord = siteRecord.order_by('-publish_date')[0]
    return siteRecord

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

def phases(request, year, month, day, slug):
    siteRecord = siteRecordFilter(year, month, day, slug)
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
                    intergreenHtml = intergreenHtml + '<input type="text" name="' + inputName + '" id="ig" value="' + str(intergreen_value) + '" class="ig"/>'
                intergreenHtml = intergreenHtml + '</div>'
                intergreenHtml = intergreenHtml + "</td>"
            intergreenHtml = intergreenHtml + "</tr>"
        intergreenHtml = intergreenHtml + "</table>"


    siteHtml = getSiteHtml(siteRecord)
    nextUrl = '../stages/'
    nextName = 'Stages'
    previousUrl = '../stages/'
    previousName = 'Stages'
    return render_to_response('forms/intergreens.html', locals())

# phasesAdd
def phasesAdd(request, year, month, day, slug, letter, phaseType):
    siteRecord = siteRecordFilter(year, month, day, slug)
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
