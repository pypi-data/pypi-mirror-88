import os

from tyadmin_api_cli.utils import init_django_env, get_lower_case_name
from tyadmin_api_cli.contants import SYS_LABELS


def gen_url(project_name_settings, user_label_list):
    init_django_env(project_name_settings)
    import django
    from django.conf import settings
    model_list = []
    model_fk_dict = {}
    app_model_import_dict = {}
    gen_labels = SYS_LABELS + user_label_list
    for one in django.apps.apps.get_models():
        columns = []
        model_name = one._meta.model.__name__
        model_ver_name = one._meta.verbose_name
        app_label = one._meta.app_label
        if app_label in gen_labels:
            model_list.append(model_name)

    url_txt = f"""from tyadmin_api import auto_views
from django.urls import re_path, include, path
from rest_framework.routers import DefaultRouter
    
router = DefaultRouter(trailing_slash=False)
    """

    for model_name in model_list:
        url_txt += f"""
router.register('{get_lower_case_name(model_name)}', auto_views.{model_name}ViewSet)
    """

    url_txt += """
urlpatterns = [
        re_path('^', include(router.urls)),
    ]
    """

    # if os.path.exists(f'{settings.BASE_DIR}/tyadmin_api/auto_url.py'):
    #     print("已存在urls跳过")
    # else:
    with open(f'{settings.BASE_DIR}/tyadmin_api/auto_url.py', 'w', encoding='utf-8') as fw:
        fw.write(url_txt)


if __name__ == '__main__':
    name = input("请输入项目settings位置:")
    gen_url(name)
