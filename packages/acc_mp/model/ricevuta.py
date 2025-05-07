# encoding: utf-8
from gnr.core.gnrnumber import floatToDecimal,decimalRound


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('ricevuta',pkey='id',name_long='Ricevuta',name_plural='Ricevute',caption_field='protocollo')
        self.sysFields(tbl)
        tbl.column('cliente_id',size='22',name_long='cliente',name_short='cliente').relation('cliente.id',relation_name='ric_cliente', mode='foreignkey', onDelete='raise')
        tbl.column('data_ric',dtype='D',name_long='data ric',name_short='data_ric')
        tbl.column('note',name_long='note',name_short='note')
        tbl.column('protocollo',size='11',name_long='protocollo',name_short='prot')
        tbl.column('totale_ric',dtype='N',size='10,2',name_long='totale ric.',name_short='totale_ric',format='#,###.00')

    def ricalcolaTotali(self, ric_id=None):
        with self.recordToUpdate(ric_id) as record:
            totale_ric = self.db.table('acc_mp.dett_ric').readColumns(columns="""SUM($totale) AS totale_ric""",
                                                        where='$ric_id=:r_id', r_id=ric_id)

            record['totale_ric'] = floatToDecimal(totale_ric)
    
    
    def defaultValues(self):
        return dict(data_ric = self.db.workdate)

    def counter_protocollo(self,record=None):
        #F14/000001
        return dict(format='$K$YY/$NNNN',code='Ric_',period='YY',
                    date_field='data_ric',showOnLoad=True,recycle=True)

    
        
