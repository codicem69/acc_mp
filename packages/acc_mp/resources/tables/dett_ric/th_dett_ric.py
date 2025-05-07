#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('ric_id')
        r.fieldcell('prod_id')
        r.fieldcell('quantita')
        r.fieldcell('prezzo_un')
        r.fieldcell('totale')

    def th_order(self):
        return 'nc_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class ViewFromRIC(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('prod_id', hasDownArrow=True, edit=True)
        r.fieldcell('quantita',width='7em', edit=dict(remoteRowController=True, validate_notnull=True))
        r.fieldcell('prezzo_un',width='7em',edit=dict(remoteRowController=True, validate_notnull=True))
        r.fieldcell('totale')

    @public_method
    def th_remoteRowController(self,row=None,field=None,**kwargs):
        if not row['prod_id']:
            return row
        if row['quantita'] and row['prezzo_un']:
            row['totale'] = row['quantita'] * row['prezzo_un']

        return row

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('ric_id' )
        fb.field('prod_id' )
        fb.field('quantita' )
        fb.field('prezzo_un' )
        fb.field('totale' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
