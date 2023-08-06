/*
 * @wq/app 1.3.0-beta.0
 * Utilizes @wq/store and @wq/router to dynamically load and render content from a wq.db-compatible REST service
 * (c) 2012-2020, S. Andrew Sheppard
 * https://wq.io/license
 */

define(['regenerator-runtime', './store', './model', './outbox', './router', 'mustache', 'deepcopy'], function (_regeneratorRuntime, ds, modelModule, outbox, router, Mustache, deepcopy) { 'use strict';

function _interopDefaultLegacy (e) { return e && typeof e === 'object' && 'default' in e ? e : { 'default': e }; }

var _regeneratorRuntime__default = /*#__PURE__*/_interopDefaultLegacy(_regeneratorRuntime);
var ds__default = /*#__PURE__*/_interopDefaultLegacy(ds);
var modelModule__default = /*#__PURE__*/_interopDefaultLegacy(modelModule);
var outbox__default = /*#__PURE__*/_interopDefaultLegacy(outbox);
var router__default = /*#__PURE__*/_interopDefaultLegacy(router);
var Mustache__default = /*#__PURE__*/_interopDefaultLegacy(Mustache);
var deepcopy__default = /*#__PURE__*/_interopDefaultLegacy(deepcopy);

function _typeof(obj) {
  "@babel/helpers - typeof";

  if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") {
    _typeof = function (obj) {
      return typeof obj;
    };
  } else {
    _typeof = function (obj) {
      return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj;
    };
  }

  return _typeof(obj);
}

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) {
  try {
    var info = gen[key](arg);
    var value = info.value;
  } catch (error) {
    reject(error);
    return;
  }

  if (info.done) {
    resolve(value);
  } else {
    Promise.resolve(value).then(_next, _throw);
  }
}

function _asyncToGenerator(fn) {
  return function () {
    var self = this,
        args = arguments;
    return new Promise(function (resolve, reject) {
      var gen = fn.apply(self, args);

      function _next(value) {
        asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value);
      }

      function _throw(err) {
        asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err);
      }

      _next(undefined);
    });
  };
}

function _defineProperty(obj, key, value) {
  if (key in obj) {
    Object.defineProperty(obj, key, {
      value: value,
      enumerable: true,
      configurable: true,
      writable: true
    });
  } else {
    obj[key] = value;
  }

  return obj;
}

function ownKeys(object, enumerableOnly) {
  var keys = Object.keys(object);

  if (Object.getOwnPropertySymbols) {
    var symbols = Object.getOwnPropertySymbols(object);
    if (enumerableOnly) symbols = symbols.filter(function (sym) {
      return Object.getOwnPropertyDescriptor(object, sym).enumerable;
    });
    keys.push.apply(keys, symbols);
  }

  return keys;
}

function _objectSpread2(target) {
  for (var i = 1; i < arguments.length; i++) {
    var source = arguments[i] != null ? arguments[i] : {};

    if (i % 2) {
      ownKeys(Object(source), true).forEach(function (key) {
        _defineProperty(target, key, source[key]);
      });
    } else if (Object.getOwnPropertyDescriptors) {
      Object.defineProperties(target, Object.getOwnPropertyDescriptors(source));
    } else {
      ownKeys(Object(source)).forEach(function (key) {
        Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key));
      });
    }
  }

  return target;
}

function _slicedToArray(arr, i) {
  return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest();
}

function _arrayWithHoles(arr) {
  if (Array.isArray(arr)) return arr;
}

function _iterableToArrayLimit(arr, i) {
  if (typeof Symbol === "undefined" || !(Symbol.iterator in Object(arr))) return;
  var _arr = [];
  var _n = true;
  var _d = false;
  var _e = undefined;

  try {
    for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) {
      _arr.push(_s.value);

      if (i && _arr.length === i) break;
    }
  } catch (err) {
    _d = true;
    _e = err;
  } finally {
    try {
      if (!_n && _i["return"] != null) _i["return"]();
    } finally {
      if (_d) throw _e;
    }
  }

  return _arr;
}

function _unsupportedIterableToArray(o, minLen) {
  if (!o) return;
  if (typeof o === "string") return _arrayLikeToArray(o, minLen);
  var n = Object.prototype.toString.call(o).slice(8, -1);
  if (n === "Object" && o.constructor) n = o.constructor.name;
  if (n === "Map" || n === "Set") return Array.from(o);
  if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen);
}

function _arrayLikeToArray(arr, len) {
  if (len == null || len > arr.length) len = arr.length;

  for (var i = 0, arr2 = new Array(len); i < len; i++) arr2[i] = arr[i];

  return arr2;
}

function _nonIterableRest() {
  throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
}

var SPIN_START = 'SPIN_START';
var SPIN_DURATION = '@@SPIN_DURATION';
var SPIN_STOP = 'SPIN_STOP';
var spinner = {
    name: 'spinner',
    actions: {
        start: function start(message, duration, type) {
            return {
                type: SPIN_START,
                payload: {
                    message: message,
                    duration: duration,
                    type: type
                }
            };
        },
        alert: function alert(message) {
            return {
                type: SPIN_DURATION,
                payload: {
                    message: message,
                    duration: 1.5,
                    type: 'alert'
                }
            };
        },
        stop: function stop() {
            return {
                type: SPIN_STOP
            };
        }
    },
    thunks: {
        SPIN_DURATION: function () {
            var _SPIN_DURATION = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee(dispatch, getState, bag) {
                var action, _action$payload, message, duration, type;

                return _regeneratorRuntime__default['default'].wrap(function _callee$(_context) {
                    while (1) {
                        switch (_context.prev = _context.next) {
                            case 0:
                                action = bag.action, _action$payload = action.payload, message = _action$payload.message, duration = _action$payload.duration, type = _action$payload.type;
                                dispatch({
                                    type: SPIN_START,
                                    payload: {
                                        message: message,
                                        type: type
                                    }
                                });

                                if (!duration) {
                                    _context.next = 6;
                                    break;
                                }

                                _context.next = 5;
                                return new Promise(function (resolve) {
                                    return setTimeout(resolve, duration * 1000);
                                });

                            case 5:
                                dispatch({
                                    type: SPIN_STOP
                                });

                            case 6:
                            case "end":
                                return _context.stop();
                        }
                    }
                }, _callee);
            }));

            function SPIN_DURATION(_x, _x2, _x3) {
                return _SPIN_DURATION.apply(this, arguments);
            }

            return SPIN_DURATION;
        }()
    },
    reducer: function reducer() {
        var context = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        var action = arguments.length > 1 ? arguments[1] : undefined;

        if (action.type === SPIN_START) {
            context = _objectSpread2({
                active: true
            }, action.payload);
        } else if (action.type === SPIN_STOP) {
            context = {};
        }

        return context;
    }
};

var LOGIN_SUCCESS = 'LOGIN_SUCCESS',
    LOGIN_CHECK = 'LOGIN_CHECK',
    LOGIN_RELOAD = 'LOGIN_RELOAD',
    LOGOUT_SUBMIT = 'LOGOUT_SUBMIT',
    LOGOUT_SUCCESS = 'LOGOUT_SUCCESS',
    CSRFTOKEN = 'CSRFTOKEN';
