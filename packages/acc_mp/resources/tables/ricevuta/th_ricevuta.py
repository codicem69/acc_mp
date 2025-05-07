#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('protocollo',width='7em')
        r.fieldcell('data_ric')
        r.fieldcell('cliente_id',width='20em')
        r.fieldcell('note',width='25em')
        r.fieldcell('totale_ric', width='10em')

    def th_order(self):
        return 'protocollo:d'

    def th_query(self):
        return dict(column='protocollo', op='contains', val='',runOnStart=True)



class Form(BaseComponent):

    def th_form(self, form):

        bc = form.center.borderContainer()
        self.ricTestata(bc.borderContainer(region='top',datapath='.record',height='170px'))
        self.ricRighe(bc.contentPane(region='center'))

    def ricTestata(self, bc):
        bc.contentPane(region='center').linkerBox('cliente_id',margin='2px',openIfEmpty=True, validate_notnull=True,
                                                   columns='$rag_sociale,$indirizzo',template='test',
                                                   newRecordOnly=True,formResource='Form',
                                                   dialog_height='500px',dialog_width='800px')
        left = bc.roundedGroup(title='Dati Ricevuta',region='left',width='50%')
        fb = left.formbuilder(cols=1, border_spacing='4px')
        fb.field('protocollo',readOnly=True)
        fb.field('data_ric')
        #fb.field('cliente_id' )
        fb.field('note',width='30em' )
        fb.field('totale_ric', width='10em',readOnly=True)

        #pane = form.record
        #fb = pane.formbuilder(cols=2, border_spacing='4px')
        #fb.field('protocollo' )
        #fb.field('data_nc' )
        #fb.field('cliente_id' )
        #fb.field('note' )

    def th_bottom_custom(self, bottom):
        bar = bottom.slotBar('5,stampa_ricevuta,*,10')
        bar.stampa_ricevuta.button('Stampa Ricevuta', iconClass='print',
                                    action="""genro.publish("table_script_run",{table:"acc_mp.ricevuta",
                                                                               res_type:'print',
                                                                               resource:'stampa_ric',
                                                                               pkey: pkey})""",
                                                                               pkey='=#FORM.pkey')
        
    def ricRighe(self,pane):
        pane.inlineTableHandler(relation='@dett_ric_id',viewResource='ViewFromRIC',
                           picker='prod_id')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
