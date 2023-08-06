/*
 * @wq/router 1.3.0-alpha.2
 * Respond to URL changes with locally generated pages and custom events
 * (c) 2012-2020, S. Andrew Sheppard
 * https://wq.io/license
 */

define(['regenerator-runtime', 'redux-first-router', './store'], function (_regeneratorRuntime, reduxFirstRouter, store) { 'use strict';

function _interopDefaultLegacy (e) { return e && typeof e === 'object' && 'default' in e ? e : { 'default': e }; }

var _regeneratorRuntime__default = /*#__PURE__*/_interopDefaultLegacy(_regeneratorRuntime);

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

function _createForOfIteratorHelper(o, allowArrayLike) {
  var it;

  if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) {
    if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") {
      if (it) o = it;
      var i = 0;

      var F = function () {};

      return {
        s: F,
        n: function () {
          if (i >= o.length) return {
            done: true
          };
          return {
            done: false,
            value: o[i++]
          };
        },
        e: function (e) {
          throw e;
        },
        f: F
      };
    }

    throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
  }

  var normalCompletion = true,
      didErr = false,
      err;
  return {
    s: function () {
      it = o[Symbol.iterator]();
    },
    n: function () {
      var step = it.next();
      normalCompletion = step.done;
      return step;
    },
    e: function (e) {
      didErr = true;
      err = e;
    },
    f: function () {
      try {
        if (!normalCompletion && it.return != null) it.return();
      } finally {
        if (didErr) throw err;
      }
    }
  };
}

function createCommonjsModule(fn, basedir, module) {
	return module = {
		path: basedir,
		exports: {},
		require: function (path, base) {
			return commonjsRequire(path, (base === undefined || base === null) ? module.path : base);
		}
	}, fn(module, module.exports), module.exports;
}

function commonjsRequire () {
	throw new Error('Dynamic requires are not currently supported by @rollup/plugin-commonjs');
}

var strictUriEncode = function strictUriEncode(str) {
    return encodeURIComponent(str).replace(/[!'()*]/g, function (x) {
        return "%".concat(x.charCodeAt(0).toString(16).toUpperCase());
    });
};

var token = '%[a-f0-9]{2}';
var singleMatcher = new RegExp(token, 'gi');
var multiMatcher = new RegExp('(' + token + ')+', 'gi');

function decodeComponents(components, split) {
    try {
        // Try to decode the entire string first
        return decodeURIComponent(components.join(''));
    } catch (err) {// Do nothing
    }

    if (components.length === 1) {
        return components;
    }

    split = split || 1; // Split the array in 2 parts

    var left = components.slice(0, split);
    var right = components.slice(split);
    return Array.prototype.concat.call([], decodeComponents(left), decodeComponents(right));
}

function decode(input) {
    try {
        return decodeURIComponent(input);
    } catch (err) {
        var tokens = input.match(singleMatcher);

        for (var i = 1; i < tokens.length; i++) {
            input = decodeComponents(tokens, i).join('');
            tokens = input.match(singleMatcher);
        }

        return input;
    }
}

function customDecodeURIComponent(input) {
    // Keep track of all the replacements and prefill the map with the `BOM`
    var replaceMap = {
        '%FE%FF': "\uFFFD\uFFFD",
        '%FF%FE': "\uFFFD\uFFFD"
    };
    var match = multiMatcher.exec(input);

    while (match) {
        try {
            // Decode as big chunks as possible
            replaceMap[match[0]] = decodeURIComponent(match[0]);
        } catch (err) {
            var result = decode(match[0]);

            if (result !== match[0]) {
                replaceMap[match[0]] = result;
            }
        }

        match = multiMatcher.exec(input);
    } // Add `%C2` at the end of the map to make sure it does not replace the combinator before everything else


    replaceMap['%C2'] = "\uFFFD";
    var entries = Object.keys(replaceMap);

    for (var i = 0; i < entries.length; i++) {
        // Replace all decoded components
        var key = entries[i];
        input = input.replace(new RegExp(key, 'g'), replaceMap[key]);
    }

    return input;
}

