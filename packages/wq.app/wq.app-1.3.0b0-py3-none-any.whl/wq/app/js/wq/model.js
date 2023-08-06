/*
 * @wq/model 1.3.0-alpha.3
 * A simple model API for working with stored lists
 * (c) 2012-2020, S. Andrew Sheppard
 * https://wq.io/license
 */

define(['exports', 'regenerator-runtime', './store', 'deepcopy', 'redux-orm'], function (exports, _regeneratorRuntime, ds, deepcopy, reduxOrm) { 'use strict';

function _interopDefaultLegacy (e) { return e && typeof e === 'object' && 'default' in e ? e : { 'default': e }; }

var _regeneratorRuntime__default = /*#__PURE__*/_interopDefaultLegacy(_regeneratorRuntime);
var ds__default = /*#__PURE__*/_interopDefaultLegacy(ds);
var deepcopy__default = /*#__PURE__*/_interopDefaultLegacy(deepcopy);

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

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function");
  }

  subClass.prototype = Object.create(superClass && superClass.prototype, {
    constructor: {
      value: subClass,
      writable: true,
      configurable: true
    }
  });
  if (superClass) _setPrototypeOf(subClass, superClass);
}

function _getPrototypeOf(o) {
  _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) {
    return o.__proto__ || Object.getPrototypeOf(o);
  };
  return _getPrototypeOf(o);
}

function _setPrototypeOf(o, p) {
  _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) {
    o.__proto__ = p;
    return o;
  };

  return _setPrototypeOf(o, p);
}

function _isNativeReflectConstruct() {
  if (typeof Reflect === "undefined" || !Reflect.construct) return false;
  if (Reflect.construct.sham) return false;
  if (typeof Proxy === "function") return true;

  try {
    Date.prototype.toString.call(Reflect.construct(Date, [], function () {}));
    return true;
  } catch (e) {
    return false;
  }
}

function _objectWithoutPropertiesLoose(source, excluded) {
  if (source == null) return {};
  var target = {};
  var sourceKeys = Object.keys(source);
  var key, i;

  for (i = 0; i < sourceKeys.length; i++) {
    key = sourceKeys[i];
    if (excluded.indexOf(key) >= 0) continue;
    target[key] = source[key];
  }

  return target;
}

function _objectWithoutProperties(source, excluded) {
  if (source == null) return {};

  var target = _objectWithoutPropertiesLoose(source, excluded);

  var key, i;

  if (Object.getOwnPropertySymbols) {
    var sourceSymbolKeys = Object.getOwnPropertySymbols(source);

    for (i = 0; i < sourceSymbolKeys.length; i++) {
      key = sourceSymbolKeys[i];
      if (excluded.indexOf(key) >= 0) continue;
      if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue;
      target[key] = source[key];
    }
  }

  return target;
}

function _assertThisInitialized(self) {
  if (self === void 0) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }

  return self;
}

function _possibleConstructorReturn(self, call) {
  if (call && (typeof call === "object" || typeof call === "function")) {
    return call;
  }

  return _assertThisInitialized(self);
}

