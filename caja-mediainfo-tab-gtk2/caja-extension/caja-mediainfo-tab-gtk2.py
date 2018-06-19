#!/usr/bin/python
#coding: utf-8

try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

from gi.repository import Caja, GObject, Gtk

from MediaInfoDLL import *

GUI = """
<interface>
  <requires lib="gtk+" version="2.0"/>
  <object class="GtkScrolledWindow" id="mainWindow">
    <property name="visible">True</property>
    <property name="can_focus">True</property>
    <property name="hscrollbar_policy">never</property>
    <child>
      <object class="GtkViewport" id="viewport1">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
      </object>
    </child>
  </object>
</interface>"""

class Mediainfo(GObject.GObject, Caja.PropertyPageProvider):

  def get_property_pages(self, files):

    if len(files) != 1:
      return

    file = files[0]
    if file.get_uri_scheme() != 'file':
      return

    if file.is_directory():
      return

    filename = unquote(file.get_uri()[7:])

    MI = MediaInfo()
    MI.Open(filename.decode("utf-8"))
    MI.Option_Static("Complete")
    info = MI.Inform().splitlines()
    if len(info) < 8:
      return

    self.property_label = Gtk.Label('Media Info')
    self.property_label.show()

    self.builder = Gtk.Builder()
    self.builder.add_from_string(GUI)

    self.mainWindow = self.builder.get_object("mainWindow")
    self.viewport = self.builder.get_object("viewport1")
    self.grid = Gtk.VBox()
    self.grid.show()
    self.viewport.add(self.grid)

    for line in info:
      box = Gtk.HBox(homogeneous=True, spacing=8)
      box.show()
      label = Gtk.Label()
      label.set_markup("<b>" + line[:41].strip() + "</b>")
      label.set_justify(Gtk.Justification.LEFT)
      label.set_alignment(0, 0.5)
      label.show()
      box.pack_start(label, True, True, 0)
      label = Gtk.Label()
      label.set_text(line[42:].strip())
      label.set_justify(Gtk.Justification.LEFT)
      label.set_alignment(0, 0.5)
      label.set_selectable(True)
      label.set_line_wrap(True)
      label.show()
      box.pack_start(label, True, True, 0)
      self.grid.pack_start(box, True, True, 0)

    return Caja.PropertyPage(name="CajaPython::mediainfo", label=self.property_label, page=self.mainWindow),