var decodeUriComponent = function decodeUriComponent(encodedURI) {
    if (typeof encodedURI !== 'string') {
        throw new TypeError('Expected `encodedURI` to be of type `string`, got `' + _typeof(encodedURI) + '`');
    }

    try {
        encodedURI = encodedURI.replace(/\+/g, ' '); // Try the built in decoder first

        return decodeURIComponent(encodedURI);
    } catch (err) {
        // Fallback to a more advanced decoder
        return customDecodeURIComponent(encodedURI);
    }
};

var splitOnFirst = function splitOnFirst(string, separator) {
    if (!(typeof string === 'string' && typeof separator === 'string')) {
        throw new TypeError('Expected the arguments to be of type `string`');
    }

    if (separator === '') {
        return [string];
    }

    var separatorIndex = string.indexOf(separator);

    if (separatorIndex === -1) {
        return [string];
    }

    return [string.slice(0, separatorIndex), string.slice(separatorIndex + separator.length)];
};

var queryString = createCommonjsModule(function (module, exports) {

    var isNullOrUndefined = function isNullOrUndefined(value) {
        return value === null || value === undefined;
    };

    function encoderForArrayFormat(options) {
        switch (options.arrayFormat) {
            case 'index':
                return function (key) {
                    return function (result, value) {
                        var index = result.length;

                        if (value === undefined || options.skipNull && value === null || options.skipEmptyString && value === '') {
                            return result;
                        }

                        if (value === null) {
                            return [].concat(_toConsumableArray(result), [[encode(key, options), '[', index, ']'].join('')]);
                        }

                        return [].concat(_toConsumableArray(result), [[encode(key, options), '[', encode(index, options), ']=', encode(value, options)].join('')]);
                    };
                };

            case 'bracket':
                return function (key) {
                    return function (result, value) {
                        if (value === undefined || options.skipNull && value === null || options.skipEmptyString && value === '') {
                            return result;
                        }

                        if (value === null) {
                            return [].concat(_toConsumableArray(result), [[encode(key, options), '[]'].join('')]);
                        }

                        return [].concat(_toConsumableArray(result), [[encode(key, options), '[]=', encode(value, options)].join('')]);
                    };
                };

            case 'comma':
            case 'separator':
                return function (key) {
                    return function (result, value) {
                        if (value === null || value === undefined || value.length === 0) {
                            return result;
                        }

                        if (result.length === 0) {
                            return [[encode(key, options), '=', encode(value, options)].join('')];
                        }

                        return [[result, encode(value, options)].join(options.arrayFormatSeparator)];
                    };
                };

            default:
                return function (key) {
                    return function (result, value) {
                        if (value === undefined || options.skipNull && value === null || options.skipEmptyString && value === '') {
                            return result;
                        }

                        if (value === null) {
                            return [].concat(_toConsumableArray(result), [encode(key, options)]);
                        }

                        return [].concat(_toConsumableArray(result), [[encode(key, options), '=', encode(value, options)].join('')]);
                    };
                };
        }
    }

    function parserForArrayFormat(options) {
        var result;

        switch (options.arrayFormat) {
            case 'index':
                return function (key, value, accumulator) {
                    result = /\[(\d*)\]$/.exec(key);
                    key = key.replace(/\[\d*\]$/, '');

                    if (!result) {
                        accumulator[key] = value;
                        return;
                    }

                    if (accumulator[key] === undefined) {
                        accumulator[key] = {};
                    }

                    accumulator[key][result[1]] = value;
                };

            case 'bracket':
                return function (key, value, accumulator) {
                    result = /(\[\])$/.exec(key);
                    key = key.replace(/\[\]$/, '');

                    if (!result) {
                        accumulator[key] = value;
                        return;
                    }

                    if (accumulator[key] === undefined) {
                        accumulator[key] = [value];
                        return;
                    }

                    accumulator[key] = [].concat(accumulator[key], value);
                };

            case 'comma':
            case 'separator':
                return function (key, value, accumulator) {
                    var isArray = typeof value === 'string' && value.split('').indexOf(options.arrayFormatSeparator) > -1;
                    var newValue = isArray ? value.split(options.arrayFormatSeparator).map(function (item) {
                        return decode(item, options);
                    }) : value === null ? value : decode(value, options);
                    accumulator[key] = newValue;
                };

            default:
                return function (key, value, accumulator) {
                    if (accumulator[key] === undefined) {
                        accumulator[key] = value;
                        return;
                    }

                    accumulator[key] = [].concat(accumulator[key], value);
                };
        }
    }

    function validateArrayFormatSeparator(value) {
        if (typeof value !== 'string' || value.length !== 1) {
            throw new TypeError('arrayFormatSeparator must be single character string');
        }
    }

    function encode(value, options) {
        if (options.encode) {
            return options.strict ? strictUriEncode(value) : encodeURIComponent(value);
        }

        return value;
    }

    function decode(value, options) {
        if (options.decode) {
            return decodeUriComponent(value);
        }

        return value;
    }

    function keysSorter(input) {
        if (Array.isArray(input)) {
            return input.sort();
        }

        if (_typeof(input) === 'object') {
            return keysSorter(Object.keys(input)).sort(function (a, b) {
                return Number(a) - Number(b);
            }).map(function (key) {
                return input[key];
            });
        }

        return input;
    }

    function removeHash(input) {
        var hashStart = input.indexOf('#');

        if (hashStart !== -1) {
            input = input.slice(0, hashStart);
        }

        return input;
    }

    function getHash(url) {
        var hash = '';
        var hashStart = url.indexOf('#');

        if (hashStart !== -1) {
            hash = url.slice(hashStart);
        }

        return hash;
    }

    function extract(input) {
        input = removeHash(input);
        var queryStart = input.indexOf('?');

        if (queryStart === -1) {
            return '';
        }

        return input.slice(queryStart + 1);
    }

    function parseValue(value, options) {
        if (options.parseNumbers && !Number.isNaN(Number(value)) && typeof value === 'string' && value.trim() !== '') {
            value = Number(value);
        } else if (options.parseBooleans && value !== null && (value.toLowerCase() === 'true' || value.toLowerCase() === 'false')) {
            value = value.toLowerCase() === 'true';
        }

        return value;
    }

    function parse(input, options) {
        options = Object.assign({
            decode: true,
            sort: true,
            arrayFormat: 'none',
            arrayFormatSeparator: ',',
            parseNumbers: false,
            parseBooleans: false
        }, options);
        validateArrayFormatSeparator(options.arrayFormatSeparator);
        var formatter = parserForArrayFormat(options); // Create an object with no prototype

        var ret = Object.create(null);

        if (typeof input !== 'string') {
            return ret;
        }

        input = input.trim().replace(/^[?#&]/, '');

        if (!input) {
            return ret;
        }

        var _iterator = _createForOfIteratorHelper(input.split('&')),
            _step;

        try {
            for (_iterator.s(); !(_step = _iterator.n()).done;) {
                var param = _step.value;

                var _splitOnFirst = splitOnFirst(options.decode ? param.replace(/\+/g, ' ') : param, '='),
                    _splitOnFirst2 = _slicedToArray(_splitOnFirst, 2),
                    _key = _splitOnFirst2[0],
                    _value = _splitOnFirst2[1]; // Missing `=` should be `null`:
                // http://w3.org/TR/2012/WD-url-20120524/#collect-url-parameters


                _value = _value === undefined ? null : ['comma', 'separator'].includes(options.arrayFormat) ? _value : decode(_value, options);
                formatter(decode(_key, options), _value, ret);
            }
        } catch (err) {
            _iterator.e(err);
        } finally {
            _iterator.f();
        }

        for (var _i = 0, _Object$keys = Object.keys(ret); _i < _Object$keys.length; _i++) {
            var key = _Object$keys[_i];
            var value = ret[key];

            if (_typeof(value) === 'object' && value !== null) {
                for (var _i2 = 0, _Object$keys2 = Object.keys(value); _i2 < _Object$keys2.length; _i2++) {
                    var k = _Object$keys2[_i2];
                    value[k] = parseValue(value[k], options);
                }
            } else {
                ret[key] = parseValue(value, options);
            }
        }

        if (options.sort === false) {
            return ret;
        }

        return (options.sort === true ? Object.keys(ret).sort() : Object.keys(ret).sort(options.sort)).reduce(function (result, key) {
            var value = ret[key];

            if (Boolean(value) && _typeof(value) === 'object' && !Array.isArray(value)) {
                // Sort object keys, not values
                result[key] = keysSorter(value);
            } else {
                result[key] = value;
            }

            return result;
        }, Object.create(null));
    }

    exports.extract = extract;
    exports.parse = parse;

    exports.stringify = function (object, options) {
        if (!object) {
            return '';
        }

        options = Object.assign({
            encode: true,
            strict: true,
            arrayFormat: 'none',
            arrayFormatSeparator: ','
        }, options);
        validateArrayFormatSeparator(options.arrayFormatSeparator);

        var shouldFilter = function shouldFilter(key) {
            return options.skipNull && isNullOrUndefined(object[key]) || options.skipEmptyString && object[key] === '';
        };

        var formatter = encoderForArrayFormat(options);
        var objectCopy = {};

        for (var _i3 = 0, _Object$keys3 = Object.keys(object); _i3 < _Object$keys3.length; _i3++) {
            var key = _Object$keys3[_i3];

            if (!shouldFilter(key)) {
                objectCopy[key] = object[key];
            }
        }

        var keys = Object.keys(objectCopy);

        if (options.sort !== false) {
            keys.sort(options.sort);
        }

        return keys.map(function (key) {
            var value = object[key];

            if (value === undefined) {
                return '';
            }

            if (value === null) {
                return encode(key, options);
            }

            if (Array.isArray(value)) {
                return value.reduce(formatter(key), []).join('&');
            }

            return encode(key, options) + '=' + encode(value, options);
        }).filter(function (x) {
            return x.length > 0;
        }).join('&');
    };

    exports.parseUrl = function (input, options) {
        options = Object.assign({
            decode: true
        }, options);

        var _splitOnFirst3 = splitOnFirst(input, '#'),
            _splitOnFirst4 = _slicedToArray(_splitOnFirst3, 2),
            url = _splitOnFirst4[0],
            hash = _splitOnFirst4[1];

        return Object.assign({
            url: url.split('?')[0] || '',
            query: parse(extract(input), options)
        }, options && options.parseFragmentIdentifier && hash ? {
            fragmentIdentifier: decode(hash, options)
        } : {});
    };

    exports.stringifyUrl = function (input, options) {
        options = Object.assign({
            encode: true,
            strict: true
        }, options);
        var url = removeHash(input.url).split('?')[0] || '';
        var queryFromUrl = exports.extract(input.url);
        var parsedQueryFromUrl = exports.parse(queryFromUrl, {
            sort: false
        });
        var query = Object.assign(parsedQueryFromUrl, input.query);
        var queryString = exports.stringify(query, options);

        if (queryString) {
            queryString = "?".concat(queryString);
        }

        var hash = getHash(input.url);

        if (input.fragmentIdentifier) {
            hash = "#".concat(encode(input.fragmentIdentifier, options));
        }

        return "".concat(url).concat(queryString).concat(hash);
    };
});

var _validOrder;
var HTML = '@@HTML',
    RENDER = 'RENDER',
    FIRST = '@@FIRST',
    DEFAULT = '@@DEFAULT',
    LAST = '@@LAST',
    CURRENT = '@@CURRENT',
    validOrder = (_validOrder = {}, _defineProperty(_validOrder, FIRST, true), _defineProperty(_validOrder, DEFAULT, true), _defineProperty(_validOrder, LAST, true), _validOrder); // Exported module object

var router = {
    config: {
        store: 'main',
        tmpl404: 404,
        debug: false,
        getTemplateName: function getTemplateName(name) {
            return name;
        },
        querySerializer: queryString
    },
    routesMap: {},
    routeInfoFn: [],
    contextProcessors: []
}; // Configuration

router.init = function (config) {
    // Define baseurl (without trailing slash) if it is not /
    if (config && config.base_url) {
        router.base_url = config.base_url;
    }

    router.config = _objectSpread2(_objectSpread2({}, router.config), config); // Configuration options:
    // Define `tmpl404` if there is not a template named '404'
    // Set `debug` to true to log template & context information
    // Set getTemplateName to change how route names are resolved.

    var _connectRoutes = reduxFirstRouter.connectRoutes({}, {
        querySerializer: router.config.querySerializer,
        initialDispatch: false
    }),
        routeReducer = _connectRoutes.reducer,
        middleware = _connectRoutes.middleware,
        enhancer = _connectRoutes.enhancer,
        initialDispatch = _connectRoutes.initialDispatch;

    router.store = store.getStore(router.config.store);
    router.store.addReducer('location', routeReducer);
    router.store.addReducer('context', contextReducer);
    router.store.addReducer('routeInfo', routeInfoReducer);
    router.store.addEnhancer(enhancer);
    router.store.addMiddleware(middleware);
    router.store.setThunkHandler(router.addThunk);
    router._initialDispatch = initialDispatch;
};

router.start = function () {
    if (!router.config) {
        throw new Error('Initialize router first!');
    }

    var orderedRoutes = {};
    [FIRST, DEFAULT, LAST].forEach(function (order) {
        Object.entries(router.routesMap).forEach(function (_ref) {
            var _ref2 = _slicedToArray(_ref, 2),
                name = _ref2[0],
                path = _ref2[1];

            if (path.order === order) {
                orderedRoutes[name] = path;
            }
        });
    });
    router.store.dispatch({
        type: reduxFirstRouter.ADD_ROUTES,
        payload: {
            routes: orderedRoutes
        }
    });

    router._initialDispatch();
};

router.jqmInit = function () {
    console.warn(new Error('jqmInit() renamed to start()'));
    router.start();
};

function contextReducer() {
    var _objectSpread2$1;

    var context = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
    var action = arguments.length > 1 ? arguments[1] : undefined;

    if (action.type != RENDER && action.type != reduxFirstRouter.NOT_FOUND) {
        return context;
    }

    var current;

    if (action.type === RENDER) {
        current = action.payload;
    } else if (action.type === reduxFirstRouter.NOT_FOUND) {
        var routeInfo = _routeInfo(action.meta.location);

        current = {
            router_info: _objectSpread2(_objectSpread2({}, routeInfo), {}, {
                template: router.config.tmpl404
            }),
            rt: router.base_url,
            url: routeInfo.full_path
        };
    }

    return _objectSpread2(_objectSpread2({}, context), {}, (_objectSpread2$1 = {}, _defineProperty(_objectSpread2$1, current.router_info.name, current), _defineProperty(_objectSpread2$1, CURRENT, current), _objectSpread2$1));
}

function routeInfoReducer() {
    var routeInfo = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
    var action = arguments.length > 1 ? arguments[1] : undefined;

    if (action.meta && action.meta.location) {
        var _objectSpread3;

        var current = _routeInfo(action.meta.location);

        return _objectSpread2(_objectSpread2({}, routeInfo), {}, (_objectSpread3 = {}, _defineProperty(_objectSpread3, current.name, current), _defineProperty(_objectSpread3, CURRENT, current), _objectSpread3));
    } else {
        return routeInfo;
    }
}

function _generateContext(_x, _x2) {
    return _generateContext2.apply(this, arguments);
}

function _generateContext2() {
    _generateContext2 = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee(dispatch, getState) {
        var refresh,
            location,
            context,
            i,
            fn,
            _args = arguments;
        return _regeneratorRuntime__default['default'].wrap(function _callee$(_context) {
            while (1) {
                switch (_context.prev = _context.next) {
                    case 0:
                        refresh = _args.length > 2 && _args[2] !== undefined ? _args[2] : false;
                        location = getState().location;
                        context = {
                            router_info: _routeInfo(location),
                            rt: router.base_url
                        };
                        i = 0;

                    case 4:
                        if (!(i < router.contextProcessors.length)) {
                            _context.next = 18;
                            break;
                        }

                        fn = router.contextProcessors[i];
                        _context.t0 = _objectSpread2;
                        _context.t1 = _objectSpread2({}, context);
                        _context.next = 10;
                        return fn(context);

                    case 10:
                        _context.t2 = _context.sent;

                        if (_context.t2) {
                            _context.next = 13;
                            break;
                        }

                        _context.t2 = {};

                    case 13:
                        _context.t3 = _context.t2;
                        context = (0, _context.t0)(_context.t1, _context.t3);

                    case 15:
                        i++;
                        _context.next = 4;
                        break;

                    case 18:
                        if (context[reduxFirstRouter.NOT_FOUND]) {
                            context.router_info.template = router.config.tmpl404;
                            context.url = context.router_info.full_path;
                        }

                        return _context.abrupt("return", router.render(context, refresh));

                    case 20:
                    case "end":
                        return _context.stop();
                }
            }
        }, _callee);
    }));
    return _generateContext2.apply(this, arguments);
}

