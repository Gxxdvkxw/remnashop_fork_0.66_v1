from dishka import Provider, Scope, provide

from src.services import (
    CommandService,
    MaintenanceService,
    NotificationService,
    PlanService,
    UserService,
    WebhookService,
)


class ServicesProvider(Provider):
    scope = Scope.APP

    webhook_service = provide(source=WebhookService)
    command_service = provide(source=CommandService)

    maintenance_service = provide(source=MaintenanceService)
    notification_service = provide(source=NotificationService)

    user_service = provide(source=UserService, scope=Scope.REQUEST)
    # promocode_service = provide(PromocodeService)
    plan_service = provide(source=PlanService, scope=Scope.REQUEST)
