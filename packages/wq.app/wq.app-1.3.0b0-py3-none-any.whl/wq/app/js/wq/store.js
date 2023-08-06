/*
 * @wq/store 1.3.0-alpha.2
 * Locally-persistent, optionally server-populated JSON datastore(s)
 * (c) 2012-2020, S. Andrew Sheppard
 * https://wq.io/license
 */

define(['exports', 'regenerator-runtime', 'redux', 'redux-logger', 'redux-persist', 'localforage'], function (exports, _regeneratorRuntime, redux, logger, reduxPersist, localForage) { 'use strict';

function _interopDefaultLegacy (e) { return e && typeof e === 'object' && 'default' in e ? e : { 'default': e }; }

var _regeneratorRuntime__default = /*#__PURE__*/_interopDefaultLegacy(_regeneratorRuntime);
var logger__default = /*#__PURE__*/_interopDefaultLegacy(logger);
var localForage__default = /*#__PURE__*/_interopDefaultLegacy(localForage);

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

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _defineProperties(target, props) {
  for (var i = 0; i < props.length; i++) {
    var descriptor = props[i];
    descriptor.enumerable = descriptor.enumerable || false;
    descriptor.configurable = true;
    if ("value" in descriptor) descriptor.writable = true;
    Object.defineProperty(target, descriptor.key, descriptor);
  }
}

function _createClass(Constructor, protoProps, staticProps) {
  if (protoProps) _defineProperties(Constructor.prototype, protoProps);
  if (staticProps) _defineProperties(Constructor, staticProps);
  return Constructor;
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

function _toConsumableArray(arr) {
  return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread();
}

function _arrayWithoutHoles(arr) {
  if (Array.isArray(arr)) return _arrayLikeToArray(arr);
}

function _arrayWithHoles(arr) {
  if (Array.isArray(arr)) return arr;
}

function _iterableToArray(iter) {
  if (typeof Symbol !== "undefined" && Symbol.iterator in Object(iter)) return Array.from(iter);
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

function _nonIterableSpread() {
  throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
}

function _nonIterableRest() {
  throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
}

function _typeof$1(obj) {
    if (typeof Symbol === "function" && _typeof(Symbol.iterator) === "symbol") {
        _typeof$1 = function _typeof$1(obj) {
            return _typeof(obj);
        };
    } else {
        _typeof$1 = function _typeof$1(obj) {
            return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : _typeof(obj);
        };
    }

    return _typeof$1(obj);
}

function ownKeys$1(object, enumerableOnly) {
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

function _objectSpread(target) {
    for (var i = 1; i < arguments.length; i++) {
        var source = arguments[i] != null ? arguments[i] : {};

        if (i % 2) {
            ownKeys$1(source, true).forEach(function (key) {
                _defineProperty$1(target, key, source[key]);
            });
        } else if (Object.getOwnPropertyDescriptors) {
            Object.defineProperties(target, Object.getOwnPropertyDescriptors(source));
        } else {
            ownKeys$1(source).forEach(function (key) {
                Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key));
            });
        }
    }

    return target;
}

function _defineProperty$1(obj, key, value) {
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
/*
  autoMergeLevel2: 
    - merges 2 level of substate
    - skips substate if already modified
    - this is essentially redux-perist v4 behavior
*/


function autoMergeLevel2(inboundState, originalState, reducedState, _ref) {
    var debug = _ref.debug;

    var newState = _objectSpread({}, reducedState); // only rehydrate if inboundState exists and is an object


    if (inboundState && _typeof$1(inboundState) === 'object') {
        Object.keys(inboundState).forEach(function (key) {
            // ignore _persist data
            if (key === '_persist') return; // if reducer modifies substate, skip auto rehydration

            if (originalState[key] !== reducedState[key]) {
                return;
            }

            if (isPlainEnoughObject(reducedState[key])) {
                // if object is plain enough shallow merge the new values (hence "Level2")
                newState[key] = _objectSpread({}, newState[key], {}, inboundState[key]);
                return;
            } // otherwise hard set


            newState[key] = inboundState[key];
        });
    }
    return newState;
}

function isPlainEnoughObject(o) {
    return o !== null && !Array.isArray(o) && _typeof$1(o) === 'object';
}

function createStorage(name) {
    return localForage__default['default'].createInstance({
        name: name
    });
}
var serialize = false;
var deserialize = false;

var REMOVE = '@@KVP_REMOVE';
var SET = '@@KVP_SET';
var CLEAR = '@@KVP_CLEAR'; // Internal variables and functions

var _verbosity = {
    Network: 1,
    Lookup: 2,
    Values: 3
};

var Store = /*#__PURE__*/function () {
    function Store(name) {
        var _this = this;

        _classCallCheck(this, Store);

        if (_stores[name]) {
            throw name + ' store already exists!';
        }

        this.name = name;
        _stores[name] = this;
        this.debug = false; // Base URL of web service

        this.service = undefined; // Default parameters (e.g f=json)

        this.defaults = {};
        this.ready = {
            then: function then() {
                throw new Error('Call init first!');
            }
        }; // Registered redux functions

        this._reducers = {};
        this._enhanceReducers = [];
        this._persistKeys = [];
        this._transforms = [];
        this._middleware = [];
        this._enhancers = [];
        this._subscribers = [];
        this._deferActions = [];
        this._thunkHandler = null;
        this._promises = {}; // Save promises to prevent redundant fetches

        this.addReducer('kvp', function (state, action) {
            return _this.kvpReducer(state, action);
        }, true);
    }

    _createClass(Store, [{
        key: "init",
        value: function init() {
            var _this2 = this;

            var opts = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
            var self = this;
            var optlist = ['debug', 'storageFail', 'service', 'defaults', 'fetchFail', 'ajax', 'formatKeyword'];
            optlist.forEach(function (opt) {
                if (opts.hasOwnProperty(opt)) {
                    self[opt] = opts[opt];
                }
            });

            if (self.debug) {
                for (var level in _verbosity) {
                    if (self.debug >= _verbosity[level]) {
                        self['debug' + level] = true;
                    }
                }

                self.addMiddleware(logger__default['default']);
            }

            var storeReady;
            self.ready = new Promise(function (resolve) {
                return storeReady = resolve;
            });
            var reducer = redux.combineReducers(this._reducers);

            this._enhanceReducers.forEach(function (enhanceReducer) {
                reducer = enhanceReducer(reducer);
            });

            var enhancers = redux.compose.apply(void 0, _toConsumableArray(this._enhancers).concat([redux.applyMiddleware.apply(void 0, _toConsumableArray(this._middleware))]));
            this.lf = createStorage(this.name);
            var persistConfig = {
                key: 'root',
                storage: this.lf,
                stateReconciler: autoMergeLevel2,
                serialize: serialize,
                deserialize: deserialize,
                transforms: this._transforms,
                whitelist: this._persistKeys,
                writeFailHandler: function writeFailHandler(error) {
                    return _this2.storageFail(error);
                }
            };
            var persistedReducer = reduxPersist.persistReducer(persistConfig, reducer);
            this._store = redux.createStore(persistedReducer, {}, enhancers);
            this._persistor = reduxPersist.persistStore(this._store);

            this._persistor.subscribe(function () {
                var _this2$_persistor$get = _this2._persistor.getState(),
                    bootstrapped = _this2$_persistor$get.bootstrapped;

                if (bootstrapped) {
                    storeReady();
                }
            });

            this._unsubscribers = this._subscribers.map(function (fn) {
                return _this2._store.subscribe(fn);
            });

            this._deferActions.forEach(this._store.dispatch);
        }
    }, {
        key: "dispatch",
        value: function dispatch(action) {
            if (this._store) {
                return this._store.dispatch(action);
            } else {
                this._deferActions.push(action);
            }
        }
    }, {
        key: "subscribe",
        value: function subscribe(fn) {
            var _this3 = this;

            this._subscribers.push(fn);

            if (this._store) {
                return this._store.subscribe(fn);
            } else {
                var index = this._subscribers.length - 1;
                return function () {
                    if (!_this3._unsubscribers) {
                        throw new Error('Store was never fully initialized!');
                    }

                    _this3._unsubscribers[index]();
                };
            }
        }
    }, {
        key: "getState",
        value: function getState() {
            return this._store.getState();
        }
    }, {
        key: "addReducer",
        value: function addReducer(name, reducer, persist, deserialize) {
            this._reducers[name] = reducer;

            if (persist) {
                this.persistKey(name, persist, deserialize);
            }
        }
    }, {
        key: "addEnhanceReducer",
        value: function addEnhanceReducer(name, enhanceReducer, persist, deserialize) {
            this._enhanceReducers.push(enhanceReducer);

            if (persist) {
                this.persistKey(name, persist, deserialize);
            }
        }
    }, {
        key: "persistKey",
        value: function persistKey(name, serialize, deserialize) {
            this._persistKeys.push(name);

            if (serialize && deserialize) {
                this._transforms.push(reduxPersist.createTransform(serialize, deserialize, {
                    whitelist: [name]
                }));
            }
        }
    }, {
        key: "addMiddleware",
        value: function addMiddleware(middleware) {
            this._middleware.push(middleware);
        }
    }, {
        key: "addEnhancer",
        value: function addEnhancer(enhancer) {
            this._enhancers.push(enhancer);
        }
    }, {
        key: "bindActionCreators",
        value: function bindActionCreators(actions) {
            return redux.bindActionCreators(actions, this.dispatch.bind(this));
        }
    }, {
        key: "addThunk",
        value: function addThunk(name, thunk) {
            if (!this._thunkHandler) {
                throw new Error('@wq/router is required to handle thunks');
            }

            this._thunkHandler(name, thunk);
        }
    }, {
        key: "setThunkHandler",
        value: function setThunkHandler(handler) {
            this._thunkHandler = handler;
        }
    }, {
        key: "kvpReducer",
        value: function kvpReducer() {
            var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
            var action = arguments.length > 1 ? arguments[1] : undefined;

            if (action.type === REMOVE) {
                state = _objectSpread2({}, state);
                delete state[action.payload.key];
            } else if (action.type === SET) {
                state = _objectSpread2(_objectSpread2({}, state), {}, _defineProperty({}, action.payload.key, action.payload.value));
            } else if (action.type === CLEAR) {
                state = {};
            }

            return state;
        } // Get value from datastore

    }, {
        key: "get",
        value: function () {
            var _get = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee(query) {
                var self, promises, key, kvp;
                return _regeneratorRuntime__default['default'].wrap(function _callee$(_context) {
                    while (1) {
                        switch (_context.prev = _context.next) {
                            case 0:
                                _context.next = 2;
                                return this.ready;

                            case 2:
                                self = this;

                                if (!Array.isArray(query)) {
                                    _context.next = 6;
                                    break;
                                }

                                promises = query.map(function (row) {
                                    return self.get(row);
                                });
                                return _context.abrupt("return", Promise.all(promises));

                            case 6:
                                query = self.normalizeQuery(query);
                                key = self.toKey(query);

                                if (self.debugLookup) {
                                    console.log('looking up ' + key);
                                } // Check storage first


                                kvp = this.getState().kvp;

                                if (!kvp[key]) {
                                    _context.next = 15;
                                    break;
                                }

                                if (self.debugLookup) {
                                    console.log('in storage');
                                }

                                return _context.abrupt("return", kvp[key]);

                            case 15:
                                if (!(typeof query == 'string')) {
                                    _context.next = 18;
                                    break;
                                }

                                if (self.debugLookup) {
                                    console.log('not found');
                                }

                                return _context.abrupt("return", null);

                            case 18:
                                return _context.abrupt("return", self.fetch(query, true));

                            case 19:
                            case "end":
                                return _context.stop();
                        }
                    }
                }, _callee, this);
            }));

            function get(_x) {
                return _get.apply(this, arguments);
            }

            return get;
        }() // Set value

    }, {
        key: "set",
        value: function () {
            var _set = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee2(query, value) {
                var self, key;
                return _regeneratorRuntime__default['default'].wrap(function _callee2$(_context2) {
                    while (1) {
                        switch (_context2.prev = _context2.next) {
                            case 0:
                                self = this;
                                key = self.toKey(query);

                                if (!(value === null)) {
                                    _context2.next = 8;
                                    break;
                                }

                                if (self.debugLookup) {
                                    console.log('deleting ' + key);
                                }

                                self.dispatch({
                                    type: REMOVE,
                                    payload: {
                                        key: key
                                    }
                                });
                                return _context2.abrupt("return");

                            case 8:
                                if (self.debugLookup) {
                                    console.log('saving new value for ' + key);

                                    if (self.debugValues) {
                                        console.log(value);
                                    }
                                }

                                self.dispatch({
                                    type: SET,
                                    payload: {
                                        key: key,
                                        value: value
                                    }
                                });
                                return _context2.abrupt("return");

                            case 11:
                            case "end":
                                return _context2.stop();
                        }
                    }
                }, _callee2, this);
            }));

            function set(_x2, _x3) {
                return _set.apply(this, arguments);
            }

            return set;
        }() // Callback for localStorage failure - override to inform the user

    }, {
        key: "storageFail",
        value: function storageFail(error) {
            console.warn('Error persisting store:');
            console.warn(error);
        } // Convert "/url" to {'url': "url"} (simplify common use case)

    }, {
        key: "normalizeQuery",
        value: function normalizeQuery(query) {
            if (typeof query === 'string' && query.charAt(0) == '/') {
                query = {
                    url: query.replace(/^\//, '')
                };
            }

            return query;
        } // Helper to allow simple objects to be used as keys

    }, {
        key: "toKey",
        value: function toKey(query) {
            var self = this;
            query = self.normalizeQuery(query);

            if (!query) {
                throw 'Invalid query!';
            }

            if (typeof query == 'string') {
                return query;
            } else {
                return new URLSearchParams(query).toString();
            }
        } // Helper to check existence of a key without loading the object

    }, {
        key: "exists",
        value: function exists(query) {
            var self = this;
            var key = self.toKey(query);
            return self.keys().then(function (keys) {
                var found = false;
                keys.forEach(function (k) {
                    if (k === key) {
                        found = true;
                    }
                });
                return found;
            });
        } // Fetch data from server

    }, {
        key: "fetch",
        value: function fetch(query, cache) {
            var _this4 = this;

            var self = this;
            query = self.normalizeQuery(query);
            var key = self.toKey(query);

            var data = _objectSpread2(_objectSpread2({}, self.defaults), query);

            var url = self.service;

            if (data.hasOwnProperty('url')) {
                url = url + '/' + data.url;
                delete data.url;
            }

            if (data.format && !self.formatKeyword) {
                url += '.' + data.format;
                delete data.format;
            }

            if (this._promises[key]) {
                return this._promises[key];
            }

            if (self.debugNetwork) {
                console.log('fetching ' + key);
            }

            var promise = self.ajax(url, data, 'GET');
            this._promises[key] = promise.then( /*#__PURE__*/function () {
                var _ref = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee3(data) {
                    return _regeneratorRuntime__default['default'].wrap(function _callee3$(_context3) {
                        while (1) {
                            switch (_context3.prev = _context3.next) {
                                case 0:
                                    delete _this4._promises[key];

                                    if (data) {
                                        _context3.next = 4;
                                        break;
                                    }

                                    self.fetchFail(query, 'Error parsing data!');
                                    return _context3.abrupt("return");

                                case 4:
                                    if (self.debugNetwork) {
                                        console.log('received result for ' + key);

                                        if (self.debugValues) {
                                            console.log(data);
                                        }
                                    }

                                    if (!cache) {
                                        _context3.next = 8;
                                        break;
                                    }

                                    _context3.next = 8;
                                    return self.set(query, data);

                                case 8:
                                    return _context3.abrupt("return", data);

                                case 9:
                                case "end":
                                    return _context3.stop();
                            }
                        }
                    }, _callee3);
                }));

                return function (_x4) {
                    return _ref.apply(this, arguments);
                };
            }(), function (error) {
                delete _this4._promises[key];
                console.error(error);
                self.fetchFail(query, 'Error parsing data!');
            });
            return this._promises[key];
        } // Hook to allow full AJAX customization

    }, {
        key: "ajax",
        value: function ajax(url, data, method, headers) {
            var urlObj = new URL(url, window.location);

            if (!method) {
                method = 'GET';
            } else {
                method = method.toUpperCase();
            }

            if (method == 'GET') {
                Object.entries(data || {}).forEach(function (_ref2) {
                    var _ref3 = _slicedToArray(_ref2, 2),
                        key = _ref3[0],
                        value = _ref3[1];

                    return urlObj.searchParams.append(key, value);
                });
                data = null;
            }

            return fetch(urlObj, {
                method: method,
                body: data,
                headers: headers
            }).then(function (response) {
                if (response.ok) {
                    if (response.status === 204) {
                        return null;
                    } else {
                        return response.json();
                    }
                } else {
                    return response.text().then(function (result) {
                        var error = new Error();

                        try {
                            error.json = JSON.parse(result);
                        } catch (e) {
                            error.text = result;
                        }

                        error.status = response.status;
                        throw error;
                    });
                }
            });
        } // Callback for fetch() failures - override to inform the user

    }, {
        key: "fetchFail",
        value: function fetchFail(query, error) {
            var self = this;
            var key = self.toKey(query);
            console.warn('Error loading ' + key + ': ' + error);
        } // Helper function for prefetching data

    }, {
        key: "prefetch",
        value: function prefetch(query) {
            var self = this;
            return self.fetch(query, true);
        } // Clear local caches

    }, {
        key: "reset",
        value: function () {
            var _reset = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee4() {
                return _regeneratorRuntime__default['default'].wrap(function _callee4$(_context4) {
                    while (1) {
                        switch (_context4.prev = _context4.next) {
                            case 0:
                                this.dispatch({
                                    type: CLEAR
                                });
                                _context4.next = 3;
                                return this._persistor.purge();

                            case 3:
                            case "end":
                                return _context4.stop();
                        }
                    }
                }, _callee4, this);
            }));

            function reset() {
                return _reset.apply(this, arguments);
            }

            return reset;
        }() // List storage keys matching this store's key prefix

    }, {
        key: "keys",
        value: function () {
            var _keys = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee5() {
                return _regeneratorRuntime__default['default'].wrap(function _callee5$(_context5) {
                    while (1) {
                        switch (_context5.prev = _context5.next) {
                            case 0:
                                return _context5.abrupt("return", Object.keys(this.getState().kvp));

                            case 1:
                            case "end":
                                return _context5.stop();
                        }
                    }
                }, _callee5, this);
            }));

            function keys() {
                return _keys.apply(this, arguments);
            }

            return keys;
        }()
    }]);

    return Store;
}();

var _stores = {}; // Hybrid module object provides/is a singleton instance...

var ds = new Store('main'); // ... and a way to retrieve/autoinit other stores

ds.getStore = getStore;

function getStore(name) {
    if (_stores[name]) {
        return _stores[name];
    } else {
        return new Store(name);
    }
}

exports.Store = Store;
exports.default = ds;
exports.getStore = getStore;

Object.defineProperty(exports, '__esModule', { value: true });

});
//# sourceMappingURL=store.js.map
