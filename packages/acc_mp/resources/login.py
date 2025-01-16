# -*- coding: UTF-8 -*-

from gnr.web.gnrwebpage import BaseComponent
        
class LoginComponent(BaseComponent):
    
    auth_workdate = 'admin,user' #questa riga ci permette di avere la data di lavoro nel login anche per gli user così in caso di
                                 #inserire un record con protocollo datato in un anno differente possiamo al login decidere la data di login


