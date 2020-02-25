# -*- coding: utf-8 -*-

from odoo import fields, models


class product_template_attribute_value(models.Model):
    """
    Overwrite to add extra and multiplier
    """
    _inherit = "product.template.attribute.value"

    def _compute_price_extra(self):
        """
        Force standard price_extra always be zero
        """
        for ptav in self:
            ptav.price_extra = 0.0

    price_plus = fields.Float(
        string='Price Extra',
        digits='Product Price',
    )
    price_multiple = fields.Float(
        string='Coefficient (%)',
        digits='Product Price',
    )
    price_extra = fields.Float(
        compute=_compute_price_extra,
        store=False,
        string="Price Change",
    )
    sequence_esp = fields.Integer(string="Pricing Sequence")

    _order = "sequence_esp, product_attribute_value_id, id"

