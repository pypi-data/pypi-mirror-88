/*
 * @wq/leaflet 1.3.0-alpha.1
 * Leaflet integration for @wq/map
 * (c) 2013-2020, S. Andrew Sheppard
 * https://wq.io/license
 */

define(['./map', 'react', './react', 'prop-types', 'react-leaflet', 'esri-leaflet', 'mustache', 'react-leaflet-markercluster', 'leaflet', 'react-leaflet-draw', 'leaflet.wms'], function (map, React, react, PropTypes, reactLeaflet, esriLeaflet, Mustache, MarkerClusterGroup, L, reactLeafletDraw, wms) { 'use strict';

function _interopDefaultLegacy (e) { return e && typeof e === 'object' && 'default' in e ? e : { 'default': e }; }

var map__default = /*#__PURE__*/_interopDefaultLegacy(map);
var React__default = /*#__PURE__*/_interopDefaultLegacy(React);
var PropTypes__default = /*#__PURE__*/_interopDefaultLegacy(PropTypes);
var Mustache__default = /*#__PURE__*/_interopDefaultLegacy(Mustache);
var MarkerClusterGroup__default = /*#__PURE__*/_interopDefaultLegacy(MarkerClusterGroup);
var L__default = /*#__PURE__*/_interopDefaultLegacy(L);

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

function _extends() {
  _extends = Object.assign || function (target) {
    for (var i = 1; i < arguments.length; i++) {
      var source = arguments[i];

      for (var key in source) {
        if (Object.prototype.hasOwnProperty.call(source, key)) {
          target[key] = source[key];
        }
      }
    }

    return target;
  };

  return _extends.apply(this, arguments);
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

function Ready() {
    var _ref = react.usePlugin('map') || {},
        ready = _ref.ready,
        _useLeaflet = reactLeaflet.useLeaflet(),
        map = _useLeaflet.map;

    React.useEffect(function () {
        ready && map && ready(map);
    }, [ready, map]);
    return null;
}

function Map(_ref2) {
    var bounds = _ref2.bounds,
        children = _ref2.children,
        mapProps = _ref2.mapProps,
        containerStyle = _ref2.containerStyle;

    var style = _objectSpread2({
        flex: '1',
        minHeight: 200
    }, containerStyle);

    var maxZoom = mapProps && mapProps.maxZoom || 18;
    return /*#__PURE__*/React__default['default'].createElement(reactLeaflet.Map, _extends({
        bounds: bounds,
        style: style,
        maxZoom: maxZoom
    }, mapProps), /*#__PURE__*/React__default['default'].createElement(Ready, null), children);
}
Map.propTypes = {
    bounds: PropTypes__default['default'].array,
    children: PropTypes__default['default'].node,
    mapProps: PropTypes__default['default'].object,
    containerStyle: PropTypes__default['default'].object
};

var BaseLayer = reactLeaflet.LayersControl.BaseLayer,
    Overlay = reactLeaflet.LayersControl.Overlay;
function Legend(_ref) {
    var position = _ref.position,
        collapsed = _ref.collapsed,
        children = _ref.children;

    if (!position) {
        position = 'topright';
    }

    if (collapsed === undefined) {
        collapsed = true;
    }

    return /*#__PURE__*/React__default['default'].createElement(reactLeaflet.LayersControl, {
        position: position,
        collapsed: collapsed
    }, children);
}
Legend.propTypes = {
    position: PropTypes__default['default'].object,
    collapsed: PropTypes__default['default'].bool,
    children: PropTypes__default['default'].node
};
function BasemapToggle(_ref2) {
    var name = _ref2.name,
        active = _ref2.active,
        children = _ref2.children,
        rest = _objectWithoutProperties(_ref2, ["name", "active", "children"]);

    return /*#__PURE__*/React__default['default'].createElement(BaseLayer, _extends({
        name: name,
        checked: active
    }, rest), children);
}
BasemapToggle.propTypes = {
    name: PropTypes__default['default'].string,
    active: PropTypes__default['default'].bool,
    children: PropTypes__default['default'].node
};
function OverlayToggle(_ref3) {
    var name = _ref3.name,
        active = _ref3.active,
        children = _ref3.children,
        rest = _objectWithoutProperties(_ref3, ["name", "active", "children"]);

    return /*#__PURE__*/React__default['default'].createElement(Overlay, _extends({
        name: name,
        checked: active
    }, rest), children);
}
OverlayToggle.propTypes = {
    name: PropTypes__default['default'].string,
    active: PropTypes__default['default'].bool,
    children: PropTypes__default['default'].node
};

function Tile(props) {
    return /*#__PURE__*/React__default['default'].createElement(reactLeaflet.TileLayer, props);
}

var BasemapLayer = /*#__PURE__*/function (_MapLayer) {
    _inherits(BasemapLayer, _MapLayer);

    var _super = _createSuper(BasemapLayer);

    function BasemapLayer() {
        _classCallCheck(this, BasemapLayer);

        return _super.apply(this, arguments);
    }

    _createClass(BasemapLayer, [{
        key: "createLeafletElement",
        value: function createLeafletElement(_ref) {
            var layer = _ref.layer,
                rest = _objectWithoutProperties(_ref, ["layer"]);

            return esriLeaflet.basemapLayer(layer, rest);
        }
    }]);

    return BasemapLayer;
}(reactLeaflet.MapLayer);

function EsriBasemap(_ref2) {
    var layer = _ref2.layer,
        labels = _ref2.labels,
        rest = _objectWithoutProperties(_ref2, ["layer", "labels"]);

    var leaflet = reactLeaflet.useLeaflet(),
        props = _objectSpread2(_objectSpread2({}, rest), {}, {
        layer: layer,
        leaflet: leaflet
    });

    if (labels) {
        var labelProps = _objectSpread2(_objectSpread2({}, props), {}, {
            layer: props.layer + 'Labels'
        });

        return /*#__PURE__*/React__default['default'].createElement(reactLeaflet.LayerGroup, null, /*#__PURE__*/React__default['default'].createElement(BasemapLayer, props), /*#__PURE__*/React__default['default'].createElement(BasemapLayer, labelProps));
    } else {
        return /*#__PURE__*/React__default['default'].createElement(BasemapLayer, props);
    }
}
EsriBasemap.propTypes = {
    layer: PropTypes__default['default'].string.isRequired,
    labels: PropTypes__default['default'].bool
};

function Geojson(_ref) {
    var url = _ref.url,
        data = _ref.data,
        style = _ref.style,
        icon = _ref.icon,
        popup = _ref.popup,
        oneach = _ref.oneach,
        cluster = _ref.cluster,
        clusterIcon = _ref.clusterIcon;

    var _usePlugin = react.usePlugin('leaflet'),
        config = _usePlugin.config,
        _ref2 = react.usePlugin('jqmrenderer') || {},
        jqmConfig = _ref2.config,
        geojson = map.useGeoJSON(url, data),
        options = {};

    if (!geojson || !geojson.type) {
        return null;
    }

    if (popup) {
        var template = config.popups[popup] || jqmConfig && jqmConfig.templates["".concat(popup, "_popup")] || popup;

        popup = function popup(_ref3, layer) {
            var id = _ref3.id,
                properties = _ref3.properties;
            layer.bindPopup(Mustache__default['default'].render(template, _objectSpread2({
                id: id
            }, properties)));
        };
    }

    if (oneach && popup) {
        options.onEachFeature = function (feat, layer) {
            popup(feat, layer);
            oneach(feat, layer);
        };
    } else if (oneach) {
        options.onEachFeature = oneach;
    } else if (popup) {
        options.onEachFeature = popup;
    }

    if (icon) {
        options.pointToLayer = function pointToLayer(geojson, latlng) {
            // Define icon as a function to customize per-feature
            var key;

            if (typeof icon == 'function') {
                key = icon(geojson.properties);
            } else if (icon.indexOf('{{') > -1) {
                key = Mustache__default['default'].render(icon, geojson.properties);
            } else {
                key = icon;
            }

            return L__default['default'].marker(latlng, {
                icon: config.icons[key]
            });
        };
    }

    var Component;

    if (cluster) {
        Component = MarkerCluster;
        options.clusterIcon = clusterIcon;
    } else {
        Component = reactLeaflet.GeoJSON;
    }

    return /*#__PURE__*/React__default['default'].createElement(Component, _extends({
        data: geojson,
        style: style
    }, options));
}
Geojson.propTypes = {
    url: PropTypes__default['default'].string,
    data: PropTypes__default['default'].object,
    style: PropTypes__default['default'].func,
    icon: PropTypes__default['default'].oneOfType([PropTypes__default['default'].string, PropTypes__default['default'].func]),
    popup: PropTypes__default['default'].string,
    oneach: PropTypes__default['default'].func,
    cluster: PropTypes__default['default'].bool,
    clusterIcon: PropTypes__default['default'].oneOfType([PropTypes__default['default'].string, PropTypes__default['default'].func])
};

function MarkerCluster(_ref4) {
    var clusterIcon = _ref4.clusterIcon,
        rest = _objectWithoutProperties(_ref4, ["clusterIcon"]);

    var options = {};

    if (clusterIcon) {
        options.iconCreateFunction = function clusterDiv(cluster) {
            var cls;
            var context = {
                count: cluster.getChildCount()
            };

            if (context.count >= 100) {
                context.large = true;
            } else if (context.count >= 10) {
                context.medium = true;
            } else {
                context.small = true;
            }

            if (typeof clusterIcon == 'function') {
                cls = clusterIcon(context);
            } else if (clusterIcon.indexOf('{{') > -1) {
                cls = Mustache__default['default'].render(clusterIcon, context);
            } else {
                cls = clusterIcon;
            }

            var html = Mustache__default['default'].render('<div><span>{{count}}</span></div>', context);
            return new L__default['default'].DivIcon({
                html: html,
                className: 'marker-cluster ' + cls,
                iconSize: new L__default['default'].Point(40, 40)
            });
        };
    }

    return /*#__PURE__*/React__default['default'].createElement(MarkerClusterGroup__default['default'], options, /*#__PURE__*/React__default['default'].createElement(reactLeaflet.GeoJSON, rest));
}

MarkerCluster.propTypes = {
    clusterIcon: PropTypes__default['default'].oneOfType([PropTypes__default['default'].string, PropTypes__default['default'].func])
};

function Highlight(_ref) {
    var data = _ref.data;

    function style() {
        return {
            color: '#00ffff'
        };
    }

    return /*#__PURE__*/React__default['default'].createElement(reactLeaflet.GeoJSON, {
        data: data,
        style: style
    });
}
Highlight.propTypes = {
    data: PropTypes__default['default'].object
};

var TYPES = {
    point: ['marker'],
    line_string: ['polyline'],
    polygon: ['polygon', 'rectangle'],
    all: ['marker', 'polyline', 'polygon', 'rectangle']
};

var FeatureImpl = /*#__PURE__*/function (_MapLayer) {
    _inherits(FeatureImpl, _MapLayer);

    var _super = _createSuper(FeatureImpl);

    function FeatureImpl() {
        _classCallCheck(this, FeatureImpl);

        return _super.apply(this, arguments);
    }

    _createClass(FeatureImpl, [{
        key: "createLeafletElement",
        value: function createLeafletElement(props) {
            return L.GeoJSON.geometryToLayer(props.data);
        }
    }]);

    return FeatureImpl;
}(reactLeaflet.MapLayer);

function Feature(props) {
    var leaflet = reactLeaflet.useLeaflet();
    return /*#__PURE__*/React__default['default'].createElement(FeatureImpl, _extends({
        leaflet: leaflet
    }, props));
}

function Draw(_ref) {
    var type = _ref.type,
        data = _ref.data,
        setData = _ref.setData;
    var ref = React.useRef(),
        controls = {
        polyline: false,
        polygon: false,
        rectangle: false,
        circle: false,
        marker: false,
        circlemarker: false
    },
        types = TYPES[type] || TYPES.all;
    types.forEach(function (type) {
        return controls[type] = {};
    });

    function save() {
        var _ref2 = ref && ref.current,
            leafletElement = _ref2.leafletElement;

        if (!leafletElement) {
            return;
        }

        setData(leafletElement.toGeoJSON());
    }

    return /*#__PURE__*/React__default['default'].createElement(reactLeaflet.FeatureGroup, {
        ref: ref
    }, /*#__PURE__*/React__default['default'].createElement(reactLeafletDraw.EditControl, {
        draw: controls,
        onCreated: save,
        onEdited: save,
        onDeleted: save
    }), data && data.features.map(function (feature, i) {
        return /*#__PURE__*/React__default['default'].createElement(Feature, {
            key: i,
            data: feature.geometry
        });
    }));
    /* FIXME
    var $submit = $geom.parents('form').find('[type=submit]');
    m.on('draw:drawstart draw:editstart draw:deletestart', function() {
        $submit.attr('disabled', true);
    });
     m.on('draw:drawstop draw:editstop draw:deletestop', function() {
        $submit.attr('disabled', false);
    });
    */
}
Draw.propTypes = {
    type: PropTypes__default['default'].string,
    data: PropTypes__default['default'].object,
    setData: PropTypes__default['default'].func
};

var index = {
    name: 'leaflet',
    dependencies: [map__default['default']],
    config: {
        popups: {},
        icons: {
            default: new L__default['default'].Icon.Default()
        },
        defaults: {
            // Defaults to simplify creation of new icons of the same dimensions
            // as L.Icon.Default
            icon: {
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41]
            }
        }
    },
    init: function init(config) {
        if (config) {
            this.config = _objectSpread2(_objectSpread2({}, this.config), config);
        }
    },
    createIcon: function createIcon(name, options) {
        return this.config.icons[name] = L__default['default'].icon(_objectSpread2(_objectSpread2({}, this.config.defaults.icon), options));
    },
    components: {
        Map: Map,
        Legend: Legend,
        BasemapToggle: BasemapToggle,
        OverlayToggle: OverlayToggle
    },
    basemaps: {
        Group: reactLeaflet.LayerGroup,
        Empty: reactLeaflet.LayerGroup,
        Tile: Tile
    },
    overlays: {
        Group: reactLeaflet.LayerGroup,
        Empty: reactLeaflet.LayerGroup,
        Geojson: Geojson,
        Highlight: Highlight,
        Draw: Draw
    }
};

return index;

});
//# sourceMappingURL=leaflet.js.map
