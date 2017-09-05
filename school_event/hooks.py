# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from openerp import SUPERUSER_ID
from openerp import api


def post_init_hook(cr, registry):

    env = api.Environment(cr, SUPERUSER_ID, {})
    rule_id = env.ref('calendar.calendar_event_rule_employee')
    cr.execute("""UPDATE ir_rule SET active = False
                WHERE id = %s""", (rule_id.id,))