router.register = function (path, nameOrContext, context) {
    var order = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : DEFAULT;
    var thunk = arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : null;
    var name;
    var newUsage = ' Usage: router.register(path[, name[, contextFn]])';

    if (!validOrder[order]) {
        // Assume old-style prevent() callback was passed
        throw new Error('prevent() no longer supported.' + newUsage);
    }

    if (context) {
        if (typeof context !== 'function') {
            throw new Error('Unexpected ' + context + ' for contextFn.' + newUsage);
        }
    } else if (typeof nameOrContext === 'function') {
        context = nameOrContext;
        nameOrContext = null;
    }

    if (nameOrContext) {
        name = nameOrContext;

        if (typeof name !== 'string') {
            throw new Error('Unexpected ' + name + ' for route name.' + newUsage);
        }
    } else {
        if (path.indexOf('/') > -1) {
            throw new Error('router.register() now requires a route name if path contains /.' + newUsage);
        } // Assume there is a template with the same name


        name = path;
    }

    if (context && context.length > 1) {
        throw new Error('contextFn should take a single argument (the existing context) and return a new context for merging.');
    }

    function thunkFn(dispatch, getState, bag) {
        _generateContext(dispatch, getState);

        if (thunk) {
            thunk(dispatch, getState, bag);
        }
    }

    router.routesMap[name.toUpperCase()] = {
        path: _normalizePath(path),
        thunk: thunkFn,
        order: order
    };

    if (context) {
        router.addContextForRoute(name, context);
    }

    return name;
};

