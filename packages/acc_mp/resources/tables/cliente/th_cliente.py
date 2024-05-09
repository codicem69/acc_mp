#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('rag_sociale', width='30em')
        r.fieldcell('indirizzo', width='20em')
        r.fieldcell('cap', width='6em')
        r.fieldcell('citta',width='20em')
        r.fieldcell('vat')
        r.fieldcell('cf')
        #r.fieldcell('cod_univoco')
        #r.fieldcell('pec')
        #r.fieldcell('email')
        #r.fieldcell('tel')
        #r.fieldcell('note')
        r.fieldcell('balance', totalize=True, range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='color:black;font-weight:bold;')

    def th_order(self):
        return 'rag_sociale'

    def th_query(self):
        return dict(column='full_cliente', op='contains', val='')

    def th_sections_fatemesse(self):
        return [dict(code='tutti',caption='!![it]Tutti'),
                dict(code='div_zero',caption='!![it]Non nullo',
                        condition='$balance!=0'),
                dict(code='da_saldare',caption='!![it]Da saldare',
                        condition='$balance>0'),
                dict(code='over_paym',caption='!![it]Maggior pagamento',
                        condition='$balance<0')]
    
    def th_sections_cliente(self):
        #prendiamo agency_id nel currentEnv
        ag_id=self.db.currentEnv.get('current_agency_id')
        #effettuaiamo la ricerca di tutti i clienti filtrando quelli relativi all'agency_id
        f = self.db.table('acc_mp.cliente').query(where='',order_by='$rag_sociale').selection().output('records')#$agency_id=:ag_id',ag_id=self.db.currentEnv.get('current_agency_id')).fetch()
        #creaiamo una lista vuota dove andremo ad appendere i dizionari con il valore tutti e con i clienti
        result=[]
        result.append(dict(code='tutti',caption='!![it]Tutti'))
        for r in f:
            result.append(dict(code=r['id'], caption=r['rag_sociale'],
                     condition='$id=:cliente',condition_cliente=r['id']))
        return result
    
    def th_top_toolbarsuperiore(self,top):
        bar=top.slotToolbar('5,sections@fatemesse,sections@cliente,15',
                        childname='superiore',_position='<bar',sections_cliente_multiButton=False,
                        sections_cliente_lbl='!![it]Cliente',
                        sections_cliente_width='60em')
class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        self.cliente(bc.roundedGroupFrame(title='!![it]Cliente',region='top',datapath='.record',height='210px', splitter=True))
        tc = bc.tabContainer(margin='2px',region='center')
        self.fat_emesse(tc.contentPane(title='!![it]Fatture'))

    def cliente(self, pane):
        fb = pane.div(margin_left='50px',margin_right='80px').formbuilder(cols=3, border_spacing='4px',colswidth='auto',fld_width='100%')
        #fb = pane.formbuilder(cols=2, border_spacing='4px')
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
        fb.field('balance', readOnly=True )

    def fat_emesse(self,pane):
        pane.dialogTableHandler(relation='@fatt_cliente',
                                viewResource='ViewFromFatture',extendedQuery=True,pbl_classes=True)
        
    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