var auth = {
    name: 'auth',
    persist: true,
    pages: {
        login: {
            url: 'login'
        },
        logout: {
            url: 'logout',
            thunk: function thunk(dispatch, getState) {
                if (!getState().auth.user) {
                    return;
                }

                dispatch({
                    type: LOGOUT_SUBMIT
                });
            }
        }
    },
    start: function start() {
        this.refreshCSRFToken();
        this.app.store.dispatch({
            type: LOGIN_CHECK
        });
    },
    getState: function getState() {
        return this.app.store.getState().auth || {};
    },
    reducer: function reducer() {
        var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        var action = arguments.length > 1 ? arguments[1] : undefined;

        switch (action.type) {
            case LOGIN_SUCCESS:
            case LOGIN_RELOAD:
                {
                    var _action$payload = action.payload,
                        user = _action$payload.user,
                        config = _action$payload.config,
                        csrftoken = _action$payload.csrftoken;
                    return {
                        user: user,
                        config: config,
                        csrftoken: csrftoken
                    };
                }

            case LOGOUT_SUBMIT:
                {
                    return {};
                }

            case LOGOUT_SUCCESS:
                {
                    var _ref = action.payload || {},
                        _csrftoken = _ref.csrftoken;

                    if (_csrftoken) {
                        return {
                            csrftoken: _csrftoken
                        };
                    } else {
                        return {};
                    }
                }

            case CSRFTOKEN:
                {
                    var _csrftoken2 = action.payload.csrftoken;
                    return _objectSpread2(_objectSpread2({}, state), {}, {
                        csrftoken: _csrftoken2
                    });
                }

            default:
                {
                    return state;
                }
        }
    },
    thunks: {
        CSRFTOKEN: function CSRFTOKEN() {
            this.refreshCSRFToken();
        },
        // LOGIN_SUBMIT handled automatically by @wq/outbox form logic
        LOGIN_SUCCESS: function LOGIN_SUCCESS() {
            this.refreshUserInfo();
        },
        LOGIN_RELOAD: function LOGIN_RELOAD() {
            this.refreshUserInfo();
        },
        LOGIN_CHECK: function LOGIN_CHECK(dispatch, getState) {
            var user = getState().auth.user,
                ds = this.app.store;
            setTimeout(function () {
                ds.fetch('/login').then(function (result) {
                    if (result && result.user && result.config) {
                        dispatch({
                            type: LOGIN_RELOAD,
                            payload: result
                        });
                    } else {
                        var _ref2 = result || {},
                            csrftoken = _ref2.csrftoken;

                        dispatch({
                            type: user ? LOGOUT_SUCCESS : CSRFTOKEN,
                            payload: {
                                csrftoken: csrftoken
                            }
                        });
                    }
                });
            }, 10);
        },
        LOGOUT_SUBMIT: function LOGOUT_SUBMIT(dispatch) {
            this.app.store.fetch('/logout').then(function (result) {
                dispatch({
                    type: LOGOUT_SUCCESS,
                    payload: result
                });
            });
        },
        LOGOUT_SUCCESS: function LOGOUT_SUCCESS() {
            this.refreshUserInfo();
        }
    },
    context: function context(ctx) {
        return this.userInfo(ctx);
    },
    userInfo: function userInfo(ctx) {
        var _this$getState = this.getState(),
            user = _this$getState.user,
            config = _this$getState.config,
            csrftoken = _this$getState.csrftoken,
            pageConf = ctx.router_info && ctx.router_info.page_config || {},
            wqPageConf = config && config.pages && config.pages[pageConf.name] || {};

        return {
            user: user,
            is_authenticated: !!user,
            app_config: this.app.config,
            wq_config: config,
            csrf_token: csrftoken,
            router_info: _objectSpread2(_objectSpread2({}, ctx.router_info), {}, {
                page_config: _objectSpread2(_objectSpread2({}, pageConf), {}, {
                    can_view: wqPageConf.can_view !== false,
                    can_add: wqPageConf.can_add || false,
                    can_change: wqPageConf.can_change || false,
                    can_delete: wqPageConf.can_delete || false
                })
            })
        };
    },
    refreshUserInfo: function refreshUserInfo() {
        var _this = this;

        return _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee() {
            var app, context;
            return _regeneratorRuntime__default['default'].wrap(function _callee$(_context) {
                while (1) {
                    switch (_context.prev = _context.next) {
                        case 0:
                            _context.next = 2;
                            return _this.refreshCSRFToken();

                        case 2:
                            app = _this.app, context = app.router.getContext();
                            app.router.render(_objectSpread2(_objectSpread2({}, context), _this.userInfo(context)), true); // FIXME: Better way to do this?

                            app.spin.start();
                            _context.next = 7;
                            return app.prefetchAll();

                        case 7:
                            app.spin.stop();
                            _context.next = 10;
                            return app.router.reload();

                        case 10:
                        case "end":
                            return _context.stop();
                    }
                }
            }, _callee);
        }))();
    },
    refreshCSRFToken: function refreshCSRFToken() {
        var _this2 = this;

        return _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee2() {
            var _this2$getState, csrftoken;

            return _regeneratorRuntime__default['default'].wrap(function _callee2$(_context2) {
                while (1) {
                    switch (_context2.prev = _context2.next) {
                        case 0:
                            _this2$getState = _this2.getState(), csrftoken = _this2$getState.csrftoken;

                            _this2.app.outbox.setCSRFToken(csrftoken);

                        case 2:
                        case "end":
                            return _context2.stop();
                    }
                }
            }, _callee2);
        }))();
    }
};

var app = {
    OFFLINE: 'offline',
    FAILURE: 'failure',
    ERROR: 'error',

    get wq_config() {
        return this.getAuthState().config || this.config;
    },

    get user() {
        return this.getAuthState().user;
    },

    get csrftoken() {
        return this.getAuthState().csrftoken;
    }

};
var SERVER = '@@SERVER';
var CORE_PLUGINS = ['renderer'];
app.models = {};
app.plugins = {};
var _register = {};

