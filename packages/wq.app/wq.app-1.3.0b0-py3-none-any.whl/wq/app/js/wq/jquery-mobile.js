/*
 * @wq/jquery-mobile 1.3.0-alpha.3
 * Modified jQuery Mobile for use with @wq/app
 * (c) 2012-2020, S. Andrew Sheppard
 * https://wq.io/license
 */

define(['regenerator-runtime', 'jquery', 'mustache', 'jquery.mobile', 'localforage'], function (_regeneratorRuntime, jQuery, Mustache, jqmInit, localForage) { 'use strict';

function _interopDefaultLegacy (e) { return e && typeof e === 'object' && 'default' in e ? e : { 'default': e }; }

var _regeneratorRuntime__default = /*#__PURE__*/_interopDefaultLegacy(_regeneratorRuntime);
var jQuery__default = /*#__PURE__*/_interopDefaultLegacy(jQuery);
var Mustache__default = /*#__PURE__*/_interopDefaultLegacy(Mustache);
var jqmInit__default = /*#__PURE__*/_interopDefaultLegacy(jqmInit);
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

var LOCALFORAGE_PREFIX = '__lfsc__:blob~~local_forage_type~image/jpeg~';
var photos = {
    name: 'photos'
};
var _defaults = {
    quality: 75,
    destinationType: 0 //Camera.DestinationType.DATA_URL

};
var $, jqm, spin;

photos.init = function (config) {
    $ = config && config.jQuery || window.jQuery;
    spin = photos.app.spin;
};

photos.context = function () {
    return {
        image_url: function image_url() {
            try {
                return this.body && _getUrl(this.body);
            } catch (e) {// Image will be blank, but at least template won't crash
            }
        }
    };
};

photos.run = function ($page) {
    $page.on('change', 'input[type=file]', photos.preview);
    $page.on('click', 'button[data-wq-action=take]', photos.take);
    $page.on('click', 'button[data-wq-action=pick]', photos.pick);
};

photos.preview = function (imgid, file) {
    if (typeof imgid !== 'string' && !file) {
        imgid = $(this).data('wq-preview');

        if (!imgid) {
            return;
        }

        file = this.files[0];

        if (!file) {
            return;
        }
    }

    $('#' + imgid).attr('src', _getUrl(file));
};

function _getUrl(file) {
    var URL = window.URL || window.webkitURL;
    return URL && URL.createObjectURL(file);
}

photos.take = function (input, preview) {
    var options = $.extend({
        sourceType: Camera.PictureSourceType.CAMERA,
        correctOrientation: true,
        saveToPhotoAlbum: true
    }, _defaults);

    _start.call(this, options, input, preview);
};

photos.pick = function (input, preview) {
    var options = $.extend({
        sourceType: Camera.PictureSourceType.SAVEDPHOTOALBUM
    }, _defaults);

    _start.call(this, options, input, preview);
};

function _start(options, input, preview) {
    if (typeof input !== 'string' && !preview) {
        input = $(this).data('wq-input');

        if (!input) {
            return;
        }

        preview = jqm.activePage.find('#' + input).data('wq-preview');
    }

    navigator.camera.getPicture(function (data) {
        load(data, input, preview);
    }, function (msg) {
        error(msg);
    }, options);
}

photos.base64toBlob = /*#__PURE__*/function () {
    var _ref = _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee(data) {
        var serializer;
        return _regeneratorRuntime__default['default'].wrap(function _callee$(_context) {
            while (1) {
                switch (_context.prev = _context.next) {
                    case 0:
                        _context.next = 2;
                        return photos.app.store.ready;

                    case 2:
                        _context.next = 4;
                        return localForage__default['default'].getSerializer();

                    case 4:
                        serializer = _context.sent;
                        return _context.abrupt("return", serializer.deserialize(LOCALFORAGE_PREFIX + data));

                    case 6:
                    case "end":
                        return _context.stop();
                }
            }
        }, _callee);
    }));

    return function (_x) {
        return _ref.apply(this, arguments);
    };
}();

photos._files = {};

photos.storeFile = function (name, type, blob, input) {
    // Save blob data for later retrieval
    var file = {
        name: name,
        type: type,
        body: blob
    };
    photos._files[name] = file;

    if (input) {
        $('#' + input).val(name);
    }
};

function load(data, input, preview) {
    spin.start('Loading image...');
    photos.base64toBlob(data).then(function (blob) {
        var number = Math.round(Math.random() * 1e10);
        var name = $('#' + input).val() || 'photo' + number + '.jpg';
        photos.storeFile(name, 'image/jpeg', blob, input);
        spin.stop();

        if (preview) {
            photos.preview(preview, blob);
        }
    });
}

