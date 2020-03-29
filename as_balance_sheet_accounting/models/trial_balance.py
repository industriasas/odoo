# -*- coding: utf-8 -*-
from lxml import etree
from lxml.objectify import fromstring
from odoo import models, api, _, fields, tools
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.xml_utils import _check_with_xsd

class ReportTrialBalanceReport(models.AbstractModel):
    _inherit = "l10n_mx.trial.report"

    v_cost_center = fields.Boolean('Allow Cost Center Filters')
    v_department = fields.Boolean('Allow Department Filters')


    def _with_correct_filters(self):
        res = super(ReportTrialBalanceReport, self)._with_correct_filters()
        if res.v_cost_center:
            res.filter_v_cost_centers = []
            res.filter_v_cost_center = True
        if res.v_department:
            res.filter_v_departments = []
            res.filter_v_department = True
        return res

    @api.model
    def _init_filter_v_cost_center(self, options, previous_options=None):
        if not self.filter_v_cost_center:
            return

        options['v_cost_center'] = self.filter_v_cost_center
        CostCenter = self.env['tf.cost.center'].sudo()
        options['v_cost_centers'] = previous_options and previous_options.get('v_cost_centers') or []
        record_ids = [int(acc_grp) for acc_grp in options['v_cost_centers']]
        selected_v_cost_centers = record_ids and CostCenter.browse(record_ids) or CostCenter
        options['selected_v_cost_center_names'] = selected_v_cost_centers.mapped('name')

    @api.model
    def _get_options_v_cost_center_domain(self, options):
        domain = []
        if options.get('v_cost_centers'):
            v_cost_center_ids = [int(acc_grp) for acc_grp in options['v_cost_centers']]
            domain.append(('cost_center_id', 'in', v_cost_center_ids))
        return domain

    @api.model
    def _init_filter_v_department(self, options, previous_options=None):
        if not self.filter_v_department:
            return
        options['v_department'] = self.filter_v_department
        CostCenter = self.env['tf.department'].sudo()
        options['v_departments'] = previous_options and previous_options.get('v_departments') or []
        record_ids = [int(acc_grp) for acc_grp in options['v_departments']]
        selected_v_departments = record_ids and CostCenter.browse(record_ids) or CostCenter
        options['selected_v_department_names'] = selected_v_departments.mapped('name')

    @api.model
    def _get_options_v_department_domain(self, options):
        domain = []
        if options.get('v_departments'):
            v_department_ids = [int(rec) for rec in options['v_departments']]
            domain.append(('department_id', 'in', v_department_ids))
        return domain

    @api.model
    def _get_lines_third_level(self, line, grouped_accounts, initial_balances,
                               options, comparison_table):
        """Return list of accounts found in the third level"""
        lines = []
        domain = safe_eval(line.domain or '[]')
        domain += [
            ('deprecated', '=', False),
            ('company_id', 'in', self.env.context['company_ids']),
        ]

        domain_cd = []
        if options.get('v_cost_centers'):
            domain_cd += self._get_options_v_cost_center_domain(options)
        if options.get('v_departments'):
            domain_cd += self._get_options_v_department_domain(options)

        if domain_cd:
            tf_line_ids = self.env['account.move.line'].search(domain_cd)
            if tf_line_ids:
                domain.append(('id', 'in', [tf_x.account_id.id for tf_x in tf_line_ids]))

        basis_account_ids = self.env['account.tax'].search_read(
            [('cash_basis_base_account_id', '!=', False)], ['cash_basis_base_account_id'])
        basis_account_ids = [account['cash_basis_base_account_id'][0] for account in basis_account_ids]
        domain.append((('id', 'not in', basis_account_ids)))
        account_ids = self.env['account.account'].search(domain, order='code')
        tags = account_ids.mapped('tag_ids').filtered(
            lambda r: r.color == 4).sorted(key=lambda a: a.name)
        for tag in tags:
            accounts = account_ids.search([
                ('tag_ids', 'in', [tag.id]),
                ('id', 'in', account_ids.ids),
            ])
            name = tag.name
            name = name[:63] + "..." if len(name) > 65 else name
            cols = [{'name': ''}]
            childs = self._get_lines_fourth_level(accounts, grouped_accounts, initial_balances, options,
                                                  comparison_table)
            if not childs:
                continue
            if not options.get('coa_only'):
                n_cols = len(comparison_table) * 2 + 2
                child_cols = [c['columns'] for c in childs]
                cols = []
                for col in range(n_cols):
                    cols += [sum(a[col] for a in child_cols)]
            lines.append({
                'id': 'level_two_%s' % tag.id,
                'parent_id': 'level_one_%s' % line.id,
                'name': name,
                'columns': cols,
                'level': 3,
                'unfoldable': True,
                'unfolded': True,
                'tag_id': tag.id,
            })
            lines.extend(childs)
        return lines