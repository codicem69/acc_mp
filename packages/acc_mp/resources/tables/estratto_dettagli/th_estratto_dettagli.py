#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('estratto_id')
        r.fieldcell('fattura_id')
        r.fieldcell('sifiva')
        r.fieldcell('gasiva')
        r.fieldcell('benziva')
        r.fieldcell('sif')
        r.fieldcell('benz_8')
        r.fieldcell('note')

    def th_order(self):
        return '@estratto_id.data'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class ViewEstrattoRighe(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        #r.fieldcell('estratto_id')
        r.fieldcell('fattura_id', edit=True, width='15em')
        r.fieldcell('sifiva', edit=True, totalize=True)
        r.fieldcell('gasiva', edit=True, totalize=True)
        r.fieldcell('benziva', edit=True, totalize=True)
        r.fieldcell('sif', edit=True, totalize=True)
        r.fieldcell('benz_8', edit=True, totalize=True)
        r.fieldcell('note', edit=True, width='auto')

    def th_order(self):
        return '@estratto_id.data'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('estratto_id' )
        fb.field('fattura_id' )
        fb.field('sifiva' )
        fb.field('gasiva' )
        fb.field('benziva' )
        fb.field('sif' )
        fb.field('benz_8' )
        fb.field('note' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
