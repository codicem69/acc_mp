# encoding: utf-8

from gnr.core.gnrdecorator import metadata

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('tipologia_venduto', pkey='code', name_long='!![it]Tipologia venduto', name_plural='!![it]Tipologie venduto',
                                            caption_field='descrizione',lookup=True)
        self.sysFields(tbl,id=False)
        tbl.column('code',size=':6',name_long='!![it]Codifica')
        tbl.column('descrizione', name_short='!![it]Descrizione')

    @metadata(mandatory=True)
    def sysRecord_SIFIVA(self):
        return self.newrecord(code='SIFIVA', descrizione='Olio Naz. / Sif+IVA / Bunker')
    
    @metadata(mandatory=True)
    def sysRecord_GASNAZ(self):
        return self.newrecord(code='GASNAZ', descrizione='Gasolio naz.')
    
    @metadata(mandatory=True)
    def sysRecord_BENNAZ(self):
        return self.newrecord(code='BENNAZ', descrizione='Benzina naz.')
    
    @metadata(mandatory=True)
    def sysRecord_SIF(self):
        return self.newrecord(code='SIF', descrizione='SIF')
    
    @metadata(mandatory=True)
    def sysRecord_BENZ_8(self):
        return self.newrecord(code='BENZ_8', descrizione='Benzina S/IVA')