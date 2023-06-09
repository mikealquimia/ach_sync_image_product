# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import xmlrpc.client
import logging
_logger = logging.getLogger(__name__)

class SyncImageProduct(models.Model):
    _name = 'sync.image_product'
    _description = 'Sync Image Product'

    name = fields.Char(string="Name", required=True)
    state = fields.Selection([('draft','Draft'),('logging','Logging'),('progress','Progress'),('done','Done')], string="State", default='draft')
    url_database = fields.Char(string="URL", required=True)
    database_name = fields.Char(string="Database", required=True)
    username_database = fields.Char(string="User Name", required=True)
    password_username_database = fields.Char(string="Password", required=True)

    product_type = fields.Selection([('product','Product Variant'),('template','Product Template')], string="Type product")
    field_reference_id = fields.Many2one('sync.image_product_fields', string="Field Reference")
    field_image_id = fields.Many2one('sync.image_product_fields', string="Field Image")
    set_field_image_id = fields.Many2one('ir.model.fields', string="Set Field Image")

    def logging_db(self):
        url = self.url_database
        db = self.database_name
        username = self.username_database
        password = self.password_username_database
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        version = common.version()
        uid = common.authenticate(db, username, password, {})
        if uid:
            self.write({'state':'logging'})
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url_database))
            try:
                if self.product_type == 'product':
                    image_fields = models.execute_kw(self.database_name, uid, self.password_username_database, 'ir.model.fields', 'search_read', [[['model_id','=','product.product']]], {'fields': ['name','field_description','ttype']})
                if self.product_type == 'template':
                    image_fields = models.execute_kw(self.database_name, uid, self.password_username_database, 'ir.model.fields', 'search_read', [[['model_id','=','product.template']]], {'fields': ['name','field_description','ttype']})
                if image_fields:
                    for field in image_fields:
                        vals = {
                            'name': field['name'],
                            'name_import': field['name'],
                            'field_description_import': field['field_description'],
                            'ttype_import': field['ttype'],
                        }
                        self.env['sync.image_product_fields'].create(vals)
            except:
                raise UserError('An error has occurred with the connection data, verify your data access or server data')
        else:
            raise UserError('An error has occurred with the connection data, verify your data access')

    def import_data(self):
        url = self.url_database
        db = self.database_name
        username = self.username_database
        password = self.password_username_database
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        version = common.version()
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        if self.product_type == 'product':
            ids = models.execute_kw(db, uid, password, 'product.product', 'search', [[]])
            model = 'product.product'
        if self.product_type == 'template':
            ids = models.execute_kw(db, uid, password, 'product.template', 'search', [[]])
            model = 'product.template'
        list_fields = []
        list_fields.append(self.field_reference_id.name_import)
        list_fields.append(self.field_image_id.name_import)
        data = models.execute_kw(db, uid, password, model, 'read', [ids], {'fields': list_fields})
        for delete in data:
            delete.pop("id")
        for vals in data:
            if vals[self.field_image_id.name_import] and vals[self.field_reference_id.name_import]:
                #try:
                #    self.env.cr.execute("UPDATE {model} SET {image} = {val} WHERE {reference} = {val_ref};".format(model=model.replace('.','_'),
                #                                                                                                   image=self.set_field_image_id.name,
                #                                                                                                   val=vals[self.field_image_id.name_import],
                #                                                                                                   reference=self.field_reference_id.name_import,
                #                                                                                                   val_ref=vals[self.field_reference_id.name_import]))
                #except:
                try:
                    update_ids = self.env[model].search([(self.field_reference_id.name_import,'=',vals[self.field_reference_id.name_import])])
                    print(update_ids)
                    for data in update_ids:
                        data.write({self.set_field_image_id.name:vals[self.field_image_id.name_import]})
                except:
                    _logger.error('Not update reigster')
        return

class SyncImageProductFields(models.Model):
    _name = 'sync.image_product_fields'
    _description = 'Odoo Sync Ir Models Fields'

    name = fields.Char(string="Name")
    name_import = fields.Char(string="Field Import")
    field_description_import = fields.Char(string="Description Import")
    ttype_import = fields.Selection([
        ('binary','binary'),('boolean','boolean'),('char','char'),('date','date'),('datetime','datetime'),
        ('float','float'),('html','html'),('integer','integer'),('many2many','many2many'),('many2one','many2one'),('monetary','monetary'),
        ('many2one_reference','many2one_reference'),('one2many','one2many'),('reference','reference'),('selection','selection'),('text','text')],
        string="Type Import")