router.registerFirst = function (path, name, context) {
    router.register(path, name, context, FIRST);
};

router.registerLast = function (path, name, context) {
    router.register(path, name, context, LAST);
};

router.addThunk = function (name, thunk) {
    router.routesMap[name] = {
        thunk: thunk,
        order: FIRST
    };
};

router.addThunks = function (thunks, thisObj) {
    Object.entries(thunks).forEach(function (_ref3) {
        var _ref4 = _slicedToArray(_ref3, 2),
            name = _ref4[0],
            thunk = _ref4[1];

        if (thisObj) {
            thunk = thunk.bind(thisObj);
        }

        router.addThunk(name, thunk);
    });
};

router.addContext = function (fn) {
    router.contextProcessors.push(fn);
};

router.addContextForRoute = function (pathOrName, fn) {
    var name = _getRouteName(pathOrName);

    function contextForRoute(context) {
        if (context.router_info.name == name) {
            return fn(context);
        } else {
            return {};
        }
    }

    router.addContext(contextForRoute);
};

router.onShow = function () {
    throw new Error('router.onShow() is removed.  Use a run() plugin instead');
};

router.addRoute = function () {
    throw new Error('router.addRoute() is removed.  Use a run() plugin instead');
};

router.push = function (path) {
    reduxFirstRouter.push(path);
};