app.init = function (config) {
    if (!config) {
        config = {};
    }

    if (!config.pages) {
        config.pages = {};
    }

    CORE_PLUGINS.forEach(function (type) {
        if (!app[type]) {
            throw new Error("Register a ".concat(type, " with app.use()"));
        }
    });
    app.use(spinner);
    app.use(syncUpdateUrl);

    if (config.pages.login && !app.plugins.auth) {
        // FIXME: Require explicit auth registration in 2.0
        app.use(auth);
    }

    router__default['default'].addRouteInfo(_extendRouteInfo);
    router__default['default'].addContext(function () {
        return spinner.start() && {};
    });
    router__default['default'].addContext(_getSyncInfo); // Router (wq/router.js) configuration

    if (!config.router) {
        config.router = {
            base_url: ''
        };
    }

    config.router.getTemplateName = function (name) {
        return name.split(':')[0];
    }; // Store (wq/store.js) configuration


    if (!config.store) {
        config.store = {
            service: config.router.base_url,
            defaults: {
                format: 'json'
            }
        };
    }

    if (!config.store.fetchFail) {
        config.fetchFail = _fetchFail;
    }

    Object.entries(app.plugins).forEach(function (_ref) {
        var _ref2 = _slicedToArray(_ref, 2),
            name = _ref2[0],
            plugin = _ref2[1];

        if (plugin.ajax) {
            config.store.ajax = plugin.ajax.bind(plugin);
        }

        if (plugin.reducer) {
            ds__default['default'].addReducer(name, function (state, action) {
                return plugin.reducer(state, action);
            }, plugin.persist || false);
        }

        if (plugin.actions) {
            Object.assign(plugin, ds__default['default'].bindActionCreators(plugin.actions));
        }

        if (plugin.thunks) {
            router__default['default'].addThunks(plugin.thunks, plugin);
        }

        if (plugin.subscriber) {
            ds__default['default'].subscribe(function () {
                return plugin.subscriber(ds__default['default'].getState());
            });
        }

        if (plugin.pages) {
            Object.assign(config.pages, plugin.pages);
        }
    });
    app.spin = {
        start: function start(msg, duration, opts) {
            return spinner.start(msg, duration, opts);
        },
        forSeconds: function forSeconds(duration) {
            return spinner.start(null, duration);
        },
        stop: function stop() {
            return spinner.stop();
        }
    }; // Outbox (wq/outbox.js) configuration

    if (!config.outbox) {
        config.outbox = {};
    } // Propagate debug setting to other modules


    if (config.debug) {
        config.router.debug = config.debug;
        config.store.debug = config.debug;
        CORE_PLUGINS.forEach(function (type) {
            if (config[type]) {
                config[type].debug = config.debug;
            }
        });
    } // Load missing (non-local) content as JSON, or as server-rendered HTML?
    // Default (as of 1.0) is to load JSON and render on client.


    config.loadMissingAsJson = config.loadMissingAsJson || !config.loadMissingAsHtml;
    config.loadMissingAsHtml = !config.loadMissingAsJson; // After a form submission, sync in the background, or wait before
    // continuing?  Default is to sync in the background.

    if (config.backgroundSync === undefined) {
        config.backgroundSync = true;
    }

    app.config = config;
    app['native'] = !!window.cordova; // Initialize wq/router.js

    router__default['default'].init(config.router);
    app.base_url = router__default['default'].base_url;
    app.store = ds__default['default'];
    app.outbox = outbox__default['default'];
    outbox__default['default'].app = app;
    app.router = router__default['default']; // Option to submit forms in the background rather than wait for each post

    if (config.backgroundSync) {
        if (config.backgroundSync === -1) {
            outbox__default['default'].pause();
        } else if (config.backgroundSync > 1) {
            console.warn('Sync interval is now controlled by redux-offline');
        }
    } // Deprecated hooks


    var deprecated = {
        noBackgroundSync: 'backgroundSync: false',
        postsave: 'a postsaveurl() plugin hook or a postsave page config',
        saveerror: 'an onsync() plugin hook',
        showOutboxErrors: 'an onsync() and/or run() hook',
        _addOutboxItemsToContext: "@wq/outbox's IMMEDIATE mode",
        presync: 'the template context',
        postsync: 'the template context or an onsync() plugin hook'
    };
    Object.entries(deprecated).forEach(function (_ref3) {
        var _ref4 = _slicedToArray(_ref3, 2),
            hook = _ref4[0],
            alternative = _ref4[1];

        // TODO: Make this an error in 2.0
        if (config[hook]) {
            console.warn(new Error("config.".concat(hook, " has no effect.  Use ").concat(alternative, " instead.  See wq.app 1.2 release notes for more info.")));
        }
    });

    if (app.hasPlugin('onsave')) {
        console.warn(new Error('An onsave() plugin hook has no effect.  Use an onsync() hook instead.  See wq.app 1.2 release notes for more info.'));
    }

    Object.keys(app.config.pages).forEach(function (page) {
        app.config.pages[page].name = page;
    });
    app.callPlugins('init'); // Register routes with wq/router.js

    var root = false;
    Object.keys(app.config.pages).forEach(function (page) {
        var conf = _getBaseConf(page);

        if (!conf.url) {
            root = true;
        }

        if (conf.list) {
            conf.modes.forEach(function (mode) {
                var register = _register[mode] || _register.detail;
                register(page, mode);
            });
            (conf.server_modes || []).forEach(function (mode) {
                _register.detail(page, mode, _serverContext);
            });
            app.models[page] = modelModule__default['default'](conf);
        } else if (conf) {
            _registerOther(page);
        }
    }); // Register outbox

    router__default['default'].register('outbox/', 'outbox_list', function () {
        return outbox__default['default'].loadItems();
    });
    router__default['default'].register('outbox/<slug>', 'outbox_detail', _renderOutboxItem);
    router__default['default'].register('outbox/<slug>/edit', 'outbox_edit', _renderOutboxItem); // Fallback index page

    if (!root && !app.config.pages.index) {
        router__default['default'].registerLast('', 'index');
    }

    app.use({
        context: function context(ctx, routeInfo) {
            // FIXME: Remove in 2.0, in favor of useSitemap()
            if (routeInfo.name !== 'index') {
                return;
            }

            var context = {};
            context.pages = Object.keys(app.config.pages).map(function (page) {
                var conf = app.config.pages[page];
                return {
                    name: page,
                    url: conf.url,
                    list: conf.list
                };
            });
            return context;
        }
    }); // Fallback for all other URLs

    router__default['default'].registerLast(':path*', SERVER, _serverContext);
    Object.entries(app.plugins).forEach(function (_ref5) {
        var _ref6 = _slicedToArray(_ref5, 2),
            name = _ref6[0],
            plugin = _ref6[1];

        if (plugin.context) {
            router__default['default'].addContext(function (ctx) {
                return plugin.context(ctx, ctx.router_info);
            });
        }
    });
    router__default['default'].addContext(function () {
        return spinner.stop() && {};
    }); // Initialize wq/store.js and wq/outbox.js

    ds__default['default'].init(config.store);
    app.service = ds__default['default'].service;
    var ready = ds__default['default'].ready.then(function () {
        return outbox__default['default'].init(config.outbox);
    });

    if (app.config.jqmInit) {
        // FIXME: Remove in 2.0
        ready = ready.then(app.jqmInit);
    }

    if (app.config.autoStart !== false) {
        ready = ready.then(app.start);
    }

    return ready;
};

var pcount = 0;

app.use = function (plugin) {
    if (Array.isArray(plugin)) {
        plugin.forEach(function (p) {
            return app.use(p);
        });
        return;
    }

    if (plugin.dependencies) {
        app.use(plugin.dependencies);
    }

    if (app.plugins[plugin.name]) {
        if (app.plugins[plugin.name] === plugin) {
            return;
        } else {
            throw new Error("App already has a plugin named ".concat(plugin.name, "!"));
        }
    }

    pcount++;

    if (!plugin.name) {
        plugin.name = 'plugin' + pcount;
    }

    app.plugins[plugin.name] = plugin;
    plugin.app = app;

    if (plugin.type) {
        if (app[plugin.type]) {
            throw new Error("App already has a ".concat(plugin.type, " (").concat(app[plugin.type].name, ")"));
        }

        app[plugin.type] = plugin;
    }
};

app.prefetchAll = function () {
    return Promise.all(Object.keys(app.models).map(function (name) {
        return app.models[name].prefetch();
    }));
};

app.jqmInit = function () {
    console.warn(new Error('jqmInit() renamed to start()'));
    app.start();
};

app.start = function () {
    router__default['default'].start();
    app.callPlugins('start');
};

function _getSyncInfo() {
    return _getSyncInfo2.apply(this, arguments);
}

function _getSyncInfo2() {
    _getSyncInfo2 = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee4() {
        var unsynced;
        return _regeneratorRuntime__default['default'].wrap(function _callee4$(_context4) {
            while (1) {
                switch (_context4.prev = _context4.next) {
                    case 0:
                        _context4.next = 2;
                        return outbox__default['default'].unsynced();

                    case 2:
                        unsynced = _context4.sent;
                        return _context4.abrupt("return", {
                            svc: app.service,
                            native: app['native'],
                            syncing: app.syncing,
                            unsynced: unsynced
                        });

                    case 4:
                    case "end":
                        return _context4.stop();
                }
            }
        }, _callee4);
    }));
    return _getSyncInfo2.apply(this, arguments);
}

app.go = function () {
    throw new Error('app.go() has been removed.  Use app.nav() instead');
}; // Sync outbox and handle result


app.sync = function (retryAll) {
    if (retryAll) {
        console.warn('app.sync(true) renamed to app.retryAll()');
        app.retryAll();
    } else {
        throw new Error('app.sync() no longer used.');
    }
};

