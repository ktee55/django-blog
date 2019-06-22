/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "/";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./resources/js/app.js":
/*!*****************************!*\
  !*** ./resources/js/app.js ***!
  \*****************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _bling_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./bling.js */ "./resources/js/bling.js");

var modal = Object(_bling_js__WEBPACK_IMPORTED_MODULE_0__["$"])('.modal');
var photos = Object(_bling_js__WEBPACK_IMPORTED_MODULE_0__["$$"])('#photos img');

function insertImage() {
  // let image = '<a href="' + this.dataset.origin + '"><img src="' + this.dataset.medium + '"></a>';
  var image = "<a href=\"".concat(this.dataset.origin, "\"><img src=\"").concat(this.dataset.medium, "\"></a>");
  Object(_bling_js__WEBPACK_IMPORTED_MODULE_0__["$"])('#id_content').value += image;
}

function expandModal() {
  modal.classList.add('show-modal');
}

function closeModal(e) {
  // console.log(e.target);
  if (!e.target.classList.contains('clearablefileinput')) {
    modal.classList.remove('show-modal');
  }
}

photos.forEach(function (photo) {
  return photo.on('click', insertImage);
});
Object(_bling_js__WEBPACK_IMPORTED_MODULE_0__["$"])('#expand-modal').on('click', expandModal);
modal.on('click', closeModal); // let modal = document.querySelector('.modal');
// let photos = document.querySelectorAll('#photos img');
// function insertImage() {
//   let image = '<a href="' + this.dataset.origin + '"><img src="' + this.dataset.medium + '"></a>';
//   document.querySelector('#id_content').value += image;
// }
// function expandModal() {
//   modal.classList.add('show');
// }
// function closeModal(e) {
//   // console.log(e);
//   // if(e.target==='form') return;
//   modal.classList.remove('show');
// }
// photos.forEach( photo => photo.addEventListener('click', insertImage));
// document.querySelector('#expand-modal').addEventListener('click', expandModal);
// modal.addEventListener('click', closeModal);

/***/ }),

/***/ "./resources/js/bling.js":
/*!*******************************!*\
  !*** ./resources/js/bling.js ***!
  \*******************************/
/*! exports provided: $, $$ */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "$", function() { return $; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "$$", function() { return $$; });
// based on https://gist.github.com/paulirish/12fb951a8b893a454b32
var $ = document.querySelector.bind(document);
var $$ = document.querySelectorAll.bind(document);

Node.prototype.on = window.on = function (name, fn) {
  this.addEventListener(name, fn);
};

NodeList.prototype.__proto__ = Array.prototype; // eslint-disable-line

NodeList.prototype.on = NodeList.prototype.addEventListener = function (name, fn) {
  this.forEach(function (elem) {
    elem.on(name, fn);
  });
};



/***/ }),

/***/ "./resources/sass/main.scss":
/*!**********************************!*\
  !*** ./resources/sass/main.scss ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports) {

// removed by extract-text-webpack-plugin

/***/ }),

/***/ 0:
/*!**************************************************************!*\
  !*** multi ./resources/js/app.js ./resources/sass/main.scss ***!
  \**************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(/*! C:\Users\Ko\Desktop\django_blog\resources\js\app.js */"./resources/js/app.js");
module.exports = __webpack_require__(/*! C:\Users\Ko\Desktop\django_blog\resources\sass\main.scss */"./resources/sass/main.scss");


/***/ })

/******/ });