#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#   determine - generate traffic signal timing diagrams to determine green running time. 
#   Copyright (C) Brendan M. Sleight, et al. <determine@barwap.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import sys
import tempfile
import shutil
import glob
import gtk
import gtkmozembed
import gobject


# Multiple os'es have data files stores in lots of locations
if os.path.isfile( os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), "glade/determine.xml" ) ):
    # Local testing
    DATA_PATH = os.path.dirname( os.path.realpath( __file__ ) ) 
    sys.path.append( os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), "libdetermine" ) )
elif os.path.isfile("/usr/share/determine/glade/determine.xml"):
    # "GNU/Linux, *nix"
    DATA_PATH = "/usr/share/determine/"
elif os.path.isfile("c:\\windows\\determine\\glade\\determine.xml"):
    # "Windows"
    DATA_PATH = "c:\\windows\\determine\\"
   
# Get libdetermine
try:
    import libdetermine
except:
    print "Error importing libdetermine"
    sys.exit(1)


REPORT_NAME = "/report.xml"
REPORT_TRANS = "/traffic_signals_report.xsl"
SITE_NAME = "/site.xml"
SITE_TRANS = "/traffic_signals_site.xsl"

def comboFromList(textList, comboType="comboBox"):
    if comboType=="comboBoxEntry":
        combobox = gtk.combo_box_entry_new_text()
    else:
        combobox = gtk.combo_box_new_text()
    for text in textList:
        combobox.append_text(text)
    return combobox
    

class DetermineGUI:
    # When our window is destroyed, we want to break out of the GTK main loop. 
    # We do this by calling gtk_main_quit(). We could have also just specified 
    # gtk_main_quit as the handler in Glade!
    def on_main_window_destroy(self, widget, data=None):
        shutil.rmtree(self.tmpDir)
        gtk.main_quit()

    # Called when the user clicks the 'New' menu.  
    def on_menu_new_activate(self, menuitem, data=None):
        # Need to ave?
        # FIXME
        self.site = libdetermine.siteClass()
        self.update_site_xml()

    # Called when the user clicks the 'Open' menu.   
    def on_menu_open_activate(self, menuitem, data=None):