router.render = function (context, refresh) {
    if (refresh) {
        if (refresh === true) {
            refresh = (context._refreshCount || 0) + 1;
        }

        context = _objectSpread2(_objectSpread2({}, context), {}, {
            _refreshCount: refresh
        });
    }

    return router.store.dispatch({
        type: RENDER,
        payload: context
    });
};

router.getContext = function () {
    var _router$store$getStat = router.store.getState(),
        _router$store$getStat2 = _router$store$getStat.context,
        context = _router$store$getStat2 === void 0 ? {} : _router$store$getStat2;

    return context[CURRENT];
}; // Re-render existing context


router.refresh = function () {
    var context = router.getContext();
    router.render(context, true);
}; // Regenerate context, then re-render page


router.reload = function () {
    var context = router.getContext(),
        refresh = (context._refreshCount || 0) + 1;
    return _generateContext(function (action) {
        return router.store.dispatch(action);
    }, function () {
        return router.store.getState();
    }, refresh);
}; // Simple 404 page helper


router.notFound = function () {
    return _defineProperty({}, reduxFirstRouter.NOT_FOUND, true);
}; // Use when loading HTML from server


router.rawHTML = function (html) {
    return _defineProperty({}, HTML, html);
};

router.base_url = '';

router.addRouteInfo = function (fn) {
    router.routeInfoFn.push(fn);
};

