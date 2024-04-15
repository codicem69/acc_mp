#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='acc_mp package',sqlschema='acc_mp',sqlprefix=True,
                    name_short='Acc_mp', name_long='acc_mp', name_full='Acc_mp')
                    
    def custom_type_money(self):
        return dict(dtype='N',format='#,###.00')

    def config_db(self, pkg):
        pass
        
class Table(GnrDboTable):
    pass