#        if self.check_for_save(): self.on_save_menu_item_activate(None, None)        
        self.siteFileName = self.get_open_filename()
        if self.siteFileName: 
            self.site = libdetermine.parseSiteConfig(self.siteFileName, self.countryConfig)
            self.update_site_xml()

    # called when use clicks 'Save'
    def on_menu_save_activate(self, menuitem, data=None):
        if self.siteFileName == None:
            self.siteFileName = self.get_save_filename("Save site as ...")
        if self.siteFileName != None:
            self.save_file(self.siteFileName, self.tmpDir + SITE_NAME, self.tmpDir + SITE_TRANS)

    # Called when user clicks 'Save As'
    def on_menu_save_as_activate(self, menuitem, data=None):
        self.siteFileName = self.get_save_filename("Save site as ...")
        if self.siteFileName != None:
            self.save_file(self.siteFileName, self.tmpDir + SITE_NAME, self.tmpDir + SITE_TRANS)

    # called when use clicks 'Save'
    def on_menu_save_report_activate(self, menuitem, data=None):
        if self.reportFileName == None:
            self.reportFileName = self.get_save_filename("Save site as ...")
        if self.reportFileName != None:
            self.save_file(self.reportFileName, self.tmpDir + REPORT_NAME, self.tmpDir + REPORT_TRANS)

    # Called when user clicks 'Save Report As'
    def on_menu_save_report_as_activate(self, menuitem, data=None):
        self.reportFileName = self.get_save_filename("Save report as ...")
        if self.reportFileName != None:
            self.save_file(self.reportFileName, self.tmpDir + REPORT_NAME, self.tmpDir + REPORT_TRANS)

    def on_view_site_activate(self, menuitem, data=None):
        self.update_site_xml()

    def on_view_report_activate(self, menuitem, data=None):
        self.dialog_waiting_diagram = self.builder.get_object("dialog_waiting_diagram")
        self.progressbar_waiting_diagram = self.builder.get_object("progressbar_waiting_diagram")
        # Will take a while to view report - see progress bar
        self.dialog_waiting_diagram.show()
        self.report = libdetermine.generateReport(self.countryConfig, self.site, gtk, self.progressbar_waiting_diagram)
        reportFile = self.tmpDir + REPORT_NAME
        f=open(reportFile, 'w')
        f.write(self.report.xml())
        f.close()
        self.mozillaWidget.load_url(reportFile)
        self.dialog_waiting_diagram.hide()

    # Select menuitem address
    def on_menuitem_address_activate(self, menuitem, data=None):
        self.entry_site_address = self.builder.get_object("entry_site_address")
        self.entry_site_address.set_text(self.site.address)
        print "Hello ?"
        self.dialog_set_site_address.show()
        
    def on_button_ok_site_address_clicked(self, button, data=None):
        self.site.address = self.entry_site_address.get_text()
        self.update_site_xml()
        self.dialog_set_site_address.hide()
    def on_button_cancel_site_address_clicked(self, button, data=None):
        self.dialog_set_site_address.hide()

    def on_menuitem_add_phases_activate(self, menuitem, data=None):
        self.dialog_add_phase = self.builder.get_object("dialog_add_phase")
        # Add phase types
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        frame_phase_letter = self.builder.get_object("frame_phase_letter")
        frame_phase_letter.add(comboFromList(letters, comboType="comboBoxEntry"))
        # Add phase types
        frame_phase_type = self.builder.get_object("frame_phase_type")
        frame_phase_type.add(comboFromList(self.countryConfig.listNames()))
        frame_phase_type.get_children()[0].connect('changed', self.changed_phase_type)
        self.dialog_add_phase.show_all()

    def changed_phase_type(self, combobox):
        spinbutton_post_green_time = self.builder.get_object("spinbutton_post_green_time")
        postGreenConfigurable = self.countryConfig.phaseType(combobox.get_active_text()).postGreenConfigurable
        spinbutton_post_green_time.set_sensitive(postGreenConfigurable)
        if not postGreenConfigurable:
            spinbutton_post_green_time.set_value(0)

        spinbutton_pre_green_time = self.builder.get_object("spinbutton_pre_green_time")
        preGreenTimeConfigurable = self.countryConfig.phaseType(combobox.get_active_text()).preGreenTimeConfigurable
        spinbutton_pre_green_time.set_sensitive(preGreenTimeConfigurable)
        if not preGreenTimeConfigurable:
            spinbutton_pre_green_time.set_value(0)

    def on_button_add_phase_clicked(self, button, data=None):
        phase_letter = self.builder.get_object("frame_phase_letter").get_children()[0].get_active_text()
        phase_type = self.builder.get_object("frame_phase_type").get_children()[0].get_active_text()
        mingreen = self.builder.get_object("spinbutton_mingreen").get_value_as_int()
        pre_green_time = self.builder.get_object("spinbutton_pre_green_time").get_value_as_int()
        post_green_time = self.builder.get_object("spinbutton_post_green_time").get_value_as_int()
        description = self.builder.get_object("entry_phase_description").get_text()
        self.site.phases.newPhase(phase_letter, self.countryConfig.phaseType(phase_type), greenMin=mingreen, postGreenTime=post_green_time,
                                  preGreenTime=pre_green_time, description=description)
        self.builder.get_object("frame_phase_letter").get_children()[0].destroy()
        self.builder.get_object("frame_phase_type").get_children()[0].destroy()
        self.update_site_xml()
        self.dialog_add_phase.hide()

    def on_button_cancel_add_phase_clicked(self, button, data=None):
        self.builder.get_object("frame_phase_letter").get_children()[0].destroy()
        self.builder.get_object("frame_phase_type").get_children()[0].destroy()
        self.dialog_add_phase.hide()

    def on_dialog_add_phase_delete_event(self, widget, data=None):
        self.builder.get_object("frame_phase_letter").get_children()[0].destroy()
        self.builder.get_object("frame_phase_type").get_children()[0].destroy()
        self.dialog_add_phase.hide()
        return True

    def on_menuitem_remove_phases_activate(self, menuitem, data=None):
        self.dialog_remove_phase = self.builder.get_object("dialog_remove_phase")
        frame_remove_phase_letter = self.builder.get_object("frame_remove_phase_letter")
        frame_remove_phase_letter.add(comboFromList(self.site.phases.phaseListLetters()))
        self.dialog_remove_phase.show_all()

    def on_button_cancel_remove_phase_clicked(self, button, data=None):
        frame_remove_phase_letter = self.builder.get_object("frame_remove_phase_letter")
        frame_remove_phase_letter.get_children()[0].destroy()
        self.dialog_remove_phase.hide()

    def on_dialog_remove_phase_delete_event(self, widget, data=None):
        frame_remove_phase_letter = self.builder.get_object("frame_remove_phase_letter")
        frame_remove_phase_letter.get_children()[0].destroy()
        self.dialog_remove_phase.hide()
        return True

    def on_button_remove_phase_clicked(self, button, data=None):
        phase_remove_letter = self.builder.get_object("frame_remove_phase_letter").get_children()[0].get_active_text()
        phase_remove = self.site.phases.phase(phase_remove_letter)
        self.site.phases.phases.remove(phase_remove)
        frame_remove_phase_letter = self.builder.get_object("frame_remove_phase_letter")
        frame_remove_phase_letter.get_children()[0].destroy()
        self.update_site_xml()
        self.dialog_remove_phase.hide()

    def on_menu_add_stage_activate(self, menuitem, data=None):
        self.dialog_add_stage = self.builder.get_object("dialog_add_stage")
        label_add_stage_current_stages = self.builder.get_object("label_add_stage_current_stages")
        label_add_stage_current_stages.set_text(self.site.stages.text())
        self.dialog_add_stage.show()

    def on_button_cancel_add_stage_clicked(self, button, data=None):
        self.dialog_add_stage.hide()

    def on_button_add_stage_clicked(self, button, data=None):
        new_stage_number = self.builder.get_object("spinbutton_add_stage").get_value_as_int()
        self.site.stages.newStage(new_stage_number)
        self.update_site_xml()
        self.dialog_add_stage.hide()
        self.on_menu_edit_stage_activate(self, button)

    def on_menu_remove_stage_activate(self, menuitem, data=None):
        self.dialog_remove_stage = self.builder.get_object("dialog_remove_stage")
        frame_remove_stage_which_stage = self.builder.get_object("frame_remove_stage_which_stage")
        frame_remove_stage_which_stage.add(comboFromList(self.site.stages.listStageNames()))
        self.dialog_remove_stage.show_all()

    def on_dialog_remove_stage_delete_event(self, widget, data=None):
        self.builder.get_object("frame_remove_stage_which_stage").get_children()[0].destroy()
        self.dialog_remove_stage.hide()
        return True

    def on_button_remove_stage_cancel_clicked(self, button, data=None):
        self.builder.get_object("frame_remove_stage_which_stage").get_children()[0].destroy()
        self.dialog_remove_stage.hide()

    def on_button_remove_stage_ok_clicked(self, button, data=None):
        stage_selected = None
        stage_number = self.builder.get_object("frame_remove_stage_which_stage").get_children()[0].get_active_text()
        try:
            stage_selected = self.site.stages.stage(stage_number)
        except:
            pass
        if stage_selected:
            self.site.stages.stages.remove(stage_selected)
        self.builder.get_object("frame_remove_stage_which_stage").get_children()[0].destroy()
        self.update_site_xml()
        self.dialog_remove_stage.hide()


    def on_menu_edit_stage_activate(self, menuitem, data=None):
        self.dialog_edit_stage = self.builder.get_object("dialog_edit_stage")
        label_edit_stage_current_stages = self.builder.get_object("label_edit_stage_current_stages")
        label_edit_stage_current_stages.set_text(self.site.stages.text())
        frame_edit_stage_which_stage = self.builder.get_object("frame_edit_stage_which_stage")
        frame_edit_stage_which_stage.add(comboFromList(self.site.stages.listStageNames()))
        frame_edit_stage_which_phase = self.builder.get_object("frame_edit_stage_which_phase")
        frame_edit_stage_which_phase.add(comboFromList(self.site.phases.phaseListLetters()))
        self.dialog_edit_stage.show_all()

    def on_button_edit_stage_remove_phase_clicked(self, button, data=None):
        phase_letter = self.builder.get_object("frame_edit_stage_which_phase").get_children()[0].get_active_text()
        phase_selected = self.site.phases.phase(phase_letter)
        stage_number = self.builder.get_object("frame_edit_stage_which_stage").get_children()[0].get_active_text()
        stage_selected = self.site.stages.stage(stage_number)
        if phase_selected in stage_selected.phases:
            stage_selected.phases.remove(phase_selected)
        label_edit_stage_current_stages = self.builder.get_object("label_edit_stage_current_stages")
        label_edit_stage_current_stages.set_text(self.site.stages.text())

    # Should be clever and combine the add remove in one function. Ho hum...
    def on_button_edit_stage_remove_ph_clicked(self, button, data=None):
        phase_letter = self.builder.get_object("frame_edit_stage_which_phase").get_children()[0].get_active_text()
        phase_selected = self.site.phases.phase(phase_letter)
        stage_number = self.builder.get_object("frame_edit_stage_which_stage").get_children()[0].get_active_text()
        stage_selected = self.site.stages.stage(stage_number)
        if phase_selected not in stage_selected.phases:
            stage_selected.phases.append(phase_selected)
        label_edit_stage_current_stages = self.builder.get_object("label_edit_stage_current_stages")
        label_edit_stage_current_stages.set_text(self.site.stages.text())

    def on_button_edit_stages_ok_clicked(self, button, data=None):
        self.builder.get_object("frame_edit_stage_which_stage").get_children()[0].destroy()
        self.builder.get_object("frame_edit_stage_which_phase").get_children()[0].destroy()
        self.update_site_xml()
        self.dialog_edit_stage.hide()

    def on_dialog_edit_stage_delete_event(self, widget, data=None):
        self.builder.get_object("frame_edit_stage_which_stage").get_children()[0].destroy()
        self.builder.get_object("frame_edit_stage_which_phase").get_children()[0].destroy()
        self.update_site_xml()
        self.dialog_edit_stage.hide()
        return True

    def on_menuitem_edit_intergreens_activate(self, menuitem, data=None):
        self.dialog_edit_intergreens = self.builder.get_object("dialog_edit_intergreens")
        frame_edit_intergreens = self.builder.get_object("frame_edit_intergreens")
        total_phases = len(self.site.phases.phases)
        self.intergreen_spinbutton = []
        if total_phases >0:
            table_intergreen = gtk.Table(total_phases +1 , total_phases +1, True)
            label_array = []
            for row in range(0, total_phases +1):
                for col in range(0, total_phases +1):
                   if row==0 and col==0:
                       label_array.append(gtk.Label(" "))
                   elif row==0:
                       label_array.append(gtk.Label(self.site.phases.phases[col-1].letter))
                   elif col==0:
                       label_array.append(gtk.Label(self.site.phases.phases[row-1].letter))
                   elif col==row:
                       label_array.append(gtk.Label("X"))
                   else:
                       from_phase = self.site.phases.phases[row-1]
                       from_phase_letter = self.site.phases.phases[col-1].letter
                       intergreen_value = from_phase.intergreenFrom(from_phase_letter)
                       adjustment = gtk.Adjustment(intergreen_value,0,255,1,1,0)
                       self.intergreen_spinbutton.append(gtk.SpinButton(adjustment, 0.0, 0))
                   if row==0 or col==0 or col==row:
                       table_intergreen.attach(label_array[len(label_array)-1], row, row+1, col, col+1)
                   else:
                       table_intergreen.attach(self.intergreen_spinbutton[len(self.intergreen_spinbutton)-1], row, row+1, col, col+1)
            frame_edit_intergreens.add(table_intergreen)
        self.dialog_edit_intergreens.show_all()
        
    def on_button_edit_intergreens_cancel_clicked(self, button, data=None):
        self.builder.get_object("frame_edit_intergreens").get_children()[0].destroy()
        self.dialog_edit_intergreens.hide()

    def on_dialog_edit_intergreens_delete_event(self, widget, data=None):
        self.builder.get_object("frame_edit_intergreens").get_children()[0].destroy()
        self.dialog_edit_intergreens.hide()
        return True

    def on_button_edit_intergreens_ok_clicked(self, widget, data=None):
        total_phases = len(self.site.phases.phases)
        if total_phases >0:
            index = 0
            for row in range(0, total_phases):
                for col in range(0, total_phases):
                   if col!=row:
                       from_phase = self.site.phases.phases[row]
                       from_phase_letter = self.site.phases.phases[col].letter
                       old_intergreen_value = from_phase.intergreenFrom(from_phase_letter)
                       new_intergreen_value = self.intergreen_spinbutton[index].get_value_as_int()
                       if new_intergreen_value != old_intergreen_value:
                           from_phase.setIntergreenFrom(from_phase_letter,new_intergreen_value) 
                       index = index + 1
        self.update_site_xml()
        self.builder.get_object("frame_edit_intergreens").get_children()[0].destroy()
        self.dialog_edit_intergreens.hide()

    def on_menuitem_edit_phase_delays_activate(self, menuitem, data=None):
        self.dialog_edit_phase_delays = self.builder.get_object("dialog_edit_phase_delays")
        label_current_phase_delays = self.builder.get_object("label_current_phase_delays")
        label_current_phase_delays.set_text(self.site.phases.phaseDelayText())
        frame_phase_delay_phase_remove = self.builder.get_object("frame_phase_delay_phase_remove")
        frame_phase_delay_phase_remove.add(comboFromList(self.site.phases.phaseListLetters()))
        frame_phase_delay_phase_add = self.builder.get_object("frame_phase_delay_phase_add")
        frame_phase_delay_phase_add.add(comboFromList(self.site.phases.phaseListLetters()))
        frame_phase_delay_phase_stages_f = self.builder.get_object("frame_phase_delay_phase_stages_f")
        frame_phase_delay_phase_stages_f.add(comboFromList(self.site.stages.listStageNames()))
        frame_phase_delay_phase_stages_to = self.builder.get_object("frame_phase_delay_phase_stages_to")
        frame_phase_delay_phase_stages_to.add(comboFromList(self.site.stages.listStageNames()))
        self.dialog_edit_phase_delays.show_all()

    def on_dialog_edit_phase_delays_delete_event(self, widget, data=None):
        self.builder.get_object("frame_phase_delay_phase_remove").get_children()[0].destroy()
        self.builder.get_object("frame_phase_delay_phase_add").get_children()[0].destroy()
        self.builder.get_object("frame_phase_delay_phase_stages_f").get_children()[0].destroy()
        self.builder.get_object("frame_phase_delay_phase_stages_to").get_children()[0].destroy()
        self.dialog_edit_phase_delays.hide()
        return True

    def on_button_edit_phase_delay_ok_clicked(self, button, data=None):
        self.builder.get_object("frame_phase_delay_phase_remove").get_children()[0].destroy()
        self.builder.get_object("frame_phase_delay_phase_add").get_children()[0].destroy()
        self.builder.get_object("frame_phase_delay_phase_stages_f").get_children()[0].destroy()
        self.builder.get_object("frame_phase_delay_phase_stages_to").get_children()[0].destroy()
        self.dialog_edit_phase_delays.hide()