function error(msg) {
    spin.start('Error Loading Image: ' + msg, 1.5, {
        theme: jqm.pageLoadErrorMessageTheme,
        textonly: true
    });
}

var _thunks;
var HTML = '@@HTML',
    // @wq/router
RENDER = 'RENDER',
    // @wq/router
SPIN_START = 'SPIN_START',
    // @wq/app:spinner
SPIN_STOP = 'SPIN_STOP'; // @wq/app:spinner

var jqmRenderer = {
    name: 'jqmrenderer',
    type: 'renderer',
    dependencies: [photos],
    config: {
        templates: {},
        partials: {},
        injectOnce: false,
        debug: false,
        noScroll: false,
        transitions: {
            default: 'none',
            dialog: 'none',
            maxwidth: 800
        }
    },
    init: function init(config) {
        var appConf = this.app.config;

        if (!config) {
            var _appConf$template, _appConf$router;

            config = {};

            if ((_appConf$template = appConf.template) === null || _appConf$template === void 0 ? void 0 : _appConf$template.templates) {
                console.warn('Rename config.template.templates to config.jqmrenderer.templates');
                config.templates = appConf.template.templates;

                if (appConf.template.partials) {
                    config.partials = appConf.template.partials;
                }
            }

            if (appConf.transitions) {
                console.warn('Rename config.transitions to config.jqmrenderer.transitions');
                config.transitions = appConf.transitions;
            }

            if ((_appConf$router = appConf.router) === null || _appConf$router === void 0 ? void 0 : _appConf$router.injectOnce) {
                console.warn('Rename config.router.injectOnce to config.jqmrenderer.injectOnce');
                config.injectOnce = appConf.router.injectOnce;
            }
        }

        if (!('debug' in config)) {
            config.debug = appConf.debug;
        }

        if (config.transitions) {
            config.transitions = _objectSpread2(_objectSpread2({}, this.config.transitions), config.transitions);
        }

        if (config.templates && config.templates.partials) {
            config.partials = config.templates.partials;
        }

        Object.assign(this.config, config);
        config = this.config; // Configuration options:
        // Set `injectOnce`to true to re-use rendered templates
        // Set `debug` to true to log template & context information
        // Set `noScroll` to work around jsdom scroll support.

        if (config.noScroll) {
            window.scrollTo = function () {};
        }

        jQuery__default['default'](document).on('mobileinit', function () {
            jQuery__default['default'].extend(jQuery__default['default'].mobile, {
                hashListeningEnabled: false,
                pushStateEnabled: false
            });
        });
        jqmInit__default['default'](jQuery__default['default'], window, document);
        var jqm = jQuery__default['default'].mobile;
        this.$ = jQuery__default['default'];
        this.jqm = jqm; // Configure jQuery Mobile transitions

        if (config.transitions) {
            jqm.defaultPageTransition = config.transitions['default'];
            jqm.defaultDialogTransition = config.transitions.dialog;
            jqm.maxTransitionWidth = config.transitions.maxwidth;
        } // Ready to go!


        jqm.initializePage();
    },
    context: function context(ctx, routeInfo) {
        if (routeInfo.mode === 'edit' && routeInfo.variant === 'new') {
            return {
                new_attachment: true
            };
        }
    },
    thunks: (_thunks = {}, _defineProperty(_thunks, RENDER, function () {
        this.renderPage(this.app.router.getContext());
    }), _defineProperty(_thunks, SPIN_START, function (dispatch, getState) {
        this.updateSpinner(getState());
    }), _defineProperty(_thunks, SPIN_STOP, function (dispatch, getState) {
        this.updateSpinner(getState());
    }), _thunks),
    renderPage: function renderPage(context) {
        this._lastContext = context;

        var router_info = context.router_info,
            _ref = router_info || {},
            url = _ref.full_path,
            pageid = _ref.dom_id,
            routeName = _ref.name,
            template = _ref.template,
            ui = null; // FIXME


        if (!routeName) {
            return;
        }

        var $page,
            html = context[HTML];

        if (html) {
            if (this.config.debug) {
                console.log('Injecting pre-rendered HTML:');
                console.log(html);
            }

            $page = this.injectHTML(html, url, pageid);
        } else {
            if (this.config.debug) {
                console.log('Rendering ' + url + " with template '" + template + "' and context:");
                console.log(context);
            }

            if ( this.config.injectOnce) {
                // Only render the template once
                $page = this.injectOnce(template, context, url, pageid);
            } else {
                // Default: render the template every time the page is loaded
                $page = this.inject(template, context, url, pageid);
            }
        }

        this._handlePage($page, ui);
    },
    updateSpinner: function updateSpinner(state) {
        var spinner = state.spinner,
            jqm = this.jqm;

        if (spinner && spinner.active) {
            var opts = {};

            if (spinner.message) {
                opts.text = spinner.message;
                opts.textVisible = true;
            }

            if (spinner.type === 'alert') {
                opts.theme = jqm.pageLoadErrorMessageTheme;
                opts.textonly = true;
            }

            jqm.loading('show', opts);
        } else {
            jqm.loading('hide');
        }
    },
    // Render page and inject it into DOM (replace existing page if it exists)
    inject: function inject(template, context, url, pageid) {
        var $ = this.$,
            jqm = this.jqm;
        template = this.config.templates[template] || template;
        var html = Mustache__default['default'].render(template, context, this.config.partials);

        if (!html.match(/<div/)) {
            throw "No content found in template '" + template + "'!";
        }

        var title = html.split(/<\/?title>/)[1];
        var body = html.split(/<\/?body[^>?]*>/)[1];

        if (body) {
            html = body;
        }

        var $page = $(html.trim()); // Check for <div data-role=page>, in case it is not the only element in
        // the selection (due to an external footer or something)

        var $rolePage = $page.filter(":jqmData(role='page')");

        if ($rolePage.length > 0) {
            if (this.config.debug && $rolePage.length != $page.length) {
                console.info($page.length - $rolePage.length + ' extra element(s) ignored.');
            }

            $page = $rolePage;
        } else if ($page.length > 1) {
            $page = $('<div>').append($page);
        }

        var role = $page.jqmData('role');
        var $oldpage;

        if (pageid) {
            if (pageid === true) {
                pageid = template + '-page';
            }

            $oldpage = $('#' + pageid);
        }

        if (!$oldpage || !$oldpage.length) {
            $oldpage = $(":jqmData(url='" + url + "')");

            if (pageid && $oldpage.attr('id') && $oldpage.attr('id') != pageid) {
                $oldpage = null;
            }
        }

        if ($oldpage && $oldpage.length) {
            $oldpage.remove();
        }

        if (role == 'popup' || role == 'panel') {
            $page.appendTo(jqm.activePage[0]);

            if (role == 'popup') {
                $page.popup();
            } else {
                $page.panel();
            }

            $page.trigger('create');
        } else {
            $page.attr('data-' + jqm.ns + 'url', url);
            $page.attr('data-' + jqm.ns + 'title', title);

            if (pageid) {
                $page.attr('id', pageid);
            }

            $page.appendTo(jqm.pageContainer);
            $page.page();
        }

        return $page;
    },
    // Render template only once
    injectOnce: function injectOnce(template, context, url, id) {
        var $ = this.$,
            jqm = this.jqm;

        if (!id) {
            id = template + '-page';
        }

        var $page = $('#' + id);

        if (!$page.length) {
            // Initial render, use context if available
            $page = this.inject(template, context, url, id);
        } else {
            // Template was already rendered; ignore context but update URL
            // - it is up to the caller to update the DOM
            $page.attr('data-' + jqm.ns + 'url', url);
            $page.jqmData('url', url);
        }

        return $page;
    },
    // Render HTML loaded from server
    injectHTML: function injectHTML(html, url, id) {
        return this.inject('{{{html}}}', {
            html: html
        }, url, id);
    },
    // Initialize page events
    _handlePage: function _handlePage($page, ui) {
        var _this = this;

        var $ = this.$,
            jqm = this.jqm; // Run any/all plugins on the specified page

        $page.on('pageshow', function () {
            _this.handleShow($page);
        }); // Ensure local links are routed

        $page.on('click', 'a', function (evt) {
            return _this._handleLink(evt);
        }); // Handle form events

        $page.on('click', 'form [type=submit]', function (evt) {
            return _this._handleSubmitClick(evt);
        });
        $page.on('submit', 'form', function (evt) {
            return _this._handleForm(evt);
        }); // Display page/popup/panel

        var role = $page.jqmData('role') || 'page';
        var options;

        if (role == 'page') {
            options = ui && ui.options || {};
            options.allowSamePageTransition = true;
            jqm.changePage($page, options);
        } else if (role == 'popup') {
            options = {};

            if (ui && ui.options) {
                options.transition = ui.options.transition;
                options.positionTo = $page.data('wq-position-to');
                var link = ui.options.link;

                if (link) {
                    if (link.jqmData('position-to')) {
                        options.positionTo = link.jqmData('position-to');
                    } // 'origin' won't work since we're opening the popup manually


                    if (!options.positionTo || options.positionTo == 'origin') {
                        options.positionTo = link[0];
                    } // Remove link highlight *after* popup is closed


                    $page.bind('popupafterclose.resetlink', function () {
                        link.removeClass('ui-btn-active');
                        $(this).unbind('popupafterclose.resetlink');
                    });
                }
            }

            $page.popup('open', options);
        } else if (role == 'panel') {
            $page.panel('open');
        }
    },
    _handleLink: function _handleLink(evt) {
        var target = evt.currentTarget;

        if (target.rel === 'external') {
            return;
        }

        var href = target.href;

        if (href === undefined) {
            return;
        }

        var url = new URL(href, window.location);

        if (url.origin != window.location.origin) {
            return;
        }

        evt.preventDefault();
        this.app.router.push(url.pathname + url.search);
    },
    // Remember which submit button was clicked (and its value)
    _handleSubmitClick: function _handleSubmitClick(evt) {
        var $ = this.$;
        var $button = $(evt.target),
            $form = $(evt.target.form),
            name = $button.attr('name'),
            value = $button.attr('value');

        if (name !== undefined && value !== undefined) {
            $form.data('wq-submit-button-name', name);
            $form.data('wq-submit-button-value', value);
        }
    },
    // Handle form submit from [url]_edit views
    _handleForm: function _handleForm(evt) {
        var _this2 = this;

        return _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee() {
            var $, app, $form, $submitVal, backgroundSync, storage, outboxId, preserve, url, vals, $files, has_files, addVal, _yield$app$submitForm, _yield$app$submitForm2, item, error;

            return _regeneratorRuntime__default['default'].wrap(function _callee$(_context) {
                while (1) {
                    switch (_context.prev = _context.next) {
                        case 0:
                            addVal = function _addVal(name, val) {
                                if (vals[name] !== undefined) {
                                    if (!Array.isArray(vals[name])) {
                                        vals[name] = [vals[name]];
                                    }

                                    vals[name].push(val);
                                } else {
                                    vals[name] = val;
                                }
                            };

                            $ = _this2.$, app = _this2.app;
                            $form = $(evt.target);

                            if (app) {
                                _context.next = 5;
                                break;
                            }

                            return _context.abrupt("return");

                        case 5:
                            if (!evt.isDefaultPrevented()) {
                                _context.next = 7;
                                break;
                            }

                            return _context.abrupt("return");

                        case 7:
                            $form.find('[type=submit]').prop('disabled', true);

                            if ($form.data('wq-submit-button-name')) {
                                $submitVal = $('<input>').attr('name', $form.data('wq-submit-button-name')).attr('value', $form.data('wq-submit-button-value'));
                                $form.append($submitVal);
                            }

                            if (!($form.data('wq-json') !== undefined && !$form.data('wq-json'))) {
                                _context.next = 12;
                                break;
                            }

                            app.spin.forSeconds(10);
                            return _context.abrupt("return");

                        case 12:
                            if ($form.data('wq-background-sync') !== undefined) {
                                backgroundSync = $form.data('wq-background-sync');
                            } else {
                                backgroundSync = app.config.backgroundSync;
                            }

                            if ($form.data('wq-storage') !== undefined) {
                                storage = $form.data('wq-storage');
                            }

                            outboxId = $form.data('wq-outbox-id');
                            preserve = $form.data('wq-outbox-preserve');
                            url = $form.attr('action').replace(app.service + '/', '');
                            vals = {};
                            $files = $form.find('input[type=file]');
                            has_files = false;
                            $files.each(function (i, input) {
                                if ($(input).val().length > 0) {
                                    has_files = true;
                                }
                            });

                            if (app.isRegistered(url)) {
                                _context.next = 24;
                                break;
                            }

                            // Unrecognized URL; assume a regular form post
                            app.spin.forSeconds(10);
                            return _context.abrupt("return");

                        case 24:
                            if (!(has_files && !window.Blob)) {
                                _context.next = 27;
                                break;
                            }

                            // Files present but there's no Blob API.  Looks like we're in a an old
                            // browser that can't upload files via AJAX.  Bypass wq/outbox.js
                            // entirely and hope server is able to respond to regular form posts
                            // with HTML (hint: wq.db is).
                            app.spin.forSeconds(10);
                            return _context.abrupt("return");

                        case 27:
                            // Modern browser and/or no files present; skip regular form submission,
                            // we're saving this via wq/outbox.js
                            evt.preventDefault(); // Use a simple JSON structure for values, which is better for outbox
                            // serialization.

                            $.each($form.serializeArray(), function (i, v) {
                                addVal(v.name, v.value);
                            }); // Handle <input type=file>.  Use HTML JSON form-style objects, but
                            // with Blob instead of base64 encoding to represent the actual file.

                            if (has_files) {
                                $files.each(function () {
                                    var name = this.name,
                                        file,
                                        slice;

                                    if (!this.files || !this.files.length) {
                                        return;
                                    }

                                    for (var i = 0; i < this.files.length; i++) {
                                        file = this.files[i];
                                        slice = file.slice || file.webkitSlice;
                                        addVal(name, {
                                            type: file.type,
                                            name: file.name,
                                            // Convert to blob for better serialization
                                            body: slice.call(file, 0, file.size, file.type)
                                        });
                                    }
                                });
                            } // Handle blob-stored files created by (e.g.) wq/photos.js


                            $form.find('input[data-wq-type=file]').each(function () {
                                // wq/photo.js files in memory, copy over to form
                                var name = this.name;
                                var value = this.value;
                                var curVal = Array.isArray(vals[name]) ? vals[name][0] : vals[name];
                                var photos = app.plugins.photos;

                                if (curVal && typeof curVal === 'string') {
                                    delete vals[name];
                                }

                                if (!value || !photos) {
                                    return;
                                }

                                var data = photos._files[value];

                                if (data) {
                                    has_files = true;
                                    addVal(name, data);
                                    delete photos._files[value];
                                }
                            });

                            if ($submitVal) {
                                $submitVal.remove();
                            }

                            $form.find('.error').html('');
                            _context.next = 35;
                            return app.submitForm({
                                url: url,
                                storage: storage,
                                backgroundSync: backgroundSync,
                                has_files: has_files,
                                outboxId: outboxId,
                                preserve: preserve,
                                data: vals
                            });

                        case 35:
                            _yield$app$submitForm = _context.sent;
                            _yield$app$submitForm2 = _slicedToArray(_yield$app$submitForm, 2);
                            item = _yield$app$submitForm2[0];
                            error = _yield$app$submitForm2[1];

                            if (item && item.id) {
                                $form.attr('data-wq-outbox-id', item.id);

                                if (error) {
                                    _this2._showOutboxErrors(item, $form);
                                }
                            }

                            $form.find('[type=submit]').prop('disabled', false);

                        case 41:
                        case "end":
                            return _context.stop();
                    }
                }
            }, _callee);
        }))();
    },
    _showOutboxErrors: function _showOutboxErrors(item, $page) {
        if ($page.is('form') && item.options.method == 'DELETE') {
            if (!$page.find('.error').length) {
                // Delete form does not contain error placeholders
                // but main form might
                $page = $page.parents('.ui-page');
            }
        }

        if (!item.error) {
            showError('Error saving data.');
            return;
        } else if (typeof item.error === 'string') {
            showError(item.error);
            return;
        } // Save failed and error information is in JSON format
        // (likely a 400 bad data error)


        var errs = Object.keys(item.error);

        if (errs.length == 1 && errs[0] == 'detail') {
            // General API errors have a single "detail" attribute
            showError(item.error.detail);
        } else {
            // REST API provided per-field error information
            // Form errors (other than non_field_errors) are keyed by fieldname
            errs.forEach(function (f) {
                // FIXME: there may be multiple errors per field
                var err = item.error[f][0];

                if (f == 'non_field_errors') {
                    showError(err);
                } else {
                    if (_typeof(err) !== 'object') {
                        showError(err, f);
                    } else {
                        // Nested object errors (e.g. attachment)
                        item.error[f].forEach(function (err, i) {
                            for (var n in err) {
                                var fid = f + '-' + i + '-' + n;
                                showError(err[n][0], fid);
                            }
                        });
                    }
                }
            });

            if (!item.error.non_field_errors) {
                showError('One or more errors were found.');
            }
        }

        function showError(err, field) {
            if (field) {
                field = field + '-';
            } else {
                field = '';
            }

            var sel = '.' + item.options.modelConf.name + '-' + field + 'errors';
            $page.find(sel).html(err);
        }
    },
    handleShow: function handleShow() {
        this.runPlugins();
    },
    runPlugins: function runPlugins() {
        var _this3 = this;

        return _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee2() {
            var context, routeInfo, item;
            return _regeneratorRuntime__default['default'].wrap(function _callee2$(_context2) {
                while (1) {
                    switch (_context2.prev = _context2.next) {
                        case 0:
                            if (_this3.app) {
                                _context2.next = 2;
                                break;
                            }

                            return _context2.abrupt("return");

                        case 2:
                            context = _this3._lastContext, routeInfo = context.router_info;

                            if (!context.outbox_id) {
                                _context2.next = 7;
                                break;
                            }

                            item = context;
                            _context2.next = 18;
                            break;

                        case 7:
                            if (!routeInfo.item_id) {
                                _context2.next = 17;
                                break;
                            }

                            if (!context.local) {
                                _context2.next = 12;
                                break;
                            }

                            item = context;
                            _context2.next = 15;
                            break;

                        case 12:
                            _context2.next = 14;
                            return _this3.app.models[routeInfo.page].find(routeInfo.item_id);

                        case 14:
                            item = _context2.sent;

                        case 15:
                            _context2.next = 18;
                            break;

                        case 17:
                            item = {};

                        case 18:
                            _this3.app.callPlugins('run', [_this3.jqm.activePage, _objectSpread2(_objectSpread2({}, routeInfo), {}, {
                                item: item,
                                context: context
                            })]);

                        case 19:
                        case "end":
                            return _context2.stop();
                    }
                }
            }, _callee2);
        }))();
    },
    run: function run($page, routeInfo) {
        this.runOutbox($page, routeInfo);
        this.runPatterns($page, routeInfo);
    },
    runOutbox: function runOutbox($page, routeInfo) {
        var _this4 = this;

        return _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime__default['default'].mark(function _callee3() {
            var name, outbox_id, outbox, item;
            return _regeneratorRuntime__default['default'].wrap(function _callee3$(_context3) {
                while (1) {
                    switch (_context3.prev = _context3.next) {
                        case 0:
                            name = routeInfo.name, outbox_id = routeInfo.outbox_id, outbox = _this4.app.outbox;

                            if (!(name === 'outbox_edit')) {
                                _context3.next = 6;
                                break;
                            }

                            _context3.next = 4;
                            return outbox.loadItem(outbox_id);

                        case 4:
                            item = _context3.sent;

                            if (item.error) {
                                _this4._showOutboxErrors(item, $page);
                            }

                        case 6:
                        case "end":
                            return _context3.stop();
                    }
                }
            }, _callee3);
        }))();
    },
    runPatterns: function runPatterns($page, _ref2) {
        var _this5 = this;

        var page = _ref2.page,
            mode = _ref2.mode,
            pageContext = _ref2.context;
        var $ = this.$;
        $page.find('button[data-wq-action=addattachment]').click(function (evt) {
            var $button = $(evt.target),
                section = $button.data('wq-section'),
                count = $page.find('.section-' + section).length,
                template = _this5.config.templates[page + '_' + (mode ? mode : 'edit')],
                pattern = '{{#' + section + '}}([\\s\\S]+){{/' + section + '}}',
                match = template && template.match(pattern),
                context = {
                '@index': count,
                new_attachment: true
            };

            if (!match) {
                return;
            }

            for (var key in pageContext) {
                context[key.replace(section + '.', '')] = pageContext[key];
            }

            var $attachment = $(Mustache__default['default'].render(match[1], context, _this5.config.partials));

            if ($attachment.is('tr')) {
                $button.parents('tr').before($attachment);
                $attachment.enhanceWithin();
            } else {
                $button.parents('li').before($attachment);
                $attachment.enhanceWithin();
                $button.parents('ul').listview('refresh');
            }
        });
        $page.on('click', 'button[data-wq-action=removeattachment]', function (evt) {
            var $button = $(evt.target),
                section = $button.data('wq-section'),
                $row = $button.parents('.section-' + section);
            $row.remove();
        });
    },
    onsync: function onsync() {
        var router = this.app.router,
            context = router.getContext(),
            _context$router_info = context.router_info,
            routeInfo = _context$router_info === void 0 ? {} : _context$router_info,
            page = routeInfo.page,
            mode = routeInfo.mode;

        if (page === 'outbox' || mode === 'list') {
            router.reload();
        }
    }
};

return jqmRenderer;

});
//# sourceMappingURL=jquery-mobile.js.map
