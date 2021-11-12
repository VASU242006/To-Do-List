import django_tables2 as tables
from .models import TODO
from django_tables2.utils import A
from django.shortcuts import redirect
import datetime


# def due_date_row_color(**kwargs):
#     row = kwargs.get("record", None)
#     d1 = datetime.datetime.now()
#     today_date = d1.date()
#     if (row.task_end_date) < (today_date):
#         # taskdata_obj = get_object_or_404(TaskData, pk =task_data_id)
#         # taskdata_obj.task_due_date_color_data ='red'
#         # taskdata_obj.save()
#         return "color:red;"
#     else:
#         return 'color:black;'


def status_decision(**kwargs):
    row = kwargs.get("record")
    # task_data_id =row.pk
    d1 = datetime.datetime.now()
    today_date = d1.date()
    # print((row.end_date).day - (today_date).day)
    # print((row.end_date).month - (today_date).month)  

    if row.status == 'P':
        if (row.end_date).day - (today_date).day >=0 and (row.end_date).day - (today_date).day <= 2 and (row.end_date).month - (today_date).month == 0 and (row.end_date).year - (today_date).year == 0:
            return "color: blue;"
        elif (row.end_date).day - (today_date).day > 2 and (row.end_date).month - (today_date).month >= 0 and (row.end_date).year - (today_date).year >= 0:    
            return "color: black;"            
        elif row.end_date < today_date:
            return "color: red;"
        else:
            return "color: black;"
    else:
        return "color: darkgreen;"
       


class TODOTable(tables.Table):
    id = tables.Column(verbose_name='Task Id')
    delete = tables.TemplateColumn(template_name='base/task_delete_btn.html', orderable=False)
    edit = tables.TemplateColumn(template_name='base/task_edit_btn.html', orderable=False)
    # Status = tables.TemplateColumn(template_name='app/task_status_panding_btn.html')
    # , orderable=False, text='Edit'

    title = tables.LinkColumn('view_todo', args=[A('id')])
    # class Meta:
    #     model = TODO
    #     sequence = ("title", "status", "priority", "end_date")
    #     exclude = ("user", "date")
    
    class Meta:
        row_attrs = {
            "style": status_decision

        }
        # row_attrs = { "style": lambda record: "background-color: #8B0000;"
        #     if record['id'] else "background-color: #000000;" }
        # attrs = {'class': 'table table-centered datatable dt-responsive nowrap table-card-list','style':"border-collapse: collapse; border-spacing: 0 12px; width: 100%"}
        model = TODO
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("id", "title", "status", "date",
                  "priority", "end_date", "edit", "delete")