function _normalizePath(path) {
    path = path.replace('<slug>', ':slug');
    return router.base_url + '/' + path;
}

function _getRouteName(pathOrName) {
    var name;

    if (router.routesMap[pathOrName.toUpperCase()]) {
        name = pathOrName;
    } else {
        Object.entries(router.routesMap).forEach(function (_ref7) {
            var _ref8 = _slicedToArray(_ref7, 2),
                rname = _ref8[0],
                rpath = _ref8[1];

            if (_normalizePath(pathOrName) === rpath.path) {
                name = rname;
            }
        });
    }

    if (!name) {
        throw new Error('Unrecognized route: ' + pathOrName);
    }

    return name.toLowerCase();
}

function _removeBase(pathname) {
    return pathname.replace(router.base_url + '/', '');
}

var _lastRouteInfo = null;

function _routeInfo(location) {
    var info = _computeRouteInfo(location);

    if (JSON.stringify(info) !== JSON.stringify(_lastRouteInfo)) {
        _lastRouteInfo = info;
    }

    return _lastRouteInfo;
}

function _computeRouteInfo(location) {
    if (location.current && location.prev) {
        location = _objectSpread2(_objectSpread2({}, location.current), {}, {
            prev: location.prev
        });
    }

    var info = {};
    info.name = location.type.toLowerCase();
    info.template = router.config.getTemplateName(info.name);
    info.prev_path = _removeBase(location.prev.pathname);
    info.path = _removeBase(location.pathname);
    info.path_enc = escape(info.path);
    info.full_path = location.pathname + (location.search ? '?' + location.search : '');
    info.full_path_enc = escape(info.full_path);
    info.params = location.query;
    info.slugs = location.payload;
    info.base_url = router.base_url;
    router.routeInfoFn.forEach(function (fn) {
        return info = fn(info);
    });
    return info;
}

return router;

});
//# sourceMappingURL=router.js.map
