# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('estratto_corrisp', pkey='id', name_long='!![it]Estratto corrispettivi', name_plural='!![it]Estratti corrispettivi',caption_field='id')
        self.sysFields(tbl)

        tbl.column('data', dtype='D', name_short='!![it]Data')
        tbl.formulaColumn('tot_sifiva',select=dict(table='acc_mp.estratto_dettagli',
                                                columns="SUM($sifiva)",
                                                where='$estratto_id=#THIS.id'),
                                    dtype='money',name_long='Tot.Olio naz./ SIF con IVA / Bunker')
        tbl.formulaColumn('tot_gasiva',select=dict(table='acc_mp.estratto_dettagli',
                                                columns="SUM($gasiva)",
                                                where='$estratto_id=#THIS.id'),
                                    dtype='money',name_long='Tot. Gasolio nazionale')
        tbl.formulaColumn('tot_benziva',select=dict(table='acc_mp.estratto_dettagli',
                                                columns="SUM($benziva)",
                                                where='$estratto_id=#THIS.id'),
                                    dtype='money',name_long='Tot. Benzina nazionale')
        tbl.formulaColumn('tot_sif',select=dict(table='acc_mp.estratto_dettagli',
                                                columns="SUM($sif)",
                                                where='$estratto_id=#THIS.id'),
                                    dtype='money',name_long='Tot. SIF')
        tbl.formulaColumn('tot_benz_8',select=dict(table='acc_mp.estratto_dettagli',
                                                columns="SUM($benz_8)",
                                                where='$estratto_id=#THIS.id'),
                                    dtype='money',name_long='Tot. Benzina sanza IVA')