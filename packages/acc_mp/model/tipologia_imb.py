# encoding: utf-8

from gnr.core.gnrdecorator import metadata

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('tipologia_imb', pkey='code', name_long='!![it]Tipologia imbarcazione', name_plural='!![it]Tipologia imbarcazioni',
                                            caption_field='descrizione',lookup=True)
        self.sysFields(tbl,id=False)
        tbl.column('code',size=':2',name_long='!![it]Codifica')
        tbl.column('descrizione', name_short='!![it]Descrizione')

    @metadata(mandatory=True)
    def sysRecord_MP(self):
        return self.newrecord(code='MP', descrizione='M/P')

    @metadata(mandatory=True)
    def sysRecord_MY(self):
        return self.newrecord(code='MY', descrizione='M/Y')

    @metadata(mandatory=True)
    def sysRecord_MN(self):
        return self.newrecord(code='MN', descrizione='M/N')

    @metadata(mandatory=True)
    def sysRecord_MB(self):
        return self.newrecord(code='MN', descrizione='M/B')

    @metadata(mandatory=True)
    def sysRecord_MV(self):
        return self.newrecord(code='MN', descrizione='M/V')    