app.retryAll = function () {
    app.outbox.unsynced().then(function (unsynced) {
        if (!unsynced) {
            return;
        }

        app.outbox.retryAll();
    });
};

app.emptyOutbox = function (confirmFirst) {
    /* global confirm */
    if (confirmFirst) {
        if (navigator.notification && navigator.notification.confirm) {
            navigator.notification.confirm('Empty Outbox?', function (button) {
                if (button == 1) {
                    app.emptyOutbox();
                }
            });
            return;
        } else {
            if (!confirm('Empty Outbox?')) {
                return;
            }
        }
    }

    return outbox__default['default'].empty();
};

app.confirmSubmit = function (form, message) {
    /* global confirm */
    if (navigator.notification && navigator.notification.confirm) {
        if (form.dataset.wqConfirmSubmit) {
            return true;
        }

        navigator.notification.confirm(message, function (button) {
            if (button == 1) {
                form.dataset.wqConfirmSubmit = true;
                form.submit();
            }
        });
    } else {
        if (confirm(message)) {
            return true;
        }
    }

    return false;
}; // Handle navigation after form submission


app.postSaveNav = function (item, alreadySynced) {
    var url;
    var pluginUrl = app.callPlugins('postsaveurl', [item, alreadySynced]).filter(function (item) {
        return !!item;
    });

    if (pluginUrl.length) {
        url = pluginUrl[0];
    } else {
        url = app.postsaveurl(item, alreadySynced);
    } // Navigate to computed URL


    if (app.config.debug) {
        console.log('Successfully saved; continuing to ' + url);
    }

    router__default['default'].push(url);
};

app.postsaveurl = function (item, alreadySynced) {
    var postsave, pconf, match, mode, url, itemid, modelConf; // conf.postsave can be set redirect to another page

    modelConf = item.options.modelConf;

    if (item.deletedId) {
        postsave = modelConf.postdelete;
    } else {
        postsave = modelConf.postsave;
    }

    if (!postsave) {
        // Otherwise, default is to return the page for the item just saved
        if (!alreadySynced || item.deletedId) {
            // If backgroundSync, return to list view while syncing
            postsave = modelConf.name + '_list';
        } else {
            // If !backgroundSync, return to the newly synced item
            postsave = modelConf.name + '_detail';
        }
    } // conf.postsave should explicitly indicate which template mode to use

    /* eslint no-useless-escape: off */


    match = postsave.match(/^([^\/]+)_([^_\/]+)$/);

    if (match) {
        postsave = match[1];
        mode = match[2];
    } // Retrieve configuration for postsave page, if any


    pconf = _getConf(postsave, true); // Compute URL

    if (!pconf) {
        // If conf.postsave is not the name of a list page, assume it's a
        // simple page or a URL
        var urlContext;

        if (item.deletedId) {
            urlContext = _objectSpread2({
                deleted: true
            }, router__default['default'].getContext());
        } else {
            urlContext = _objectSpread2(_objectSpread2({}, item.data), item.result);
        }

        url = app.base_url + '/' + Mustache__default['default'].render(postsave, urlContext);
    } else if (!pconf.list) {
        url = app.base_url + '/' + pconf.url;
    } else {
        if (pconf.modes.concat(pconf.server_modes || []).indexOf(mode) == -1) {
            throw 'Unknown template mode!';
        } // For list pages, the url can differ depending on the mode


        url = app.base_url + '/' + pconf.url + '/';

        if (mode != 'list') {
            // Detail or edit view; determine item id and add to url
            if (postsave == modelConf.name && !item.synced) {
                // Config indicates return to detail/edit view of the model
                // that was just saved, but the item hasn't been synced yet.
                // Navigate to outbox URL instead.
                url = app.base_url + '/outbox/' + item.id;

                if (mode != 'edit' && item.error) {
                    // Return to edit form if there was an error
                    mode = 'edit';
                }
            } else {
                // Item has been successfully synced
                if (postsave == modelConf.name) {
                    // If postsave page is the same as the item's page, use the
                    // new id
                    itemid = item.result && item.result.id;
                } else {
                    // Otherwise, look for a foreign key reference
                    // FIXME: what if the foreign key has a different name?
                    itemid = item.result && item.result[postsave + '_id'];
                }

                if (!itemid) {
                    throw 'Could not find ' + postsave + ' id in result!';
                }

                url += itemid;
            }

            if (mode != 'detail') {
                url += '/' + mode;
            }
        }
    }

    return url;
};

var syncUpdateUrl = {
    onsync: function onsync(obitem) {
        var context = router__default['default'].getContext() || {},
            _context$router_info = context.router_info,
            routeInfo = _context$router_info === void 0 ? {} : _context$router_info,
            full_path = routeInfo.full_path,
            item_id = routeInfo.item_id,
            parent_id = routeInfo.parent_id,
            _ref7 = obitem || {},
            outboxId = _ref7.id,
            result = _ref7.result,
            _ref8 = result || {},
            resultId = _ref8.id,
            outboxSlug = "outbox-".concat(outboxId);

        if (resultId && (item_id === outboxSlug || parent_id === outboxSlug)) {
            router__default['default'].push(full_path.replace(outboxSlug, resultId));
        }
    }
}; // Return a list of all foreign key fields

app.getParents = function (page) {
    var conf = _getBaseConf(page);

    return conf.form.filter(function (field) {
        return field['wq:ForeignKey'];
    }).map(function (field) {
        return field['wq:ForeignKey'];
    });
}; // Shortcuts for $.mobile.changePage


app.nav = function (url) {
    url = app.base_url + '/' + url;
    router__default['default'].push(url);
};

app.replaceState = function (url) {
    throw new Error('app.replaceState() no longer supported.');
};

app.refresh = function () {
    router__default['default'].refresh();
};

app.hasPlugin = function (method) {
    var plugin,
        fn,
        hasPlugin = false;

    for (plugin in app.plugins) {
        fn = app.plugins[plugin][method];

        if (fn) {
            hasPlugin = true;
        }
    }

    return hasPlugin;
};

app.callPlugins = function (method, args) {
    var plugin,
        fn,
        fnArgs,
        queue = [];

    for (plugin in app.plugins) {
        fn = app.plugins[plugin][method];

        if (args) {
            fnArgs = args;
        } else {
            fnArgs = [app.config[plugin]];
        }

        if (fn) {
            queue.push(fn.apply(app.plugins[plugin], fnArgs));
        }
    }

    return queue;
}; // Internal variables and functions


app.splitRoute = function (routeName) {
    var match = routeName.match(/^(.+)_([^_]+)$/);
    var page, mode, variant;

    if (match) {
        page = match[1];
        mode = match[2];

        if (mode.indexOf(':') > -1) {
            var _mode$split = mode.split(':');

            var _mode$split2 = _slicedToArray(_mode$split, 2);

            mode = _mode$split2[0];
            variant = _mode$split2[1];
        } else {
            variant = null;
        }
    } else {
        page = routeName;
        mode = null;
        variant = null;
    }

    return [page, mode, variant];
};

function _joinRoute(page, mode, variant) {
    if (variant) {
        return page + '_' + mode + ':' + variant;
    } else if (mode) {
        return page + '_' + mode;
    } else {
        return page;
    }
}