function _createSuper(Derived) {
  var hasNativeReflectConstruct = _isNativeReflectConstruct();

  return function _createSuperInternal() {
    var Super = _getPrototypeOf(Derived),
        result;

    if (hasNativeReflectConstruct) {
      var NewTarget = _getPrototypeOf(this).constructor;

      result = Reflect.construct(Super, arguments, NewTarget);
    } else {
      result = Super.apply(this, arguments);
    }

    return _possibleConstructorReturn(this, result);
  };
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

function model(config) {
    return new Model(config);
}

var _orms = {};
var CREATE = 'CREATE',
    UPDATE = 'UPDATE',
    SUCCESS = 'SUCCESS',
    DELETE = 'DELETE',
    OVERWRITE = 'OVERWRITE';

var ORMWithReducer = /*#__PURE__*/function (_ORM) {
    _inherits(ORMWithReducer, _ORM);

    var _super = _createSuper(ORMWithReducer);

    function ORMWithReducer(store) {
        var _this;

        _classCallCheck(this, ORMWithReducer);

        _this = _super.call(this, {
            stateSelector: function stateSelector(state) {
                return state.orm;
            }
        });
        _this.store = store;
        return _this;
    }

    _createClass(ORMWithReducer, [{
        key: "getReverseRels",
        value: function getReverseRels(modelName) {
            var _this2 = this;

            if (!this._rrel) {
                this._rrel = {};
                var models = {};
                this.getModelClasses().forEach(function (cls) {
                    models[cls.modelName] = cls;
                });
                Object.values(models).forEach(function (cls) {
                    Object.entries(cls.fields).forEach(function (_ref) {
                        var _ref2 = _slicedToArray(_ref, 2),
                            name = _ref2[0],
                            field = _ref2[1];

                        if (!(field instanceof reduxOrm.ForeignKey)) {
                            return;
                        }

                        var to = field.toModelName,
                            toModel = models[to];

                        if (!toModel || !toModel.wqConfig) {
                            return;
                        }

                        var isNested = (toModel.wqConfig.form || []).filter(function (f) {
                            return f.type === 'repeat' && f.name === field.relatedName;
                        }).length > 0;

                        if (!_this2._rrel[to]) {
                            _this2._rrel[to] = [];
                        }

                        _this2._rrel[to].push({
                            model: cls.modelName,
                            fkName: name,
                            relatedName: field.relatedName,
                            nested: isNested
                        });
                    });
                });
            }

            return this._rrel[modelName] || [];
        }
    }, {
        key: "getNestedModels",
        value: function getNestedModels(modelName) {
            return this.getReverseRels(modelName).filter(function (rel) {
                return rel.nested;
            });
        }
    }, {
        key: "reducer",
        value: function reducer(state, action) {
            var _this3 = this;

            var session = this.session(state || this.getEmptyState()),
                match = action.type.match(/^([^_]+)_(.+)_([^_]+)$/);

            if (!match || match[1] !== this.prefix) {
                return session.state;
            }

            var modelName = match[2].toLowerCase(),
                actName = match[3],
                cls = session[modelName];

            if (!cls) {
                return session.state;
            }

            var currentCount = cls.count();
            var updateCount;

            switch (actName) {
                case CREATE:
                    {
                        this._nestedCreate(cls, action.payload);

                        updateCount = true;
                        break;
                    }

                case UPDATE:
                case SUCCESS:
                    {
                        var items = Array.isArray(action.payload) ? action.payload : [action.payload];

                        if (action.meta && action.meta.currentId && action.meta.currentId != items[0].id) {
                            this._updateID(cls, action.meta.currentId, items[0].id);
                        }

                        items.forEach(function (item) {
                            return _this3._nestedUpdate(cls, item);
                        });
                        updateCount = true;
                        break;
                    }

                case DELETE:
                    {
                        this._nestedDelete(cls.withId(action.payload));

                        updateCount = true;
                        break;
                    }

                case OVERWRITE:
                    {
                        var _action$payload = action.payload,
                            list = _action$payload.list,
                            info = _objectWithoutProperties(_action$payload, ["list"]);

                        this._removeObsolete(cls.all(), list, true);

                        list.forEach(function (item) {
                            return _this3._nestedUpdate(cls, item);
                        });

                        session._modelmeta.upsert(_objectSpread2({
                            id: cls.modelName
                        }, info));

                        break;
                    }
            }

            if (updateCount) {
                var meta = session._modelmeta.withId(cls.modelName);

                if (meta) {
                    // Use delta in case server count != local count.
                    var countChange = cls.count() - currentCount,
                        update = {
                        count: meta.count + countChange
                    };

                    if (meta.pages === 1 && meta.per_page === meta.count) {
                        update.per_page = update.count;
                    }

                    meta.update(update);
                } else {
                    session._modelmeta.create({
                        id: cls.modelName,
                        pages: 1,
                        count: cls.count(),
                        per_page: cls.count()
                    });
                } // FIXME: Update count for nested models

            }

            return session.state;
        }
    }, {
        key: "_setNested",
        value: function _setNested(cls, data) {
            var _this4 = this;

            var item = _objectSpread2({}, data),
                session = cls.session,
                nested = this.getNestedModels(cls.modelName);

            var exist = data.id ? cls.withId(data.id) : null; // Normalize nested records into their own models

            nested.forEach(function (_ref3) {
                var model = _ref3.model,
                    fkName = _ref3.fkName,
                    relatedName = _ref3.relatedName;

                if (!Array.isArray(item[relatedName])) {
                    return;
                }

                if (exist && exist[relatedName] && exist[relatedName].toRefArray) {
                    _this4._removeObsolete(exist[relatedName], item[relatedName]);
                }

                item[relatedName].forEach(function (row) {
                    session[model].upsert(_objectSpread2(_objectSpread2({}, row), {}, _defineProperty({}, fkName, item.id)));
                });
                delete item[relatedName];
            });
            return item;
        }
    }, {
        key: "_removeObsolete",
        value: function _removeObsolete(qs, newItems, nested) {
            var _this5 = this;

            var idsToKeep = newItems.map(function (row) {
                return row.id;
            }).filter(function (id) {
                return !!id;
            }),
                obsolete = qs.filter(function (item) {
                return !idsToKeep.includes(item.id);
            });

            if (nested) {
                obsolete.toModelArray().forEach(function (item) {
                    return _this5._nestedDelete(item);
                });
            } else {
                obsolete.delete();
            }
        }
    }, {
        key: "_nestedCreate",
        value: function _nestedCreate(cls, data) {
            var item = this._setNested(cls, data);

            cls.create(item);
        }
    }, {
        key: "_nestedUpdate",
        value: function _nestedUpdate(cls, data) {
            var item = this._setNested(cls, data);

            cls.upsert(item);
        }
    }, {
        key: "_nestedDelete",
        value: function _nestedDelete(instance) {
            var nested = this.getNestedModels(instance.getClass().modelName);
            nested.forEach(function (_ref4) {
                var relatedName = _ref4.relatedName;
                instance[relatedName].delete();
            });
            instance.delete();
        }
    }, {
        key: "_updateID",
        value: function _updateID(cls, oldId, newId) {
            // New ID was assigned (i.e. by the server)
            var exist = cls.withId(oldId),
                rrel = this.getReverseRels(cls.modelName);

            if (!exist) {
                return;
            } // Update any existing FKs to point to the new ID
            // (including both nested and non-nested relationships)


            rrel.forEach(function (_ref5) {
                var fkName = _ref5.fkName,
                    relatedName = _ref5.relatedName;
                exist[relatedName].update(_defineProperty({}, fkName, newId));
            }); // Remove and replace (see redux-orm #176)

            cls.upsert(_objectSpread2(_objectSpread2({}, exist.ref), {}, {
                id: newId
            }));
            exist.delete();
        }
    }, {
        key: "prefix",
        get: function get() {
            if (this.store.name === 'main') {
                return 'ORM';
            } else {
                return "".concat(this.store.name.toUpperCase(), "ORM");
            }
        }
    }]);

    return ORMWithReducer;
}(reduxOrm.ORM);

var ModelMeta = /*#__PURE__*/function (_ORMModel) {
    _inherits(ModelMeta, _ORMModel);

    var _super2 = _createSuper(ModelMeta);

    function ModelMeta() {
        _classCallCheck(this, ModelMeta);

        return _super2.apply(this, arguments);
    }

    return ModelMeta;
}(reduxOrm.Model);

ModelMeta.modelName = '_modelmeta';

function orm(store) {
    if (!_orms[store.name]) {
        var _orm = _orms[store.name] = new ORMWithReducer(store);

        store.addReducer('orm', function (state, action) {
            return _orm.reducer(state, action);
        }, true);

        _orm.register(ModelMeta);
    }

    return _orms[store.name];
}

model.cacheOpts = {
    // First page (e.g. 50 records) is stored locally; subsequent pages can be
    // loaded from server.
    first_page: {
        server: true,
        client: true,
        page: 1,
        reversed: true
    },
    // All data is prefetched and stored locally, no subsequent requests are
    // necessary.
    all: {
        server: false,
        client: true,
        page: 0,
        reversed: false
    },
    // "Important" data is cached; other data can be accessed via pagination.
    filter: {
        server: true,
        client: true,
        page: 0,
        reversed: true
    },
    // No data is cached locally; all data require a network request.
    none: {
        server: true,
        client: false,
        page: 0,
        reversed: false
    }
}; // Retrieve a stored list as an object with helper functions
//  - especially useful for server-paginated lists
//  - methods must be called asynchronously

var Model = /*#__PURE__*/function () {
    function Model(config) {
        _classCallCheck(this, Model);

        if (!config) {
            throw 'No configuration provided!';
        }

        if (typeof config == 'string') {
            config = {
                query: config,
                name: config
            };
        }

        if (!config.name) {
            throw new Error('Model name is now required.');
        }

        if (!config.cache) {
            config.cache = 'first_page';
        }

        this.config = config;
        this.name = config.name;
        this.idCol = config.idCol || 'id';
        this.opts = model.cacheOpts[config.cache];

        if (!this.opts) {
            throw 'Unknown cache option ' + config.cache;
        }

        ['max_local_pages', 'partial', 'reversed'].forEach(function (name) {
            if (name in config) {
                throw '"' + name + '" is deprecated in favor of "cache"';
            }
        }); // Default to main store, but allow overriding

        if (config.store) {
            if (config.store instanceof ds__default['default'].constructor) {
                this.store = config.store;
            } else {
                this.store = ds__default['default'].getStore(config.store);
            }
        } else {
            this.store = ds__default['default'];
        }

        this.orm = orm(this.store);

        try {
            this._model = this.orm.get(this.name);
        } catch (e) {
            var idCol = this.idCol;

            var M = /*#__PURE__*/function (_ORMModel2) {
                _inherits(M, _ORMModel2);

                var _super3 = _createSuper(M);

                function M() {
                    _classCallCheck(this, M);

                    return _super3.apply(this, arguments);
                }

                _createClass(M, null, [{
                    key: "idAttribute",
                    get: function get() {
                        return idCol;
                    }
                }, {
                    key: "fields",
                    get: function get() {
                        var fields = {};
                        (config.form || []).forEach(function (field) {
                            if (field['wq:ForeignKey']) {
                                fields[field.name + '_id'] = reduxOrm.fk({
                                    to: field['wq:ForeignKey'],
                                    as: field.name,
                                    relatedName: field['wq:related_name'] || config.url || config.name + 's'
                                });
                            } else if (field.type !== 'repeat') {
                                fields[field.name] = reduxOrm.attr();
                            }
                        });
                        return fields;
                    }
                }, {
                    key: "wqConfig",
                    get: function get() {
                        return config;
                    }
                }]);

                return M;
            }(reduxOrm.Model);

            M.modelName = this.name;
            this.orm.register(M);
            this._model = M;
        }

        if (config.query) {
            this.query = this.store.normalizeQuery(config.query);
        } else if (config.url !== undefined) {
            this.query = {
                url: config.url
            };
        } // Configurable functions to e.g. filter data by


        this.functions = config.functions || {};
    }

    _createClass(Model, [{
        key: "expandActionType",
        value: function expandActionType(type) {
            return "".concat(this.orm.prefix, "_").concat(this.name.toUpperCase(), "_").concat(type);
        }
    }, {
        key: "dispatch",
        value: function dispatch(type, payload, meta) {
            var action = {
                type: this.expandActionType(type),
                payload: payload
            };

            if (meta) {
                action.meta = meta;
            }

            return this.store.dispatch(action);
        }
    }, {
        key: "getSession",
        value: function getSession() {
            return this.orm.session(this.store.getState().orm);
        }
    }, {
        key: "getSessionModel",
        value: function getSessionModel() {
            var model = this.getSession()[this.name];

            if (!model) {
                throw new Error('Could not find model in session');
            }

            return model;
        }
    }, {
        key: "getQuerySet",
        value: function getQuerySet() {
            var model = this.getSessionModel();
            return model.all().orderBy(this.idCol, this.opts.reversed ? 'desc' : 'asc');
        }
    }, {
        key: "getPage",
        value: function () {
            var _getPage = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee(page_num) {
                var query, result, data;
                return _regeneratorRuntime__default['default'].wrap(function _callee$(_context) {
                    while (1) {
                        switch (_context.prev = _context.next) {
                            case 0:
                                query = _objectSpread2({}, this.query);

                                if (page_num !== null) {
                                    query.page = page_num;
                                }

                                _context.next = 4;
                                return this.store.fetch(query);

                            case 4:
                                result = _context.sent;
                                data = this._processData(result);

                                if (!data.page) {
                                    data.page = page_num;
                                }

                                return _context.abrupt("return", data);

                            case 8:
                            case "end":
                                return _context.stop();
                        }
                    }
                }, _callee, this);
            }));

            function getPage(_x) {
                return _getPage.apply(this, arguments);
            }

            return getPage;
        }()
    }, {
        key: "_processData",
        value: function _processData(data) {
            if (!data) {
                data = [];
            }

            if (Array.isArray(data)) {
                data = {
                    list: data
                };
            }

            if (!data.pages) {
                data.pages = 1;
            }

            if (!data.count) {
                data.count = data.list.length;
            }

            if (!data.per_page) {
                data.per_page = data.list.length;
            }

            return data;
        }
    }, {
        key: "_withNested",
        value: function _withNested(instance) {
            var data = deepcopy__default['default'](instance.ref);
            var nested = this.orm.getNestedModels(instance.getClass().modelName);
            nested.forEach(function (_ref6) {
                var relatedName = _ref6.relatedName;
                data[relatedName] = instance[relatedName].toRefArray();
            });
            return data;
        }
    }, {
        key: "load",
        value: function () {
            var _load = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee2() {
                var _this6 = this;

                var info;
                return _regeneratorRuntime__default['default'].wrap(function _callee2$(_context2) {
                    while (1) {
                        switch (_context2.prev = _context2.next) {
                            case 0:
                                _context2.next = 2;
                                return this.info();

                            case 2:
                                info = _context2.sent;
                                return _context2.abrupt("return", _objectSpread2(_objectSpread2({}, info), {}, {
                                    list: this.getQuerySet().toModelArray().map(function (instance) {
                                        return _this6._withNested(instance);
                                    })
                                }));

                            case 4:
                            case "end":
                                return _context2.stop();
                        }
                    }
                }, _callee2, this);
            }));

            function load() {
                return _load.apply(this, arguments);
            }

            return load;
        }()
    }, {
        key: "info",
        value: function () {
            var _info = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee3() {
                var retry,
                    info,
                    _info$ref,
                    pages,
                    count,
                    per_page,
                    _args3 = arguments;

                return _regeneratorRuntime__default['default'].wrap(function _callee3$(_context3) {
                    while (1) {
                        switch (_context3.prev = _context3.next) {
                            case 0:
                                retry = _args3.length > 0 && _args3[0] !== undefined ? _args3[0] : true;
                                info = this.getSession()._modelmeta.withId(this.name);

                                if (!info) {
                                    _context3.next = 7;
                                    break;
                                }

                                _info$ref = info.ref, pages = _info$ref.pages, count = _info$ref.count, per_page = _info$ref.per_page;
                                return _context3.abrupt("return", {
                                    pages: pages,
                                    count: count,
                                    per_page: per_page
                                });

                            case 7:
                                if (!(this.query && retry)) {
                                    _context3.next = 13;
                                    break;
                                }

                                _context3.next = 10;
                                return this.prefetch();

                            case 10:
                                return _context3.abrupt("return", this.info(false));

                            case 13:
                                return _context3.abrupt("return", {
                                    pages: 1,
                                    count: 0,
                                    per_page: 0
                                });

                            case 14:
                            case "end":
                                return _context3.stop();
                        }
                    }
                }, _callee3, this);
            }));

            function info() {
                return _info.apply(this, arguments);
            }

            return info;
        }()
    }, {
        key: "ensureLoaded",
        value: function () {
            var _ensureLoaded = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee4() {
                return _regeneratorRuntime__default['default'].wrap(function _callee4$(_context4) {
                    while (1) {
                        switch (_context4.prev = _context4.next) {
                            case 0:
                                _context4.next = 2;
                                return this.info();

                            case 2:
                            case "end":
                                return _context4.stop();
                        }
                    }
                }, _callee4, this);
            }));

            function ensureLoaded() {
                return _ensureLoaded.apply(this, arguments);
            }

            return ensureLoaded;
        }() // Load data for the given page number

    }, {
        key: "page",
        value: function () {
            var _page = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee5(page_num) {
                return _regeneratorRuntime__default['default'].wrap(function _callee5$(_context5) {
                    while (1) {
                        switch (_context5.prev = _context5.next) {
                            case 0:
                                if (this.config.url) {
                                    _context5.next = 3;
                                    break;
                                }

                                if (!(page_num > this.opts.page)) {
                                    _context5.next = 3;
                                    break;
                                }

                                throw new Error('No URL, cannot retrieve page ' + page_num);

                            case 3:
                                if (!(page_num <= this.opts.page)) {
                                    _context5.next = 7;
                                    break;
                                }

                                return _context5.abrupt("return", this.load());

                            case 7:
                                return _context5.abrupt("return", this.getPage(page_num));

                            case 8:
                            case "end":
                                return _context5.stop();
                        }
                    }
                }, _callee5, this);
            }));

            function page(_x2) {
                return _page.apply(this, arguments);
            }

            return page;
        }() // Iterate across stored data

    }, {
        key: "forEach",
        value: function () {
            var _forEach = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee6(cb, thisarg) {
                var data;
                return _regeneratorRuntime__default['default'].wrap(function _callee6$(_context6) {
                    while (1) {
                        switch (_context6.prev = _context6.next) {
                            case 0:
                                _context6.next = 2;
                                return this.load();

                            case 2:
                                data = _context6.sent;
                                data.list.forEach(cb, thisarg);

                            case 4:
                            case "end":
                                return _context6.stop();
                        }
                    }
                }, _callee6, this);
            }));

            function forEach(_x3, _x4) {
                return _forEach.apply(this, arguments);
            }

            return forEach;
        }() // Find an object by id

    }, {
        key: "find",
        value: function () {
            var _find = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee7(value, localOnly) {
                var model, instance;
                return _regeneratorRuntime__default['default'].wrap(function _callee7$(_context7) {
                    while (1) {
                        switch (_context7.prev = _context7.next) {
                            case 0:
                                if (!(localOnly && typeof localOnly !== 'boolean')) {
                                    _context7.next = 2;
                                    break;
                                }

                                throw new Error('Usage: find(value[, localOnly).  To customize id attr use config.idCol');

                            case 2:
                                _context7.next = 4;
                                return this.ensureLoaded();

                            case 4:
                                model = this.getSessionModel(), instance = model.withId(value);

                                if (!instance) {
                                    _context7.next = 9;
                                    break;
                                }

                                return _context7.abrupt("return", this._withNested(instance));

                            case 9:
                                if (!(value !== undefined && !localOnly && this.opts.server && this.config.url)) {
                                    _context7.next = 15;
                                    break;
                                }

                                _context7.next = 12;
                                return this.store.fetch('/' + this.config.url + '/' + value);

                            case 12:
                                return _context7.abrupt("return", _context7.sent);

                            case 15:
                                return _context7.abrupt("return", null);

                            case 16:
                            case "end":
                                return _context7.stop();
                        }
                    }
                }, _callee7, this);
            }));

            function find(_x5, _x6) {
                return _find.apply(this, arguments);
            }

            return find;
        }()
    }, {
        key: "filterFields",
        value: function filterFields() {
            var _this7 = this;

            var fields = [this.idCol];
            fields = fields.concat((this.config.form || []).map(function (field) {
                return field['wq:ForeignKey'] ? "".concat(field.name, "_id") : field.name;
            }));
            fields = fields.concat(Object.keys(this.functions));
            fields = fields.concat(this.config.filter_fields || []);

            if (this.config.filter_ignore) {
                fields = fields.filter(function (field) {
                    return !_this7.config.filter_ignore.includes(field);
                });
            }

            return fields;
        } // Filter an array of objects by one or more attributes

    }, {
        key: "filterPage",
        value: function () {
            var _filterPage = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee8(filter, any, localOnly) {
                var _this8 = this;

                var filterFields, result, qs, defaultFilter, customFilter, hasDefaultFilter, hasCustomFilter;
                return _regeneratorRuntime__default['default'].wrap(function _callee8$(_context8) {
                    while (1) {
                        switch (_context8.prev = _context8.next) {
                            case 0:
                                // Ignore fields that are not explicitly registered
                                // (e.g. for use with list views that have custom URL params)
                                filterFields = this.filterFields();
                                Object.keys(filter).forEach(function (field) {
                                    if (!filterFields.includes(field)) {
                                        if (!(_this8.config.filter_ignore || []).includes(field)) {
                                            console.warn("Ignoring unrecognized field \"".concat(field, "\"") + " while filtering ".concat(_this8.name, " list.") + ' Add to form or filter_fields to enable filtering,' + ' or to filter_ignore to remove this warning.');
                                        }

                                        filter = _objectSpread2({}, filter);
                                        delete filter[field];
                                    }
                                }); // If partial list, we can never be 100% sure all filter matches are
                                // stored locally. In that case, run query on server.

                                if (!(!localOnly && this.opts.server && this.config.url)) {
                                    _context8.next = 7;
                                    break;
                                }

                                _context8.next = 5;
                                return this.store.fetch(_objectSpread2({
                                    url: this.config.url
                                }, filter));

                            case 5:
                                result = _context8.sent;
                                return _context8.abrupt("return", this._processData(result));

                            case 7:
                                if (!(!filter || !Object.keys(filter).length)) {
                                    _context8.next = 9;
                                    break;
                                }

                                return _context8.abrupt("return", this.load());

                            case 9:
                                _context8.next = 11;
                                return this.ensureLoaded();

                            case 11:
                                qs = this.getQuerySet();

                                if (any) {
                                    // any=true: Match on any of the provided filter attributes
                                    qs = qs.filter(function (item) {
                                        return Object.keys(filter).filter(function (attr) {
                                            return _this8.matches(item, attr, filter[attr]);
                                        }).length > 0;
                                    });
                                } else {
                                    // Default: require match on all filter attributes
                                    // Use object filter to take advantage of redux-orm indexes -
                                    // except for boolean/array/computed filters.
                                    defaultFilter = {}, customFilter = {}, hasDefaultFilter = false, hasCustomFilter = false;
                                    Object.keys(filter).forEach(function (attr) {
                                        var comp = filter[attr];

                                        if (_this8.isCustomFilter(attr, comp)) {
                                            customFilter[attr] = comp;
                                            hasCustomFilter = true;
                                        } else {
                                            defaultFilter[attr] = comp;
                                            hasDefaultFilter = true;
                                        }
                                    });

                                    if (hasDefaultFilter) {
                                        qs = qs.filter(defaultFilter);
                                    }

                                    if (hasCustomFilter) {
                                        qs = qs.filter(function (item) {
                                            var match = true;
                                            Object.keys(customFilter).forEach(function (attr) {
                                                if (!_this8.matches(item, attr, customFilter[attr])) {
                                                    match = false;
                                                }
                                            });
                                            return match;
                                        });
                                    }
                                }

                                return _context8.abrupt("return", this._processData(qs.toModelArray().map(function (instance) {
                                    return _this8._withNested(instance);
                                })));

                            case 14:
                            case "end":
                                return _context8.stop();
                        }
                    }
                }, _callee8, this);
            }));

            function filterPage(_x7, _x8, _x9) {
                return _filterPage.apply(this, arguments);
            }

            return filterPage;
        }() // Filter an array of objects by one or more attributes

    }, {
        key: "filter",
        value: function () {
            var _filter2 = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee9(_filter, any, localOnly) {
                var data;
                return _regeneratorRuntime__default['default'].wrap(function _callee9$(_context9) {
                    while (1) {
                        switch (_context9.prev = _context9.next) {
                            case 0:
                                _context9.next = 2;
                                return this.filterPage(_filter, any, localOnly);

                            case 2:
                                data = _context9.sent;
                                return _context9.abrupt("return", data.list);

                            case 4:
                            case "end":
                                return _context9.stop();
                        }
                    }
                }, _callee9, this);
            }));

            function filter(_x10, _x11, _x12) {
                return _filter2.apply(this, arguments);
            }

            return filter;
        }() // Create new item

    }, {
        key: "create",
        value: function () {
            var _create = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee10(object, meta) {
                return _regeneratorRuntime__default['default'].wrap(function _callee10$(_context10) {
                    while (1) {
                        switch (_context10.prev = _context10.next) {
                            case 0:
                                this.dispatch(CREATE, object, meta);

                            case 1:
                            case "end":
                                return _context10.stop();
                        }
                    }
                }, _callee10, this);
            }));

            function create(_x13, _x14) {
                return _create.apply(this, arguments);
            }

            return create;
        }() // Merge new/updated items into list

    }, {
        key: "update",
        value: function () {
            var _update2 = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee11(_update, meta) {
                return _regeneratorRuntime__default['default'].wrap(function _callee11$(_context11) {
                    while (1) {
                        switch (_context11.prev = _context11.next) {
                            case 0:
                                if (!(meta && typeof meta === 'string')) {
                                    _context11.next = 2;
                                    break;
                                }

                                throw new Error('Usage: update(items[, meta]).  To customize id attr use config.idCol');

                            case 2:
                                return _context11.abrupt("return", this.dispatch(UPDATE, _update, meta));

                            case 3:
                            case "end":
                                return _context11.stop();
                        }
                    }
                }, _callee11, this);
            }));

            function update(_x15, _x16) {
                return _update2.apply(this, arguments);
            }

            return update;
        }()
    }, {
        key: "remove",
        value: function () {
            var _remove = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee12(id, meta) {
                return _regeneratorRuntime__default['default'].wrap(function _callee12$(_context12) {
                    while (1) {
                        switch (_context12.prev = _context12.next) {
                            case 0:
                                if (!(meta && typeof meta === 'string')) {
                                    _context12.next = 2;
                                    break;
                                }

                                throw new Error('Usage: remove(id).  To customize id attr use config.idCol');

                            case 2:
                                return _context12.abrupt("return", this.dispatch(DELETE, id, meta));

                            case 3:
                            case "end":
                                return _context12.stop();
                        }
                    }
                }, _callee12, this);
            }));

            function remove(_x17, _x18) {
                return _remove.apply(this, arguments);
            }

            return remove;
        }() // Overwrite entire list

    }, {
        key: "overwrite",
        value: function () {
            var _overwrite = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee13(data, meta) {
                return _regeneratorRuntime__default['default'].wrap(function _callee13$(_context13) {
                    while (1) {
                        switch (_context13.prev = _context13.next) {
                            case 0:
                                if (data.pages == 1 && data.list) {
                                    data.count = data.per_page = data.list.length;
                                } else {
                                    data = this._processData(data);
                                }

                                return _context13.abrupt("return", this.dispatch(OVERWRITE, data, meta));

                            case 2:
                            case "end":
                                return _context13.stop();
                        }
                    }
                }, _callee13, this);
            }));

            function overwrite(_x19, _x20) {
                return _overwrite.apply(this, arguments);
            }

            return overwrite;
        }() // Prefetch list

    }, {
        key: "prefetch",
        value: function () {
            var _prefetch = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee14() {
                var data;
                return _regeneratorRuntime__default['default'].wrap(function _callee14$(_context14) {
                    while (1) {
                        switch (_context14.prev = _context14.next) {
                            case 0:
                                _context14.next = 2;
                                return this.getPage(null);

                            case 2:
                                data = _context14.sent;
                                return _context14.abrupt("return", this.overwrite(data));

                            case 4:
                            case "end":
                                return _context14.stop();
                        }
                    }
                }, _callee14, this);
            }));

            function prefetch() {
                return _prefetch.apply(this, arguments);
            }

            return prefetch;
        }() // Helper for partial list updates (useful for large lists)
        // Note: params should contain correct arguments to fetch only "recent"
        // items from server; idcol should be a unique identifier for the list

    }, {
        key: "fetchUpdate",
        value: function () {
            var _fetchUpdate = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee15(params, idCol) {
                var q, data;
                return _regeneratorRuntime__default['default'].wrap(function _callee15$(_context15) {
                    while (1) {
                        switch (_context15.prev = _context15.next) {
                            case 0:
                                if (!idCol) {
                                    _context15.next = 2;
                                    break;
                                }

                                throw new Error('Usage: fetchUpdate(params).  To customize id attr use config.idCol');

                            case 2:
                                // Update local list with recent items from server
                                q = _objectSpread2(_objectSpread2({}, this.query), params);
                                _context15.next = 5;
                                return this.store.fetch(q);

                            case 5:
                                data = _context15.sent;
                                return _context15.abrupt("return", this.update(data));

                            case 7:
                            case "end":
                                return _context15.stop();
                        }
                    }
                }, _callee15, this);
            }));

            function fetchUpdate(_x21, _x22) {
                return _fetchUpdate.apply(this, arguments);
            }

            return fetchUpdate;
        }() // Unsaved form items related to this list

    }, {
        key: "unsyncedItems",
        value: function unsyncedItems(withData) {
            // Note: wq/outbox needs to have already been loaded for this to work
            var outbox = this.store.outbox;

            if (!outbox) {
                return Promise.resolve([]);
            }

            return outbox.unsyncedItems(this.query, withData);
        } // Apply a predefined function to a retreived item

    }, {
        key: "compute",
        value: function compute(fn, item) {
            if (this.functions[fn]) {
                return this.functions[fn](item);
            } else {
                return null;
            }
        }
    }, {
        key: "isCustomFilter",
        value: function isCustomFilter(attr, comp) {
            return this.functions[attr] || isPotentialBoolean(comp) || Array.isArray(comp);
        }
    }, {
        key: "matches",
        value: function matches(item, attr, comp) {
            var value;

            if (this.functions[attr]) {
                value = this.compute(attr, item);
            } else {
                value = item[attr];
            }

            if (Array.isArray(comp)) {
                return comp.filter(function (c) {
                    return checkValue(value, c);
                }).length > 0;
            } else {
                return checkValue(value, comp);
            }

            function checkValue(value, comp) {
                if (isRawBoolean(value)) {
                    return value === toBoolean(comp);
                } else if (typeof value === 'number') {
                    return value === +comp;
                } else if (Array.isArray(value)) {
                    return value.filter(function (v) {
                        return checkValue(v, comp);
                    }).length > 0;
                } else {
                    return value === comp;
                }
            }
        }
    }, {
        key: "model",
        get: function get() {
            return this.getSessionModel();
        }
    }, {
        key: "objects",
        get: function get() {
            return this.getQuerySet();
        }
    }]);

    return Model;
}();

function isRawBoolean(value) {
    return [null, true, false].indexOf(value) > -1;
}

function toBoolean(value) {
    if ([true, 'true', 1, '1', 't', 'y'].indexOf(value) > -1) {
        return true;
    } else if ([false, 'false', 0, '0', 'f', 'n'].indexOf(value) > -1) {
        return false;
    } else if ([null, 'null'].indexOf(value) > -1) {
        return null;
    } else {
        return value;
    }
}

function isPotentialBoolean(value) {
    return isRawBoolean(toBoolean(value));
}

model.Model = Model;

exports.Model = Model;
exports.default = model;

Object.defineProperty(exports, '__esModule', { value: true });

});
//# sourceMappingURL=model.js.map
