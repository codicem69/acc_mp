#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('tip_id', width='5em')
        r.fieldcell('nome', width='30em')
        r.fieldcell('reg_n')
        r.fieldcell('cliente_id', width='auto')

    def th_order(self):
        return 'nome'

    def th_query(self):
        return dict(column='nome', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        self.imbarcazione(bc.roundedGroupFrame(title='!![it]Imbarcazione',region='top',datapath='.record',height='210px', splitter=True))
        tc = bc.tabContainer(margin='2px',region='center')
        self.fat_emesse(tc.contentPane(title='!![it]Fatture'))
    
    def imbarcazione(self, pane):
        fb = pane.div(margin_left='50px',margin_right='80px').formbuilder(cols=3, border_spacing='4px',colswidth='auto',fld_width='100%')
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        
        fb.field('tip_id', hasDownArrow=True )
        fb.field('nome', width='20em' )
        fb.field('reg_n' )
        fb.field('cliente_id', hasDownArrow=True, width='50em' )

    def fat_emesse(self,pane):
        pane.dialogTableHandler(relation='@fatt_imb',
                                viewResource='ViewFattureImb',extendedQuery=True,pbl_classes=True)
        
    def th_options(self):
        return dict(dialog_windowRatio = 1)