function _extendRouteInfo(routeInfo) {
    var routeName = routeInfo.name,
        itemid = routeInfo.slugs.slug || null;

    var _app$splitRoute = app.splitRoute(routeName),
        _app$splitRoute2 = _slicedToArray(_app$splitRoute, 3),
        page = _app$splitRoute2[0],
        mode = _app$splitRoute2[1],
        variant = _app$splitRoute2[2],
        conf = _getConf(page, true, true),
        pageid = null;

    if (conf) {
        if (mode && mode !== 'list') {
            pageid = page + '_' + mode + (variant ? '_' + variant : '') + (itemid ? '_' + itemid : '') + '-page';
        }
    } else if (page === 'outbox') {
        conf = {
            name: 'outbox',
            url: 'outbox',
            page: 'outbox',
            form: [],
            modes: ['list', 'detail', 'edit']
        };
    } else {
        page = routeName;
        mode = null;
        conf = {
            name: page,
            page: page,
            form: [],
            modes: []
        };
    }

    return _objectSpread2(_objectSpread2({}, routeInfo), {}, {
        page: page,
        page_config: conf,
        mode: mode,
        variant: variant,
        item_id: itemid,
        dom_id: pageid
    });
} // Generate list view context and render with [url]_list template;
// handles requests for [url] and [url]/


_register.list = function (page) {
    var conf = _getBaseConf(page),
        register = conf.url === '' ? router__default['default'].registerLast : router__default['default'].register,
        url = conf.url === '' ? '' : conf.url + '/';

    register(url, _joinRoute(page, 'list'), function (ctx) {
        return _displayList(ctx);
    }); // Special handling for /[parent_list_url]/[parent_id]/[url]

    app.getParents(page).forEach(function (ppage) {
        var pconf = _getBaseConf(ppage);

        var url = pconf.url;
        var registerParent;

        if (url === '') {
            registerParent = router__default['default'].registerLast;
        } else {
            registerParent = router__default['default'].register;
            url += '/';
        }

        url += ':parent_id/' + conf.url;
        registerParent(url, _joinRoute(page, 'list', ppage), parentContext);
    });

    function parentContext(_x) {
        return _parentContext.apply(this, arguments);
    }

    function _parentContext() {
        _parentContext = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee(ctx) {
            var routeInfo, page, ppage, parent_id, pconf, pitem, parentUrl, parentInfo;
            return _regeneratorRuntime__default['default'].wrap(function _callee$(_context) {
                while (1) {
                    switch (_context.prev = _context.next) {
                        case 0:
                            routeInfo = ctx.router_info;
                            page = routeInfo.page;
                            ppage = routeInfo.variant;
                            parent_id = routeInfo.slugs.parent_id;
                            pconf = _getConf(ppage);
                            _context.next = 7;
                            return app.models[ppage].find(parent_id);

                        case 7:
                            pitem = _context.sent;

                            if (pitem) {
                                parentUrl = pconf.url + '/' + pitem.id;
                            } else if (parent_id.indexOf('outbox-') == -1) {
                                parentUrl = 'outbox/' + parent_id.split('-')[1];
                            } else {
                                parentUrl = null;
                            }

                            parentInfo = {
                                parent_id: parent_id,
                                parent_url: parentUrl,
                                parent_label: pitem && pitem.label,
                                parent_page: ppage,
                                parent_conf: pconf
                            };
                            parentInfo['parent_is_' + ppage] = true;
                            return _context.abrupt("return", _displayList(ctx, _objectSpread2(_objectSpread2({}, parentInfo), {}, {
                                router_info: _objectSpread2(_objectSpread2({}, routeInfo), parentInfo)
                            })));

                        case 12:
                        case "end":
                            return _context.stop();
                    }
                }
            }, _callee);
        }));
        return _parentContext.apply(this, arguments);
    }
};

app._addOutboxItemsToContext = function (context, unsyncedItems) {
    // Add any outbox items to context
    context.unsynced = unsyncedItems.length;
    context.unsyncedItems = unsyncedItems;
};

function _displayList(_x2, _x3) {
    return _displayList2.apply(this, arguments);
} // Generate item detail view context and render with [url]_detail template;
// handles requests for [url]/[id]


function _displayList2() {
    _displayList2 = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee6(ctx, parentInfo) {
        var routeInfo, page, params, url, conf, model, pnum, next, prev, filter, key, showUnsynced, getData, getUnsynced, _getUnsynced, unsynced1, data1, unsynced2, data, unsyncedItems, prevIsLocal, currentIsLocal, prevp, nextp, context;

        return _regeneratorRuntime__default['default'].wrap(function _callee6$(_context6) {
            while (1) {
                switch (_context6.prev = _context6.next) {
                    case 0:
                        _getUnsynced = function _getUnsynced3() {
                            _getUnsynced = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee5() {
                                return _regeneratorRuntime__default['default'].wrap(function _callee5$(_context5) {
                                    while (1) {
                                        switch (_context5.prev = _context5.next) {
                                            case 0:
                                                if (!showUnsynced) {
                                                    _context5.next = 4;
                                                    break;
                                                }

                                                return _context5.abrupt("return", model.unsyncedItems());

                                            case 4:
                                                return _context5.abrupt("return", []);

                                            case 5:
                                            case "end":
                                                return _context5.stop();
                                        }
                                    }
                                }, _callee5);
                            }));
                            return _getUnsynced.apply(this, arguments);
                        };

                        getUnsynced = function _getUnsynced2() {
                            return _getUnsynced.apply(this, arguments);
                        };

                        getData = function _getData() {
                            if (filter) {
                                return model.filterPage(filter);
                            } else if (pnum > model.opts.page) {
                                return model.page(pnum);
                            } else {
                                return model.load();
                            }
                        };

                        routeInfo = ctx.router_info, page = routeInfo.page, params = routeInfo.params, url = routeInfo.full_path, conf = _getConf(page), model = app.models[page];
                        pnum = model.opts.page, next = null, prev = null;

                        if (params || parentInfo) {
                            if (params && params.page) {
                                pnum = params.page;
                            }

                            filter = {};

                            for (key in params || {}) {
                                if (key != 'page') {
                                    filter[key] = params[key];
                                }
                            }

                            if (parentInfo) {
                                conf.form.forEach(function (field) {
                                    if (field['wq:ForeignKey'] == parentInfo.parent_page) {
                                        filter[field.name + '_id'] = parentInfo.parent_id;
                                    }
                                });
                            }
                        }

                        if (filter && !Object.keys(filter).length) {
                            filter = null;
                        } // Load from server if data might not exist locally


                        if (!app.config.loadMissingAsHtml) {
                            _context6.next = 16;
                            break;
                        }

                        if (model.opts.client) {
                            _context6.next = 10;
                            break;
                        }

                        return _context6.abrupt("return", _loadFromServer(url));

                    case 10:
                        if (!(filter && model.opts.server)) {
                            _context6.next = 12;
                            break;
                        }

                        return _context6.abrupt("return", _loadFromServer(url));

                    case 12:
                        if (!(pnum > model.opts.page)) {
                            _context6.next = 14;
                            break;
                        }

                        return _context6.abrupt("return", _loadFromServer(url));

                    case 14:
                        _context6.next = 17;
                        break;

                    case 16:
                        if (filter && pnum > model.opts.page) {
                            filter.page = pnum;
                        }

                    case 17:
                        if (!pnum && (!model.opts.client || filter)) {
                            pnum = 1;
                        }

                        showUnsynced = pnum == model.opts.page || pnum == 1 && !model.opts.client;
                        _context6.next = 21;
                        return getUnsynced();

                    case 21:
                        unsynced1 = _context6.sent;
                        _context6.next = 24;
                        return getData();

                    case 24:
                        data1 = _context6.sent;
                        _context6.next = 27;
                        return getUnsynced();

                    case 27:
                        unsynced2 = _context6.sent;

                        if (!(unsynced1 && unsynced2 && unsynced1.length != unsynced2.length)) {
                            _context6.next = 34;
                            break;
                        }

                        _context6.next = 31;
                        return getData();

                    case 31:
                        data = _context6.sent;
                        _context6.next = 35;
                        break;

                    case 34:
                        data = data1;

                    case 35:
                        unsyncedItems = unsynced2;

                        if (pnum > model.opts.page && (model.opts.client || pnum > 1)) {
                            if (+pnum - 1 > model.opts.page && (model.opts.client || pnum > 2)) {
                                prevp = filter ? _objectSpread2({}, filter) : {};
                                prevp.page = +pnum - 1;
                                prev = conf.url + '/?' + new URLSearchParams(prevp).toString();
                            } else if (pnum == 1 && !filter) {
                                prev = conf.url + '/';
                                prevIsLocal = true;
                            }
                        }

                        if (pnum < data.pages && (model.opts.server || pnum)) {
                            nextp = filter ? _objectSpread2({}, filter) : {};
                            nextp.page = +pnum + 1;
                            next = conf.url + '/?' + new URLSearchParams(nextp).toString();

                            if (nextp.page == 1) {
                                currentIsLocal = true;
                            }
                        }

                        context = _objectSpread2(_objectSpread2(_objectSpread2({}, data), parentInfo), {}, {
                            previous: prev ? '/' + prev : null,
                            next: next ? '/' + next : null,
                            multiple: prev || next ? true : false,
                            page: pnum,
                            show_unsynced: showUnsynced,
                            previous_is_local: prevIsLocal,
                            current_is_local: currentIsLocal
                        });

                        app._addOutboxItemsToContext(context, unsyncedItems);

                        return _context6.abrupt("return", _addLookups(page, context, false));

                    case 41:
                    case "end":
                        return _context6.stop();
                }
            }
        }, _callee6);
    }));
    return _displayList2.apply(this, arguments);
}

