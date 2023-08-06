define([
    'nbextensions/visualpython/src/common/vpCommon'
    
    , './api.js'
    , './constData.js'
    , './blockRenderer.js'
], function (vpCommon, api, constData, blockRenderer ) {
    const { ChangeOldToNewState
            , FindStateValue
            , MapTypeToName } = api;

    const { RenderHTMLDomColor } = blockRenderer;

    const { BLOCK_CODELINE_TYPE
            , BLOCK_TYPE
        
            , NUM_INDENT_DEPTH_PX
            , NUM_SHADOWBLOCK_OPACITY
            
            , STR_DIV
            , STR_OPACITY
            , STR_POSITION
            , STR_RELATIVE
            , STR_WIDTH
            , STR_100PERCENT

            , VP_BLOCK
            , VP_CLASS_BLOCK_CODETYPE_NAME
            , VP_CLASS_BLOCK_SHADOWBLOCK_CONTAINER } = constData;
    
    var ShadowBlock = function(blockContainerThis, type, childListDom, realBlock) {
        this.state = {
            type
            , blockType: BLOCK_TYPE.SHADOW_BLOCK
            , name: ''
            , direction: -1
            , rootBlockUuid: ''
        }
        this.blockContainerThis = blockContainerThis;

        var name = MapTypeToName(type);
        this.setBlockName(name);
        this.realBlock = realBlock;
        this.rootDom = null;
        this.selectBlock = null;
        this.tempChildListDom = null;
        this.init(childListDom);
    }

    ShadowBlock.prototype.init = function(childListDom) {

        /** root container 생성 */
        var containerDom = document.createElement(STR_DIV);
        containerDom.classList.add(VP_CLASS_BLOCK_SHADOWBLOCK_CONTAINER);

        // if( childListDom == null) {
            /** root dom 생성 */
        var blockMainDom = document.createElement(STR_DIV);
        blockMainDom.classList.add(VP_BLOCK);
        $(blockMainDom).css(STR_WIDTH, STR_100PERCENT);

        blockMainDom = RenderHTMLDomColor(this, blockMainDom);
        $(blockMainDom).css(STR_OPACITY, NUM_SHADOWBLOCK_OPACITY);
        $(blockMainDom).css(STR_POSITION, STR_RELATIVE);

        var blockInnerDom = $(`<div class='vp-block-inner'></div>`);
        var nameDom = $(`<div class='vp-block-header'>
                                <strong class="vp-apiblock-style-flex-column-center 
                                        ${this.getBlockCodeLineType() !== BLOCK_CODELINE_TYPE.HOLDER 
                                                ? VP_CLASS_BLOCK_CODETYPE_NAME 
                                                : ''}" 
                                    style="margin-right:10px; font-size:12px; color: #252525;">
                                    ${this.getBlockName()}
                                </strong>    
                            </div>`);

        $(blockInnerDom).append(nameDom); 
        $(blockMainDom).append(blockInnerDom);
        $(containerDom).append(blockMainDom);
            // this.setBlockMainDom(containerDom);
            // return ;
        // }


        var rootBlockDepth = 0;
        var childLowerDepthBlockList;
        if (this.realBlock) {
            rootBlockDepth = this.realBlock.getDepth();
            childLowerDepthBlockList = this.realBlock.getChildLowerDepthBlockList();
        }

        childListDom.forEach( (childDom,index) => {
            $(childDom).css(STR_OPACITY, NUM_SHADOWBLOCK_OPACITY);
            var childBlockDepth = childLowerDepthBlockList[index+1].getDepth();
            var minusedChildBlockDepth = childBlockDepth - rootBlockDepth;
            if (minusedChildBlockDepth <= 0) {
                $(childDom).css(STR_WIDTH, STR_100PERCENT);
            } else {
                $(childDom).css(STR_WIDTH, `calc(100% - ${NUM_INDENT_DEPTH_PX * minusedChildBlockDepth}px)`);
            }
            $(containerDom).append(childDom);
        });
        
        this.setBlockMainDom(containerDom);
    }

    ShadowBlock.prototype.getBlockName = function() {
        return this.state.name;
    }
    ShadowBlock.prototype.setBlockName = function(name) {
        this.setState({
            name
        });
    }

    ShadowBlock.prototype.getBlockCodeLineType = function() {
        return this.state.type;
    }








    ShadowBlock.prototype.getBlockMainDom = function() {
        return this.rootDom;
    }
    ShadowBlock.prototype.setBlockMainDom = function(rootDom) {
        this.rootDom = rootDom;
    }






    ShadowBlock.prototype.setSelectBlock = function(selectBlock) {
        this.selectBlock = selectBlock;
    }
    ShadowBlock.prototype.getSelectBlock = function() {
        return this.selectBlock;
    }
    // ShadowBlock.prototype.deleteShadowBlock = function() {
    //     var blockMainDom = this.getBlockMainDom();
    //     $(blockMainDom).remove();
    //     $(blockMainDom).empty();
    // }







        // ** Block state 관련 메소드들 */
    ShadowBlock.prototype.setState = function(newState) {
        this.state = ChangeOldToNewState(this.state, newState);
        this.consoleState();
    }

    /**
        특정 state Name 값을 가져오는 함수
        @param {string} stateKeyName
    */
    ShadowBlock.prototype.getState = function(stateKeyName) {
        return FindStateValue(this.state, stateKeyName);
    }
    ShadowBlock.prototype.getStateAll = function() {
        return this.state;
    }
    ShadowBlock.prototype.consoleState = function() {
        // console.log(this.state);
    }

    return ShadowBlock;
});
