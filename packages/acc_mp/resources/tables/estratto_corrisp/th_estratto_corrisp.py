#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('data')
        r.fieldcell('tot_sifiva')
        r.fieldcell('tot_gasiva')
        r.fieldcell('tot_benziva')
        r.fieldcell('tot_sif')
        r.fieldcell('tot_benz_8')
        r.cell('Tot. giornaliero',formula='tot_sifiva+tot_gasiva+tot_benziva+tot_sif+tot_benz_8', dtype='N', font_weight='bold', format='#,###.00')

    def th_order(self):
        return 'data:d'

    def th_query(self):
        return dict(column='id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        self.estrattoTestata(bc.borderContainer(region='top',datapath='.record',height='50px'))
        self.estrattoRighe(bc.contentPane(region='center'))

    def estrattoTestata(self,pane):    
        #pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('data' )

    def estrattoRighe(self,pane):
        pane.inlineTableHandler(relation='@estratto_righe',viewResource='ViewEstrattoRighe',
                                picker='fattura_id',
                                picker_condition='$data=:edata',
                                picker_condition_edata='^#FORM.record.data',
                                picker_viewResource='ViewFatEmessePicker',
                                liveUpdate=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