_register.detail = function (page, mode) {
    var contextFn = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : _displayItem;

    var conf = _getBaseConf(page);

    var url = _getDetailUrl(conf.url, mode);

    var register = conf.url === '' ? router__default['default'].registerLast : router__default['default'].register;
    register(url, _joinRoute(page, mode), contextFn);
};

function _getDetailUrl(url, mode) {
    if (url) {
        url += '/';
    }

    url += '<slug>';

    if (mode != 'detail') {
        url += '/' + mode;
    }

    return url;
} // Generate item edit context and render with [url]_edit template;
// handles requests for [url]/[id]/edit and [url]/new


_register.edit = function (page) {
    var conf = _getBaseConf(page);

    var register = conf.url === '' ? router__default['default'].registerLast : router__default['default'].register;
    register(_getDetailUrl(conf.url, 'edit'), _joinRoute(page, 'edit'), _displayItem);
    router__default['default'].registerFirst(conf.url + '/new', _joinRoute(page, 'edit', 'new'), _displayItem);
};

function _displayItem(_x4) {
    return _displayItem2.apply(this, arguments);
} // Render non-list pages with with [url] template;
// handles requests for [url] and [url]/


function _displayItem2() {
    _displayItem2 = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee7(ctx) {
        var routeInfo, itemid, page, mode, variant, url, conf, model, item, localOnly;
        return _regeneratorRuntime__default['default'].wrap(function _callee7$(_context7) {
            while (1) {
                switch (_context7.prev = _context7.next) {
                    case 0:
                        routeInfo = ctx.router_info, itemid = routeInfo.item_id, page = routeInfo.page, mode = routeInfo.mode, variant = routeInfo.variant, url = routeInfo.full_path, conf = _getConf(page), model = app.models[page];

                        if (!(mode == 'edit' && variant == 'new')) {
                            _context7.next = 5;
                            break;
                        }

                        item = _objectSpread2(_objectSpread2({}, routeInfo.params), conf.defaults);
                        _context7.next = 15;
                        break;

                    case 5:
                        localOnly = !app.config.loadMissingAsJson;
                        _context7.next = 8;
                        return model.find(itemid, localOnly);

                    case 8:
                        item = _context7.sent;

                        if (item) {
                            _context7.next = 15;
                            break;
                        }

                        if (!(model.opts.server && app.config.loadMissingAsHtml)) {
                            _context7.next = 14;
                            break;
                        }

                        return _context7.abrupt("return", _loadFromServer(url));

                    case 14:
                        return _context7.abrupt("return", router__default['default'].notFound());

                    case 15:
                        if (!item) {
                            _context7.next = 28;
                            break;
                        }

                        item.local = true;

                        if (!(mode == 'edit')) {
                            _context7.next = 25;
                            break;
                        }

                        if (!(variant == 'new')) {
                            _context7.next = 22;
                            break;
                        }

                        return _context7.abrupt("return", _addLookups(page, item, 'new'));

                    case 22:
                        return _context7.abrupt("return", _addLookups(page, item, true));

                    case 23:
                        _context7.next = 26;
                        break;

                    case 25:
                        return _context7.abrupt("return", _addLookups(page, item, false));

                    case 26:
                        _context7.next = 33;
                        break;

                    case 28:
                        if (!(model.opts.server && app.config.loadMissingAsHtml)) {
                            _context7.next = 32;
                            break;
                        }

                        return _context7.abrupt("return", _loadFromServer(url));

                    case 32:
                        return _context7.abrupt("return", router__default['default'].notFound());

                    case 33:
                    case "end":
                        return _context7.stop();
                }
            }
        }, _callee7);
    }));
    return _displayItem2.apply(this, arguments);
}

function _registerOther(page) {
    var conf = _getBaseConf(page);

    router__default['default'].register(conf.url, page, conf.context || _displayOther, undefined, conf.thunk || null);

    function _displayOther() {
        return _displayOther2.apply(this, arguments);
    }

    function _displayOther2() {
        _displayOther2 = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee2() {
            return _regeneratorRuntime__default['default'].wrap(function _callee2$(_context2) {
                while (1) {
                    switch (_context2.prev = _context2.next) {
                        case 0:
                            if (!conf.server_only) {
                                _context2.next = 4;
                                break;
                            }

                            return _context2.abrupt("return", _loadFromServer(app.base_url + '/' + conf.url));

                        case 4:
                            return _context2.abrupt("return", {});

                        case 5:
                        case "end":
                            return _context2.stop();
                    }
                }
            }, _callee2);
        }));
        return _displayOther2.apply(this, arguments);
    }
}

function _renderOutboxItem(_x5) {
    return _renderOutboxItem2.apply(this, arguments);
}

function _renderOutboxItem2() {
    _renderOutboxItem2 = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee8(ctx) {
        var routeInfo, mode, item, id, page, template, idMatch, context;
        return _regeneratorRuntime__default['default'].wrap(function _callee8$(_context8) {
            while (1) {
                switch (_context8.prev = _context8.next) {
                    case 0:
                        routeInfo = ctx.router_info;
                        mode = routeInfo.mode;
                        _context8.next = 4;
                        return outbox__default['default'].loadItem(+routeInfo.slugs.slug);

                    case 4:
                        item = _context8.sent;

                        if (!(!item || !item.options || !item.options.modelConf)) {
                            _context8.next = 7;
                            break;
                        }

                        return _context8.abrupt("return", router__default['default'].notFound());

                    case 7:
                        page = item.options.modelConf.name, template = page + '_' + mode, idMatch = item.options.url.match(new RegExp(item.options.modelConf.url + '/([^/]+)$'));

                        if (item.data.id) {
                            id = item.data.id;
                        } else if (idMatch) {
                            id = idMatch[1];
                        } else {
                            id = 'new';
                        }

                        context = _objectSpread2({
                            outbox_id: item.id,
                            error: item.error,
                            router_info: _objectSpread2(_objectSpread2({}, routeInfo), {}, {
                                page_config: item.options.modelConf,
                                template: template,
                                outbox_id: item.id
                            })
                        }, deepcopy__default['default'](item.data));

                        if (id != 'new') {
                            context.id = id;
                        }

                        return _context8.abrupt("return", _addLookups(page, context, mode === 'edit'));

                    case 12:
                    case "end":
                        return _context8.stop();
                }
            }
        }, _callee8);
    }));
    return _renderOutboxItem2.apply(this, arguments);
}

