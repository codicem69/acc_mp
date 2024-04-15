#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('rag_sociale')
        r.fieldcell('indirizzo')
        r.fieldcell('cap')
        r.fieldcell('citta')
        r.fieldcell('vat')
        r.fieldcell('cf')
        r.fieldcell('cod_univoco')
        r.fieldcell('pec')
        r.fieldcell('email')
        r.fieldcell('tel')
        r.fieldcell('note')
        r.fieldcell('balance')

    def th_order(self):
        return 'rag_sociale'

    def th_query(self):
        return dict(column='full_cliente', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('rag_sociale' )
        fb.field('indirizzo' )
        fb.field('cap' )
        fb.field('citta' )
        fb.field('vat' )
        fb.field('cf' )
        fb.field('cod_univoco' )
        fb.field('pec' )
        fb.field('email' )
        fb.field('tel' )
        fb.field('note' )
        fb.field('balance' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