#    def button_edit_phase_delays_add(self, button, data=None):

    def on_menuitem_remove_diagram_activate(self, menuitem, data=None):
        self.dialog_remove_diagram = self.builder.get_object("dialog_remove_diagram")
        frame_remove_diagram_diagrams = self.builder.get_object("frame_remove_diagram_diagrams")
        frame_remove_diagram_diagrams.add(comboFromList(self.site.listDiagrams()))
        # label_diagram_text
        label_diagram_text = self.builder.get_object("label_diagram_text")
        label_diagram_text.set_text(self.site.diagramsText())
        self.dialog_remove_diagram.show_all()

    def on_dialog_remove_diagram_delete_event(self, widget, data=None):
        self.builder.get_object("frame_remove_diagram_diagrams").get_children()[0].destroy()
        self.update_site_xml()
        self.dialog_remove_diagram.hide()
        return True

    def on_button_diagram_remove_ok_clicked(self, button, data=None):
        self.builder.get_object("frame_remove_diagram_diagrams").get_children()[0].destroy()
        self.update_site_xml()
        self.dialog_remove_diagram.hide()

    def on_button_diagram_remove_remove_clicked(self, button, data=None):
        diagram_title = self.builder.get_object("frame_remove_diagram_diagrams").get_children()[0].get_active_text()
        diagram = self.site.diagram(diagram_title)
        self.site.requiredDiagrams.remove(diagram)
        label_diagram_text = self.builder.get_object("label_diagram_text")
        label_diagram_text.set_text(self.site.diagramsText())

    def on_menuitem_add_diagram_activate(self, menuitem, data=None):
        self.dialog_add_diagram = self.builder.get_object("dialog_add_diagram")
        self.newDiagram = libdetermine.requiredDiagramClass("Default Title", 96, self.site.stages.stages[0].stageName, 1)
        frame_add_diagram_starting_stage = self.builder.get_object("frame_add_diagram_starting_stage")
        frame_add_diagram_starting_stage.add(comboFromList(self.site.stages.listStageNames()))
        frame_add_diagram_moveto_stage = self.builder.get_object("frame_add_diagram_moveto_stage")
        frame_add_diagram_moveto_stage.add(comboFromList(self.site.stages.listStageNames()))
        label_new_diagram = self.builder.get_object("label_new_diagram")
        label_new_diagram.set_text(self.newDiagram.diagramsText())
        self.dialog_add_diagram.show_all()

    def on_dialog_add_diagram_delete_event(self, widget, data=None):
        self.builder.get_object("frame_add_diagram_starting_stage").get_children()[0].destroy()
        self.builder.get_object("frame_add_diagram_moveto_stage").get_children()[0].destroy()
        self.update_site_xml()
        self.dialog_add_diagram.hide()
        return True

    def on_button_add_diagram_cancel_clicked(self, button, data=None):
        self.builder.get_object("frame_add_diagram_starting_stage").get_children()[0].destroy()
        self.builder.get_object("frame_add_diagram_moveto_stage").get_children()[0].destroy()
        self.update_site_xml()
        self.dialog_add_diagram.hide()

    def on_button_add_diagram_add_clicked(self, button, data=None):
        self.builder.get_object("frame_add_diagram_starting_stage").get_children()[0].destroy()
        self.builder.get_object("frame_add_diagram_moveto_stage").get_children()[0].destroy()
        self.site.requiredDiagrams.append(self.newDiagram)
        self.update_site_xml()
        self.dialog_add_diagram.hide()

    def on_button_add_diagram_title_clicked(self, button, data=None):
        entry_diagram_add_title = self.builder.get_object("entry_diagram_add_title")
        self.newDiagram.title = entry_diagram_add_title.get_text()
        self.builder.get_object("label_new_diagram").set_text(self.newDiagram.diagramsText())

    def on_button_add_diagram_starting_stage_clicked(self, button, data=None):
        self.newDiagram.startingStageName = self.builder.get_object("frame_add_diagram_starting_stage").get_children()[0].get_active_text()
        self.builder.get_object("label_new_diagram").set_text(self.newDiagram.diagramsText())

    def on_button_add_diagram_cycle_time_clicked(self, button, data=None):
        self.newDiagram.cycleTime = self.builder.get_object("spinbutton_add_diagram_cycle_time").get_value_as_int()
        self.builder.get_object("label_new_diagram").set_text(self.newDiagram.diagramsText())

    def on_button_add_diagram_loop_clicked(self, button, data=None):
        self.newDiagram.loop = self.builder.get_object("spinbutton_add_diagram_loop").get_value_as_int()
        self.builder.get_object("label_new_diagram").set_text(self.newDiagram.diagramsText())

    def on_button_add_diagram_movement_clicked(self, button, data=None):
        timeSeconds = self.builder.get_object("spinbutton_add_diagram_at_time").get_value_as_int()
        toStageName = self.builder.get_object("frame_add_diagram_moveto_stage").get_children()[0].get_active_text()
        movement = libdetermine.requiredDiagramMovementClass(timeSeconds, toStageName)
        self.newDiagram.movements.append(movement)
        self.builder.get_object("label_new_diagram").set_text(self.newDiagram.diagramsText())


    # Called when the user clicks the 'About' menu. We use gtk_show_about_dialog() 
    # which is a convenience function to show a GtkAboutDialog. This dialog will
    # NOT be modal but will be on top of the main application window.    
    def on_menu_about_activate(self, menuitem, data=None):    
        if self.about_dialog: 
            self.about_dialog.present()
            return
        authors = [
        "Brendan M. Sleight <bms.determine@barwap.com>"
        ]
        about_dialog = gtk.AboutDialog()
        about_dialog.set_transient_for(self.main_window)
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("Determine")
        about_dialog.set_version("0.0.1")
        about_dialog.set_copyright("Copyright \xc2\xa9 2009 Brendan M. Sleight")
        about_dialog.set_website("http://www.????.com")
        about_dialog.set_comments("Generate traffic signal timing diagrams\n to determine green running times.")
        about_dialog.set_authors            (authors)
        about_dialog.set_logo_icon_name     (gtk.STOCK_ABOUT)
        # callbacks for destroying the dialog
        def close(dialog, response, editor):
            editor.about_dialog = None
            dialog.destroy()
        def delete_event(dialog, event, editor):
            editor.about_dialog = None
            return True
        about_dialog.connect("response", close, self)
        about_dialog.connect("delete-event", delete_event, self)
        self.about_dialog = about_dialog
        about_dialog.show()

    def update_site_xml(self):
        siteFile = self.tmpDir + SITE_NAME
        f=open(siteFile, 'w')
        f.write(self.site.xml())
        f.close()
        self.mozillaWidget.load_url(siteFile)

    # We call get_open_filename() when we want to get a filename to open from the
    # user. It will present the user with a file chooser dialog and return the 
    # filename or None.    
    def get_open_filename(self):        
        filename = None
        chooser = gtk.FileChooserDialog("Open File...", self.main_window,
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        
        response = chooser.run()
        if response == gtk.RESPONSE_OK: filename = chooser.get_filename()
        chooser.destroy()
        return filename

    def save_file(self, saveFileName, tmpfile, tmpTransform):
        # Addd a try except
        shutil.copyfile(tmpfile, saveFileName)
        dirname = os.path.dirname(saveFileName)
        basename = os.path.basename(tmpTransform)
        shutil.copyfile(tmpTransform, dirname + "/" + basename)



    def get_save_filename(self, title):
        filename = None
        chooser = gtk.FileChooserDialog(title, self.main_window,
                                        gtk.FILE_CHOOSER_ACTION_SAVE,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                                         gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        xmlFilter = gtk.FileFilter()
        xmlFilter.set_name("Determine files")
        xmlFilter.add_pattern("*.xml")
        chooser.add_filter(xmlFilter)
        response = chooser.run()
        if response == gtk.RESPONSE_OK: filename = chooser.get_filename()
        chooser.destroy()
        
        return filename + ".xml"


    def __init__(self):
        self.siteFileName = None
        self.reportFileName = None
        self.about_dialog = None
        self.tmpDir = tempfile.mkdtemp(prefix='tmp-determine-')
        
        self.site = libdetermine.siteClass()
        # Start with UK Signals - In future make this a stored option.
        self.countryConfig = libdetermine.parseCountryConfig(os.path.join(DATA_PATH, "./country-configs/uk.xml"))
        # Copy the stylesheets
        for xslt in glob.glob(DATA_PATH + "/xslt/*.xsl"):
            shutil.copy(xslt, self.tmpDir)


        # use GtkBuilder to build our interface from the XML file 
        try:
            self.builder = gtk.Builder()
            self.builder.add_from_file(os.path.join(DATA_PATH, "./glade/determine.xml")) 
        except:
            self.error_message("Failed to load UI XML file: determine.xml")
            sys.exit(1)

        # get the widgets which will be referenced in callbacks
        self.main_window = self.builder.get_object("main_window")
        self.mozilla_frame = self.builder.get_object("mozilla_frame")
        self.dialog_set_site_address = self.builder.get_object("dialog_set_site_address")

        # connect signals
        self.builder.connect_signals(self)

        # Set up mozilla frame
        self.mozillaWidget = gtkmozembed.MozEmbed()
        self.mozilla_frame.add(self.mozillaWidget)
        self.mozillaWidget.show()
        self.mozillaWidget.load_url(os.path.join(DATA_PATH, "./manual/index.html"))

        # Set master_window_size
        self.main_window.maximize()

    # Run main application window
    def main(self):
        self.main_window.show()
        gtk.main()

if __name__ == "__main__":
    determine = DetermineGUI()
    determine.main()