app.isRegistered = function (url) {
    if (_getConfByUrl(url, true)) {
        return true;
    } else {
        return false;
    }
};

app.submitForm = /*#__PURE__*/function () {
    var _ref10 = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee3(_ref9) {
        var url, storage, backgroundSync, has_files, outboxId, preserve, vals, conf, options, item;
        return _regeneratorRuntime__default['default'].wrap(function _callee3$(_context3) {
            while (1) {
                switch (_context3.prev = _context3.next) {
                    case 0:
                        url = _ref9.url, storage = _ref9.storage, backgroundSync = _ref9.backgroundSync, has_files = _ref9.has_files, outboxId = _ref9.outboxId, preserve = _ref9.preserve, vals = _ref9.data;
                        conf = _getConfByUrl(url, true);
                        options = {
                            url: url
                        };

                        if (storage) {
                            options.storage = storage;
                        } else if (!backgroundSync) {
                            options.storage = 'temporary';
                        } else if (has_files) {
                            options.storage = 'store';
                        }

                        if (_hasNestedObject(vals)) {
                            if (has_files) {
                                vals = _flattenJson(vals);
                            } else {
                                options.json = true;
                            }
                        }

                        if (outboxId) {
                            options.id = outboxId;

                            if (preserve && preserve.split) {
                                options.preserve = preserve.split(/,/);
                            }
                        }

                        if (vals._method) {
                            options.method = vals._method;
                            delete vals._method;
                        } else {
                            options.method = 'POST';
                        }

                        if (conf) {
                            options.modelConf = conf;

                            if (conf.label_template) {
                                if (typeof conf.label_template === 'function') {
                                    options.label = conf.label_template(vals);
                                } else {
                                    options.label = Mustache__default['default'].render(conf.label_template, vals);
                                }
                            }
                        }

                        options.csrftoken = app.csrftoken;
                        _context3.next = 11;
                        return outbox__default['default'].save(vals, options);

                    case 11:
                        item = _context3.sent;

                        if (!backgroundSync) {
                            _context3.next = 15;
                            break;
                        }

                        // Send user to next screen while app syncs in background
                        app.postSaveNav(item, false);
                        return _context3.abrupt("return", [item, null]);

                    case 15:
                        // Submit form immediately and wait for server to respond
                        app.spin.start();
                        _context3.next = 18;
                        return outbox__default['default'].waitForItem(item.id);

                    case 18:
                        item = _context3.sent;
                        app.spin.stop();

                        if (item) {
                            _context3.next = 22;
                            break;
                        }

                        return _context3.abrupt("return", [item, app.FAILURE]);

                    case 22:
                        if (!item.synced) {
                            _context3.next = 25;
                            break;
                        }

                        // Item was synced
                        app.postSaveNav(item, true);
                        return _context3.abrupt("return", [item, null]);

                    case 25:
                        if (item.error) {
                            _context3.next = 30;
                            break;
                        }

                        // Save failed without server error: probably offline
                        // FIXME: waitForItem() probably doesn't resolve until back online.
                        app.postSaveNav(item, false);
                        return _context3.abrupt("return", [item, null]);

                    case 30:
                        if (!(typeof item.error === 'string')) {
                            _context3.next = 34;
                            break;
                        }

                        return _context3.abrupt("return", [item, app.FAILURE]);

                    case 34:
                        return _context3.abrupt("return", [item, app.ERROR]);

                    case 35:
                    case "end":
                        return _context3.stop();
                }
            }
        }, _callee3);
    }));

    return function (_x6) {
        return _ref10.apply(this, arguments);
    };
}();

function _hasNestedObject(value) {
    return Object.values(value).some(function (val) {
        return _typeof(val) === 'object' && (!Array.isArray(val) || _typeof(val[0]) === 'object');
    });
}

function _flattenJson(value) {
    var prefix = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : '';
    var result = {};

    if (prefix) {
        if (value === null || value === undefined) {
            return _defineProperty({}, prefix, '');
        } else if (_typeof(value) !== 'object') {
            return _defineProperty({}, prefix, value);
        }
    }

    Object.entries(value).forEach(function (_ref13) {
        var _ref14 = _slicedToArray(_ref13, 2),
            key = _ref14[0],
            val = _ref14[1];

        var fullKey = prefix ? "".concat(prefix, "[").concat(key, "]") : key;

        if (Array.isArray(val)) {
            val.forEach(function (row, i) {
                return Object.assign(result, _flattenJson(row, "".concat(fullKey, "[").concat(i, "]")));
            });
        } else if (_typeof(val) === 'object') {
            if (_isFile(val)) {
                result[fullKey] = val;
            } else if (_isGeometry(val)) {
                result[fullKey] = JSON.stringify(val);
            } else {
                Object.assign(result, _flattenJson(val, fullKey));
            }
        } else {
            result[fullKey] = val;
        }
    });
    return result;
}

function _isFile(val) {
    return val && val.type && val.name && val.body;
}

function _isGeometry(val) {
    return val && val.type && val.coordinates;
}

app.getAuthState = function () {
    return this.plugins.auth && this.plugins.auth.getState() || {};
}; // Add various callback functions to context object to automate foreign key
// lookups within templates


function _addLookups(page, context, editable) {
    var conf = _getConf(page);

    var lookups = {};

    function addLookups(field, nested) {
        var fname = nested || field.name; // Choice (select/radio) lookups

        if (field.choices) {
            lookups[fname + '_label'] = _choice_label_lookup(field.name, field.choices);

            if (editable) {
                lookups[fname + '_choices'] = _choice_dropdown_lookup(field.name, field.choices);
            }
        } // Foreign key lookups


        if (field['wq:ForeignKey']) {
            var nkey;

            if (nested) {
                nkey = fname.match(/^\w+\.(\w+)\[(\w+)\]$/);
            } else {
                nkey = fname.match(/^(\w+)\[(\w+)\]$/);
            }

            if (!nkey) {
                if (nested) {
                    lookups[fname] = _this_parent_lookup(field);
                } else {
                    lookups[fname] = _parent_lookup(field, context);
                }

                if (!context[fname + '_label']) {
                    lookups[fname + '_label'] = _parent_label_lookup(field);
                }
            }

            if (editable) {
                lookups[fname + '_list'] = _parent_dropdown_lookup(field, context, nkey);
            }
        } // Load types/initial list of nested forms
        // (i.e. repeats/attachments/EAV/child model)


        if (field.children) {
            field.children.forEach(function (child) {
                var fname = field.name ? field.name + '.' + child.name : child.name;
                addLookups(child, fname);
            });

            if (editable == 'new' && !context[field.name]) {
                lookups[field.name] = _default_attachments(field, context);
            }
        }
    }

    conf.form.forEach(function (field) {
        addLookups(field, false);
    }); // Process lookup functions

    var keys = Object.keys(lookups);
    var queue = keys.map(function (key) {
        return lookups[key];
    });
    return Promise.all(queue).then(function (results) {
        results.forEach(function (result, i) {
            var key = keys[i];
            context[key] = result;
        });
        results.forEach(function (result, i) {
            var parts = keys[i].split('.'),
                nested;

            if (parts.length != 2) {
                return;
            }

            nested = context[parts[0]];

            if (!nested) {
                return;
            }

            if (!Array.isArray(nested)) {
                nested = [nested];
            }

            nested.forEach(function (row) {
                row[parts[1]] = row[parts[1]] || result;
            });
        });
    }).then(function () {
        return context;
    });
} // Preset list of choices


