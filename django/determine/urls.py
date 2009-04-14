from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

base = r'^sites/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/'
basePhase = base + r'phases/$'
basePhaseAdd = base + r'phases/add/(?P<letter>[A-Za-z]+)/(?P<phaseType>[^/]+)/$'
baseStage = base + r'stages/$'
baseStageAdd = base + r'stages/(?P<stageName>[^/]+)/$'
baseIntergreen = base + r'intergreens/$'
baseDelays = base + r'delays/$'
baseDiagrams = base + r'diagrams/$'
basediagramEdit = base + r'diagrams/edit/(?P<diagramNumber>\d{1,2})$'

urlpatterns = patterns('',
    # Example:
    # (r'^determine/', include('determine.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^new-site/', 'determine.web.views.newSite'),
    (basePhase, 'determine.web.views.phases'),
    (basePhaseAdd, 'determine.web.views.phasesAdd'),
    (baseStage, 'determine.web.views.stages'),
    (baseStageAdd, 'determine.web.views.stagesAdd'),
    (baseIntergreen, 'determine.web.views.intergreens'),
    (baseDelays, 'determine.web.views.delays'),
    # List current diagrams Option to add a digram or edit exisiting diagrams
    #  each diagram has an edit button with the diagram text listed
    (baseDiagrams, 'determine.web.views.diagrams'),
    # Add a new diagram - with a link when finished to ../
#    (basediagramAdd, 'determine.web.views.diagramAdd'),
    # Scrub the above - just add a new diagram then use the edit feature
    # Edit an existing diagram - with a link when finished to ../
#    (basediagramEdit, 'determine.web.views.diagramEdit'),




#baseDelays
    (r'^form/$', 'determine.web.views.form'), 
    (r'^admin/(.*)', admin.site.root),
)

# xmlstarlet tr  /home/bms/work/legal/digrams/traffic_signals_report.xsl /home/bms/work/legal/digrams/26-000146_corrected.xml.xml | ./wkhtmltopdf - - 2>/dev/null
# enscript -1 -p list.html -b header -h --highlight=html --color  -w html --title="XML" ./26-000146_corrected.xml.xml

