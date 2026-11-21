"""Explicit module/action grants, including planned modules; grants do not create routes."""
MODULES = ('users roles settings audit_logs products categories brands warehouses customers suppliers '
           'vendors employees inventory batches purchases sales pos returns_adjustments accounting '
           'chart_of_accounts cash_bank credit_debit expenses receivables payables customer_ledgers '
           'supplier_ledgers general_ledger financial_statements bom production_planning manufacturing '
           'quality_control production_costing raw_materials dashboard reports').split()
ACTIONS = ('read', 'create', 'update', 'approve', 'post', 'reverse', 'export')
PERMISSIONS = {f'{module}:{action}' for module in MODULES for action in ACTIONS}


def grants(modules, actions=ACTIONS):
    return {f'{module}:{action}' for module in modules.split() for action in actions}


ROLE_GRANTS = {
    'Super Admin': PERMISSIONS,
    'Admin': PERMISSIONS - grants('roles', ('create', 'update')),
    'Accountant': grants('accounting chart_of_accounts cash_bank credit_debit expenses receivables payables customer_ledgers supplier_ledgers general_ledger financial_statements reports dashboard'),
    'Sales Manager': grants('sales customers pos returns_adjustments') | grants('products inventory dashboard', ('read',)),
    'Purchase Manager': grants('purchases suppliers vendors') | grants('products inventory dashboard', ('read',)),
    'Inventory Manager': grants('inventory warehouses batches products categories brands raw_materials') | grants('dashboard', ('read',)),
    'Production Manager': grants('bom production_planning manufacturing quality_control production_costing') | grants('inventory products raw_materials batches dashboard', ('read',)),
    'Cashier': grants('pos', ('read', 'create', 'post')) | grants('sales customers products dashboard', ('read',)),
    'Viewer': grants('dashboard reports products inventory', ('read',)),
}
