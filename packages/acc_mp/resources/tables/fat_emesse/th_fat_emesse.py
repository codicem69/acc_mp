#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrdecorator import metadata

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        #r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('cliente_id', width='30em', name='!![it]Cliente')
        r.fieldcell('imbarcazione_id', width='30em', name='!![it]Imbarcazione')
        r.fieldcell('data')
        r.fieldcell('doc_n')
        r.fieldcell('importo', totalize=True)
        r.fieldcell('scadenza')
        r.fieldcell('giorni_scadenza', width='11em')
        r.fieldcell('tot_pag', totalize='total.totpag',name='^name_totpag')
        r.fieldcell('saldo', totalize=True,name='^name_saldo', 
                          range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='color:black;font-weight:bold;')
        r.fieldcell('semaforo_al',semaphore=True)
        r.fieldcell('saldo_effettivo', totalize=True,
                          range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='color:black;font-weight:bold;')
        r.fieldcell('semaforo_eff',semaphore=True)
        r.fieldcell('note',width='auto')

    def th_order(self):
        return 'data:d,doc_n:d'
    
    def th_query(self):
        return dict(column='id', op='contains', val='')

    def th_options(self):
        return dict(grid_footer='Totali')
       
    def th_sections_fatemesse(self):
        return [dict(code='tutti',caption='!![it]Tutte'),
                dict(code='da_saldare',caption='!![it]da saldare',
                        condition='$saldo>0'),
                dict(code='saldati',caption='!![it]Saldate',condition='$saldo=0'),
                dict(code='scaduti',caption='!![it]Scadute',condition='$scadenza<now() and $saldo>0'),
                dict(code='non_scadute',caption='!![it]Non scadute',condition='$scadenza>now() and $saldo>0'),
                dict(code='senza_scadenza',caption='!![it]Senza scadenza',condition='$scadenza is null and $saldo!=0'),
                dict(code='senza_imb',caption='!![it]Senza Imbarcazione',condition='$imbarcazione_id IS NULL')]
    
    #def th_sections_cliente_id(self):
    #    return [dict(code='cliente',caption='!![en]Customer',condition="$cliente_id!=''")]
                
    def th_top_toolbarsuperiore(self,top):
        bar=top.slotToolbar('5,sections@fatemesse,sections@cliente_id,sections@imbarcazione,10,actions,resourceActions,15',
                        childname='superiore',_position='<bar',sections_cliente_id_multivalue=False,
                        sections_cliente_id_multiButton=False,sections_cliente_id_lbl='!![it]Cliente',
                        sections_cliente_id_width='40em',
                        sections_imbarcazione_multivalue=False,
                        sections_imbarcazione_multiButton=False,sections_imbarcazione_lbl='!![it]Imbarcazione',sections_imbarcazione_remote=self.sectionsImbarcazione)
                        #,gradient_from='#999',gradient_to='#888')
        bar.actions.div('Actions')
        #passiamo nel dbEnv al path data_saldo la data che inseriamo nella querybysample data <= che a sua volta sara prelevata dalla formulaColumn
        #per calcolare il totale pagato alla data
        bar.data('^acc_mp_fat_emesse.view.queryBySample.c_0',serverpath='data_saldo',dbenv=True)
        bar.dataController("""if(data_saldo) {SET name_saldo='Saldo al '+ data_saldo; SET name_totpag = 'Tot.Pag. al '+data_saldo;} else 
                           {SET name_saldo='Saldo al '+ data_att; SET name_totpag='Tot.Pag. al '+ data_att;}""",
                           data_saldo='^acc_mp_fat_emesse.view.queryBySample.c_0',data_att=self.workdate.strftime("%d/%m/%Y"),_onStart=True)
        
    @public_method(remote_cliente='^.cliente_id.current')
    def sectionsImbarcazione(self,cliente=None):
        #print(x)
        if cliente is None or cliente=='_all_':
            f = self.db.table('acc_mp.imbarcazione').query(where="",order_by='$nome').selection().output('records')   
        else:     
            f = self.db.table('acc_mp.imbarcazione').query(where="LOWER($cliente_id)=:cid",cid=cliente,order_by='$nome').selection().output('records')
        
        result=[]
        result.append(dict(code='tutti',caption='!![en]All'))
        #print(x)
        for r in f:
            result.append(dict(code=r['id'], caption=r['nome']+' - '+str(r['reg_n']),
                     condition='$imbarcazione_id=:imb',condition_imb=r['id']))
        return result
        
    def th_queryBySample(self):
        return dict(fields=[dict(field='data', lbl='Date <=',width='10em', op='lesseq', tag='dateTextBox'),
                            dict(field='data', lbl='Date >=',width='10em', op='greatereq', val='', tag='dateTextBox'),
                            dict(field='data', lbl='!![it]Data fattura',width='10em', tag='dateTextBox')],
                            cols=4, isDefault=True) 

