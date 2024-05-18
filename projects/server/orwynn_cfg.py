from orwynn.admin import handle_get_indexed_codes
from orwynn.auth import AuthCfg
from orwynn.boot import BootCfg, RouteSpec
from orwynn.mongo import MongoCfg
from orwynn.preload import PreloadCfg, handle_preload
from orwynn.rbac import PermissionModel, RbacCfg

from src.share import handle_share

default = {
    "__default__": [
        BootCfg(
            std_verbosity=2,
            route_specs=[
                RouteSpec(
                    method="post",
                    route="/preload",
                    handler=handle_preload
                ),
                RouteSpec(
                    method="get",
                    route="/admin/codes",
                    handler=handle_get_indexed_codes
                ),
                RouteSpec(
                    method="get",
                    route="/share/{filename}",
                    handler=handle_share
                )
            ],
        ),
        RbacCfg(
            permissions=[
                PermissionModel(
                    code="start-operation-permission",
                    name="Начать выполнение операции",
                    dscr="Возможность брать операции в работу."
                ),
                PermissionModel(
                    code="create-objective-permission",
                    name="Создать задачу",
                    dscr="Возможность создавать задачи."
                ),
                PermissionModel(
                    code="create-tprocess-permission",
                    name="Создать тех. процесс",
                    dscr="Возможность создавать тех. процессы."
                ),
                PermissionModel(
                    code="del-report-permission",
                    name="Удалить отчет",
                    dscr=""
                ),
            ]
        ),
        AuthCfg(
            # check_user_func= \
            #     UserUtils.req_check_user,
            # try_login_user= \
            #     UserUtils.try_req_login_user,
            # try_logout_user= \
            #     UserUtils.try_req_logout_user,
            auth_token_secret="hello",  # noqa: S106
            auth_token_algo="HS256",  # noqa: S106
            auth_token_exp_time=2592000
        )
    ],
    "test": [
        MongoCfg(
            url="mongodb://localhost:9006",
            database_name="achievements_test_db",
            must_clean_db_on_destroy=True
        ),
        PreloadCfg(
            must_clean_preloads_on_destroy=True
        )
    ],
    "dev": [
        MongoCfg(
            url="mongodb://localhost:9006",
            database_name="achievements_dev_db",
            must_clean_db_on_destroy=True
        )
    ],
    "prod": [
        MongoCfg(
            url="mongodb://mongo:27017",
            database_name="achievements_prod_db"
        )
    ],
}
