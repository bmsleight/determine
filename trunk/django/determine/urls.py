from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

base = r'^sites/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/'
basePhase = base + r'phases/$'
basePhaseAdd = base + r'phases/add/(?P<letter>[A-Za-z]+)/(?P<phaseType>[^/]+)/$'
baseStage = base + r'stages/$'
baseStageAdd = base + r'stages/(?P<stageName>[^/]+)/$'

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
    

    (r'^form/$', 'determine.web.views.form'), 
    (r'^admin/(.*)', admin.site.root),
)
