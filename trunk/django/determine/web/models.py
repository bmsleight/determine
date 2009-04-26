from django.db import models
from django.conf import settings

import datetime

COUNTRY_CONFIG = (
   ('uk.xml', 'UK'),
)


class SignalSite(models.Model):
    title = models.CharField(max_length=200)
#    siteXML = models.FileField(upload_to='sites/%Y/%b/%d', blank=True)
    slug = models.SlugField(unique_for_date='publish_date',help_text='Automatically built from the title.',max_length=200)
    publish_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    country = models.CharField(max_length=20, choices=COUNTRY_CONFIG, default='UK')
    locked = models.BooleanField(default=False)

    def __str__(self):
                return self.title
    class Meta:
        ordering = ["-publish_date"]


    def get_absolute_url(self):
        return "/sites/%s/%s/" % (self.publish_date.strftime("%Y/%b/%d").lower(), self.slug)
    def get_absolute_url_report(self):
        return "/sites/%s/%s/report/" % (self.publish_date.strftime("%Y/%b/%d").lower(), self.slug)


    def get_xml_filename(self):
        return str("sites/%s/%s.xml" % (self.publish_date.strftime("%Y/%b/%d").lower(), self.slug))
    def get_xml_filename_full(self):
        return str(settings.MEDIA_ROOT + "sites/%s/%s.xml" % (self.publish_date.strftime("%Y/%b/%d").lower(), self.slug))
    def get_xml_dirs(self):
        return str("sites/%s/" % (self.publish_date.strftime("%Y/%b/%d").lower()))
    def get_xml_dirs_full(self):
        return str(settings.MEDIA_ROOT + "sites/%s/" % (self.publish_date.strftime("%Y/%b/%d").lower()))
    def get_report_xml_filename_full(self):
        return str(settings.MEDIA_ROOT + "sites/%s/%s_report.xml" % (self.publish_date.strftime("%Y/%b/%d").lower(), self.slug))
    def get_report_pdf_filename_full(self):
        return str(settings.MEDIA_ROOT + "sites/%s/%s.pdf" % (self.publish_date.strftime("%Y/%b/%d").lower(), self.slug))
    def get_country_config_xml_full(self):
        return str(settings.MEDIA_ROOT + "country-configs/%s" % (self.country))
    def get_site_xslt_full(self):
        return str(settings.MEDIA_ROOT + "xslt/traffic_signals_site.xsl")
    def get_site_xslt_report_full(self):
        return str(settings.MEDIA_ROOT + "xslt/traffic_signals_report.xsl")

# Create your models here.
