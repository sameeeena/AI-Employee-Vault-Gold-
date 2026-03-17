
## Request Log - d6af2498
- **Timestamp:** 2026-03-04 02:35:54.775
- **Model:** account.move
- **Method:** create
- **Args:** [{"partner_id": 1, "move_type": "out_invoice", "invoice_date": "2026-03-04", "ref": "TEST-INV-001", "invoice_line_ids": [[0, 0, {"product_id": 1, "quantity": 1.0, "price_unit": 100.0}]]}]
- **Kwargs:** {}

- **Response:** {"jsonrpc": "2.0", "id": 1772573754, "error": {"code": 0, "message": "Odoo Server Error", "data": {"name": "odoo.exceptions.UserError", "message": "Object account.move doesn't exist", "arguments": ["Object account.move doesn't exist"], "context": {}, "debug": "Traceback (most recent call last):\n  File \"C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py\", line 2273, in _serve_db\n    return service_model.retrying(serve_func, env=self.env)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^...

---


## Error Log
- **Timestamp:** 2026-03-04 02:35:55.928
- **Model:** account.move
- **Method:** create
- **Error:** 500: {'code': 0, 'message': 'Odoo Server Error', 'data': {'name': 'odoo.exceptions.UserError', 'message': "Object account.move doesn't exist", 'arguments': ["Object account.move doesn't exist"], 'context': {}, 'debug': 'Traceback (most recent call last):\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py", line 2273, in _serve_db\n    return service_model.retrying(serve_func, env=self.env)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\service\\model.py", line 185, in retrying\n    result = func()\n             ^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py", line 2328, in _serve_ir_http\n    response = self.dispatcher.dispatch(rule.endpoint, args)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py", line 2543, in dispatch\n    result = self.request.registry[\'ir.http\']._dispatch(endpoint)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\addons\\base\\models\\ir_http.py", line 355, in _dispatch\n    result = endpoint(**request.params)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py", line 788, in route_wrapper\n    result = endpoint(self, *args, **params_ok)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\addons\\rpc\\controllers\\jsonrpc.py", line 16, in jsonrpc\n    return dispatch_rpc(service, method, args)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py", line 439, in dispatch_rpc\n    return dispatch(method, params)\n           ^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\service\\model.py", line 130, in dispatch\n    res = execute_cr(cr, uid, model, method_, args, kw)\n          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\service\\model.py", line 145, in execute_cr\n    raise UserError(f"Object {obj} doesn\'t exist")  # pylint: disable=missing-gettext\n    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nodoo.exceptions.UserError: Object account.move doesn\'t exist\n'}}

---


## Request Log - 06d0e1c3
- **Timestamp:** 2026-03-04 02:47:41.172
- **Model:** account.move
- **Method:** create
- **Args:** [{"partner_id": 1, "move_type": "out_invoice", "invoice_date": "2026-03-04", "ref": "TEST-INV-001", "invoice_line_ids": [[0, 0, {"product_id": 1, "quantity": 1.0, "price_unit": 100.0}]]}]
- **Kwargs:** {}

- **Response:** {"jsonrpc": "2.0", "id": 1772574461, "result": 65}...

---


## Request Log - 6dae076d
- **Timestamp:** 2026-03-04 02:47:43.251
- **Model:** account.move
- **Method:** action_post
- **Args:** [[65]]
- **Kwargs:** {}

- **Response:** {"jsonrpc": "2.0", "id": 1772574463, "result": false}...

---


## Request Log - 64a69d45
- **Timestamp:** 2026-03-04 02:58:08.995
- **Model:** account.move
- **Method:** create
- **Args:** [{"partner_id": 9, "move_type": "out_invoice", "invoice_date": "2026-03-04", "ref": "TEST-INV-002", "invoice_line_ids": [[0, 0, {"product_id": 1, "quantity": 2.0, "price_unit": 150.0}]]}]
- **Kwargs:** {}

- **Response:** {"jsonrpc": "2.0", "id": 1772575088, "result": 66}...

---


## Request Log - 1b0843dd
- **Timestamp:** 2026-03-04 02:58:11.043
- **Model:** account.move
- **Method:** action_post
- **Args:** [[66]]
- **Kwargs:** {}

- **Response:** {"jsonrpc": "2.0", "id": 1772575091, "result": false}...

---


## Request Log - 3cdf9b24
- **Timestamp:** 2026-03-04 02:58:38.074
- **Model:** account.move
- **Method:** create
- **Args:** [{"partner_id": 9, "move_type": "out_invoice", "invoice_date": "2026-03-04", "ref": "FINAL-TEST", "invoice_line_ids": [[0, 0, {"product_id": 1, "quantity": 1.0, "price_unit": 100.0}]]}]
- **Kwargs:** {}

- **Response:** {"jsonrpc": "2.0", "id": 1772575118, "result": 67}...

---


## Request Log - 875e285a
- **Timestamp:** 2026-03-04 02:58:39.422
- **Model:** account.move
- **Method:** action_post
- **Args:** [[67]]
- **Kwargs:** {}

- **Response:** {"jsonrpc": "2.0", "id": 1772575119, "result": false}...

---


## Request Log - a93cfa79
- **Timestamp:** 2026-03-04 02:58:52.676
- **Model:** account.move
- **Method:** search_read
- **Args:** [[["date", ">=", "2026-01-01"], ["date", "<=", "2026-12-31"], ["state", "=", "posted"], ["move_type", "in", ["out_invoice", "in_invoice", "entry"]]], ["id", "name", "date", "amount_total", "move_type"]]
- **Kwargs:** {"order": "date"}

- **Response:** {"jsonrpc": "2.0", "id": 1772575132, "result": [{"id": 19, "name": "BNK1/2026/00001", "date": "2026-01-03", "amount_total": 850.0, "move_type": "entry"}, {"id": 55, "name": "BNK1/2026/00001", "date": "2026-01-03", "amount_total": 850.0, "move_type": "entry"}, {"id": 33, "name": "INV/2026/00008", "date": "2026-01-22", "amount_total": 2000.0, "move_type": "out_invoice"}, {"id": 22, "name": "BNK1/2026/00002", "date": "2026-01-22", "amount_total": 2000.0, "move_type": "entry"}, {"id": 58, "name": "B...

---


## Request Log - 1c883ea1
- **Timestamp:** 2026-03-04 02:58:53.826
- **Model:** account.account
- **Method:** search_read
- **Args:** [[["user_type_id.name", "=", "Income"]]]
- **Kwargs:** {"fields": ["id", "name", "code"]}

- **Response:** {"jsonrpc": "2.0", "id": 1772575133, "error": {"code": 0, "message": "Odoo Server Error", "data": {"name": "builtins.ValueError", "message": "Invalid field account.account.user_type_id in condition ('user_type_id.name', '=', 'Income')", "arguments": ["Invalid field account.account.user_type_id in condition ('user_type_id.name', '=', 'Income')"], "context": {}, "debug": "Traceback (most recent call last):\n  File \"C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py\", line 914, ...

---


## Error Log
- **Timestamp:** 2026-03-04 02:58:55.104
- **Model:** account.account
- **Method:** search_read
- **Error:** 500: {'code': 0, 'message': 'Odoo Server Error', 'data': {'name': 'builtins.ValueError', 'message': "Invalid field account.account.user_type_id in condition ('user_type_id.name', '=', 'Income')", 'arguments': ["Invalid field account.account.user_type_id in condition ('user_type_id.name', '=', 'Income')"], 'context': {}, 'debug': 'Traceback (most recent call last):\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 914, in __get_field\n    field = model._fields[field_name]\n            ~~~~~~~~~~~~~^^^^^^^^^^^^\nKeyError: \'user_type_id\'\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py", line 2273, in _serve_db\n    return service_model.retrying(serve_func, env=self.env)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\service\\model.py", line 185, in retrying\n    result = func()\n             ^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py", line 2328, in _serve_ir_http\n    response = self.dispatcher.dispatch(rule.endpoint, args)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py", line 2543, in dispatch\n    result = self.request.registry[\'ir.http\']._dispatch(endpoint)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\addons\\base\\models\\ir_http.py", line 355, in _dispatch\n    result = endpoint(**request.params)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py", line 788, in route_wrapper\n    result = endpoint(self, *args, **params_ok)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\addons\\rpc\\controllers\\jsonrpc.py", line 16, in jsonrpc\n    return dispatch_rpc(service, method, args)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py", line 439, in dispatch_rpc\n    return dispatch(method, params)\n           ^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\service\\model.py", line 130, in dispatch\n    res = execute_cr(cr, uid, model, method_, args, kw)\n          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\service\\model.py", line 147, in execute_cr\n    result = retrying(partial(call_kw, recs, method, args, kw), env)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\service\\model.py", line 185, in retrying\n    result = func()\n             ^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\service\\model.py", line 94, in call_kw\n    result = method(recs, *args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\models.py", line 5774, in search_read\n    records = self.search_fetch(domain or [], fields, offset=offset, limit=limit, order=order)\n              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\models.py", line 1408, in search_fetch\n    query = self._search(domain, offset=offset, limit=limit, order=order or self._order)\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\models.py", line 5364, in _search\n    domain = domain.optimize_full(self)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 445, in optimize_full\n    return self._optimize(model, OptimizationLevel.FULL)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 459, in _optimize\n    previous, domain = domain, domain._optimize_step(model, next_level)\n                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 653, in _optimize_step\n    children = self._flatten(child._optimize(model, level) for child in self.children)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 608, in _flatten\n    for child in children:\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 653, in <genexpr>\n    children = self._flatten(child._optimize(model, level) for child in self.children)\n                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 459, in _optimize\n    previous, domain = domain, domain._optimize_step(model, next_level)\n                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 938, in _optimize_step\n    field, property_name = self.__get_field(model)\n                           ^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 916, in __get_field\n    self._raise("Invalid field %s.%s", model._name, field_name)\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 901, in _raise\n    raise error(message % (*args, self.field_expr, self.operator, self.value))\nValueError: Invalid field account.account.user_type_id in condition (\'user_type_id.name\', \'=\', \'Income\')\n'}}

---


## Request Log - e0a9f32e
- **Timestamp:** 2026-03-04 03:01:53.670
- **Model:** account.move
- **Method:** search_read
- **Args:** [[["date", ">=", "2026-01-01"], ["date", "<=", "2026-12-31"], ["state", "=", "posted"], ["move_type", "in", ["out_invoice", "in_invoice", "entry"]]], ["id", "name", "date", "amount_total", "move_type"]]
- **Kwargs:** {"order": "date"}

- **Response:** {"jsonrpc": "2.0", "id": 1772575313, "result": [{"id": 19, "name": "BNK1/2026/00001", "date": "2026-01-03", "amount_total": 850.0, "move_type": "entry"}, {"id": 55, "name": "BNK1/2026/00001", "date": "2026-01-03", "amount_total": 850.0, "move_type": "entry"}, {"id": 33, "name": "INV/2026/00008", "date": "2026-01-22", "amount_total": 2000.0, "move_type": "out_invoice"}, {"id": 22, "name": "BNK1/2026/00002", "date": "2026-01-22", "amount_total": 2000.0, "move_type": "entry"}, {"id": 58, "name": "B...

---


## Request Log - 78ba35e8
- **Timestamp:** 2026-03-04 03:01:54.827
- **Model:** account.account
- **Method:** search_read
- **Args:** [[["user_type_id.name", "=", "Income"]]]
- **Kwargs:** {"fields": ["id", "name", "code"]}

- **Response:** {"jsonrpc": "2.0", "id": 1772575314, "error": {"code": 0, "message": "Odoo Server Error", "data": {"name": "builtins.ValueError", "message": "Invalid field account.account.user_type_id in condition ('user_type_id.name', '=', 'Income')", "arguments": ["Invalid field account.account.user_type_id in condition ('user_type_id.name', '=', 'Income')"], "context": {}, "debug": "Traceback (most recent call last):\n  File \"C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py\", line 914, ...

---


## Error Log
- **Timestamp:** 2026-03-04 03:01:56.112
- **Model:** account.account
- **Method:** search_read
- **Error:** 500: {'code': 0, 'message': 'Odoo Server Error', 'data': {'name': 'builtins.ValueError', 'message': "Invalid field account.account.user_type_id in condition ('user_type_id.name', '=', 'Income')", 'arguments': ["Invalid field account.account.user_type_id in condition ('user_type_id.name', '=', 'Income')"], 'context': {}, 'debug': 'Traceback (most recent call last):\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 914, in __get_field\n    field = model._fields[field_name]\n            ~~~~~~~~~~~~~^^^^^^^^^^^^\nKeyError: \'user_type_id\'\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py", line 2273, in _serve_db\n    return service_model.retrying(serve_func, env=self.env)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\service\\model.py", line 185, in retrying\n    result = func()\n             ^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py", line 2328, in _serve_ir_http\n    response = self.dispatcher.dispatch(rule.endpoint, args)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py", line 2543, in dispatch\n    result = self.request.registry[\'ir.http\']._dispatch(endpoint)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\addons\\base\\models\\ir_http.py", line 355, in _dispatch\n    result = endpoint(**request.params)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py", line 788, in route_wrapper\n    result = endpoint(self, *args, **params_ok)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\addons\\rpc\\controllers\\jsonrpc.py", line 16, in jsonrpc\n    return dispatch_rpc(service, method, args)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\http.py", line 439, in dispatch_rpc\n    return dispatch(method, params)\n           ^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\service\\model.py", line 130, in dispatch\n    res = execute_cr(cr, uid, model, method_, args, kw)\n          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\service\\model.py", line 147, in execute_cr\n    result = retrying(partial(call_kw, recs, method, args, kw), env)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\service\\model.py", line 185, in retrying\n    result = func()\n             ^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\service\\model.py", line 94, in call_kw\n    result = method(recs, *args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\models.py", line 5774, in search_read\n    records = self.search_fetch(domain or [], fields, offset=offset, limit=limit, order=order)\n              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\models.py", line 1408, in search_fetch\n    query = self._search(domain, offset=offset, limit=limit, order=order or self._order)\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\models.py", line 5364, in _search\n    domain = domain.optimize_full(self)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 445, in optimize_full\n    return self._optimize(model, OptimizationLevel.FULL)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 459, in _optimize\n    previous, domain = domain, domain._optimize_step(model, next_level)\n                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 653, in _optimize_step\n    children = self._flatten(child._optimize(model, level) for child in self.children)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 608, in _flatten\n    for child in children:\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 653, in <genexpr>\n    children = self._flatten(child._optimize(model, level) for child in self.children)\n                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 459, in _optimize\n    previous, domain = domain, domain._optimize_step(model, next_level)\n                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 938, in _optimize_step\n    field, property_name = self.__get_field(model)\n                           ^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 916, in __get_field\n    self._raise("Invalid field %s.%s", model._name, field_name)\n  File "C:\\Program Files\\Odoo 19.0.20260302\\server\\odoo\\orm\\domains.py", line 901, in _raise\n    raise error(message % (*args, self.field_expr, self.operator, self.value))\nValueError: Invalid field account.account.user_type_id in condition (\'user_type_id.name\', \'=\', \'Income\')\n'}}

---


## Request Log - e3c38e1e
- **Timestamp:** 2026-03-04 03:03:25.728
- **Model:** account.move
- **Method:** search_read
- **Args:** [[["date", ">=", "2026-01-01"], ["date", "<=", "2026-12-31"], ["state", "=", "posted"], ["move_type", "in", ["out_invoice", "in_invoice", "entry"]]], ["id", "name", "date", "amount_total", "move_type"]]
- **Kwargs:** {"order": "date"}

- **Response:** {"jsonrpc": "2.0", "id": 1772575405, "result": [{"id": 19, "name": "BNK1/2026/00001", "date": "2026-01-03", "amount_total": 850.0, "move_type": "entry"}, {"id": 55, "name": "BNK1/2026/00001", "date": "2026-01-03", "amount_total": 850.0, "move_type": "entry"}, {"id": 33, "name": "INV/2026/00008", "date": "2026-01-22", "amount_total": 2000.0, "move_type": "out_invoice"}, {"id": 22, "name": "BNK1/2026/00002", "date": "2026-01-22", "amount_total": 2000.0, "move_type": "entry"}, {"id": 58, "name": "B...

---


## Request Log - 7dc6f38d
- **Timestamp:** 2026-03-04 03:03:59.828
- **Model:** account.move
- **Method:** create
- **Args:** [{"partner_id": 9, "move_type": "out_invoice", "invoice_date": "2026-03-04", "ref": "FINAL-TEST-2", "invoice_line_ids": [[0, 0, {"product_id": 1, "quantity": 1.0, "price_unit": 250.0}]]}]
- **Kwargs:** {}

- **Response:** {"jsonrpc": "2.0", "id": 1772575439, "result": 68}...

---


## Request Log - 2da2450e
- **Timestamp:** 2026-03-04 03:04:01.600
- **Model:** account.move
- **Method:** action_post
- **Args:** [[68]]
- **Kwargs:** {}

- **Response:** {"jsonrpc": "2.0", "id": 1772575441, "result": false}...

---


## Request Log - cf43ba13
- **Timestamp:** 2026-03-04 03:04:05.880
- **Model:** account.move
- **Method:** search_read
- **Args:** [[["date", ">=", "2026-01-01"], ["date", "<=", "2026-12-31"], ["state", "=", "posted"], ["move_type", "in", ["out_invoice", "in_invoice", "entry"]]], ["id", "name", "date", "amount_total", "move_type"]]
- **Kwargs:** {"order": "date"}

- **Response:** {"jsonrpc": "2.0", "id": 1772575445, "result": [{"id": 19, "name": "BNK1/2026/00001", "date": "2026-01-03", "amount_total": 850.0, "move_type": "entry"}, {"id": 55, "name": "BNK1/2026/00001", "date": "2026-01-03", "amount_total": 850.0, "move_type": "entry"}, {"id": 22, "name": "BNK1/2026/00002", "date": "2026-01-22", "amount_total": 2000.0, "move_type": "entry"}, {"id": 58, "name": "BNK1/2026/00002", "date": "2026-01-22", "amount_total": 2000.0, "move_type": "entry"}, {"id": 5, "name": "INV/202...

---


## Request Log - 734a6446
- **Timestamp:** 2026-03-04 03:04:09.894
- **Model:** account.move
- **Method:** search_read
- **Args:** [[["date", "<=", "2026-03-04"], ["state", "=", "posted"]], ["id", "name", "date", "amount_total", "move_type"]]
- **Kwargs:** {}

- **Response:** {"jsonrpc": "2.0", "id": 1772575449, "result": [{"id": 68, "name": "INV/2026/00013", "date": "2026-03-04", "amount_total": 250.0, "move_type": "out_invoice"}, {"id": 67, "name": "INV/2026/00012", "date": "2026-03-04", "amount_total": 100.0, "move_type": "out_invoice"}, {"id": 66, "name": "INV/2026/00011", "date": "2026-03-04", "amount_total": 300.0, "move_type": "out_invoice"}, {"id": 65, "name": "INV/2026/00010", "date": "2026-03-04", "amount_total": 100.0, "move_type": "out_invoice"}, {"id": 4...

---


## Request Log - 3bd8d742
- **Timestamp:** 2026-03-17 03:47:02.439
- **Model:** account.move
- **Method:** create
- **Args:** [{"partner_id": 45, "move_type": "out_invoice", "invoice_date": "2026-03-17", "ref": "INV-20260317-034659", "invoice_line_ids": [[0, 0, {"product_id": 53, "quantity": 5.0, "price_unit": 150.0}]]}]
- **Kwargs:** {}

- **Response:** {"jsonrpc": "2.0", "id": 1773701222, "result": 69}...

---


## Request Log - 3b087309
- **Timestamp:** 2026-03-17 03:47:05.179
- **Model:** account.move
- **Method:** action_post
- **Args:** [[69]]
- **Kwargs:** {}

- **Response:** {"jsonrpc": "2.0", "id": 1773701225, "result": false}...

---


## Request Log - be4fd033
- **Timestamp:** 2026-03-17 03:47:09.170
- **Model:** account.move
- **Method:** search_read
- **Args:** [[["date", ">=", "2026-01-01"], ["date", "<=", "2026-03-17"], ["state", "=", "posted"], ["move_type", "in", ["out_invoice", "in_invoice", "entry"]]], ["id", "name", "date", "amount_total", "move_type"]]
- **Kwargs:** {"order": "date"}

- **Response:** {"jsonrpc": "2.0", "id": 1773701229, "result": [{"id": 19, "name": "BNK1/2026/00001", "date": "2026-01-03", "amount_total": 850.0, "move_type": "entry"}, {"id": 55, "name": "BNK1/2026/00001", "date": "2026-01-03", "amount_total": 850.0, "move_type": "entry"}, {"id": 5, "name": "INV/2026/00005", "date": "2026-01-22", "amount_total": 2000.0, "move_type": "out_invoice"}, {"id": 22, "name": "BNK1/2026/00002", "date": "2026-01-22", "amount_total": 2000.0, "move_type": "entry"}, {"id": 33, "name": "IN...

---