function _choice_label_lookup(name, choices) {
    function choiceLabel() {
        if (!this[name]) {
            return;
        }

        var label;
        choices.forEach(function (choice) {
            if (choice.name == this[name]) {
                label = choice.label;
            }
        }, this);
        return label;
    }

    return Promise.resolve(choiceLabel);
}

function _choice_dropdown_lookup(name, choices) {
    choices = choices.map(function (choice) {
        return _objectSpread2({}, choice);
    });

    function choiceDropdown() {
        choices.forEach(function (choice) {
            if (choice.name == this[name]) {
                choice.selected = true;
            } else {
                choice.selected = false;
            }
        }, this);
        return choices;
    }

    return Promise.resolve(choiceDropdown);
} // Simple foreign key lookup


function _parent_lookup(field, context) {
    var model = app.models[field['wq:ForeignKey']];
    var id = context[field.name + '_id'];

    if (id) {
        if (id.match && id.match(/^outbox/)) {
            return _getOutboxRecord(model, id);
        } else {
            return model.find(id);
        }
    } else {
        return null;
    }
} // Foreign key lookup for objects other than root


function _this_parent_lookup(field) {
    var model = app.models[field['wq:ForeignKey']];
    return Promise.all([_getOutboxRecordLookup(model), model.load()]).then(function (results) {
        var obRecords = results[0];
        var existing = {};
        results[1].list.forEach(function (item) {
            existing[item.id] = item;
        });
        return function () {
            var parentId = this[field.name + '_id'];
            return obRecords[parentId] || existing[parentId];
        };
    });
} // Foreign key label


function _parent_label_lookup(field) {
    return _this_parent_lookup(field).then(function (lookup) {
        return function () {
            var p = lookup.call(this);
            return p && p.label;
        };
    });
} // List of all potential foreign key values (useful for generating dropdowns)


function _parent_dropdown_lookup(field, context, nkey) {
    var model = app.models[field['wq:ForeignKey']];
    var result;

    if (field.filter) {
        result = model.filter(_computeFilter(field.filter, context));
    } else {
        result = model.load().then(function (data) {
            return _getOutboxRecords(model).then(function (records) {
                return records.concat(data.list);
            });
        });
    }

    return result.then(function (choices) {
        return function () {
            var parents = [],
                current;

            if (nkey) {
                current = this[nkey[1]] && this[nkey[1]][nkey[2]];
            } else {
                current = this[field.name + '_id'];
            }

            choices.forEach(function (v) {
                var item = _objectSpread2({}, v);

                if (item.id == current) {
                    item.selected = true; // Currently selected item
                }

                parents.push(item);
            }, this);
            return parents;
        };
    });
}

function _getOutboxRecords(model) {
    return model.unsyncedItems().then(function (items) {
        return items.map(function (item) {
            return {
                id: 'outbox-' + item.id,
                label: item.label,
                outbox_id: item.id,
                outbox: true
            };
        });
    });
}

function _getOutboxRecordLookup(model) {
    return _getOutboxRecords(model).then(function (records) {
        var lookup = {};
        records.forEach(function (record) {
            lookup[record.id] = record;
        });
        return lookup;
    });
}

function _getOutboxRecord(model, id) {
    return _getOutboxRecordLookup(model).then(function (records) {
        return records[id];
    });
} // List of empty annotations for new objects


function _default_attachments(field, context) {
    if (field.type != 'repeat') {
        return Promise.resolve({});
    }

    if (!field.initial) {
        return Promise.resolve([]);
    }

    if (typeof field.initial == 'string' || typeof field.initial == 'number') {
        var attachments = [];

        for (var i = 0; i < +field.initial; i++) {
            attachments.push({
                '@index': i,
                new_attachment: true
            });
        }

        return Promise.resolve(attachments);
    }

    var typeField;
    field.children.forEach(function (tf) {
        if (tf.name == field.initial.type_field) {
            typeField = tf;
        }
    });

    if (!typeField) {
        return Promise.resolve([]);
    }

    var model = app.models[typeField['wq:ForeignKey']];
    var filterConf = field.initial.filter;

    if (!filterConf || !Object.keys(filterConf).length) {
        if (typeField.filter) {
            filterConf = typeField.filter;
        }
    }

    var filter = _computeFilter(filterConf, context);

    return model.filter(filter).then(function (types) {
        var attachments = [];
        types.forEach(function (t, i) {
            var obj = {
                '@index': i,
                new_attachment: true
            };
            obj[typeField.name + '_id'] = t.id;
            obj[typeField.name + '_label'] = t.label;
            attachments.push(obj);
        });
        return attachments;
    });
} // Load configuration based on page id


function _getBaseConf(page) {
    return _getConf(page, false, true);
}

function _getConf(page, silentFail, baseConf) {
    var conf = (baseConf ? app.config : app.wq_config).pages[page];

    if (!conf) {
        if (silentFail) {
            return;
        } else {
            throw new Error('Configuration for "' + page + '" not found!');
        }
    }

    return _objectSpread2({
        page: page,
        form: [],
        modes: conf.list ? ['list', 'detail', 'edit'] : []
    }, conf);
} // Helper to load configuration based on URL


function _getConfByUrl(url, silentFail) {
    var parts = url.split('/');
    var conf;

    for (var p in app.wq_config.pages) {
        if (app.wq_config.pages[p].url == parts[0]) {
            conf = app.wq_config.pages[p];
        }
    }

    if (!conf) {
        if (silentFail) {
            return;
        } else {
            throw 'Configuration for "/' + url + '" not found!';
        }
    }

    return conf;
}

function _computeFilter(filter, context) {
    var computedFilter = {};
    Object.keys(filter).forEach(function (key) {
        var values = filter[key];

        if (!Array.isArray(values)) {
            values = [values];
        }

        values = values.map(function (value) {
            if (value && value.indexOf && value.indexOf('{{') > -1) {
                value = Mustache__default['default'].render(value, context);

                if (value === '') {
                    return null;
                } else if (value.match(/^\+\d+$/)) {
                    return +value.substring(1);
                }
            }

            return value;
        });

        if (values.length > 1) {
            computedFilter[key] = values;
        } else {
            computedFilter[key] = values[0];
        }
    });
    return computedFilter;
}

function _loadFromServer(_x7) {
    return _loadFromServer2.apply(this, arguments);
}

function _loadFromServer2() {
    _loadFromServer2 = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee9(url) {
        var response, html;
        return _regeneratorRuntime__default['default'].wrap(function _callee9$(_context9) {
            while (1) {
                switch (_context9.prev = _context9.next) {
                    case 0:
                        // options = (ui && ui.options) || {};
                        if (app.config.debug) {
                            console.log('Loading ' + url + ' from server');

                            if (app.base_url && url.indexOf(app.base_url) !== 0) {
                                console.warn(url + ' does not include ' + app.base_url);
                            }
                        }

                        _context9.next = 3;
                        return fetch(url);

                    case 3:
                        response = _context9.sent;
                        _context9.next = 6;
                        return response.text();

                    case 6:
                        html = _context9.sent;
                        return _context9.abrupt("return", router__default['default'].rawHTML(html));

                    case 8:
                    case "end":
                        return _context9.stop();
                }
            }
        }, _callee9);
    }));
    return _loadFromServer2.apply(this, arguments);
}

function _serverContext(ctx) {
    var routeInfo = ctx.router_info,
        url = routeInfo.full_path;
    return _loadFromServer(url);
}

function _fetchFail(query, error) {
    /* eslint no-unused-vars: off */
    app.spin.alert('Error Loading Data');
}

return app;

});
//# sourceMappingURL=app-core.js.map
