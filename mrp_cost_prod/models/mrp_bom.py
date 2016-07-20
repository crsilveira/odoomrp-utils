# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from openerp import models, fields, api, exceptions, _
import openerp.addons.decimal_precision as dp


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.one
    @api.depends('bom_line_ids', 'bom_line_ids.product_id.standard_price','bom_line_ids.product_qty')
    def _compute_cost(self):
        total = 0.0
        for x in self.bom_line_ids:
            if x.product_id.standard_price:
                total += x.product_id.standard_price * x.product_qty
        self.cost_total = total

    cost_total = fields.Float(
        string='Custo Total', compute='_compute_cost',
        digits=dp.get_precision('Product Price'))

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    product_cost = fields.Float(related='product_id.product_tmpl_id.standard_price', 
        string='Custo', store=True, digits=dp.get_precision('Product Price'))
    total_cost = fields.Float(compute='_total_cost', store=True, string='Total Custo',
        digits=dp.get_precision('Product Price'))

    @api.one
    @api.depends('product_id.product_tmpl_id.standard_price','product_qty')
    def _total_cost(self):
        if self.product_id.product_tmpl_id.standard_price:
            self.total_cost = self.product_id.product_tmpl_id.standard_price * self.product_qty

