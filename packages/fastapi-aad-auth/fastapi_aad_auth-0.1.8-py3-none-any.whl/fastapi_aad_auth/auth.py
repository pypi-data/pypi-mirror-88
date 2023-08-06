"""Authenticator Class."""
from functools import wraps
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI
from starlette.authentication import requires
from starlette.middleware.authentication import AuthenticationError, AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, Response
from starlette.routing import Mount, request_response, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from fastapi_aad_auth._base.backend import BaseOAuthBackend
from fastapi_aad_auth._base.state import AuthenticationState
from fastapi_aad_auth._base.validators import SessionValidator
from fastapi_aad_auth.config import Config
from fastapi_aad_auth.errors import base_error_handler, ConfigurationError
from fastapi_aad_auth.mixins import LoggingMixin
from fastapi_aad_auth.utilities import deprecate


_BASE_ROUTES = ['openapi', 'swagger_ui_html', 'swagger_ui_redirect', 'redoc_html']


class Authenticator(LoggingMixin):
    """Authenticator class.

    Creates the key components based on the provided configurations
    """

    def __init__(self, config: Config = None, add_to_base_routes: bool = True, base_context: Dict[str, Any] = None, user_klass: Optional[type] = None):
        """Initialise the AAD config based on the provided configuration.

        Keyword Args:
            config (fastapi_aad_auth.config.Config): Authentication configuration (includes ui and routing, as well as AAD Application and Tenant IDs)
            add_to_base_routes (bool): Add the authentication to the router
        """
        super().__init__()
        if config is None:
            config = Config()
        if user_klass is not None:
            config.user_klass = user_klass
        self.config = config
        if base_context is None:
            base_context = {}
        if self.config.login_ui.context:
            context = self.config.login_ui.context.copy()
            context.update(base_context)
            base_context = context
        self._base_context = base_context
        self._add_to_base_routes = add_to_base_routes
        self._session_validator = self._init_session_validator()
        self._providers = self._init_providers()
        self.auth_backend = self._init_auth_backend()
        self._ui_routes = self._init_ui()
        self._auth_routes = self._init_auth_routes()

    def _init_session_validator(self):
        auth_serializer = SessionValidator.get_session_serializer(self.config.auth_session.secret.get_secret_value(),
                                                                  self.config.auth_session.salt.get_secret_value())
        return SessionValidator(auth_serializer)
        # Lets setup the oauth backend

    def _init_providers(self):
        return [u._provider_klass.from_config(session_validator=self._session_validator, config=self.config, provider_config=u) for u in self.config.providers]

    def _init_auth_backend(self):
        validators = [self._session_validator]
        for provider in self._providers:
            validators += provider.validators
        return BaseOAuthBackend(validators)

    def _init_ui(self):
        login_template_path = Path(self.config.login_ui.template_file)
        user_template_path = Path(self.config.login_ui.user_template_file)
        login_templates = Jinja2Templates(directory=str(login_template_path.parent))
        user_templates = Jinja2Templates(directory=str(user_template_path.parent))

        async def login(request: Request, *args, **kwargs):
            context = self._base_context.copy()  # type: ignore
            if not self.config.enabled or request.user.is_authenticated:
                # This is authenticated so go straight to the homepage
                return RedirectResponse(self.config.routing.home_path)
            context['request'] = request  # type: ignore
            if 'login' not in context or context['login'] is None:  # type: ignore
                post_redirect = self._session_validator.pop_post_auth_redirect(request)
                context['login'] = '<br>'.join([provider.get_login_button(post_redirect) for provider in self._providers])  # type: ignore
            return login_templates.TemplateResponse(login_template_path.name, context)  # type: ignore

        routes = [Route(self.config.routing.landing_path, endpoint=login, methods=['GET'], name='login'),
                  Mount(self.config.login_ui.static_path, StaticFiles(directory=str(self.config.login_ui.static_directory)), name='static-login')]

        if self.config.routing.user_path:

            @self.auth_required()
            async def get_user(request: Request):
                context = self._base_context.copy()  # type: ignore
                self.logger.debug(f'Getting token for {request.user}')
                context['request'] = request  # type: ignore
                if self.config.enabled:
                    self.logger.debug(f'Auth {request.auth}')
                    try:
                        context['user'] = self._session_validator.get_state_from_session(request).user
                    except ValueError:
                        # If we have one provider, we can force the login, otherwise...
                        return self.__force_authenticate(request)
                else:
                    self.logger.debug('Auth not enabled')
                    context['token'] = None  # type: ignore
                return user_templates.TemplateResponse(user_template_path.name, context)

            async def get_token(request: Request, auth_state: AuthenticationState = Depends(self.auth_backend)):
                if not isinstance(auth_state, AuthenticationState):
                    user = self.__get_user_from_request(request)
                else:
                    user = auth_state.user
                if hasattr(user, 'username'):  # type: ignore
                    access_token = self.__get_access_token(user)
                    if access_token:
                        # We want to get the token for each provider that is authenticated
                        return JSONResponse(access_token)   # type: ignore
                    else:
                        if any([u in request.headers['user-agent'] for u in ['Mozilla', 'Gecko', 'Trident', 'WebKit', 'Presto', 'Edge', 'Blink']]):
                            # If we have one provider, we can force the login, otherwise we need to request which login route
                            return self.__force_authenticate(request)
                        else:
                            return JSONResponse('Unable to access token as user has not authenticated via session')
                return RedirectResponse(f'{self.config.routing.landing_path}?redirect=/me/token')

            routes += [Route(self.config.routing.user_path, endpoint=get_user, methods=['GET'], name='user'),
                       Route(f'{self.config.routing.user_path}/token', endpoint=get_token, methods=['GET'], name='get-token')]
        return routes

    def _init_auth_routes(self):

        async def logout(request: Request):
            self.logger.debug(f'Logging out - request url {request.url}')
            if self.config.enabled:
                self.logger.debug(f'Auth {request.auth}')
                for provider in self._providers:
                    provider.logout(request)
                self._session_validator.logout(request)
            return RedirectResponse(self.config.routing.post_logout_path)
        routes = [Route(self.config.routing.logout_path, endpoint=logout, methods=['GET'], name='logout')]
        for provider in self._providers:
            routes += provider.get_routes(noauth_redirect=self.config.routing.home_path)
        # We have a deprecated behaviour here
        return routes

    def __force_authenticate(self, request: Request):
        if len(self._providers) == 1:
            return self._providers[0].authenticator.process_login_request(request, force=True, redirect=request.url.path)
        else:
            return RedirectResponse(f'{self.config.routing.landing_path}?redirect={request.url.path}')

    def __get_access_token(self, user):
        access_token = None
        while access_token is None:
            provider = next(self._providers)
            try:
                access_token = provider.autheticator.get_access_token(user)
            except ValueError:
                pass
        return access_token

    def __get_user_from_request(self, request: Request):
        if hasattr(request.user, 'username'):
            user = request.user
        else:
            auth_state = self.auth_backend.check(request)
            user = auth_state.user
        return user

    def _set_error_handlers(self, app):
        error_template_path = Path(self.config.login_ui.error_template_file)
        error_templates = Jinja2Templates(directory=str(error_template_path.parent))
        if self.config.login_ui.app_name:
            self._base_context['appname'] = self.config.login_ui.app_name
        else:
            self._base_context['appname'] = app.title
        self._base_context['static_path'] = self.config.login_ui.static_path

        @app.exception_handler(ConfigurationError)
        async def configuration_error_handler(request: Request, exc: ConfigurationError) -> Response:
            error_message = "Oops! It seems like the application has not been configured correctly, please contact an admin"
            error_type = 'Authentication Configuration Error'
            status_code = 500
            return base_error_handler(request, exc, error_type, error_message, error_templates, error_template_path, context=self._base_context.copy(), status_code=status_code)

        @app.exception_handler(AuthenticationError)
        async def authentication_error_handler(request: Request, exc: AuthenticationError) -> Response:
            error_message = "Oops! It seems like you cannot access this information. If this is an error, please contact an admin"
            error_type = 'Authentication Error'
            status_code = 403
            return base_error_handler(request, exc, error_type, error_message, error_templates, error_template_path, context=self._base_context.copy(), status_code=status_code)

    def auth_required(self, scopes: str = 'authenticated', redirect: str = 'login'):
        """Decorator to require specific scopes (and redirect to the login ui) for an endpoint.

        This can be used for toggling authentication (e.g. between an internal/external server)
        as well as handling the redirection based on the session information

        Keyword Args:
            scopes: scopes for the fastapi requires decorator
            redirect: name of the redirection url
        """

        def wrapper(endpoint):
            if self.config.enabled:

                @wraps(endpoint)
                async def require_endpoint(request: Request, *args, **kwargs):
                    self._session_validator.set_post_auth_redirect(request, request.url.path)

                    @requires(scopes, redirect=redirect)
                    async def req_wrapper(request: Request, *args, **kwargs):
                        return await endpoint(request, *args, **kwargs)

                    return await req_wrapper(request, *args, **kwargs)

                return require_endpoint
            else:
                return endpoint

        return wrapper

    def app_routes_add_auth(self, app: FastAPI, route_list: List[str], invert: bool = False):
        """Add authentication to specified routes in application router.

        Used for default routes (e.g. api/docs and api/redocs, openapi.json etc)

        Args:
            app: fastapi application
            route_list: list of routes to add authentication to (e.g. api docs, redocs etc)

        Keyword Args:
            invert: Switch between using the route list as a block list or an allow list

        """
        if self.config.enabled:
            routes = app.router.routes
            for i, route in enumerate(routes):
                # Can use allow list or block list (i.e. invert = True sets all except the route list to have auth
                if (route.name in route_list and not invert) or (route.name not in route_list and invert):  # type: ignore
                    route.endpoint = self.auth_required()(route.endpoint)  # type: ignore
                    route.app = request_response(route.endpoint)  # type: ignore
                app.router.routes[i] = route
        return app

    def configure_app(self, app: FastAPI, add_error_handlers=True):
        """Configure the fastapi application to use these authentication handlers.

        Adds authentication middleware, error handler and adds authentication
        to the default routes as well as adding the authentication specific routes

        Args:
            app: fastapi application

        Keyword Args:
            add_error_handlers (bool) : add the error handlers to the app (default is true, but can be set to False to configure specific handling)
        """

        def on_auth_error(request: Request, exc: Exception):
            self.logger.exception(f'Error {exc} for request {request}')
            self._session_validator.set_post_auth_redirect(request, request.url.path)
            return RedirectResponse(self.config.routing.landing_path)

        app.add_middleware(AuthenticationMiddleware, backend=self.  auth_backend, on_error=on_auth_error)
        if add_error_handlers:
            self._set_error_handlers(app)
        # Check if session middleware is there
        if not any([SessionMiddleware in u.cls.__mro__ for u in app.user_middleware]):
            app.add_middleware(SessionMiddleware, **self.config.session.dict())
        if self._add_to_base_routes:
            self.app_routes_add_auth(app, _BASE_ROUTES)
        app.routes.extend(self._ui_routes)
        app.routes.extend(self._auth_routes)
        # TODO: select a specific provider to use here
        app.swagger_ui_init_oauth = self._providers[0].validators[0].init_oauth


_DEPRECATED_VERSION = '0.2.0'


@deprecate(_DEPRECATED_VERSION, replaced_by=f'{Authenticator.__module__}:{Authenticator.__name__}')
class AADAuth(Authenticator):   # noqa: D101
    __doc__ = Authenticator.__doc__

    @property  # type: ignore
    @deprecate(_DEPRECATED_VERSION, replaced_by=f'{Authenticator.__module__}:{Authenticator.__name__}.auth_backend.requires_auth')
    def api_auth_scheme(self):
        """Get the API Authentication Schema."""
        return self.auth_backend.requires_auth()
