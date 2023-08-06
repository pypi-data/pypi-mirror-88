from django.views.generic import ListView


class PaginatedListView(ListView):

    def pager_v2(self, rango=2):
        fin = int(self.object_list.__len__() / self.paginate_by)
        if self.object_list.__len__() / self.paginate_by > fin:
            fin += 1
        ini = 1
        page = self.request.GET.get('page', "1")
        if page.isdigit():
            page = int(page)
            ini = page - rango
            if ini <= 0:
                rango -= -1 + ini
                ini = 1
            if page + rango <= fin:
                fin = page + rango
            else:
                rango = (rango + page) - fin
                if ini - rango <= 0:
                    ini = 1
                else:
                    ini -= rango
        return range(ini, fin + 1)

    def get_context_data(self, **kwargs):
        context = super(PaginatedListView, self).get_context_data(**kwargs)
        page = self.request.GET.get("page", 1)
        context["current_page"] = int(page)
        pages = self.pager_v2(2)
        context["pages"] = pages
        return context


def confirmation_pay(model,request):
    data = request.POST
    id = data.get("x_extra1")
    if request.method == 'POST' and id:
        recharge = model.objects.filter(id=id).first()
        if recharge:
            recharge.x_cust_id_cliente = data.get("x_cust_id_cliente")
            recharge.x_description = data.get("x_description")
            recharge.x_amount_ok = data.get("x_amount_ok")
            recharge.x_id_invoice = data.get("x_id_invoice")
            recharge.x_amount_base = data.get("x_amount_base")
            recharge.x_tax = data.get("x_tax")
            recharge.x_currency_code = data.get("x_currency_code")
            recharge.x_franchise = data.get("x_franchise")
            recharge.x_transaction_date = data.get("x_transaction_date")
            recharge.x_approval_code = data.get("x_approval_code")
            recharge.x_transaction_id = data.get("x_transaction_id")
            recharge.x_ref_payco = data.get("x_ref_payco")
            recharge.x_cod_response = data.get("x_cod_response")
            recharge.x_cod_transaction_state = data.get("x_cod_transaction_state")
            recharge.x_transaction_state = data.get("x_transaction_state")
            recharge.x_signature = data.get("x_signature")
            recharge.x_response = data.get("x_response")
            recharge.x_response_reason_text = data.get("x_response_reason_text")
            recharge.x_extra1 = data.get("x_extra1")
            recharge.x_extra2 = data.get("x_extra2")
            recharge.x_extra3 = data.get("x_extra3")
            recharge.x_amount = data.get("x_amount")
            recharge.x_amount_country = data.get("x_amount_country")
            recharge.x_bank_name = data.get("x_bank_name")
            recharge.x_cardnumber = data.get("x_cardnumber")
            recharge.x_quotas = data.get("x_quotas")
            recharge.x_fecha_transaccion = data.get("x_fecha_transaccion")
            recharge.x_errorcode = data.get("x_errorcode")
            recharge.x_customer_doctype = data.get("x_customer_doctype")
            recharge.x_customer_lastname = data.get("x_customer_lastname")
            recharge.x_customer_name = data.get("x_customer_name")
            recharge.x_customer_email = data.get("x_customer_email")
            recharge.x_customer_phone = data.get("x_customer_phone")
            recharge.x_customer_country = data.get("x_customer_country")
            recharge.x_customer_city = data.get("x_customer_city")
            recharge.x_customer_address = data.get("x_customer_address")
            recharge.x_customer_ip = data.get("x_customer_ip")
            recharge.x_test_request = data.get("x_test_request")
            recharge.save()
            return recharge
        else:
            return None
    else:
        return None