class ViewFromFatture(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('cliente_id', width='30em', name='!![it]Cliente')
        r.fieldcell('imbarcazione_id', width='30em', name='!![it]Imbarcazione')
        r.fieldcell('data')
        r.fieldcell('doc_n')
        r.fieldcell('importo', totalize=True)
        r.fieldcell('scadenza')
        r.fieldcell('giorni_scadenza', width='11em')
        r.fieldcell('tot_pag', totalize=True,name='^name_totpag')
        r.fieldcell('saldo', totalize=True,name='^name_saldo', 
                          range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='color:black;font-weight:bold;')
        r.fieldcell('semaforo_al',semaphore=True)
        r.fieldcell('saldo_effettivo', totalize=True,
                          range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='color:black;font-weight:bold;')
        #r.fieldcell('saldo', totalize=True,
        #                  range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='color:black;font-weight:bold;')
        r.fieldcell('semaforo_eff',semaphore=True)

    def th_order(self):
        return 'data:d,doc_n:d'
    
    def th_query(self):
        return dict(column='id', op='contains', val='')

    def th_options(self):
        return dict(grid_footer='Totali')
    
    def th_sections_fatemesse(self):
        return [dict(code='tutti',caption='!![it]Tutte'),
                dict(code='da_saldare',caption='!![it]Da saldare',
                        condition='$saldo>0'),
                dict(code='saldati',caption='!![it]Saldate',condition='$saldo=0'),
                dict(code='scaduti',caption='!![it]Scadute',condition='$scadenza<now() and $saldo>0'),
                dict(code='non_scadute',caption='!![it]Non scadute',condition='$scadenza>now() and $saldo>0'),
                dict(code='senza_scadenza',caption='!![it]Senza scadenza',condition='$scadenza is null and $saldo!=0'),
                dict(code='senza_imb',caption='!![it]Senza Imbarcazione',condition='$imbarcazione_id IS NULL')]
    
                    
    def th_top_toolbarsuperiore(self,top):
        bar=top.slotToolbar('5,sections@fatemesse,sections@imbarcazione,10,actions,resourceActions,15',
                        childname='superiore',_position='<bar',sections_imbarcazione_multiButton=False,
                        sections_imbarcazione_lbl='!![it]Imbarcazione',
                        sections_imbarcazione_width='30em',sections_imbarcazione_remote=self.sectionsImbarcazione)
                        #,gradient_from='#999',gradient_to='#888')
        bar.actions.div('Actions')
        bar.data('^acc_mp_cliente.form.acc_mp_fat_emesse.view.queryBySample.c_0',serverpath='data_saldo',dbenv=True)
        bar.dataController("""if(data_saldo) {SET name_saldo='Saldo al '+ data_saldo; SET name_totpag = 'Tot.Pag. al '+data_saldo;} else 
                           {SET name_saldo='Saldo al '+ data_att; SET name_totpag='Tot.Pag. al '+ data_att;}""",
                           data_saldo='^acc_mp_fat_emesse.view.queryBySample.c_0',data_att=self.workdate.strftime("%d/%m/%Y"),_onStart=True)
        
    @public_method(remote_cliente='^#FORM.record.id')
    def sectionsImbarcazione(self,cliente,**kwargs):
        #prendiamo agency_id nel currentEnv
        #ag_id=self.db.currentEnv.get('current_agency_id')
        #effettuaiamo la ricerca di tutti i clienti filtrando quelli relativi all'agency_id
        if cliente is None:
            f = self.db.table('acc_mp.imbarcazione').query(where="",order_by='$nome').selection().output('records')   
        else:     
            f = self.db.table('acc_mp.imbarcazione').query(where="$cliente_id=:cid",cid=cliente,order_by='$nome').selection().output('records')
        #print(x)
        #f = self.db.table('acc_mp.imbarcazione').query(where='$cliente_id=:cid',cid=cliente,order_by='$nome').selection().output('records')#$agency_id=:ag_id',ag_id=self.db.currentEnv.get('current_agency_id')).fetch()
        #creaiamo una lista vuota dove andremo ad appendere i dizionari con il valore tutti e con i clienti
        
        result=[]
        result.append(dict(code='tutti',caption='!![en]All'))
        
        for r in f:
            result.append(dict(code=r['id'], caption=r['nome'],
                     condition='$imbarcazione_id=:imb',condition_imb=r['id']))
                     #condition='$cliente_id=:cid',condition_cid=r['cliente_id']))
        #print(x)  
        return result
    #def th_bottom_toolbarinferiore(self,bottom):
    #    bar=bottom.slotToolbar('5,sections@cliente_id,15',
    #                    childname='inferiore',_position='<bar',sections_cliente_id_multivalue=False,sections_cliente_id_multiButton=False)
        
    def th_queryBySample(self):
        return dict(fields=[dict(field='data', lbl='Date <=',width='10em', op='lesseq', val=''),
                            dict(field='data', lbl='Date >=',width='10em', op='greatereq', val=''),
                            dict(field='data', lbl='!![it]Data fattura',width='10em')],
                            cols=5, isDefault=True)      

class ViewFattureImb(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('cliente_id', width='30em', name='!![it]Cliente')
        r.fieldcell('imbarcazione_id', width='30em', name='!![it]Imbarcazione')
        r.fieldcell('data')
        r.fieldcell('doc_n')
        r.fieldcell('importo', totalize=True)
        r.fieldcell('scadenza')
        r.fieldcell('giorni_scadenza', width='11em')
        r.fieldcell('tot_pag', totalize=True)
        r.fieldcell('saldo', totalize=True,
                          range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='color:black;font-weight:bold;')
        r.fieldcell('semaforo_eff',semaphore=True)

    def th_order(self):
        return 'data:d,doc_n:d'
    
    def th_query(self):
        return dict(column='id', op='contains', val='')

    def th_sections_fatemesse(self):
        return [dict(code='tutti',caption='!![it]Tutte'),
                dict(code='da_saldare',caption='!![it]Da saldare',
                        condition='$saldo>0'),
                dict(code='saldati',caption='!![it]Saldate',condition='$saldo=0'),
                dict(code='scaduti',caption='!![it]Scadute',condition='$scadenza<now() and $saldo>0'),
                dict(code='non_scadute',caption='!![it]Non scadute',condition='$scadenza>now() and $saldo>0'),
                dict(code='senza_scadenza',caption='!![it]Senza scadenza',condition='$scadenza is null and $saldo!=0')]
    
                    
    def th_top_toolbarsuperiore(self,top):
        bar=top.slotToolbar('5,sections@fatemesse,10,actions,resourceActions,15',
                        childname='superiore',_position='<bar')
                        #,gradient_from='#999',gradient_to='#888')
        bar.actions.div('Actions')

class ViewFatEmessePicker(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        #r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        #r.fieldcell('cliente_id', width='30em', name='!![it]Cliente')
        r.fieldcell('imbarcazione_id', width='10em', name='!![it]Imbarcazione')
        r.fieldcell('doc_n')
        r.fieldcell('importo', totalize=True)
        r.fieldcell('note')

    def th_order(self):
        return 'data,doc_n'
        
class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        self.fatEmesse(bc.roundedGroupFrame(title='!![it]Fatture emesse',region='top',datapath='.record',height='300px', splitter=True))
        tc = bc.tabContainer(margin='2px',region='center')
        self.paym_fatEmesse(tc.contentPane(title='!![it]Pagamenti'))
        

    def fatEmesse(self,pane):
        fb = pane.formbuilder(cols=3, border_spacing='4px')
        #fb.field('cliente_id', lbl='!![it]Cliente', hasDownArrow=True, colspan=3, width='100%' )
        #fb.field('imbarcazione_id', lbl='!![it]Imbarcazione', hasDownArrow=True,rowcaption='$full_imb', colspan=3, width='100%',condition="$cliente_id =:cod",condition_cod='=#FORM.record.cliente_id')
        
        fb.field('imbarcazione_id', lbl='!![it]Imbarcazione', hasDownArrow=True,rowcaption='$full_imb', colspan=3, width='100%',selected_cliente_id='.cliente_id')
        fb.field('cliente_id', lbl='!![it]Cliente', hasDownArrow=True, colspan=3, width='100%',validate_notnull=True)#,condition="@cliente_imb.id=:cod",condition_cod='=#FORM.record.imbarcazione_id' )
        fb.field('data',validate_notnull=True)
        fb.field('doc_n',validate_notnull=True)
        fb.field('importo',font_weight='bold',validate_notnull=True)
        fb.field('scadenza')
        fb.field('tip_vend',validate_notnull=True)
        fb.field('note', colspan=2, width='100%')

    def paym_fatEmesse(self,pane):
        pane.inlineTableHandler(relation='@pag_fatture',
                                viewResource='ViewFromPayments')

    def th_options(self):
        return dict(dialog_windowRatio = 1, annotations= True )
