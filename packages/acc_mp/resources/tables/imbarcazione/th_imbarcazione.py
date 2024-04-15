#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('cliente_id')
        r.fieldcell('tip_id')
        r.fieldcell('nome')
        r.fieldcell('reg_n')

    def th_order(self):
        return 'cliente_id'

    def th_query(self):
        return dict(column='nome', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('cliente_id', hasDownArrow=True )
        fb.field('tip_id', hasDownArrow=True )
        fb.field('nome' )
        fb.field('reg_n' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
