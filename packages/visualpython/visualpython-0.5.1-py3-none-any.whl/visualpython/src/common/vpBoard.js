define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/container/vpContainer'
], function (requirejs, $, vpConst, vpContainer) {
    "use strict";

    /**
     * api stack global variable
     * format:
     *  {
     *      code: 'df' / '.concat(opt=1)' / '[]',
     *      type: 'var' / 'oper' / 'brac' / 'api' / 'code'
     *      metadata: {},
     * 
     *      // to load/save 
     *      prev: -1,
     *      next: -1,
     *      child: -1 / left: -1, right: -1
     *  }
     */
    var _apiBoard =  {
        // 0: { code: 'df_train', type: 'var', next: 1, metadata: { funcID: 'com_variables', prefix: [], postfix: [], options: [] } },
        // 1: { code: '[]', type: 'brac', next: 2, child: 4 },
        // 2: { code: '[]', type: 'brac', next: 3, child: 11 },
        // 3: { code: '.median()', type: 'api', next: -1, metadata: { funcID: 'pdGrp_median', prefix: [], postfix: [], options: [] } },
        // 4: { code: '&', type: 'oper', left: 5, right: 6 },
        // 5: { code: "==", type: 'oper', left: 7, right: 8 }, 
        // 6: { code: "==", type: 'oper', left: 9, right: 10 },
        // 7: { code: "df_train['Sex']", type: 'var', metadata: { funcID: 'com_variables', prefix: [], postfix: [], options: [] } },
        // 8: { code: "'male'", type: 'code', metadata: { funcID: 'com_udf', prefix: [], postfix: [], options: [ { id: 'vp_userCode', value: "'male'"} ] } },
        // 9: { code: "df_train['Pclass']", type: 'var', metadata: { funcID: 'com_variables', prefix: [], postfix: [], options: [] } },
        // 10: { code: "1", type: 'code', metadata: { funcID: 'com_udf', prefix: [], postfix: [], options: [ { id: 'vp_userCode', value: "1"} ] } },
        // 11: { code: "'Age'", type: 'code', metadata: { funcID: 'com_udf', prefix: [], postfix: [], options: [ { id: 'vp_userCode', value: "'Age'"} ] } }
    }
    var _apiHead = 0;
    var _boardNewNumber = Object.keys(_apiBoard).length;

    /**
     * TEST: minju: api board test
     * API Board
     * 1. set draggable event to .vp-ab-box
     * 2. set drag box information
     *  1) 
     */

    /** FIXME: move to constants.js : VpBoard const variables */
    const VP_PARENT_CONTAINER   = '.vp-option-page';
    const VP_DRAGGABLE          = '.vp-ab-box';
    const VP_DRAGGABLE_INBOX    = '.vp-ab-inbox';
    const VP_CONTAINER          = '.vp-ab-container';
    const VP_DROPPABLE_BOX      = '.vp-ab-droppable-box';
    const VP_BOX_MENU_ID        = '#vp_abBoxMenu';
    const VP_BOX_SELECTOR_ID    = '#vp_abBoxSelector';

    const VP_BOX_MENU_TAG     = ``;
    const VP_BOX_SELECTOR_TAG = ``;
    const VP_CONTAINER_TAG      = `<div class="vp-ab-area">
                                        <div class="vp-ab-container">
                                        </div>
                                    </div>`;
    const VP_DRAGGABLE_TAG      = `<span id="{id}" class="${VP_DRAGGABLE.substr(1)} ${VP_DRAGGABLE_INBOX.substr(1)} {type} no-selection" data-type="{type}" data-idx="{idx}">{code}</span>`


    const VP_BOX_ID_PREFIX      = 'vp_ab_box_';

    /**
     * Clear apiStack
     */
    var clear = function() {
        _apiBoard = {};
        _apiHead = 0;
        _boardNewNumber = 0;
    }

    /**
     * Clear apiStack Link
     */
    var clearLink = function() {
        Object.keys(_apiBoard).forEach(key => {
            delete _apiBoard[key].next;
            delete _apiBoard[key].child;
            delete _apiBoard[key].left;
            delete _apiBoard[key].right;
            delete _apiBoard[key].checksum;
        })
    }

    /**
     * remove not using keys
     */
    var clearUnchecked = function() {
        var keys = Object.keys(_apiBoard);
        for(var i = 0; i < keys.length; i++) {
            if (_apiBoard[keys[i]].checksum != true) {
                delete _apiBoard[keys[i]];
            }
        }
    }

    /**
     * Load Box recursively
     * @param {number} pointer 
     * @param {string} prevBox Tag Element string
     */
    var loadBox = function(pointer, prevBox = '') {
        if (pointer == undefined || pointer < 0 || Object.keys(_apiBoard).length <= 0) {
            return "";
        }
        var block = _apiBoard[pointer];
        if (block == undefined) return "";

        var box = VP_DRAGGABLE_TAG;
        box = box.replace('{id}', VP_BOX_ID_PREFIX + pointer);
        box = box.replaceAll('{type}', block.type);
        box = box.replace('{idx}', pointer);

        var code = block.code;
        
        if (block.type == "brac") {
            var child = loadBox(block.child);
            // brackets [] ()
            if (block.code === "[]") {
                code = `<span class="vp-ab-code">[</span>
                        <span class="vp-ab-droppable-box" data-type="${block.type}" data-idx="${pointer}" data-link="child">${child}</span>
                        <span class="vp-ab-code">]</span>`
            } else {
                code = `<span class="vp-ab-code">(</span>
                        <span class="vp-ab-droppable-box" data-type="${block.type}" data-idx="${pointer}" data-link="child">${child}</span>
                        <span class="vp-ab-code">)</span>`
            }
        } else if (block.type == "oper") {
            // operator + - / * & | == != < <= > >=
            var left = loadBox(block.left);
            var right = loadBox(block.right);
            // code = `(${left} ${block.code} ${right})`
            code = `
            <span class="vp-ab-code">(</span>
            <span class="vp-ab-droppable-box left" data-type="${block.type}" data-idx="${pointer}" data-link="left">${left}</span>
            <span class="vp-ab-code">${block.code}</span>
            <span class="vp-ab-droppable-box right" data-type="${block.type}" data-idx="${pointer}" data-link="right">${right}</span>
            <span class="vp-ab-code">)</span>
            `;
        } else {
            // var, code, api
            code = `<span class="vp-ab-code">${block.code}</span>`
        }
        box = box.replace('{code}', code);
        box = prevBox + box;
        if (block.next != undefined && block.next >= 0) {
            box = loadBox(block.next, box);
        }
        return box;
    }

    /**
     * Synchronize container & _apiBoard
     * @param {HTMLElement} parentTag 
     */
    var syncApiStack = function(parentTag) {
        var parentKey = parentTag.data('idx');
        var parentType = parentTag.data('type');
        var parentLink = parentTag.data('link');
        if (parentLink == undefined) {
            parentLink = 'child';
        }

        // get childrenTag
        var childrenTag = parentTag.children(VP_DRAGGABLE);

        // loop and recursive function to get children
        var childrenCount = childrenTag.length;
        if (childrenCount > 0) {
            var prevKey = -1;
            for (var i = 0; i < childrenCount; i++) {
                var childTag = childrenTag[i];
                var key = $(childTag).data('idx');
                var type = $(childTag).data('type');

                _apiBoard[key].checksum = true;
    
                if (i == 0) {
                    // first child set to child/left/right
                    if (parentKey == undefined) {
                        _apiHead = key;
                    } else {
                        _apiBoard[parentKey][parentLink] = key;
                    }
                }

                // if type is brac or oper
                if (type == 'brac') {
                    var boxTag = $(childTag).children(VP_DROPPABLE_BOX);
                    // link to child
                    syncApiStack($(boxTag));
                } else if (type == 'oper') {
                    var leftTag = $(childTag).children(VP_DROPPABLE_BOX + '.left');
                    var rightTag = $(childTag).children(VP_DROPPABLE_BOX + '.right');
                    // link to left/right children
                    syncApiStack($(leftTag));
                    syncApiStack($(rightTag));
                }
                
                if (prevKey >= 0) {
                    _apiBoard[prevKey].next = key;
                }
                // _apiBoard[key].prev = prevKey;
                prevKey = key;
            }
        } else {
            // no child
            if (parentKey == undefined) {
                _apiHead = key;
            } else {
                _apiBoard[parentKey][parentLink] = -1;
            }
        }
    }

    /**
     * @class VpBoard
     * @param {string} parentContainer
     * @constructor
     */
    var VpBoard = function (page, parentContainer = VP_PARENT_CONTAINER) {
        this.page = page;

        this.parentContainer = page.wrapSelector(''); // '#vp_optionBook'
        this.draggable      = VP_DRAGGABLE;
        this.draggableInbox = VP_DRAGGABLE_INBOX;
        this.container      = VP_CONTAINER;
        this.droppableBox   = VP_DROPPABLE_BOX;

        this.popBoxSelector = VP_BOX_SELECTOR_ID;
        this.popBoxMenu     = VP_BOX_MENU_ID;

        this.containerTag   = VP_CONTAINER_TAG;
        this.draggableTag   = VP_DRAGGABLE_TAG;
    }

    VpBoard.prototype.clear = function() {
        _apiHead = 0;
        _apiBoard = {};
        _boardNewNumber = 0;

        $(this.draggable).remove();
        this.syncApiStack();
    }

    VpBoard.prototype.getCode = function(container = this.container) {
        // TODO: run cell : $('.vp-ab-container .vp-ab-code').text().replaceAll(/\r?\n|\r/g, '').trim()
        var code = $(container).find(' .vp-ab-code').text().replaceAll(/\r?\n|\r/g, '').trim();
        return code;
    }

    /**
     * Load container & apiStack boxes
     */
    VpBoard.prototype.load = function() {

        // clean container
        $('.vp-ab-area').remove();

        this.page.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "file_io/vpBoard.css");
        
        this.loadContainer();
        this.loadApiStack();
    }

    /**
     * Load api board droppable container
     * default class : .vp-ab-container
     */
    VpBoard.prototype.loadContainer = function(parentContainer = this.parentContainer) {
        var that = this;
        var droppableEle = $(this.containerTag);
        var droppableBoxEle = $(this.droppableBox);

        // load container
        $(parentContainer).prepend(droppableEle);
    }

    /**
     * Load apiStack
     */
    VpBoard.prototype.loadApiStack = function() {
        var apiStackLength = Object.keys(_apiBoard).length
        if (apiStackLength === 0) {
            // no _apiBoard available
            return;
        }
        
        var box = loadBox(_apiHead);
        var boxEle = $(box);

        $(this.container).append(boxEle);
    }

    /*** Get/Set ApiStack ***/
    /** Get api stack 
     * @returns {object} _apiBoard
    */
    VpBoard.prototype.getApiStack = function() {
        return _apiBoard;
    }

    /**
     * sync api stack with vp-ab-container
     */
    VpBoard.prototype.syncApiStack = function(parentTag = $(this.container)) {
        clearLink();
        syncApiStack(parentTag);
        clearUnchecked();
    }
    
    VpBoard.prototype.addBlock = function(blockObj) {
        // add on api stack
        // blockObj : { code: '', type: '', metadata: {} }

        var idx = _boardNewNumber++;
        if (idx == 0) {
            _apiHead = 0;
        }
        _apiBoard[idx] = blockObj;

        // appendTo container
        var box = loadBox(idx);
        var boxEle = $(box);
        $(this.container).append(boxEle);

        // bind event
        //this.setDroppableBox(boxEle.find(this.droppableBox));
        //this.setDraggable(boxEle);

        this.syncApiStack();
    }

    VpBoard.prototype.addBlocks = function(blockObjs) {
        blockObjs.forEach(obj => {
            var idx = _boardNewNumber++;
            if (idx == 0) {
                _apiHead = 0;
            }
            _apiBoard[idx] = obj;
        });

        this.loadApiStack();
    }

    return VpBoard;
});
